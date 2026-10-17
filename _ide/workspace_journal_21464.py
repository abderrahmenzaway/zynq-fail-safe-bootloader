# 2026-07-29T13:27:14.768016800
import vitis

client = vitis.create_client()
client.set_workspace(path="vitis_workspace")

platform = client.get_component(name="hello")
status = platform.build()

comp = client.get_component(name="rpu_hello_app")
comp.build()

status = platform.build()

comp = client.get_component(name="hello_world_component")
comp.build()

status = platform.build()

comp.build()

vitis.dispose()

