# 2026-08-18T11:38:52.281914800
import vitis

client = vitis.create_client()
client.set_workspace(path="vitis_workspace")

platform = client.get_component(name="hello")
status = platform.build()

comp = client.get_component(name="zynqmp_fsbl")
status = comp.clean()

status = platform.build()

comp.build()

status = platform.build()

comp.build()

status = platform.build()

comp = client.get_component(name="zynqmp_pmufw")
comp.build()

status = platform.build()

comp = client.get_component(name="hello_world_component")
comp.build()

comp = client.get_component(name="zynqmp_fsbl")
status = comp.clean()

status = platform.build()

comp.build()

