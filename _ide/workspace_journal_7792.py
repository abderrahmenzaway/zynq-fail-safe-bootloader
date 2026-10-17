# 2026-08-03T11:33:03.520488800
import vitis

client = vitis.create_client()
client.set_workspace(path="vitis_workspace")

comp = client.get_component(name="rpu_hello_app")
status = comp.clean()

platform = client.get_component(name="hello")
status = platform.build()

comp.build()

component = client.get_component(name="hello_world_component")

lscript = component.get_ld_script(path="C:\internship_spulus\vitis_workspace\hello_world_component\src\lscript.ld")

lscript.update_memory_region("psu_ddr_0_memory_0", "0x10000000", "0x30000000")

lscript.update_memory_region("psu_ddr_0_memory_0", "0x10000000", "0x20000000")

status = comp.clean()

status = platform.build()

comp.build()

comp = client.get_component(name="hello_world_component")
status = comp.clean()

status = platform.build()

comp.build()

vitis.dispose()

