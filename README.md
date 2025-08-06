# Personal Projects Repository

This repository contains a collection of small, practical projects developed to demonstrate proficiency in Python programming, including both command-line interface (CLI) applications and a web-based application. Each project serves a distinct purpose, ranging from task management to unit conversion, and is designed to be lightweight and self-contained. Below is an overview of each project included in this repository.

## Projects Overview

### 1. Task Tracker (`simple_task_tracker.py`)

**Description**: A CLI application for managing tasks and to-do lists. It allows users to add, update, delete, and mark tasks as in-progress or done, with persistent storage in a JSON file.

**Features**:
- Add new tasks with a description and automatic ID generation.
- Update task descriptions and statuses (`todo`, `in-progress`, `done`).
- Delete tasks by ID.
- List all tasks or filter by status.
- Persistent storage using `storage.json`.
- Interactive CLI mode or single-command execution via arguments.

**Usage**:
```bash
python simple_task_tracker.py
```
- Interactive mode: Run without arguments and enter commands like `add "Buy groceries"`, `list todo`, or `delete 1`.
- Command-line mode: `python simple_task_tracker.py add "Buy groceries"`.

**Dependencies**: Python standard library (`json`, `os`, `sys`, `datetime`).

**Example**:
```bash
$ python simple_task_tracker.py
task-cli> add "Finish project"
Task added successfully (ID: 1)
task-cli> list
[1] Finish project | todo | Created: 2025-08-06 14:19:00 | Updated: 2025-08-06 14:19:00
```

---

### 2. GitHub User Activity (`github_user_activity.py`)

**Description**: A CLI tool that fetches and displays a GitHub user's recent activity using the GitHub API. It formats events like pushes, issues, pull requests, and repository creation for easy reading.

**Features**:
- Fetches user events from the GitHub API.
- Supports multiple event types: `PushEvent`, `IssuesEvent`, `WatchEvent`, `PullRequestEvent`, `CreateEvent`, and more.
- Formats events with timestamps, repository names, and event-specific details.
- Handles API errors (e.g., rate limits, user not found).

**Usage**:
```bash
python github_user_activity.py
```
- Enter a GitHub username when prompted to see their recent activity (up to 10 events).

**Dependencies**: Python standard library (`urllib`, `json`, `datetime`, `sys`).

**Example**:
```bash
$ python github_user_activity.py
Enter GitHub username: octocat
Fetching recent activity for octocat...
Recent activity for octocat:
--------------------------------------------------
Pushed 3 commits to octocat/Hello-World at 2025-08-01 10:15:00
Starred octocat/Spoon-Knife at 2025-08-01 09:30:00
```

**Note**: Requires an internet connection and respects GitHub API rate limits.

---

### 3. Expense Tracker (`expense_tracker.py`)

**Description**: A CLI application for tracking personal expenses, with support for categorizing expenses and summarizing them by month or category.

**Features**:
- Add expenses with descriptions, amounts, and optional categories.
- Update or delete expenses by ID.
- View all expenses or filter by category.
- Summarize total expenses for a specific month or overall.
- Sort expenses by category (ascending or descending).
- Export expenses to a CSV file.
- Persistent storage in `expenses.json`.

**Usage**:
```bash
python expense_tracker.py
```
- Interactive mode: Enter commands like `add "Lunch" 15.50 Food` or `summarize 07`.
- Command-line mode: `python expense_tracker.py add "Lunch" 15.50 Food`.

**Dependencies**: Python standard library (`csv`, `json`, `os`, `sys`, `datetime`).

**Example**:
```bash
$ python expense_tracker.py
expense-tracker> add "Groceries" 45.00 Food
expense successfully added
expense-tracker> view Food
1: 2025-08-06 | Groceries | 45.0 | Food
```

---

### 4. Number Guessing Game (`number_guessing_game.py`)

**Description**: A CLI-based number guessing game where players try to guess a randomly generated number between 1 and 100, with difficulty levels determining the number of allowed attempts.

**Features**:
- Three difficulty levels: Easy (10 chances), Medium (5 chances), Hard (3 chances).
- Provides hints (e.g., "number is greater/less than") and parity hints for higher difficulties.
- Tracks high scores for each difficulty level.
- Measures time taken to guess correctly.
- Option to play again.

**Usage**:
```bash
python number_guessing_game.py
```
- Follow prompts to select difficulty and enter guesses.

**Dependencies**: Python standard library (`random`, `time`).

**Example**:
```bash
$ python number_guessing_game.py
Welcome to the Number Guessing Game!
I'm thinking of a number between 1 and 100.
Please select the difficulty level:
1. Easy (10 chances)
2. Medium (5 chances)
3. Hard (3 chances)
Enter a number 1, 2 or 3
Please select a difficulty level: 1
Great! You have selected the Easy difficulty level.
Let's start the game!
Please enter your guess: 50
Incorrect guess. The number is less than 50. You have 9 remaining.
```

---

### 5. Unit Converter (`app.py`, `converters.py`)

**Description**: A web-based unit converter built with Flask, allowing conversion between units of length, weight, and temperature. It features a simple HTML interface for selecting categories, units, and input values.

**Features**:
- Supports length (e.g., meter, mile), weight (e.g., gram, pound), and temperature (e.g., Celsius, Fahrenheit) conversions.
- Handles conversions with precise calculations and formatted output.
- Web interface with dropdown menus for category and unit selection.
- Persistent form state for user convenience.

**Files**:
- `app.py`: Flask application handling routes and rendering the HTML template.
- `converters.py`: Conversion logic for length, weight, and temperature units.

**Usage**:
```bash
python app.py
```
- Open a browser and navigate to `http://localhost:5000` to use the converter.

**Dependencies**:
- Flask (`pip install flask`)
- Python standard library

**Example**:
- Access the web app, select "length" category, convert "1 meter" to "foot", and see output: `1 m = 3.280839895 ft`.

**Note**: Requires Flask to be installed. Run in debug mode for development.

---

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Install dependencies (for Unit Converter):
   ```bash
   pip install flask
   ```

3. Run any project:
   ```bash
   python <filename>.py
   ```

## Requirements

- Python 3.6+
- Flask (for Unit Converter only)
- Internet connection (for GitHub User Activity)
- No additional dependencies for CLI apps (use Python standard library).

## Inspiration

https://roadmap.sh/backend/projects

