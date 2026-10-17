#include <string.h>
#include "xparameters.h"
#include "xqspipsu.h"
#include "xcsudma.h"
#include "xil_printf.h"
#include "xil_cache.h"
#include "xil_io.h"
#include "xstatus.h"
#include "sleep.h"

/* XilPM & IPI headers for PMU communication */
#include "pm_api_sys.h"
#include "pm_defs.h"
#include "xipipsu.h"
#include "xilfpga.h"
#include "../../hello/hw/psu_init.h"

extern unsigned long psu_afi_config(void);
/* =========================================================================
 * ZynqMP boot image headers (matches zynqmp_fsbl/src/xfsbl_image_header.h)
 * ========================================================================= */
typedef struct {
    u32 EncryptedDataWordLength;
    u32 UnEncryptedDataWordLength;
    u32 TotalDataWordLength;
    u32 NextPartitionOffset;
    u64 DestinationExecutionAddress;
    u64 DestinationLoadAddress;
    u32 DataWordOffset;
    u32 PartitionAttributes;
    u32 SectionCount;
    u32 ChecksumWordOffset;
    u32 ImageHeaderOffset;
    u32 AuthCertificateOffset;
    u32 Iv;
    u32 Checksum;
} XFsbl_PartitionHeader;

#define XIH_PH_LEN                     (0x40U)

/* =========================================================================
 * QSPI & Memory Map Configuration
 * ========================================================================= */
#define QSPI_DEVICE_ID                 0U

/** QSPI Flash offsets (2 MB and 4 MB boundaries) */
#define QSPI_APU_FLASH_OFFSET          0x00200000U  /* APU Bare-metal App */
#define QSPI_BITSTREAM_FLASH_OFFSET    0x00400000U  /* PL Bitstream (~5.4 MB) */

/** DDR staging addresses */
#define APU_DDR_DEFAULT_TARGET         0x10000000U  /* 256 MB */
#define BITSTREAM_DDR_TEMP_TARGET      0x20000000U  /* 512 MB temp buffer */

#define APU_DEFAULT_APP_SIZE           0x00080000U  /* 512 KB */
#define BITSTREAM_DEFAULT_SIZE         0x0054F89CU  /* Exact led.bin size: 5,568,668 bytes */

/** Chunk size for each QSPI polled transfer (4 KB) */
#define QSPI_READ_CHUNK                0x1000U

/* Standard 3-byte address READ command for 16 MB QSPI flash */
#define FLASH_CMD_READ_3B              0x03U

/* Driver Fallbacks */
#ifndef XQSPIPSU_MANUAL_START_EN_OPTION
#define XQSPIPSU_MANUAL_START_EN_OPTION     0x10U
#endif
#ifndef XQSPIPSU_HOLD_B_DRIVE_OPTION
#define XQSPIPSU_HOLD_B_DRIVE_OPTION        0x800U
#endif
#ifndef XQSPIPSU_MSG_FLAG_TX
#define XQSPIPSU_MSG_FLAG_TX                0x4U
#endif
#ifndef XQSPIPSU_MSG_FLAG_RX
#define XQSPIPSU_MSG_FLAG_RX                0x2U
#endif
#ifndef XQSPIPSU_SELECT_FLASH_CS0
#define XQSPIPSU_SELECT_FLASH_CS0           0x1U
#endif
#ifndef XQSPIPSU_SELECT_MODE_SPI
#define XQSPIPSU_SELECT_MODE_SPI            0x1U
#endif

/* Global driver instances */
static XQspiPsu QspiInst;
static XIpiPsu  IpiInst;

/* =========================================================================
 * QSPI Initialization
 * ========================================================================= */
static int QSPI_Init(void)
{
    XQspiPsu_Config *QspiConfig;
    int Status;

    xil_printf("RPU: Initializing QSPI controller...\r\n");

    QspiConfig = XQspiPsu_LookupConfig(QSPI_DEVICE_ID);
    if (QspiConfig == NULL) {
        xil_printf("RPU: ERROR - QSPI LookupConfig failed\r\n");
        return XST_FAILURE;
    }

    Status = XQspiPsu_CfgInitialize(&QspiInst, QspiConfig, QspiConfig->BaseAddress);
    if (Status != XST_SUCCESS) {
        xil_printf("RPU: ERROR - QSPI CfgInitialize failed (%d)\r\n", Status);
        return XST_FAILURE;
    }

    XQspiPsu_SetOptions(&QspiInst,
                        XQSPIPSU_MANUAL_START_EN_OPTION |
                        XQSPIPSU_HOLD_B_DRIVE_OPTION);

    XQspiPsu_SetClkPrescaler(&QspiInst, XQSPIPSU_CLK_PRESCALE_8);

    xil_printf("RPU: QSPI controller initialized OK\r\n");
    return XST_SUCCESS;
}

/* =========================================================================
 * QSPI Read helper (3-byte address mode)
 * ========================================================================= */
static int QSPI_ReadFlash(u32 flash_addr, u8 *buffer, u32 length)
{
    XQspiPsu_Msg FlashMsg[2];
    u8 TxBuf[4];
    int Status;

    TxBuf[0] = FLASH_CMD_READ_3B;
    TxBuf[1] = (u8)((flash_addr >> 16) & 0xFFU);
    TxBuf[2] = (u8)((flash_addr >>  8) & 0xFFU);
    TxBuf[3] = (u8)((flash_addr      ) & 0xFFU);

    memset(FlashMsg, 0, sizeof(FlashMsg));

    FlashMsg[0].TxBfrPtr  = TxBuf;
    FlashMsg[0].RxBfrPtr  = NULL;
    FlashMsg[0].ByteCount = 4U;
    FlashMsg[0].BusWidth  = XQSPIPSU_SELECT_MODE_SPI;
    FlashMsg[0].Flags     = XQSPIPSU_MSG_FLAG_TX;

    FlashMsg[1].TxBfrPtr  = NULL;
    FlashMsg[1].RxBfrPtr  = buffer;
    FlashMsg[1].ByteCount = length;
    FlashMsg[1].BusWidth  = XQSPIPSU_SELECT_MODE_SPI;
    FlashMsg[1].Flags     = XQSPIPSU_MSG_FLAG_RX;

    XQspiPsu_Select(&QspiInst, XQSPIPSU_SELECT_FLASH_CS0);

    Status = XQspiPsu_PolledTransfer(&QspiInst, FlashMsg, 2U);
    if (Status != XST_SUCCESS) {
        xil_printf("RPU: ERROR - PolledTransfer failed at 0x%08X\r\n", flash_addr);
        return XST_FAILURE;
    }

    return XST_SUCCESS;
}

/* =========================================================================
 * XFsbl_ValidateChecksum (Adapted from xfsbl_image_header.c)
 *  Calculates inverted 32-bit word sum: ~sum(Buffer[0..WordLen-2])
 * ========================================================================= */
static u32 XFsbl_ValidateChecksum(const u32 *Buffer, u32 WordLen)
{
    u32 Checksum = 0U;
    u32 Count;

    for (Count = 0U; Count < (WordLen - 1U); Count++) {
        Checksum += Buffer[Count];
    }

    Checksum = ~Checksum;

    if (Buffer[WordLen - 1U] != Checksum) {
        return XST_FAILURE;
    }

    return XST_SUCCESS;
}

/* =========================================================================
 * XFsbl_CalculatePayloadChecksum
 *  Computes 32-bit word checksum over loaded payload in RAM
 * ========================================================================= */
static u32 XFsbl_CalculatePayloadChecksum(const u32 *Buffer, u32 WordLen)
{
    u32 Checksum = 0U;
    u32 Count;

    for (Count = 0U; Count < WordLen; Count++) {
        Checksum += Buffer[Count];
    }

    return ~Checksum;
}

/* =========================================================================
 * XFsbl_PartitionHeaderValidation
 *  Validates partition header checksum and basic sanity checks
 * ========================================================================= */
static int XFsbl_PartitionHeaderValidation(const XFsbl_PartitionHeader *Header)
{
    u32 Status;

    xil_printf("RPU: Validating Partition Header...\r\n");

    Status = XFsbl_ValidateChecksum((const u32 *)Header, XIH_PH_LEN / 4U);
    if (Status != XST_SUCCESS) {
        xil_printf("RPU: WARNING - Partition Header Checksum Failed!\r\n");
        return XST_FAILURE;
    }

    xil_printf("RPU: Partition Header Checksum PASSED!\r\n");
    xil_printf("     Payload Words : %u (%u bytes)\r\n",
               Header->TotalDataWordLength,
               Header->TotalDataWordLength * 4U);
    xil_printf("     Load Addr     : 0x%08X\r\n",
               (u32)Header->DestinationLoadAddress);
    xil_printf("     Exec Addr     : 0x%08X\r\n",
               (u32)Header->DestinationExecutionAddress);

    return XST_SUCCESS;
}

/* =========================================================================
 * Load Partition Data from QSPI into DDR
 * ========================================================================= */
static int Load_Partition_Data(u32 flash_offset, u32 ddr_addr, u32 size_bytes)
{
    u8  *dst  = (u8 *)(uintptr_t)ddr_addr;
    u32  done = 0U;
    u32  to_read;
    int  Status;

    xil_printf("RPU: Loading Partition Payload from QSPI\r\n");
    xil_printf("     Flash offset : 0x%08X\r\n", flash_offset);
    xil_printf("     DDR address  : 0x%08X\r\n", ddr_addr);
    xil_printf("     Size         : %u bytes\r\n", size_bytes);

    while (done < size_bytes) {
        to_read = size_bytes - done;
        if (to_read > QSPI_READ_CHUNK) {
            to_read = QSPI_READ_CHUNK;
        }

        Status = QSPI_ReadFlash(flash_offset + done, dst + done, to_read);
        if (Status != XST_SUCCESS) {
            xil_printf("RPU: ERROR - Read failed at offset 0x%08X\r\n", flash_offset + done);
            return XST_FAILURE;
        }

        done += to_read;

        if ((done % 0x100000U) == 0U) {
            xil_printf("RPU: ... %u / %u bytes loaded\r\n", done, size_bytes);
        }
    }

    /* Flush D-Cache so CSUDMA / APU sees physical RAM updates */
    Xil_DCacheFlushRange(ddr_addr, size_bytes);

    /* Memory barriers + delay to ensure AXI write buffers fully drain to DDR */
    dsb();
    isb();
    usleep(10000U); /* 10 ms delay */

    xil_printf("RPU: Partition Payload loaded & D-Cache flushed (%u bytes)\r\n", done);
    return XST_SUCCESS;
}

/* =========================================================================
 * Initialize IPI and XilPM for PMUFW Communication
 * ========================================================================= */
static int PMU_Init(void)
{
    XIpiPsu_Config *IpiConfig;
    XStatus Status;

    IpiConfig = XIpiPsu_LookupConfig(0U);
    if (IpiConfig == NULL) {
        xil_printf("RPU: ERROR - IPI LookupConfig failed\r\n");
        return XST_FAILURE;
    }

    Status = XIpiPsu_CfgInitialize(&IpiInst, IpiConfig, IpiConfig->BaseAddress);
    if (Status != XST_SUCCESS) {
        xil_printf("RPU: ERROR - IPI CfgInitialize failed (%d)\r\n", Status);
        return XST_FAILURE;
    }

    Status = XPm_InitXilpm(&IpiInst);
    if (Status != XST_SUCCESS) {
        xil_printf("RPU: ERROR - XPm_InitXilpm failed (%d)\r\n", Status);
        return XST_FAILURE;
    }

    return XST_SUCCESS;
}

/* =========================================================================
 * Program PL Bitstream via xilfpga & PMUFW
 * ========================================================================= */
/* Global or static instance */
static XFpga XFpgaInstance;

static int Program_PL_Bitstream(u32 ddr_addr, u32 size_bytes)
{
    u32 Status;
    xil_printf("\r\n--- Programming PL Bitstream via xilfpga ---\r\n");

    /* 1. Initialize XilFPGA */
    Status = XFpga_Initialize(&XFpgaInstance);
    if (Status != XFPGA_SUCCESS) {
        xil_printf("RPU: ERROR - XFpga_Initialize failed (0x%08X)\r\n", Status);
        return XST_FAILURE;
    }

    xil_printf("RPU: Loading bitstream from DDR 0x%08X (size: %u bytes)...\r\n",
               ddr_addr, size_bytes);

    /* FSBL performs AFI reset configuration during PS initialization. */
    psu_afi_config();

    /* 2. Flush D-Cache before DMA / PMUFW transfer */
    Xil_DCacheFlushRange(ddr_addr, size_bytes);

    /* 3. Load Bitstream via xilfpga */
    Status = XFpga_BitStream_Load(&XFpgaInstance,
                                  (UINTPTR)ddr_addr,
                                  0U,
                                  size_bytes,
                                  XFPGA_FULLBIT_EN);
    if (Status != XFPGA_SUCCESS) {
        xil_printf("RPU: ERROR - XFpga_BitStream_Load failed (0x%08X)\r\n", Status);
        return XST_FAILURE;
    }
    xil_printf("RPU: SUCCESS - FPGA configured and running!\r\n");

    /* Match the generated FSBL post-configuration sequence. */
    xil_printf("RPU: Applying generated PS-PL power and reset sequence...\r\n");
    psu_ps_pl_isolation_removal_data();
    psu_ps_pl_reset_config_data();

    xil_printf("RPU: PL Post-Config complete! Fabric and clock active.\r\n");
    return XST_SUCCESS;
}

/* =========================================================================
 * Boot APU Core 0 via PMUFW only (no direct APU register access from R5)
 * ========================================================================= */
static int Boot_APU_Via_PMUFW(u32 target_address)
{
    XStatus Status;

    /* Step 1: Force A53-0 fully into reset via PMUFW.
     * This ensures XPm_RequestWakeUp will resample RVBAR on reset release. */
    xil_printf("RPU: [1/2] Forcing APU Core 0 power down via PMUFW...\r\n");
    XPm_ForcePowerDown(NODE_APU_0, REQUEST_ACK_BLOCKING);

    /* Step 2: Request PMUFW to set RVBAR=target_address, then release reset.
     * setAddress=1 tells PMUFW to write RVBAR before releasing A53-0 from reset. */
    xil_printf("RPU: [2/2] Requesting APU Core 0 boot at 0x%08X...\r\n", target_address);
    Status = XPm_RequestWakeUp(NODE_APU_0, 1U, (u64)target_address, REQUEST_ACK_NO);
    if (Status != XST_SUCCESS) {
        xil_printf("RPU: ERROR - XPm_RequestWakeUp failed (%d)\r\n", Status);
        return XST_FAILURE;
    }

    xil_printf("RPU: APU Core 0 successfully booted at 0x%08X!\r\n", target_address);
    return XST_SUCCESS;
}


/* =========================================================================
 * main
 * ========================================================================= */
int main(void)
{
    int Status;
    XFsbl_PartitionHeader Header;
    u32 LoadAddress;
    u32 ExecAddress;
    u32 PayloadSize;
    u32 FlashPayloadOffset;
    u32 CalculatedChecksum;

    xil_printf("\r\n==========================================\r\n");
    xil_printf("  RPU Bootloader (FSBL-Style Loader)\r\n");
    xil_printf("==========================================\r\n");

    /* 1. Test DDR */
    xil_printf("RPU: Testing DDR at 0x%08X...\r\n", APU_DDR_DEFAULT_TARGET);
    volatile u32 *test_ptr = (volatile u32 *)(uintptr_t)APU_DDR_DEFAULT_TARGET;
    *test_ptr = 0xDEADBEEFU;

    if (*test_ptr == 0xDEADBEEFU) {
        xil_printf("RPU: DDR OK\r\n");
    } else {
        xil_printf("RPU: ERROR - DDR write failed! Halting.\r\n");
        goto halt;
    }

    /* 2. Init QSPI */
    Status = QSPI_Init();
    if (Status != XST_SUCCESS) goto halt;

    /* 3. Init PMU / XilPM */
    Status = PMU_Init();
    if (Status != XST_SUCCESS) goto halt;

    /* ---------------------------------------------------------------------
     * PART 1: PL Bitstream Loading (separate raw file at QSPI 0x00400000)
     * --------------------------------------------------------------------- */
    xil_printf("\r\n--- [STAGE 1] PL Bitstream Loading ---\r\n");
    xil_printf("RPU: Using raw Bitstream mode at QSPI 0x%08X...\r\n",
               QSPI_BITSTREAM_FLASH_OFFSET);
    LoadAddress        = BITSTREAM_DDR_TEMP_TARGET;
    PayloadSize        = BITSTREAM_DEFAULT_SIZE;
    FlashPayloadOffset = QSPI_BITSTREAM_FLASH_OFFSET;

    Status = Load_Partition_Data(FlashPayloadOffset, LoadAddress, PayloadSize);
    if (Status != XST_SUCCESS) {
        xil_printf("RPU: WARNING - Failed to load bitstream from QSPI. Skipping PL config.\r\n");
    } else {
        Status = Program_PL_Bitstream(LoadAddress, PayloadSize);
        if (Status != XST_SUCCESS) {
            xil_printf("RPU: WARNING - Bitstream programming failed!\r\n");
        }
    }

    /* ---------------------------------------------------------------------
     * PART 2: APU Application Loading & Boot (QSPI Offset: 0x00200000)
     * --------------------------------------------------------------------- */
    xil_printf("\r\n--- [STAGE 2] APU Application Loading ---\r\n");
    Status = QSPI_ReadFlash(QSPI_APU_FLASH_OFFSET, (u8 *)&Header, XIH_PH_LEN);
    if (Status != XST_SUCCESS) goto halt;

    Status = XFsbl_PartitionHeaderValidation(&Header);
    if (Status == XST_SUCCESS) {
        LoadAddress        = (u32)Header.DestinationLoadAddress;
        ExecAddress        = (u32)Header.DestinationExecutionAddress;
        PayloadSize        = Header.TotalDataWordLength * 4U;
        FlashPayloadOffset = QSPI_APU_FLASH_OFFSET + (Header.DataWordOffset * 4U);
    } else {
        xil_printf("RPU: Falling back to raw binary mode for APU app at 0x%08X...\r\n",
                   QSPI_APU_FLASH_OFFSET);
        LoadAddress        = APU_DDR_DEFAULT_TARGET;
        ExecAddress        = APU_DDR_DEFAULT_TARGET;
        PayloadSize        = APU_DEFAULT_APP_SIZE;
        FlashPayloadOffset = QSPI_APU_FLASH_OFFSET;
    }

    Status = Load_Partition_Data(FlashPayloadOffset, LoadAddress, PayloadSize);
    if (Status != XST_SUCCESS) goto halt;

    CalculatedChecksum = XFsbl_CalculatePayloadChecksum((const u32 *)(uintptr_t)LoadAddress,
                                                         PayloadSize / 4U);
    xil_printf("RPU: Calculated Payload Checksum: 0x%08X\r\n", CalculatedChecksum);

    /* Boot APU Core 0 via PMUFW */
    Status = Boot_APU_Via_PMUFW(ExecAddress);
    if (Status != XST_SUCCESS) goto halt;

    xil_printf("RPU: Boot process completed successfully! Entering background loop.\r\n");
    while (1) {}

halt:
    xil_printf("RPU: HALTED due to error.\r\n");
    while (1) {}

    return 0;
}