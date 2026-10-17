# 2026-08-18T09:38:48.643589900
import vitis

client = vitis.create_client()
client.set_workspace(path="vitis_workspace")

comp = client.get_component(name="hello_world_component")
status = comp.clean()

platform = client.get_component(name="hello")
status = platform.build()

comp.build()

status = platform.build()

status = platform.update_hw(hw_design = "$COMPONENT_LOCATION/../../project_0/design_1_wrapper2.xsa")

status = platform.build()

status = platform.build()

comp.build()

status = platform.build()

comp = client.get_component(name="rpu_hello_app")
comp.build()

status = platform.build()

comp = client.get_component(name="zynqmp_fsbl")
comp.build()

status = platform.build()

comp.build()

status = comp.clean()

status = platform.build()

comp.build()

domain = platform.get_domain(name="standalone_psu_cortexa53_0")

status = domain.remove_lib(lib_name="xilffs")

status = comp.clean()

status = platform.build()

comp.build()

status = domain.remove_lib(lib_name="xilsecure")

status = comp.clean()

status = platform.build()

comp.build()

status = platform.build()

status = comp.clean()

status = platform.build()

comp.build()

status = domain.set_lib(lib_name="xilffs", path="C:\AMDDesignTools\2025.2\Vitis\data\embeddedsw\lib\sw_services\xilffs_v5_5")

status = platform.build()

status = platform.build()

comp.build()

status = platform.build()

status = comp.clean()

status = platform.build()

comp.build()

status = domain.remove_lib(lib_name="xilffs")

status = domain.set_lib(lib_name="xilsecure", path="C:\AMDDesignTools\2025.2\Vitis\data\embeddedsw\lib\sw_services\xilsecure_v5_6")

status = platform.build()

status = platform.build()

comp.build()

status = platform.build()

comp.build()

status = comp.clean()

status = comp.clean()

status = platform.build()

comp.build()

status = domain.regenerate()

status = platform.build()

status = comp.clean()

status = platform.build()

comp.build()

status = platform.build()

status = platform.build()

comp.build()

status = comp.clean()

status = platform.build()

comp.build()

status = domain.set_lib(lib_name="xilffs", path="C:\AMDDesignTools\2025.2\Vitis\data\embeddedsw\lib\sw_services\xilffs_v5_5")

status = domain.regenerate()

status = platform.build()

status = platform.build()

comp.build()

status = platform.build()

comp.build()

component = client.get_component(name="zynqmp_fsbl")

lscript = component.get_ld_script(path="C:\internship_spulus\vitis_workspace\zynqmp_fsbl\src\lscript.ld")

lscript.set_stack_size("0x800")

lscript.set_heap_size("0")

status = comp.clean()

status = comp.clean()

status = platform.build()

comp.build()

vitis.dispose()

