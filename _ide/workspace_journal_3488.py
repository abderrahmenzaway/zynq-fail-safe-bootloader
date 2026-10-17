# 2026-07-30T10:15:04.856749300
import vitis

client = vitis.create_client()
client.set_workspace(path="vitis_workspace")

platform = client.get_component(name="hello")
status = platform.build()

comp = client.get_component(name="hello_world_component")
comp.build()

status = platform.build()

comp = client.get_component(name="zynqmp_fsbl")
comp.build()

status = platform.build()

comp.build()

comp = client.get_component(name="zynqmp_fsbl")
comp.set_app_config(key = "USER_COMPILE_DEFINITIONS", values = [""])

comp = client.get_component(name="zynqmp_fsbl")
status = comp.clean()

status = platform.build()

comp.build()

status = comp.clean()

status = platform.build()

comp.build()

status = comp.clean()

status = platform.build()

comp.build()

status = platform.set_fsbl_elf(path = "$COMPONENT_LOCATION/../zynqmp_fsbl/build/zynqmp_fsbl.elf")

status = platform.build()

comp = client.get_component(name="hello_world_component")
status = comp.clean()

status = platform.build()

comp.build()

comp = client.get_component(name="rpu_hello_app")
status = comp.clean()

status = platform.build()

comp.build()

comp = client.get_component(name="zynqmp_pmufw")
status = comp.clean()

status = platform.build()

comp.build()

comp = client.get_component(name="rpu_hello_app")
status = comp.clean()

status = platform.build()

comp.build()

vitis.dispose()

