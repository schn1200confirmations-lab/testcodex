# Task Planner Starter (Desktop + Localhost)

This project now supports:

- **Desktop app** (Tkinter + SQLite database)
- **Localhost web app** (Streamlit + SQLite database)

If you use Cursor and want browser-based usage, use the localhost option below.

## 1) Run as desktop app
```bash
python3 task_planner_desktop.py
```

### Desktop app features
- Add a task
- Select an existing row to load it back into the form
- Update selected task
- Delete selected task
- Save all visible tasks to SQLite
- Reload tasks from SQLite
- Export tasks to CSV

### Desktop persistence workflow
1. Fill the form
2. Click **Add Task**
3. Click **Save to Database**
4. Close the app
5. Reopen the app and saved tasks will be loaded automatically

## 2) Run as localhost app

### Install dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Start app
```bash
streamlit run task_planner_web.py
```

Then open:
- `http://localhost:8501`

## Data persistence (database backend)
- Both apps use SQLite and create `task_planner.db` automatically.
- The web app keeps the explicit flow: **Add Task** → **Save to Database**.
- The desktop app loads saved tasks automatically on startup.

## Configure columns and dropdown validation
Edit `planner_config.json`:

- `columns`: exact column names and order from Excel
- `dropdowns`: validation lists for dropdown columns

Example:
```json
{
  "columns": ["Task ID", "Task Name", "Assignee", "Team", "Priority", "Status", "Due Date"],
  "dropdowns": {
    "Priority": ["Low", "Medium", "High", "Critical"],
    "Status": ["Open", "In Progress", "Waiting", "Closed"],
    "Team": ["Sales", "Operations", "Finance", "IT"]
  }
}
```

## Next input needed from you
Send me these and I’ll map them exactly:
1. Your final column list (in order)
2. Dropdown validation values per column
3. Screenshot(s) of your existing Excel planner screens
