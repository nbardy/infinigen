import gin

from infinigen.core.registry import central_registry
from infinigen.core.util.test_utils import setup_gin


def test_central_registry_init():
    setup_gin("infinigen_examples/configs_nature", configs=["base.gin"])
    gin.parse_config("""
central_registry.material_categories.demo = [('mud', 1)]
central_registry.light_categories.default = [('sky_lighting', 1)]
""")
    central_registry.initialize_from_gin()
    assert "demo" in central_registry.materials._entries
    assert central_registry.lights.sample("default").__name__

