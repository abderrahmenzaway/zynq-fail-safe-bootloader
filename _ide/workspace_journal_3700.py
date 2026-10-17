# 2026-08-18T13:40:29.484527100
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

client.delete_component(name="rpu_hello_app")

client.delete_component(name="componentName")

comp = client.create_app_component(name="rpu_hello_app",platform = "$COMPONENT_LOCATION/../hello/export/hello/hello.xpfm",domain = "standalone_psu_cortexr5_0")

status = platform.build()

comp.build()

status = platform.build()

comp = client.get_component(name="zynqmp_fsbl")
comp.build()

status = platform.build()

comp = client.get_component(name="rpu_hello_app")
comp.build()

status = platform.build()

comp.build()

status = comp.clean()

status = platform.build()

comp.build()

status = platform.build()

comp.build()

status = platform.build()

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

status = comp.clean()

status = platform.build()

comp.build()

status = comp.clean()

status = platform.build()

comp.build()

status = platform.build()

comp.build()

status = comp.clean()

status = platform.build()

comp.build()

vitis.dispose()

