# 2026-07-28T09:57:54.042482100
import vitis

client = vitis.create_client()
client.set_workspace(path="vitis_workspace")

platform = client.get_component(name="hello")
domain = platform.add_domain(cpu = "psu_pmu_0",os = "standalone",name = "psu_pmu_0",display_name = "psu_pmu_0",generate_dtb = False,hw_boot_bin = "")

comp = client.create_app_component(name="pmufw",platform = "$COMPONENT_LOCATION/../hello/export/hello/hello.xpfm",domain = "psu_pmu_0")

comp = client.create_app_component(name="zynqmp_pmufw",platform = "$COMPONENT_LOCATION/../hello/export/hello/hello.xpfm",domain = "psu_pmu_0",template = "zynqmp_pmufw")

status = platform.build()

comp = client.get_component(name="zynqmp_pmufw")
comp.build()

status = platform.build()

comp.build()

status = platform.build()

platform = client.get_component(name="hello")
status = platform.build()

status = platform.build()

vitis.dispose()

