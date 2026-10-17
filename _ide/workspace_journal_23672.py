# 2026-07-28T11:01:40.136258400
import vitis

client = vitis.create_client()
client.set_workspace(path="vitis_workspace")

platform = client.get_component(name="hello")
status = platform.build()

client.delete_component(name="hello")

client.delete_component(name="hello")

platform = client.create_platform_component(name = "hello",hw_design = "$COMPONENT_LOCATION/../../project_0/design_1_wrapper.xsa",os = "standalone",cpu = "psu_cortexa53_0",domain_name = "standalone_psu_cortexa53_0",architecture = "64-bit",compiler = "gcc")

status = platform.build()

status = platform.build()

comp = client.get_component(name="zynqmp_pmufw")
comp.build()

status = comp.clean()

status = platform.build()

comp.build()

status = platform.build()

comp.build()

status = platform.build()

comp.build()

client.delete_component(name="zynqmp_pmufw")

domain = platform.add_domain(cpu = "psu_pmu_0",os = "standalone",name = "psu_pmu_0",display_name = "psu_pmu_0",support_app = "zynqmp_pmufw",generate_dtb = False,hw_boot_bin = "")

comp = client.create_app_component(name="zynqmp_pmufw",platform = "$COMPONENT_LOCATION/../hello/export/hello/hello.xpfm",domain = "psu_pmu_0",template = "zynqmp_pmufw")

status = platform.build()

comp.build()

vitis.dispose()

