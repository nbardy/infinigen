# Using the Shader Registry

The shader registry allows you to configure material and lighting shaders entirely via gin files. Each shader set overrides `central_registry` categories to select different combinations of materials and lights.

## Basic usage

Run a generator script with the default shaders defined in `configs_nature/shader_registry.gin`:

```bash
python -m infinigen_examples.generate_nature --task render -g base.gin
```

To swap to another shader set, supply an additional gin file. For example the provided `shader_sets/studio.gin` enables a studio lighting setup and glossy materials:

```bash
python -m infinigen_examples.generate_nature --task render -g base.gin shader_sets/studio.gin
```

You can invoke the same script multiple times with different shader sets to render variations of the same scene:

```bash
# Default shaders
python -m infinigen_examples.generate_nature --task render -g base.gin
# Alternate shader set
python -m infinigen_examples.generate_nature --task render -g base.gin shader_sets/sky.gin
```

Any new shader modules placed under `infinigen/assets/materials` or `infinigen/assets/lighting` can be registered in a gin file and selected in the same way.
