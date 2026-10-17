# 2026-07-31T14:43:52.498350200
import vitis

client = vitis.create_client()
client.set_workspace(path="vitis_workspace")

component = client.get_component(name="hello_world_component")

lscript = component.get_ld_script(path="C:\internship_spulus\vitis_workspace\hello_world_component\src\lscript.ld")

lscript.update_memory_region("psu_ddr_0_memory_0", "0x0", "0x30000000")

component = client.get_component(name="rpu_hello_app")

lscript = component.get_ld_script(path="C:\internship_spulus\vitis_workspace\rpu_hello_app\src\lscript.ld")

lscript.update_memory_region("psu_r5_ddr_0_memory_0", "0x30000000", "0x3fefffff")

lscript.update_memory_region("psu_r5_ddr_0_memory_0", "0x30000000", "0x10000000")

comp = client.get_component(name="hello_world_component")
status = comp.clean()

platform = client.get_component(name="hello")
status = platform.build()

comp.build()

status = comp.clean()

comp = client.get_component(name="rpu_hello_app")
status = comp.clean()

status = platform.build()

comp.build()

status = platform.build()

comp = client.get_component(name="hello_world_component")
comp.build()

status = platform.build()

comp = client.get_component(name="rpu_hello_app")
comp.build()

vitis.dispose()

