# 2026-07-29T09:53:50.606264
import vitis

client = vitis.create_client()
client.set_workspace(path="vitis_workspace")

platform = client.get_component(name="hello")
domain = platform.get_domain(name="standalone_psu_cortexr5_0")

status = domain.set_lib(lib_name="xilfpga", path="C:\AMDDesignTools\2025.2\Vitis\data\embeddedsw\lib\sw_services\xilfpga_v6_9")

status = domain.set_lib(lib_name="xilpm", path="C:\AMDDesignTools\2025.2\Vitis\data\embeddedsw\lib\sw_services\xilpm_v6_1")

status = platform.build()

comp = client.get_component(name="rpu_hello_app")
comp.build()

status = platform.build()

status = platform.build()

status = platform.build()

comp.build()

status = platform.build()

comp.build()

status = platform.build()

comp.build()

status = platform.build()

comp.build()

status = platform.build()

comp.build()

status = platform.build()

comp.build()

status = platform.build()

comp.build()

status = platform.build()

comp.build()

vitis.dispose()

