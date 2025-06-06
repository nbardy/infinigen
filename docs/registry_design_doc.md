# Registry Design for Swappable Shaders

## Overview

Infinigen currently exposes a registry pattern only for surfaces. Assets like materials
and lighting are referenced directly in Python or via gin bindings. To make all shaders
(swapping lighting or material implementations) configurable from gin, a unified registry
pattern can be introduced.

## Existing Shader Locations

- **Material shaders**: `infinigen/assets/materials` and its subfolders. There are
  over 150 modules containing `def shader_*` functions.
- **Lighting presets**: `infinigen/assets/lighting` contains modules such as
  `sky_lighting.py`, `three_point_lighting.py`, `hdri_lighting.py`, and `holdout_lighting.py`.
- **Surface registry**: implemented in `infinigen/core/surface.py` and configured
  via `infinigen_examples/configs_nature/surface_registry.gin`.

Running `grep -R "def shader_" -l infinigen | wc -l` finds 154 shader modules and
`grep -R "def add_lighting" -l infinigen | wc -l` finds 4 lighting modules.

## Central Registry Architecture

Create `core/registry.py` which manages three registries:

```python
class ShaderRegistry:
    def __init__(self):
        self._entries = defaultdict(list)

    @staticmethod
    def resolve(name, prefixes):
        for prefix in prefixes:
            try:
                return importlib.import_module("." + name, prefix)
            except ModuleNotFoundError:
                continue
        raise ValueError(f"Could not find {name}")

    def init_from_gin(self, prefixes, **category_map):
        with gin.unlock_config():
            self._entries.clear()
            for cat, lst in category_map.items():
                self._entries[cat] = [
                    (self.resolve(n, prefixes), w) for n, w in lst
                ]

    def sample(self, cat):
        mods, weights = zip(*self._entries[cat])
        return np.random.choice(mods, p=np.array(weights) / sum(weights))
```

```python
class CentralRegistry:
    def __init__(self):
        self.surfaces = surface.Registry()
        self.materials = ShaderRegistry()
        self.lights = ShaderRegistry()

    @gin.configurable("central_registry")
    def initialize_from_gin(
        self,
        surface_categories=None,
        material_categories=None,
        light_categories=None,
    ):
        if surface_categories:
            self.surfaces.initialize_from_gin(**surface_categories)
        if material_categories:
            self.materials.init_from_gin(
                ["infinigen.assets.materials"],
                **material_categories,
            )
        if light_categories:
            self.lights.init_from_gin(
                ["infinigen.assets.lighting"],
                **light_categories,
            )
```

The unified registry can then be imported by drivers:

```python
from infinigen.core.registry import central_registry

central_registry.initialize_from_gin()

mat_module = central_registry.materials.sample("stylized")
light_module = central_registry.lights.sample("studio")
```

## Example Gin Configuration

Create a gin file `configs_nature/shader_sets/studio.gin`:

```gin
central_registry.material_categories.stylized = [
    ('glass_volume', 1),
    ('marble', 1),
]
central_registry.light_categories.studio = [
    ('three_point_lighting', 1),
    ('hdri_lighting', 1),
]
```

Another gin file `configs_nature/shader_sets/sky.gin`:

```gin
central_registry.material_categories.stylized = [
    ('mud', 1),
    ('tile', 1),
]
central_registry.light_categories.studio = [
    ('sky_lighting', 1),
]
```

## Usage Commands

```bash
# Render a normal scene with the current shaders
python -m infinigen_examples.generate_nature --task render -g base.gin

# Render scene using the studio shader set
python -m infinigen_examples.generate_nature --task render \
    -g base.gin shader_sets/studio.gin

# Render scene using the sky shader set
python -m infinigen_examples.generate_nature --task render \
    -g base.gin shader_sets/sky.gin
```

### Quickstart

```bash
# Use the default shaders defined in `shader_registry.gin`
python -m infinigen_examples.generate_nature --task render -g base.gin

# Swap to the studio set
python -m infinigen_examples.generate_nature --task render -g base.gin shader_sets/studio.gin
```

This design keeps shader selection modular and configurable entirely via gin.

## Adding New Shaders

1. Place your shader module under `infinigen/assets/materials` or a lighting module under `infinigen/assets/lighting`.
2. Edit a gin config (e.g. `shader_registry.gin` or a file under `shader_sets/`) to add the module name and weight under `central_registry.material_categories` or `central_registry.light_categories`.
3. Run your render command with the config included to pick from the updated registry.
