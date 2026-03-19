import csv
import json
import tkinter as tk
from dataclasses import dataclass, field
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import Dict, List

from task_db import fetch_tasks, save_tasks

CONFIG_PATH = Path("planner_config.json")
DB_PATH = Path("task_planner.db")
DEFAULT_COLUMNS = ["Task", "Owner", "Priority", "Status", "Due Date", "Notes"]
DEFAULT_DROPDOWNS = {
    "Priority": ["Low", "Medium", "High"],
    "Status": ["Not Started", "In Progress", "Blocked", "Done"],
}


@dataclass
class PlannerConfig:
    columns: List[str] = field(default_factory=lambda: DEFAULT_COLUMNS.copy())
    dropdowns: Dict[str, List[str]] = field(default_factory=lambda: dict(DEFAULT_DROPDOWNS))


class TaskPlannerApp(tk.Tk):
    def __init__(self, config: PlannerConfig) -> None:
        super().__init__()
        self.title("Task Planner (Desktop)")
        self.geometry("1200x700")
        self.minsize(960, 600)
        self.config_data = config

        self.entries: Dict[str, ttk.Widget] = {}
        self.status_var = tk.StringVar(value="Ready.")
        self._build_layout()
        self.load_saved_tasks(show_message=False)

    def _build_layout(self) -> None:
        top_frame = ttk.Frame(self, padding=12)
        top_frame.pack(fill=tk.X)

        heading = ttk.Label(
            top_frame,
            text="Task Planner – desktop app",
            font=("Segoe UI", 14, "bold"),
        )
        heading.pack(anchor=tk.W)

        subheading = ttk.Label(
            top_frame,
            text="Tasks can be added, saved to SQLite, reloaded later, and exported to CSV.",
        )
        subheading.pack(anchor=tk.W, pady=(4, 8))

        form_frame = ttk.LabelFrame(self, text="Task Details", padding=12)
        form_frame.pack(fill=tk.X, padx=12)

        for idx, column in enumerate(self.config_data.columns):
            row = idx // 3
            col = (idx % 3) * 2

            label = ttk.Label(form_frame, text=column)
            label.grid(row=row, column=col, sticky=tk.W, padx=(0, 8), pady=6)

            widget: ttk.Widget
            values = self.config_data.dropdowns.get(column)
            if values:
                combo = ttk.Combobox(form_frame, values=values, state="readonly", width=24)
                combo.set(values[0])
                widget = combo
            else:
                entry = ttk.Entry(form_frame, width=26)
                widget = entry

            widget.grid(row=row, column=col + 1, sticky=tk.EW, padx=(0, 18), pady=6)
            self.entries[column] = widget

        for column_index in range(6):
            form_frame.columnconfigure(column_index, weight=1)

        controls = ttk.Frame(self, padding=(12, 10))
        controls.pack(fill=tk.X)

        buttons = [
            ("Add Task", self.add_task),
            ("Update Selected", self.update_selected_task),
            ("Delete Selected", self.delete_selected_task),
            ("Clear Form", self.clear_form),
            ("Save to Database", self.save_all_tasks),
            ("Reload from Database", self.load_saved_tasks),
            ("Export CSV", self.export_csv),
        ]
        for index, (label, command) in enumerate(buttons):
            ttk.Button(controls, text=label, command=command).grid(
                row=0,
                column=index,
                padx=(0, 8),
                pady=2,
                sticky=tk.W,
            )

        table_frame = ttk.Frame(self, padding=12)
        table_frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(
            table_frame,
            columns=self.config_data.columns,
            show="headings",
            selectmode="browse",
        )
        for column in self.config_data.columns:
            self.tree.heading(column, text=column)
            self.tree.column(column, width=170, anchor=tk.W)

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        status_bar = ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    def _value_from_widget(self, widget: ttk.Widget) -> str:
        if isinstance(widget, ttk.Combobox):
            return widget.get().strip()
        if isinstance(widget, ttk.Entry):
            return widget.get().strip()
        return ""

    def _collect_form_values(self) -> Dict[str, str]:
        return {column: self._value_from_widget(self.entries[column]) for column in self.config_data.columns}

    def _set_form_values(self, values: Dict[str, str]) -> None:
        for column, widget in self.entries.items():
            value = str(values.get(column, ""))
            if isinstance(widget, ttk.Combobox):
                options = self.config_data.dropdowns.get(column, [])
                if value in options:
                    widget.set(value)
                else:
                    widget.set(options[0] if options else value)
            elif isinstance(widget, ttk.Entry):
                widget.delete(0, tk.END)
                widget.insert(0, value)

    def _all_rows(self) -> List[Dict[str, str]]:
        rows: List[Dict[str, str]] = []
        for item_id in self.tree.get_children():
            row_values = self.tree.item(item_id, "values")
            rows.append({column: str(row_values[index]) for index, column in enumerate(self.config_data.columns)})
        return rows

    def add_task(self) -> None:
        values = self._collect_form_values()
        if not any(value.strip() for value in values.values()):
            messagebox.showwarning("Empty task", "Please enter at least one value.")
            return
        self.tree.insert("", tk.END, values=[values[column] for column in self.config_data.columns])
        self.status_var.set("Task added. Click 'Save to Database' to persist it.")

    def update_selected_task(self) -> None:
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showinfo("No selection", "Please select a task to update.")
            return

        values = self._collect_form_values()
        self.tree.item(selected_item[0], values=[values[column] for column in self.config_data.columns])
        self.status_var.set("Selected task updated. Click 'Save to Database' to persist it.")

    def delete_selected_task(self) -> None:
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showinfo("No selection", "Please select a task to delete.")
            return

        self.tree.delete(selected_item[0])
        self.status_var.set("Selected task deleted. Click 'Save to Database' to persist it.")

    def clear_form(self) -> None:
        for column, widget in self.entries.items():
            if isinstance(widget, ttk.Combobox):
                options = self.config_data.dropdowns.get(column, [])
                widget.set(options[0] if options else "")
            elif isinstance(widget, ttk.Entry):
                widget.delete(0, tk.END)
        self.status_var.set("Form cleared.")

    def on_tree_select(self, _event: tk.Event) -> None:
        selected_item = self.tree.selection()
        if not selected_item:
            return

        row_values = self.tree.item(selected_item[0], "values")
        form_values = {column: row_values[index] for index, column in enumerate(self.config_data.columns)}
        self._set_form_values(form_values)
        self.status_var.set("Selected task loaded into the form.")

    def save_all_tasks(self) -> None:
        rows = self._all_rows()
        save_tasks(rows)
        self.status_var.set(f"Saved {len(rows)} task(s) to {DB_PATH}.")
        messagebox.showinfo("Save complete", f"Saved {len(rows)} task(s) to {DB_PATH}")

    def load_saved_tasks(self, show_message: bool = True) -> None:
        rows = fetch_tasks(self.config_data.columns)
        for item_id in self.tree.get_children():
            self.tree.delete(item_id)
        for row in rows:
            self.tree.insert("", tk.END, values=[row[column] for column in self.config_data.columns])

        self.status_var.set(f"Loaded {len(rows)} task(s) from {DB_PATH}.")
        if show_message:
            messagebox.showinfo("Reload complete", f"Loaded {len(rows)} task(s) from {DB_PATH}")

    def export_csv(self) -> None:
        rows = self._all_rows()
        if not rows:
            messagebox.showinfo("No data", "No tasks available to export.")
            return

        path = filedialog.asksaveasfilename(
            title="Export tasks",
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv")],
        )
        if not path:
            return

        with open(path, "w", newline="", encoding="utf-8") as file_handle:
            writer = csv.DictWriter(file_handle, fieldnames=self.config_data.columns)
            writer.writeheader()
            writer.writerows(rows)

        self.status_var.set(f"Exported {len(rows)} task(s) to {path}.")
        messagebox.showinfo("Export complete", f"Saved {len(rows)} task(s) to {path}")


def load_config(path: Path = CONFIG_PATH) -> PlannerConfig:
    if not path.exists():
        return PlannerConfig()

    with path.open("r", encoding="utf-8") as file_handle:
        raw = json.load(file_handle)

    columns = raw.get("columns", DEFAULT_COLUMNS)
    dropdowns = raw.get("dropdowns", DEFAULT_DROPDOWNS)

    if not isinstance(columns, list) or not all(isinstance(column, str) and column.strip() for column in columns):
        raise ValueError("planner_config.json must contain a non-empty string list for 'columns'.")

    if not isinstance(dropdowns, dict):
        raise ValueError("planner_config.json must contain an object for 'dropdowns'.")

    normalized_dropdowns: Dict[str, List[str]] = {}
    for column_name, values in dropdowns.items():
        if not isinstance(column_name, str) or not isinstance(values, list):
            raise ValueError("Each dropdown entry must map a string column name to a list of values.")
        normalized_dropdowns[column_name] = [str(value) for value in values]

    return PlannerConfig(columns=columns, dropdowns=normalized_dropdowns)


if __name__ == "__main__":
    app = TaskPlannerApp(load_config())
    app.mainloop()
