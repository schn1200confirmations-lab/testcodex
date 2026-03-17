import json
import tkinter as tk
from dataclasses import dataclass, field
from tkinter import filedialog, messagebox, ttk
from typing import Dict, List


CONFIG_PATH = "planner_config.json"


@dataclass
class PlannerConfig:
    columns: List[str] = field(default_factory=lambda: [
        "Task",
        "Owner",
        "Priority",
        "Status",
        "Due Date",
        "Notes",
    ])
    dropdowns: Dict[str, List[str]] = field(default_factory=lambda: {
        "Priority": ["Low", "Medium", "High"],
        "Status": ["Not Started", "In Progress", "Blocked", "Done"],
    })


class TaskPlannerApp(tk.Tk):
    def __init__(self, config: PlannerConfig) -> None:
        super().__init__()
        self.title("Task Planner (Desktop Starter)")
        self.geometry("1100x640")
        self.config_data = config

        self.entries: Dict[str, ttk.Widget] = {}
        self._build_layout()

    def _build_layout(self) -> None:
        top_frame = ttk.Frame(self, padding=12)
        top_frame.pack(fill=tk.X)

        heading = ttk.Label(
            top_frame,
            text="Task Planner – starter build",
            font=("Segoe UI", 14, "bold"),
        )
        heading.pack(anchor=tk.W)

        subheading = ttk.Label(
            top_frame,
            text=(
                "Send your Excel columns / validation lists and I'll map them here. "
                "Current fields are placeholders."
            ),
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
                combo = ttk.Combobox(form_frame, values=values, state="readonly", width=22)
                combo.set(values[0])
                widget = combo
            else:
                entry = ttk.Entry(form_frame, width=24)
                widget = entry

            widget.grid(row=row, column=col + 1, sticky=tk.W, padx=(0, 18), pady=6)
            self.entries[column] = widget

        controls = ttk.Frame(self, padding=(12, 10))
        controls.pack(fill=tk.X)

        ttk.Button(controls, text="Add Task", command=self.add_task).pack(side=tk.LEFT)
        ttk.Button(controls, text="Clear", command=self.clear_form).pack(side=tk.LEFT, padx=8)
        ttk.Button(controls, text="Export CSV", command=self.export_csv).pack(side=tk.LEFT)

        table_frame = ttk.Frame(self, padding=12)
        table_frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(table_frame, columns=self.config_data.columns, show="headings")
        for column in self.config_data.columns:
            self.tree.heading(column, text=column)
            self.tree.column(column, width=170, anchor=tk.W)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _value_from_widget(self, widget: ttk.Widget) -> str:
        if isinstance(widget, ttk.Combobox):
            return widget.get().strip()
        if isinstance(widget, ttk.Entry):
            return widget.get().strip()
        return ""

    def add_task(self) -> None:
        values = [self._value_from_widget(self.entries[c]) for c in self.config_data.columns]
        if not any(values):
            messagebox.showwarning("Empty task", "Please enter at least one value.")
            return
        self.tree.insert("", tk.END, values=values)

    def clear_form(self) -> None:
        for column, widget in self.entries.items():
            if isinstance(widget, ttk.Combobox):
                options = self.config_data.dropdowns.get(column, [])
                widget.set(options[0] if options else "")
            elif isinstance(widget, ttk.Entry):
                widget.delete(0, tk.END)

    def export_csv(self) -> None:
        rows = [self.tree.item(item_id, "values") for item_id in self.tree.get_children()]
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

        with open(path, "w", encoding="utf-8") as f:
            f.write(",".join(self.config_data.columns) + "\n")
            for row in rows:
                sanitized = [str(cell).replace(",", " ") for cell in row]
                f.write(",".join(sanitized) + "\n")

        messagebox.showinfo("Export complete", f"Saved {len(rows)} task(s) to {path}")


def load_config(path: str = CONFIG_PATH) -> PlannerConfig:
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        return PlannerConfig(
            columns=raw.get("columns", PlannerConfig().columns),
            dropdowns=raw.get("dropdowns", PlannerConfig().dropdowns),
        )
    except FileNotFoundError:
        return PlannerConfig()


if __name__ == "__main__":
    app = TaskPlannerApp(load_config())
    app.mainloop()
