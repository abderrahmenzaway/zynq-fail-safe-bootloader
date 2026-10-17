# 2026-07-28T13:38:21.529098100
import vitis

client = vitis.create_client()
client.set_workspace(path="vitis_workspace")

platform = client.get_component(name="hello")
status = platform.build()

comp = client.get_component(name="hello_world_component")
comp.build()

domain = platform.get_domain(name="zynqmp_fsbl")

status = domain.regenerate()

status = platform.build()

comp.build()

status = platform.build()

status = platform.build()

comp.build()

status = domain.regenerate()

status = platform.build()

comp.build()

status = platform.build()

comp.build()

status = platform.build()

comp = client.get_component(name="zynqmp_pmufw")
comp.build()

domain = platform.add_domain(cpu = "psu_cortexr5_0",os = "standalone",name = "standalone_psu_cortexr5_0",display_name = "standalone_psu_cortexr5_0",generate_dtb = False,compiler = "gcc",hw_boot_bin = "")

status = platform.build()

comp = client.create_app_component(name="rpu_hello_app",platform = "$COMPONENT_LOCATION/../hello/export/hello/hello.xpfm",domain = "standalone_psu_cortexr5_0")

status = platform.build()

comp = client.get_component(name="rpu_hello_app")
comp.build()

status = platform.build()

comp = client.get_component(name="hello_world_component")
comp.build()

status = platform.build()

comp.build()

vitis.dispose()

