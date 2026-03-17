# Task Planner Starter (Desktop + Localhost)

I updated this project so you can run the planner either as:

- **Desktop app** (Tkinter)
- **Localhost web app** (Streamlit)

If you use Cursor and want browser-based usage, use the localhost option below.

## 1) Run as localhost app (recommended)

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

## 2) Run as desktop app
```bash
python3 task_planner_desktop.py
```

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
