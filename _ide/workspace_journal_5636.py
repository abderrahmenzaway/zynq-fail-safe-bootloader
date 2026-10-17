# 2026-08-04T11:31:32.612860800
import vitis

client = vitis.create_client()
client.set_workspace(path="vitis_workspace")

comp = client.get_component(name="hello_world_component")
status = comp.clean()

platform = client.get_component(name="hello")
status = platform.build()

comp.build()

comp = client.get_component(name="rpu_hello_app")
status = comp.clean()

status = platform.build()

comp.build()

status = comp.clean()

status = platform.build()

comp.build()

vitis.dispose()

