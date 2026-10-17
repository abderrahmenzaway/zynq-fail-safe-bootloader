# 2026-08-12T10:14:29.151977800
import vitis

client = vitis.create_client()
client.set_workspace(path="vitis_workspace")

comp = client.get_component(name="rpu_hello_app")
status = comp.clean()

platform = client.get_component(name="hello")
status = platform.build()

comp.build()

status = comp.clean()

status = platform.build()

comp.build()

