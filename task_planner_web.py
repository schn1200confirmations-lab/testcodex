import json
from io import StringIO
from pathlib import Path
from typing import Dict, List

import pandas as pd
import streamlit as st

CONFIG_PATH = Path("planner_config.json")


def load_config() -> tuple[List[str], Dict[str, List[str]]]:
    default_columns = ["Task", "Owner", "Priority", "Status", "Due Date", "Notes"]
    default_dropdowns = {
        "Priority": ["Low", "Medium", "High"],
        "Status": ["Not Started", "In Progress", "Blocked", "Done"],
    }

    if not CONFIG_PATH.exists():
        return default_columns, default_dropdowns

    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    columns = raw.get("columns", default_columns)
    dropdowns = raw.get("dropdowns", default_dropdowns)
    return columns, dropdowns


def build_form(columns: List[str], dropdowns: Dict[str, List[str]]) -> Dict[str, str]:
    values: Dict[str, str] = {}
    grid = st.columns(3)

    for idx, column in enumerate(columns):
        container = grid[idx % 3]
        options = dropdowns.get(column)

        with container:
            if options:
                values[column] = st.selectbox(column, options=options, key=f"field_{column}")
            else:
                values[column] = st.text_input(column, key=f"field_{column}")

    return values


def reset_fields(columns: List[str], dropdowns: Dict[str, List[str]]) -> None:
    for column in columns:
        key = f"field_{column}"
        if key not in st.session_state:
            continue

        options = dropdowns.get(column)
        st.session_state[key] = options[0] if options else ""


def to_csv(rows: List[Dict[str, str]], columns: List[str]) -> str:
    df = pd.DataFrame(rows, columns=columns)
    buffer = StringIO()
    df.to_csv(buffer, index=False)
    return buffer.getvalue()


def main() -> None:
    st.set_page_config(page_title="Task Planner", layout="wide")
    st.title("Task Planner (localhost starter)")
    st.caption(
        "Upload your exact Excel columns and dropdown validation values into planner_config.json "
        "to mirror your existing planner."
    )

    columns, dropdowns = load_config()

    if "tasks" not in st.session_state:
        st.session_state.tasks = []

    with st.form("task_form"):
        task_values = build_form(columns, dropdowns)
        add_clicked = st.form_submit_button("Add Task")

    action_col1, action_col2 = st.columns([1, 1])

    with action_col1:
        if st.button("Clear Current Inputs"):
            reset_fields(columns, dropdowns)
            st.rerun()

    with action_col2:
        if st.button("Clear All Tasks"):
            st.session_state.tasks = []
            st.rerun()

    if add_clicked:
        if any(str(v).strip() for v in task_values.values()):
            st.session_state.tasks.append(task_values)
            st.success("Task added.")
        else:
            st.warning("Enter at least one field before adding a task.")

    st.subheader("Task List")
    if st.session_state.tasks:
        df = pd.DataFrame(st.session_state.tasks, columns=columns)
        st.dataframe(df, use_container_width=True)

        csv_data = to_csv(st.session_state.tasks, columns)
        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name="task_planner_export.csv",
            mime="text/csv",
        )
    else:
        st.info("No tasks yet. Add your first task above.")


if __name__ == "__main__":
    main()
