# Registry Implementation TODO

This document lists the outstanding tasks for completing a fully functional registry that allows materials and lighting to be swapped via gin configuration. It should be read together with [registry_design_doc.md](./registry_design_doc.md).

## 1. Core Module
- [x] Create `infinigen/core/registry.py` implementing `ShaderRegistry` and `CentralRegistry` as described in the design document.
- [x] Unit tests for registry initialization and sampling.

## 2. Gin Configuration
- [x] Add example gin files under `infinigen_examples/configs_nature/shader_sets/` demonstrating how to register material and lighting categories.
- [x] Update existing gin configs to initialize the central registry.

## 3. Integration
- [x] Replace direct material and lighting imports in the codebase with registry lookups where appropriate.
- [x] Ensure `execute_tasks.py` initializes the central registry before scene generation begins.

## 4. Documentation
- [x] Expand user documentation with instructions on adding shaders and registering new categories.
- [x] Provide a quickstart example showing how to render with different shader sets.

## 5. Testing and Validation
- [x] Validate the registry by rendering scenes with multiple shader sets.
- [x] Extend automated tests to cover registry-based shader selection.

Once these tasks are complete, the shader registry will provide a consistent mechanism to swap surface, material, and lighting implementations from configuration files alone.
