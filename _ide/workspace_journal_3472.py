# 2026-08-03T13:31:44.787874600
import vitis

client = vitis.create_client()
client.set_workspace(path="vitis_workspace")

comp = client.get_component(name="rpu_hello_app")
status = comp.clean()

vitis.dispose()

