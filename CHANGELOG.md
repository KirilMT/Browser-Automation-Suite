# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.0] - 2025-09-21

### Added
- Implemented centralized logging throughout the application using the `logging` module.
- Created a central `utils.py` for common utility functions.
- Created local `config.py` and `app_handlers.py` from examples to make the project runnable out-of-the-box.

### Changed
- Refactored ChromeDriver path resolution to a single function in `utils.py` to avoid code duplication.
- Replaced all `print()` calls with structured logging.
- Improved error handling in the `WebDriverManager` to be more specific.
- Simplified import logic in `main.py` and `automation_system.py` to be more explicit.

### Fixed
- Removed duplicated HTML content from `src/test_env/pages/page2.html`.
- Removed placeholder commented-out code from `example_app_handlers.py`.
- Removed the interactive `input()` prompt at the end of `main.py`.

## [1.0.0] - 2025-09-20

### Added
- Initial project setup with a modular architecture for browser automation.
- Core components: `AutomationSystem`, `WebDriverManager`, `ProcessManager`.
- Configuration system using dataclasses (`config_models.py`).
- Example handlers and configuration (`example_app_handlers.py`, `example_config.py`).
- Local test environment with a simple HTTP server.
- Build scripts for creating a standalone executable (`build_exe.bat`, `build_exe.ps1`).
- Comprehensive documentation (`README.md`, `.github` docs).