# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.0] - 2025-09-22

### Changed
- **Refactored project structure for better standards compliance.**
  - Moved test environment from `src/test_env` to a top-level `tests` directory.
  - Added `src/__init__.py` to define the `src` directory as a package.
- **Replaced manual ChromeDriver management with `webdriver-manager`.** This automates driver downloading and improves portability.
- Updated `README.md` extensively to reflect the new project structure, setup instructions, and automated driver management.

### Removed
- **Removed `utils.py` and the hardcoded `chromedriver.exe`**, as they are now obsolete.

### Fixed
- Corrected import paths in `main.py` and `config_models.py` that were broken during refactoring.

## [1.1.0] - 2025-09-21

### Added
- Implemented centralized logging throughout the application using the `logging` module.
- Created local `config.py` and `app_handlers.py` from examples to make the project runnable out-of-the-box.

### Changed
- Replaced all `print()` calls with structured logging.
- Improved error handling in the `WebDriverManager` to be more specific.
- Simplified import logic in `main.py` and `automation_system.py` to be more explicit.

### Fixed
- Removed duplicated HTML content from `tests/pages/page2.html`.
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
