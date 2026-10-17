#include <stdio.h>
#include "xil_printf.h"
#include "xparameters.h"
#include "xuartps.h"


int main()
{
    /// Write a unique magic number to memory to prove execution
    volatile uint32_t *flag = (volatile uint32_t *)0x1000FF00;
    *flag = 0xDEADBEEF;
    xil_printf("Hello from APU Cortex-A53 Core 0!\r\n");
    while(1) {
        // APU Loop
    }
    return 0;
}