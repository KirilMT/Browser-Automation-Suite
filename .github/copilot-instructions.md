# AI Assistant Instructions for Generic Browser Automation Framework

This document provides instructions for an AI assistant to help it provide the best possible assistance for this project.

## Project Overview

This project, `Browser-Automation-Suite`, is a modular, reusable automation system built with Python and Selenium WebDriver. It provides a framework for automated browser-based monitoring and interaction with web applications.

## Core Architecture

The framework is designed with a clear separation of concerns:

-   **Configuration (`config_models.py`)**: A hierarchical configuration system manages all settings, from URLs to window sizes.
-   **Automation Core (`automation_system.py`)**: The main orchestrator that manages browser instances and threads.
-   **Browser Interaction (`browser_automation.py`)**: A wrapper around Selenium WebDriver for common browser actions.
-   **Application Logic (`example_app_handlers.py`)**: Contains specific logic for interacting with different pages of a target application. Handlers are designed to be extended for new applications.

## Key Files

-   **`src/automation_system.py`**: The main orchestration class. This is the heart of the system.
-   **`src/config_models.py`**: Defines the configuration classes (`AutomationConfig`, `WindowConfig`, etc.). All settings should be managed here.
-   **`src/browser_automation.py`**: Contains the `WebDriverManager` class, which handles all direct Selenium calls.
-   **`src/example_app_handlers.py`**: Home to the `BasePageHandler` and its implementations (`Page1Handler`, `Page2Handler`). This is where application-specific automation logic resides.
-   **`src/main.py`**: The entry point for running the automation.
-   **`build_exe.ps1`**: The primary script for packaging the application into a standalone executable.

## Development Guidelines

-   **When modifying `config_models.py`**:
    -   Ensure new settings are added to the appropriate dataclass.
    -   Maintain backward compatibility if possible, or document breaking changes clearly.

-   **When modifying `automation_system.py`**:
    -   Be mindful of the multi-threaded nature of the system. Ensure any new operations are thread-safe.
    -   All major workflow changes should be implemented here.

-   **When modifying `example_app_handlers.py`**:
    -   To support a new page or application, create a new class that inherits from `BasePageHandler`.
    -   Do not put generic browser logic here; it belongs in `browser_automation.py`.

-   **General Rules**:
    -   Do not add `print()` statements or other temporary debugging logs to the final code. Use the `logging` module.
    -   Follow the existing class-based architecture.

## Project Structure

```
Browser-Automation-Suite/
├── src/
│   ├── config_models.py       # Configuration management classes
│   ├── browser_automation.py  # WebDriver and browser automation utilities
│   ├── example_app_handlers.py # Application-specific page interaction handlers
│   ├── automation_system.py   # Main orchestration system
│   ├── main.py                # Entry point script
│   ├── example_config.py      # Example configuration templates
│   └── logger_config.py       # Logging setup
├── tests/
│   ├── pages/                 # Dummy HTML pages for local testing
│   └── server_manager.py      # Manages the in-process, threaded test server
├── requirements.txt           # Python dependencies
├── README.md                  # This documentation
├── build_exe.ps1              # PowerShell script for building the executable
└── .gitignore                 # Git ignore rules
```

## Key Features

- **Modular Architecture**: Clean separation of concerns.
- **Dual Browser Setup**: Manages multiple browser instances.
- **Configurable**: Highly customizable through configuration files.
- **Thread-Safe**: Designed for concurrent operations.
- **Error Handling**: Graceful shutdown and error recovery.
- **Hybrid Driver Management**: Uses `webdriver-manager` for development and a bundled driver for the executable.
- **Automated EXE Build**: A robust PowerShell script to package the project.

## Technologies

- **Programming Language:** Python
- **Libraries:** Selenium WebDriver, psutil, webdriver-manager
- **Dependencies:** As listed in `requirements.txt`.

## Quick Test Guide

1.  From the project root, run the main entry point: `python -m src.main`.
2.  The system will launch browser windows and perform automation tasks as defined in the configuration.
3.  To test the executable build, run `build_exe.ps1` in a PowerShell terminal.

## GitHub Issues

When you ask me to work on a GitHub issue, I will use the `gh` command-line tool to get the details of the issue.

You can ask me to list issues, for example:
- "What are the open issues assigned to me?"
- "List all open issues."

I will then use the following command to retrieve the necessary information:
- To see open issues assigned to you: `gh issue list --assignee "@me" --state open`
- To see all open issues: `gh issue list --state open`

## Working on Issues

When you ask me to work on an issue, I will adhere to the following process:

1.  Follow the Workflow: I will first consult the `GIT_WORKFLOW.md` file to understand the prescribed development workflow, including branching strategy, commit message conventions, and pull request procedures.
2.  Command Execution Protocol:
    *   If terminal commands are required for subsequent file modifications, provide all commands bundled together in the correct sequence.
    *   HALT execution and wait for my confirmation that the commands have been run before proceeding with any dependent tasks.
3.  Issue and Sub-Tasks Prioritization:
    *   I will announce which issue and sub-task I am about to work on based on the prioritization.
    *   IMPORTANT: If an issue is broken down into sub-tasks, I will address each sub-task sequentially and independently.
    *   I will provide my plan for the current sub-task and ask for your approval before I start making changes.
    *   I will only proceed to the next sub-task after the current one is fully resolved (each sub-task needs to be commited).
    *   If any of the issues or sub-tasks is already implemented, I will skip it and move to the next one.
    *   I will give information about the status of each issue and sub-task.
    *   After completing a sub-task, I will provide a summary of the changes and wait for your confirmation to proceed to the next one.
