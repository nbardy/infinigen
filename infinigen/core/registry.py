import importlib
from collections import defaultdict
from typing import Any, Dict, Iterable, List, Tuple

import gin
import numpy as np

from . import surface


class ShaderRegistry:
    """Generic registry for modules resolved from name strings."""

    def __init__(self) -> None:
        self._entries: Dict[str, List[Tuple[Any, float]]] = defaultdict(list)

    @staticmethod
    def resolve(name: str, prefixes: Iterable[str]):
        for prefix in prefixes:
            try:
                return importlib.import_module("." + name, prefix)
            except ModuleNotFoundError:
                continue
        raise ValueError(f"Could not find {name}")

    def init_from_gin(self, prefixes: Iterable[str], **category_map):
        with gin.unlock_config():
            self._entries.clear()
            for cat, lst in category_map.items():
                self._entries[cat] = [
                    (self.resolve(n, prefixes), w) for n, w in lst
                ]

    def sample(self, cat: str):
        mods, weights = zip(*self._entries[cat])
        return np.random.choice(mods, p=np.array(weights) / sum(weights))


class CentralRegistry:
    def __init__(self) -> None:
        self.surfaces = surface.Registry()
        self.materials = ShaderRegistry()
        self.lights = ShaderRegistry()

    @gin.configurable("central_registry")
    def initialize_from_gin(
        self,
        surface_categories: Dict[str, Iterable[Tuple[str, float]]] | None = None,
        material_categories: Dict[str, Iterable[Tuple[str, float]]] | None = None,
        light_categories: Dict[str, Iterable[Tuple[str, float]]] | None = None,
    ) -> None:
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


central_registry = CentralRegistry()
