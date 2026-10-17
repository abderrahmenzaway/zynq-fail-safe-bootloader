# 2026-08-18T13:33:04.679908100
import vitis

client = vitis.create_client()
client.set_workspace(path="vitis_workspace")

platform = client.get_component(name="hello")
status = platform.build()

comp = client.get_component(name="rpu_hello_app")
comp.build()

status = platform.build()

comp.build()

status = comp.clean()

status = platform.build()

comp.build()

vitis.dispose()

