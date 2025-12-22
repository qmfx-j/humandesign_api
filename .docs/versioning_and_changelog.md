# Versioning and Changelog Methodology

## Versioning Strategy
We adhere to [Semantic Versioning 2.0.0](https://semver.org/).

**Format**: `MAJOR.MINOR.PATCH`

- **MAJOR version**: when you make incompatible API changes.
- **MINOR version**: when you add functionality in a backward compatible manner.
- **PATCH version**: when you make backward compatible bug fixes.

**Current State**:
- Project Phase 1 & 2 Completion -> `0.2.0`
- Upcoming Phase 3 -> `0.3.0`

---

## Changelog Standards
We follow the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format.

**Location**: `CHANGELOG.md` in the root directory.

**Structure**:
- **Unreleased**: Changes not yet tagged.
- **[Version] - Date**: Grouped changes.

**Categories**:
- `Added` for new features.
- `Changed` for changes in existing functionality.
- `Deprecated` for soon-to-be removed features.
- `Removed` for now removed features.
- `Fixed` for any bug fixes.
- `Security` in case of vulnerabilities.

**Example**:
```markdown
## [0.3.0] - 2025-12-20
### Added
- **Wellness Journey**: Specialized flow for diet/environment.
### Changed
- `api.js` now handles PHS decoding.
```
