# Implementation Plan: Maia Penta Hybrid Analysis

## Phase 1: Request & Response Schemas
- [ ] **Red Phase**: Create test for new hybrid schemas (Input/Output)
- [ ] **Green Phase**: Define `HybridAnalysisRequest` and `HybridAnalysisResponse` in `schemas/`
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Request & Response Schemas' (Protocol in workflow.md)

## Phase 2: Core Hybrid Logic
- [ ] **Red Phase**: Create test for `process_hybrid_analysis` in `services/composite.py`
- [ ] **Green Phase**: Implement `process_hybrid_analysis` (orchestrating both Matrix and Penta calculations)
- [ ] **Refactor**: Optimize batch geocoding and loop efficiency
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Core Hybrid Logic' (Protocol in workflow.md)

## Phase 3: API Integration & Verification
- [ ] **Red Phase**: Create integration test for `POST /analyze/maia-penta`
- [ ] **Green Phase**: Implement the endpoint in `routers/composite.py`
- [ ] **Verify**: Ensure geocoding bypass and verbosity flags handle all edge cases
- [ ] Task: Conductor - User Manual Verification 'Phase 3: API Integration & Verification' (Protocol in workflow.md)
