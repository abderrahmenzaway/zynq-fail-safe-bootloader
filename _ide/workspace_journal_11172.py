# 2026-07-30T09:46:02.886677600
import vitis

client = vitis.create_client()
client.set_workspace(path="vitis_workspace")

platform = client.get_component(name="hello")
status = platform.build()

comp = client.get_component(name="hello_world_component")
comp.build()

vitis.dispose()

