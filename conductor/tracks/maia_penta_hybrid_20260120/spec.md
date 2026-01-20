# Specification: Maia Penta Hybrid Analysis Endpoint

## Overview
Create a new high-performance endpoint `POST /analyze/maia-penta` that provides a unified "Family Harmony" dataset. This endpoint combines pairwise relationship mechanics (Maia Matrix) for all possible dyads with a holistic group analysis (Penta Dynamics).

## Functional Requirements
1.  **Endpoint**: `POST /analyze/maia-penta`.
2.  **Input Structure**:
    - `group_type`: String (e.g., "family", "business").
    - `participants`: Dictionary of participant data (same format as `PersonInput`).
    - `verbosity`: Optional string, defaults to `"all"`.
        - `"all"`: Returns full Human Design details for every pair.
        - `"partial"`: Returns only high-level Connection Type and Classification.
3.  **Core Logic**:
    - **Dyad Matrix**: Automatically calculate every possible pair combination from the `participants` list.
    - **Group Sync (Penta)**: Calculate the collective Penta dynamics (active gates, functional roles, and gap analysis) for the entire group.
4.  **Output Structure**:
    - `penta_dynamics`: Technical summary of the group "Entity".
    - `dyad_matrix`: A list or dictionary of pairwise relationship analyses.

## Non-Functional Requirements
- **Performance**: Use async processing for batch geocoding and calculations to ensure low latency.
- **Interoperability**: Structure JSON to be directly consumable by the `compmatrix_interpretation.md` interpretation engine.

## Acceptance Criteria
- [ ] Successful POST request with 3-5 participants returns both Penta and Dyad data.
- [ ] `verbosity=partial` correctly filters the `dyad_matrix` to high-level summaries only.
- [ ] Error handling for < 2 participants.
- [ ] 100% test coverage using the geocoding bypass strategy.
