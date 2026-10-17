# 2026-07-31T14:18:19.077953800
import vitis

client = vitis.create_client()
client.set_workspace(path="vitis_workspace")

component = client.get_component(name="rpu_hello_app")

lscript = component.get_ld_script(path="C:\internship_spulus\vitis_workspace\rpu_hello_app\src\lscript.ld")

lscript.update_memory_region("psu_r5_ddr_0_memory_0", "0x10000000", "0x3fefffff")

vitis.dispose()

