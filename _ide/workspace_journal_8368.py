# 2026-07-29T13:42:32.074297200
import vitis

client = vitis.create_client()
client.set_workspace(path="vitis_workspace")

platform = client.get_component(name="hello")
status = platform.build()

status = platform.remove_boot_bsp()

status = platform.generate_boot_bsp(target_processor="psu_cortexr5_0")

status = platform.build()

domain = platform.get_domain(name="standalone_psu_cortexa53_0")

status = domain.regenerate()

status = domain.regenerate()

status = platform.update_hw(hw_design = "$COMPONENT_LOCATION/../../project_0/design_1_wrapper.xsa")

status = platform.build()

status = platform.build()

comp = client.get_component(name="hello_world_component")
comp.build()

status = comp.clean()

status = platform.build()

status = platform.build()

comp = client.get_component(name="zynqmp_pmufw")
comp.build()

status = platform.build()

comp.build()

status = comp.clean()

status = platform.build()

status = platform.build()

comp = client.get_component(name="hello_world_component")
comp.build()

status = platform.remove_boot_bsp()

status = platform.build()

status = domain.set_lib(lib_name="xilffs", path="C:\AMDDesignTools\2025.2\Vitis\data\embeddedsw\lib\sw_services\xilffs_v5_5")

status = domain.set_lib(lib_name="xilsecure", path="C:\AMDDesignTools\2025.2\Vitis\data\embeddedsw\lib\sw_services\xilsecure_v5_6")

status = domain.set_lib(lib_name="xilpm", path="C:\AMDDesignTools\2025.2\Vitis\data\embeddedsw\lib\sw_services\xilpm_v6_1")

status = domain.regenerate()

status = platform.build()

status = domain.regenerate()

status = platform.build()

status = platform.generate_boot_bsp(target_processor="psu_cortexa53_0")

comp = client.get_component(name="zynqmp_pmufw")
comp.build()

status = platform.build()

status = platform.remove_boot_bsp()

status = platform.build()

status = domain.set_config(option = "lib", param = "XILFFS_read_only", value = "true", lib_name="xilffs")

status = domain.set_config(option = "lib", param = "XILFFS_use_mkfs", value = "false", lib_name="xilffs")

status = domain.set_config(option = "lib", param = "XILSECURE_tpm_support", value = "true", lib_name="xilsecure")

status = platform.build()

comp = client.create_app_component(name="zynqmp_fsbl",platform = "$COMPONENT_LOCATION/../hello/export/hello/hello.xpfm",domain = "standalone_psu_cortexa53_0",template = "zynqmp_fsbl")

status = platform.set_pmufw_elf(path = "$COMPONENT_LOCATION/../zynqmp_pmufw/build/zynqmp_pmufw.elf")

status = platform.build()

comp = client.get_component(name="zynqmp_fsbl")
comp.build()

comp = client.get_component(name="zynqmp_fsbl")
comp.set_app_config(key = "USER_COMPILE_OPTIMIZATION_LEVEL", values = ["-O2"])

status = platform.build()

comp = client.get_component(name="zynqmp_fsbl")
comp.build()

status = comp.clean()

status = platform.build()

comp.build()

comp = client.get_component(name="zynqmp_fsbl")
comp.set_app_config(key = "USER_COMPILE_OPTIMIZATION_LEVEL", values = ["-O2"])

comp.set_app_config(key = "USER_COMPILE_OPTIMIZATION_LEVEL", values = ["-O0"])

comp.set_app_config(key = "USER_COMPILE_OPTIMIZATION_LEVEL", values = ["-O2"])

comp.set_app_config(key = "USER_COMPILE_OPTIMIZATION_LEVEL", values = ["-O0"])

component = client.get_component(name="zynqmp_fsbl")

lscript = component.get_ld_script(path="C:\internship_spulus\vitis_workspace\zynqmp_fsbl\src\lscript.ld")

lscript.set_stack_size("0x1000")

comp = client.get_component(name="zynqmp_fsbl")
status = comp.clean()

status = platform.build()

comp.build()

status = comp.clean()

status = platform.build()

comp.build()

comp = client.get_component(name="zynqmp_fsbl")
comp.set_app_config(key = "USER_COMPILE_OPTIMIZATION_LEVEL", values = ["-O2"])

comp.set_app_config(key = "USER_COMPILE_OPTIMIZATION_LEVEL", values = ["-O0"])

lscript = component.get_ld_script(path="C:\internship_spulus\vitis_workspace\zynqmp_fsbl\src\lscript_a53.ld")

lscript.set_stack_size("0x800")

status = platform.build()

comp = client.get_component(name="zynqmp_fsbl")
comp.build()

lscript.set_stack_size("0x1000")

lscript.set_heap_size("0")

status = platform.build()

comp.build()

status = platform.build()

comp.build()

lscript.set_stack_size("0x2000")

lscript.set_heap_size("1024")

status = platform.build()

comp.build()

lscript.set_stack_size("0x1000")

lscript.set_heap_size("0")

status = comp.clean()

status = comp.clean()

status = platform.build()

comp.build()

lscript.set_stack_size("0x2000")

lscript.set_heap_size("1024")

comp = client.get_component(name="zynqmp_fsbl")
comp.set_app_config(key = "USER_COMPILE_DEFINITIONS", values = [""])

comp.set_app_config(key = "USER_COMPILE_DEFINITIONS", values = ["FSBL_NAND_EXCLUDE"])

comp.set_app_config(key = "USER_COMPILE_DEFINITIONS", values = ["FSBL_NAND_EXCLUDE", "FSBL_USB_EXCLUDE"])

comp = client.get_component(name="zynqmp_fsbl")
status = comp.clean()

status = platform.build()

comp.build()

comp = client.get_component(name="zynqmp_fsbl")
comp.set_app_config(key = "USER_COMPILE_DEFINITIONS", values = ["FSBL_NAND_EXCLUDE", "FSBL_USB_EXCLUDE"])

comp.set_app_config(key = "USER_COMPILE_DEFINITIONS", values = ["FSBL_NAND_EXCLUDE", "FSBL_USB_EXCLUDE"])

comp = client.get_component(name="zynqmp_fsbl")
status = comp.clean()

status = platform.build()

comp.build()

status = comp.clean()

status = comp.clean()

status = comp.clean()

status = platform.build()

comp.build()

status = comp.clean()

status = platform.build()

comp.build()

status = comp.clean()

status = platform.build()

comp.build()

status = platform.build()

comp.build()

status = comp.clean()

status = platform.build()

comp.build()

vitis.dispose()

