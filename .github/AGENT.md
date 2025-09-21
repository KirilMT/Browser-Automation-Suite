# Gemini Code Assist Instructions

This document provides instructions for Gemini Code Assist to help it provide the best possible assistance for the **Generic Browser Automation Framework**.

## Core Principles for Assistance

-   **Efficiency is Key:** Please perform all necessary edits for a given task in a single step. Avoid making multiple, sequential edits to the same file for the same topic.
-   **Be Concise:** Do not repeat the same information or plans multiple times. Provide important information when necessary—not less, not more.
-   **Single Edit Rule:** When editing a file, apply *all planned changes in one unified edit*. Do not split the edit into multiple smaller patches. Do not re-edit the same file again for the same request.
-   **No Repetition:** Never repeat the same text, instructions, or edits in multiple replies. Each reply must be unique and progress the task forward.
-   **Atomic Updates:** For each request, complete all necessary modifications in one atomic update per file. Do not provide partial or incremental changes.
-   **One-time Summary:** After making changes, provide a short summary of what was modified. Do not restate the same summary in following replies.
-   **No Restating Code:** If you’ve already shown the final code once, do not output the same code again unless explicitly asked.

## Project Overview

This is a modular, reusable automation system built with Python and Selenium WebDriver. This system provides automated browser-based monitoring and interaction for web applications.

## Key Features

- **Modular Architecture**: Clean separation of concerns with dedicated modules for configuration, browser automation, and application-specific handlers.
- **Dual Browser Setup**: Simultaneously manages multiple browser instances for different tasks.
- **Configurable**: Easily customizable for different web applications through configuration files.
- **Thread-Safe**: Multi-threaded design for concurrent browser operations.
- **Error Handling**: Comprehensive error handling and graceful shutdown mechanisms.
- **Process Management**: Automatic cleanup of browser processes.
- **Automated EXE Build**: Batch and PowerShell scripts for packaging your automation as a standalone executable.

## Technologies

- **Programming Language:** Python
- **Framework/Libraries:** Selenium WebDriver, psutil, pyautogui
- **Dependencies:** Listed in `requirements.txt`.

## Project Structure

```
Browser-Automation-Suite/
├── src/
│   ├── config.py              # Configuration management classes
│   ├── browser_automation.py  # WebDriver and browser automation utilities
│   ├── app_handlers.py        # Application-specific page interaction handlers
│   ├── automation_system.py   # Main orchestration system
│   ├── main.py                # Entry point script
│   ├── example_config.py      # Example configuration templates
│   └── chromedriver.exe       # Chrome WebDriver executable
├── requirements.txt           # Python dependencies
├── README.md                  # This documentation
├── main.spec                  # PyInstaller spec file (ignored by git)
├── build_exe.bat              # Batch script for building EXE
├── build_exe.ps1              # PowerShell script for building EXE
└── .gitignore                 # Git ignore rules
```

## Quick Test Guide

To test the application's end-to-end workflow:
1.  Run the application with `cd src` then `python main.py`.
2.  The system will start the browser automation based on the configuration in `main.py` or a custom config file.
3.  Observe the browser instances performing the automated tasks.
4.  Check the console output for logs and status messages.

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

1.  **Follow the Workflow:** I will first consult the `GIT_WORKFLOW.md` file to understand the prescribed development workflow, including branching strategy, commit message conventions, and pull request procedures.

2.  **Command Execution Protocol:**
    *   If terminal commands are required for subsequent file modifications, provide all commands bundled together in the correct sequence.
    *   **HALT execution and wait for my confirmation** that the commands have been run before proceeding with any dependent tasks.

3.  **Issue and Sub-Tasks Prioritization:**
    *   I will announce which issue and sub-task I am about to work on based on the prioritization.
    *   IMPORTANT: If an issue is broken down into sub-tasks, I will address each sub-task **sequentially and independently**.
    *   I will provide my plan for the current sub-task and ask for your approval before I start making changes.
    *   I will only proceed to the next sub-task after the current one is fully resolved (each sub-task needs to be commited).
    *   If any of the issues or sub-tasks is already implemented, I will skip it and move to the next one.
    *   I will give information about the status of each issue and sub-task.
    *   After completing a sub-task, I will provide a summary of the changes and wait for your confirmation to proceed to the next one.
