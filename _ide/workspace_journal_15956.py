# 2026-07-27T12:47:50.240282
import vitis

client = vitis.create_client()
client.set_workspace(path="vitis_workspace")

platform = client.create_platform_component(name = "hello",hw_design = "$COMPONENT_LOCATION/../../project_0/design_1_wrapper.xsa",os = "standalone",cpu = "psu_cortexa53_0",domain_name = "standalone_psu_cortexa53_0",architecture = "64-bit",compiler = "gcc")

comp = client.create_app_component(name="hello_world_component",platform = "$COMPONENT_LOCATION/../hello/export/hello/hello.xpfm",domain = "standalone_psu_cortexa53_0")

platform = client.get_component(name="hello")
status = platform.build()

status = platform.build()

comp = client.get_component(name="hello_world_component")
comp.build()

status = platform.build()

comp.build()

domain = platform.get_domain(name="standalone_psu_cortexa53_0")

status = domain.set_lib(lib_name="xilfpga", path="C:\AMDDesignTools\2025.2\Vitis\data\embeddedsw\lib\sw_services\xilfpga_v6_9")

status = domain.remove_lib(lib_name="xilfpga")

status = domain.remove_lib(lib_name="xilmailbox")

status = domain.set_lib(lib_name="xilpm", path="C:\AMDDesignTools\2025.2\Vitis\data\embeddedsw\lib\sw_services\xilpm_v6_1")

status = domain.set_lib(lib_name="xilffs", path="C:\AMDDesignTools\2025.2\Vitis\data\embeddedsw\lib\sw_services\xilffs_v5_5")

status = platform.build()

status = platform.build()

comp.build()

vitis.dispose()

