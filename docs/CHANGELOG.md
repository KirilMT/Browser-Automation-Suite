# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.1] - 2025-10-10

### Changed
- Integrated and adapted .github and docs directories from Troubleshooting-Wizard for Browser-Automation-Suite.
- Updated documentation, contribution guidelines, and project instructions to match Browser-Automation-Suite structure and workflow.

## [1.2.3] - 2026-01-18

### Added
- Improved browser monitoring to prevent premature termination when a window is closed.

### Changed
- Fixed Page 1 window layout calculation to prevent overflow on multi-monitor setups.
- Refactored `app_handlers.py` and `example_app_handlers.py` to use `logging` module instead of `print` statements.

## [1.2.2] - 2025-10-24

### Added
- Integrated Python logging system across all modules. All print statements replaced with logger calls for configurable output.
- Added log level control (DEBUG, INFO, WARNING, ERROR) for each module.
- Updated handler templates to use robust logging and error handling.

### Changed
- Documentation updated to reflect logging system and handler customization.
- Improved error handling and output consistency throughout the codebase.

