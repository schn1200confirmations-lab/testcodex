# testcodex

I started your desktop **Task Planner** app so you can continue in Cursor.

## What is included
- `task_planner_desktop.py`: Tkinter desktop app starter with:
  - Dynamic columns from config
  - Dropdown validation lists from config
  - Form to add tasks
  - Table/grid to view tasks
  - CSV export
- `planner_config.json`: editable config file for your exact Excel structure.

## Run
```bash
python3 task_planner_desktop.py
```

## How to customize with your Excel planner
Once you send your existing planner details, update `planner_config.json`:

- `columns`: the exact column names and order from your Excel sheet
- `dropdowns`: validation list data for any column that should be a dropdown

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

## Next step from your side
Please share:
1. Column list (in order)
2. Dropdown validation values per column
3. Screenshot(s) from your current Excel planner

Then I can wire this into a closer version of your production planner (layout, filters, summary cards, etc.).
