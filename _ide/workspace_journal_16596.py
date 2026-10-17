# 2026-08-03T13:37:44.645707100
import vitis

client = vitis.create_client()
client.set_workspace(path="vitis_workspace")

platform = client.get_component(name="hello")
status = platform.build()

comp = client.get_component(name="rpu_hello_app")
comp.build()

status = comp.clean()

status = platform.build()

comp.build()

status = comp.clean()

status = platform.build()

comp.build()

status = comp.clean()

status = platform.build()

comp.build()

comp = client.get_component(name="hello_world_component")
status = comp.clean()

status = platform.build()

comp.build()

comp = client.get_component(name="rpu_hello_app")
status = comp.clean()

status = platform.build()

comp.build()

status = platform.build()

comp.build()

status = platform.build()

comp.build()

vitis.dispose()

