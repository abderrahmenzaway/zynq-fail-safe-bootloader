# 2026-08-19T09:53:26.963838100
import vitis

client = vitis.create_client()
client.set_workspace(path="vitis_workspace")

comp = client.get_component(name="rpu_hello_app")
status = comp.clean()

platform = client.get_component(name="hello")
status = platform.build()

comp.build()

status = platform.build()

comp.build()

status = comp.clean()

status = platform.build()

comp.build()

status = comp.clean()

status = comp.clean()

status = platform.build()

status = comp.clean()

status = platform.build()

comp.build()

vitis.dispose()

