# testcodex

This repo includes a browser-based **Task Planner Dashboard** for viewing and editing spreadsheet-style task data.

## Get the project
You can run it from this Git repository after cloning it locally:

```bash
git clone <your-repo-url>
cd testcodex
```

## Fastest way to run it
Use the included launcher script:

```bash
./start_frontend.sh
```

That starts a local web server and serves the app at:

```text
http://localhost:8000/index.html
```

## Alternative way to run it
If you prefer running Python directly:

```bash
python3 serve_frontend.py
```

## Files
- `index.html`: frontend markup and controls
- `styles.css`: responsive dashboard styling
- `app.js`: seeded task data, editable table logic, filters, upload/export, and local persistence
- `serve_frontend.py`: one-command local server for the frontend
- `start_frontend.sh`: shell shortcut to launch the local server
- `task_planner_desktop.py`: original Tkinter desktop starter
- `planner_config.json`: original planner config starter

## Frontend features
- Spreadsheet-like editable table with inline cell editing
- Seeded rows based on the shared Google Sheet snapshot
- Search plus filters for department, assignee, and status
- Add, duplicate, delete, and reset rows
- Upload `.xlsx`, `.xls`, `.csv`, or `.json` data
- Export the current table as CSV or JSON
- Browser `localStorage` saving so edits remain after refresh
- `Red Mark Date` (J column) is auto-calculated with `=IF(I3>0,H3+I3,"")`, cannot be edited manually, and turns red when today's date is the same as or later than the computed J-column date
- All date fields are normalized to `DD-MMM-YY` in the table, add-row dialog, uploads, and exports
- Column widths are widened for conventional editing across all columns except `Daily TASK` and `Click Up`

## Notes
- The initial seeded dataset is a local snapshot derived from the shared Google Sheet that was accessible in this environment.
- Uploading a new file replaces the in-browser table with the uploaded sheet's first tab.
- If port `8000` is busy, run with a different port such as `PORT=8010 python3 serve_frontend.py`.
