<!--USE THIS TEMPLATE TO COMPLETE THE CHANGELOG-->
<!--
## [Version number] - YYYY-MM-DD
### Added
-

### Changed
-

### Deprecated
-

### Removed
-

### Fixed
-

### Security
-
-->

# Changelog

All notable changes to this project will be documented in this file.

## 0.2.1 - 2024-06-09

### Fixed

- Fix timeout issue in PR #16 thanks to @chrda81.

## 0.2.0 - 2023-12-25

### Added

- Add tests in CI with pytest, mypy and ruff in PR #13.
- Add `delaybeforesend` argument due to pexpect in PR #12 thanks to @punchagan.

### Changed

- List of `Instructions` are now built by an external function (from `parse.py` for example) and given to `Script` as an argument. This, `Script` is completely independent of implementations of `Instructions`.

### Fixed

- Fix typo in PR #10 thanks to @punchagan.
- Fix when using asciinema argument `--append` in PR #11 thanks to @punchagan.

## 0.1.3 - 2023-06-10
