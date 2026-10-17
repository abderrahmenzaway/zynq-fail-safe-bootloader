# 2026-08-11T14:18:22.938569600
import vitis

client = vitis.create_client()
client.set_workspace(path="vitis_workspace")

platform = client.get_component(name="hello")
status = platform.update_hw(hw_design = "$COMPONENT_LOCATION/../../project_0/design_1_wrapper1.xsa")

status = platform.build()

comp = client.get_component(name="hello_world_component")
status = comp.clean()

status = platform.build()

comp.build()

comp = client.get_component(name="rpu_hello_app")
status = comp.clean()

status = platform.build()

comp.build()

status = comp.clean()

status = platform.build()

comp.build()

status = comp.clean()

status = platform.build()

comp.build()

vitis.dispose()

