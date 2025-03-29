"""
To Do tab module for the Pixel Quest to-do list.
Manages the main to-do list view and functionality.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import uuid
import calendar


class TodoTab:
    """
    Manages the tasks tab of the to-do list.
    Displays tasks, allows for task management, and provides various viewing options.
    """

    def __init__(self, todo_list, app, data_manager, theme):
        """
        Initialize the to-do tab module.

        Args:
            todo_list: Main todo list instance
            app: Main application instance
            data_manager: Data manager instance
            theme: Theme manager instance
        """
        self.todo_list = todo_list
        self.app = app
        self.data_manager = data_manager
        self.data = data_manager.data
        self.theme = theme
        self.group_filter_var = None
        self.status_filter_var = None
        self.sort_by_var = None

    def create_todo_view(self, parent):
        """
        Create the to-do list view with filters and task list.

        Args:
            parent: Parent frame to place the to-do view
        """
        # Top control panel
        control_frame = tk.Frame(parent, bg=self.theme.bg_color)
        control_frame.pack(pady=5, fill=tk.X)

        # Add task button
        add_task_button = self.theme.create_pixel_button(
            control_frame,
            "Add New Task",
            self.add_new_task,
            color="#4CAF50",
        )
        add_task_button.pack(side=tk.LEFT, padx=10)

        # Filter by group dropdown
        filter_frame = tk.Frame(control_frame, bg=self.theme.bg_color)
        filter_frame.pack(side=tk.LEFT, padx=20)

        tk.Label(
            filter_frame,
            text="Group:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT, padx=5)

        # Get groups for dropdown
        groups = ["All"] + [g["name"] for g in self.data["todo"].get("groups", [])]

        self.group_filter_var = tk.StringVar(value="All")
        group_dropdown = ttk.Combobox(
            filter_frame,
            textvariable=self.group_filter_var,
            values=groups,
            font=self.theme.small_font,
            width=12,
        )
        group_dropdown.pack(side=tk.LEFT, padx=5)

        # Add binding to refresh when filter changes
        group_dropdown.bind(
            "<<ComboboxSelected>>", lambda e: self.todo_list.refresh_display()
        )

        # Filter by status
        status_frame = tk.Frame(control_frame, bg=self.theme.bg_color)
        status_frame.pack(side=tk.LEFT, padx=20)

        tk.Label(
            status_frame,
            text="Status:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT, padx=5)

        statuses = ["Active", "Completed", "All"]
        self.status_filter_var = tk.StringVar(value="Active")
        status_dropdown = ttk.Combobox(
            status_frame,
            textvariable=self.status_filter_var,
            values=statuses,
            font=self.theme.small_font,
            width=10,
        )
        status_dropdown.pack(side=tk.LEFT, padx=5)

        # Add binding to refresh when filter changes
        status_dropdown.bind(
            "<<ComboboxSelected>>", lambda e: self.todo_list.refresh_display()
        )

        # Sort by options
        sort_frame = tk.Frame(control_frame, bg=self.theme.bg_color)
        sort_frame.pack(side=tk.LEFT, padx=20)

        tk.Label(
            sort_frame,
            text="Sort by:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT, padx=5)

        sort_options = ["Due Date", "Priority", "Created Date", "Group"]
        self.sort_by_var = tk.StringVar(value="Due Date")
        sort_dropdown = ttk.Combobox(
            sort_frame,
            textvariable=self.sort_by_var,
            values=sort_options,
            font=self.theme.small_font,
            width=12,
        )
        sort_dropdown.pack(side=tk.LEFT, padx=5)

        # Add binding to refresh when sort changes
        sort_dropdown.bind(
            "<<ComboboxSelected>>", lambda e: self.todo_list.refresh_display()
        )

        # Main content frame
        content_frame = tk.Frame(parent, bg=self.theme.bg_color)
        content_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Tasks header
        header_frame = tk.Frame(content_frame, bg=self.theme.bg_color)
        header_frame.pack(fill=tk.X, pady=5)

        # Column headers
        columns = [
            ("Status", 6),
            ("Title", 20),
            ("Description", 25),
            ("Due Date", 10),
            ("Group", 10),
            ("Priority", 10),
            ("Actions", 10),
        ]

        for i, (col_name, width) in enumerate(columns):
            header = tk.Label(
                header_frame,
                text=col_name,
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
                width=width,
                anchor="w"
                if col_name == "Title" or col_name == "Description"
                else "center",
            )
            header.grid(row=0, column=i, padx=5, sticky="w" if i in [1, 2] else "")

        # Create scrollable frame for tasks
        tasks_canvas = tk.Canvas(
            content_frame, bg=self.theme.bg_color, highlightthickness=0
        )
        scrollbar = ttk.Scrollbar(
            content_frame, orient="vertical", command=tasks_canvas.yview
        )
        scrollable_frame = tk.Frame(tasks_canvas, bg=self.theme.bg_color)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: tasks_canvas.configure(scrollregion=tasks_canvas.bbox("all")),
        )

        tasks_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        tasks_canvas.configure(yscrollcommand=scrollbar.set)

        tasks_canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y")

        # Display tasks based on filters
        self.display_tasks(scrollable_frame)

    def display_tasks(self, parent):
        """
        Display tasks based on current filters and sorting options.

        Args:
            parent: Parent frame to place the task rows
        """
        # Get filter values
        group_filter = self.group_filter_var.get()
        status_filter = self.status_filter_var.get().lower()
        sort_by = self.sort_by_var.get().lower().replace(" ", "_")

        # Get tasks based on filters
        if status_filter == "active":
            tasks = self.todo_list.get_active_tasks(
                group_filter if group_filter != "All" else None
            )
        elif status_filter == "completed":
            tasks = self.todo_list.get_completed_tasks(
                group_filter if group_filter != "All" else None
            )
        else:  # All
            tasks = self.data["todo"].get("tasks", [])
            if group_filter != "All":
                tasks = [task for task in tasks if task.get("group") == group_filter]

        # If no tasks exist yet, show a message
        if not tasks:
            message = "No tasks found with the current filters."
            tk.Label(
                parent,
                text=message,
                font=self.theme.pixel_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
                pady=20,
            ).grid(row=0, column=0, columnspan=7)
            return

        # Sort tasks
        if sort_by == "due_date":
            # Sort by due date (handling None values)
            tasks = sorted(
                tasks,
                key=lambda t: datetime.strptime(
                    t.get("due_date", "9999-12-31"), "%Y-%m-%d"
                ),
            )
        elif sort_by == "priority":
            # Priority order: high, medium, low
            priority_map = {"high": 0, "medium": 1, "low": 2, None: 3}
            tasks = sorted(tasks, key=lambda t: priority_map.get(t.get("priority")))
        elif sort_by == "created_date":
            tasks = sorted(
                tasks,
                key=lambda t: datetime.strptime(
                    t.get("created_date", "1970-01-01"), "%Y-%m-%d"
                ),
                reverse=True,
            )
        elif sort_by == "group":
            tasks = sorted(tasks, key=lambda t: t.get("group", ""))

        # Get group colors
        group_colors = {}
        for group in self.data["todo"].get("groups", []):
            group_colors[group["name"]] = group["color"]

        # Display each task
        for i, task in enumerate(tasks):
            # Row background alternates for better readability
            row_bg = (
                self.theme.bg_color
                if i % 2 == 0
                else self.theme.darken_color(self.theme.bg_color)
            )

            # Status checkbox or completed indicator
            status_frame = tk.Frame(parent, bg=row_bg)
            status_frame.grid(row=i, column=0, padx=5, pady=2, sticky="w")

            if task.get("status") == "active":
                status_btn = tk.Button(
                    status_frame,
                    text="☐",
                    font=self.theme.pixel_font,
                    bg=row_bg,
                    fg=self.theme.text_color,
                    bd=0,
                    command=lambda t=task["id"]: self.complete_task(t),
                )
                status_btn.pack(padx=5)
            else:
                # Completed task
                status_label = tk.Label(
                    status_frame,
                    text="✓",
                    font=self.theme.pixel_font,
                    bg=row_bg,
                    fg="#4CAF50",  # Green for completed
                )
                status_label.pack(padx=5)

            # Task title
            title_frame = tk.Frame(parent, bg=row_bg)
            title_frame.grid(row=i, column=1, padx=5, pady=2, sticky="w")

            title_text = task.get("title", "")
            if task.get("status") == "completed":
                # Strikethrough effect for completed tasks
                title_text = "⟨" + title_text + "⟩"

            title_label = tk.Label(
                title_frame,
                text=title_text,
                font=self.theme.small_font,
                bg=row_bg,
                fg=self.theme.text_color
                if task.get("status") == "active"
                else "#888888",
                anchor="w",
                width=20,
            )
            title_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

            # Description
            desc_frame = tk.Frame(parent, bg=row_bg)
            desc_frame.grid(row=i, column=2, padx=5, pady=2, sticky="w")

            description = task.get("description", "")
            if len(description) > 25:
                description = description[:22] + "..."

            desc_label = tk.Label(
                desc_frame,
                text=description,
                font=self.theme.small_font,
                bg=row_bg,
                fg=self.theme.text_color
                if task.get("status") == "active"
                else "#888888",
                anchor="w",
                width=25,
            )
            desc_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

            # Due date
            due_frame = tk.Frame(parent, bg=row_bg)
            due_frame.grid(row=i, column=3, padx=5, pady=2)

            due_date = task.get("due_date", "")
            if due_date:
                try:
                    due_date_obj = datetime.strptime(due_date, "%Y-%m-%d").date()
                    today = datetime.now().date()

                    # Determine date color based on due date
                    if due_date_obj < today:
                        due_color = "#F44336"  # Red for overdue
                    elif due_date_obj == today:
                        due_color = "#FF9800"  # Orange for today
                    else:
                        due_color = (
                            self.theme.text_color
                        )  # Normal color for future dates

                    # Format date in a readable way
                    due_text = due_date_obj.strftime("%b %d, %Y")

                    # Show overdue indicator
                    if due_date_obj < today and task.get("status") == "active":
                        due_text += " ⚠️"
                except ValueError:
                    due_text = due_date
                    due_color = self.theme.text_color
            else:
                due_text = "No date"
                due_color = "#888888"

            due_label = tk.Label(
                due_frame,
                text=due_text,
                font=self.theme.small_font,
                bg=row_bg,
                fg=due_color if task.get("status") == "active" else "#888888",
            )
            due_label.pack()

            # Group with color indicator
            group_frame = tk.Frame(parent, bg=row_bg)
            group_frame.grid(row=i, column=4, padx=5, pady=2)

            group_name = task.get("group", "")
            group_color = group_colors.get(group_name, "#999999")

            # Small colored circle for group color
            color_indicator = tk.Frame(group_frame, bg=group_color, width=10, height=10)
            color_indicator.pack(side=tk.LEFT, padx=2)

            group_label = tk.Label(
                group_frame,
                text=group_name,
                font=self.theme.small_font,
                bg=row_bg,
                fg=self.theme.text_color
                if task.get("status") == "active"
                else "#888888",
            )
            group_label.pack(side=tk.LEFT)

            # Priority
            priority_frame = tk.Frame(parent, bg=row_bg)
            priority_frame.grid(row=i, column=5, padx=5, pady=2)

            priority = task.get("priority", "")
            priority_colors = {
                "high": "#F44336",  # Red
                "medium": "#FF9800",  # Orange
                "low": "#4CAF50",  # Green
            }
            priority_color = priority_colors.get(priority, self.theme.text_color)

            # Format priority text
            if priority:
                priority_text = priority.title()
                # Add indicator based on priority
                if priority == "high":
                    priority_text = "⚑ " + priority_text
            else:
                priority_text = "None"

            priority_label = tk.Label(
                priority_frame,
                text=priority_text,
                font=self.theme.small_font,
                bg=row_bg,
                fg=priority_color if task.get("status") == "active" else "#888888",
            )
            priority_label.pack()

            # Action buttons (edit, delete)
            actions_frame = tk.Frame(parent, bg=row_bg)
            actions_frame.grid(row=i, column=6, padx=5, pady=2)

            # Edit button
            edit_button = tk.Button(
                actions_frame,
                text="✏️",
                font=self.theme.small_font,
                bg=self.theme.primary_color,
                fg=self.theme.text_color,
                relief=tk.FLAT,
                command=lambda t=task["id"]: self.edit_task(t),
            )
            edit_button.pack(side=tk.LEFT, padx=2)

            # Delete button
            delete_button = tk.Button(
                actions_frame,
                text="🗑️",
                font=self.theme.small_font,
                bg="#F44336",
                fg="white",
                relief=tk.FLAT,
                command=lambda t=task["id"]: self.delete_task(t),
            )
            delete_button.pack(side=tk.LEFT, padx=2)

            # Add recurrence indicator if the task is recurring
            if task.get("recurrence") and task.get("status") == "active":
                recur_button = tk.Button(
                    actions_frame,
                    text="🔄",
                    font=self.theme.small_font,
                    bg=self.theme.secondary_color,
                    fg=self.theme.text_color,
                    relief=tk.FLAT,
                    command=lambda t=task["id"]: self.show_recurrence_info(t),
                )
                recur_button.pack(side=tk.LEFT, padx=2)

    def add_new_task(self):
        """Open a dialog to add a new task."""
        self.show_task_dialog()

    def edit_task(self, task_id):
        """Open a dialog to edit an existing task."""
        # Find the task
        task = None
        for t in self.data["todo"].get("tasks", []):
            if t.get("id") == task_id:
                task = t
                break

        if not task:
            messagebox.showerror("Error", "Task not found.")
            return

        self.show_task_dialog(task)

    def show_task_dialog(self, task=None):
        """
        Show dialog for adding or editing a task.

        Args:
            task: Optional task to edit. If None, a new task will be created.
        """
        # Create a dialog window
        dialog = tk.Toplevel(self.app.root)
        dialog.title("Add New Task" if not task else "Edit Task")
        dialog.geometry("600x500")  # Larger dialog for all options
        dialog.configure(bg=self.theme.bg_color)
        dialog.transient(self.app.root)
        dialog.grab_set()

        # Task title
        title_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        title_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(
            title_frame,
            text="Task Title:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT)

        title_var = tk.StringVar(value=task.get("title", "") if task else "")
        title_entry = tk.Entry(
            title_frame,
            textvariable=title_var,
            font=self.theme.small_font,
            bg=self.theme.primary_color,
            fg=self.theme.text_color,
            width=40,
        )
        title_entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

        # Description
        desc_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        desc_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(
            desc_frame,
            text="Description:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(anchor="w")

        desc_text = tk.Text(
            desc_frame,
            font=self.theme.small_font,
            bg=self.theme.primary_color,
            fg=self.theme.text_color,
            width=50,
            height=4,
        )
        desc_text.pack(pady=5, fill=tk.X)

        if task and task.get("description"):
            desc_text.insert("1.0", task.get("description"))

        # Group selection
        group_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        group_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(
            group_frame,
            text="Group:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT)

        # Get groups
        groups = [g["name"] for g in self.data["todo"].get("groups", [])]
        if not groups:
            groups = ["Work", "Personal"]  # Default if no groups

        group_var = tk.StringVar(
            value=task.get("group", groups[0]) if task else groups[0]
        )

        group_dropdown = ttk.Combobox(
            group_frame,
            textvariable=group_var,
            values=groups,
            font=self.theme.small_font,
            width=15,
        )
        group_dropdown.pack(side=tk.LEFT, padx=10)

        # Priority selection
        priority_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        priority_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(
            priority_frame,
            text="Priority:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT)

        priorities = ["high", "medium", "low"]
        priority_var = tk.StringVar(
            value=task.get("priority", "medium") if task else "medium"
        )

        for priority in priorities:
            rb = tk.Radiobutton(
                priority_frame,
                text=priority.title(),
                variable=priority_var,
                value=priority,
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
                selectcolor=self.theme.secondary_color,
            )
            rb.pack(side=tk.LEFT, padx=10)

        # Due date
        date_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        date_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(
            date_frame,
            text="Due Date:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT)

        # Date option (with or without date)
        has_date_var = tk.BooleanVar(
            value=True if task and task.get("due_date") else False
        )
        has_date_cb = tk.Checkbutton(
            date_frame,
            text="Set Due Date",
            variable=has_date_var,
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            selectcolor=self.theme.secondary_color,
        )
        has_date_cb.pack(side=tk.LEFT, padx=10)

        # Date entry fields
        date_inputs_frame = tk.Frame(date_frame, bg=self.theme.bg_color)
        date_inputs_frame.pack(side=tk.LEFT, padx=10)

        # Default to today if no date or creating new task
        today = datetime.now().date()

        if task and task.get("due_date"):
            try:
                due_date = datetime.strptime(task.get("due_date"), "%Y-%m-%d").date()
            except ValueError:
                due_date = today
        else:
            due_date = today

        # Year
        year_var = tk.StringVar(value=str(due_date.year))
        year_vcmd = (dialog.register(lambda P: P.isdigit() and len(P) <= 4), "%P")
        year_entry = tk.Entry(
            date_inputs_frame,
            textvariable=year_var,
            validate="key",
            validatecommand=year_vcmd,
            font=self.theme.small_font,
            bg=self.theme.primary_color,
            fg=self.theme.text_color,
            width=6,
        )
        year_entry.grid(row=0, column=0, padx=2)

        # Month
        month_var = tk.StringVar(value=str(due_date.month))
        months = [str(i) for i in range(1, 13)]
        month_dropdown = ttk.Combobox(
            date_inputs_frame,
            textvariable=month_var,
            values=months,
            font=self.theme.small_font,
            width=3,
        )
        month_dropdown.grid(row=0, column=1, padx=2)

        # Day
        day_var = tk.StringVar(value=str(due_date.day))
        days = [str(i) for i in range(1, 32)]
        day_dropdown = ttk.Combobox(
            date_inputs_frame,
            textvariable=day_var,
            values=days,
            font=self.theme.small_font,
            width=3,
        )
        day_dropdown.grid(row=0, column=2, padx=2)

        # Update day dropdown when month changes
        def update_days(*args):
            try:
                month = int(month_var.get())
                year = int(year_var.get())

                # Get the last day of the month
                last_day = calendar.monthrange(year, month)[1]

                # Update days dropdown
                days = [str(i) for i in range(1, last_day + 1)]
                day_dropdown["values"] = days

                # If current day is invalid, set to last day
                if int(day_var.get()) > last_day:
                    day_var.set(str(last_day))
            except ValueError:
                pass

        month_var.trace_add("write", update_days)
        year_var.trace_add("write", update_days)

        # Recurrence section
        recur_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        recur_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(
            recur_frame,
            text="Recurrence:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(anchor="w")

        # Enable/disable recurrence
        recur_var = tk.BooleanVar(
            value=True if task and task.get("recurrence") else False
        )
        recur_cb = tk.Checkbutton(
            recur_frame,
            text="Recurring Task",
            variable=recur_var,
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            selectcolor=self.theme.secondary_color,
        )
        recur_cb.pack(anchor="w", padx=10)

        # Recurrence options
        recur_options_frame = tk.Frame(recur_frame, bg=self.theme.bg_color)
        recur_options_frame.pack(fill=tk.X, padx=10, pady=5)

        # Recurrence types
        type_frame = tk.Frame(recur_options_frame, bg=self.theme.bg_color)
        type_frame.pack(fill=tk.X, pady=5)

        tk.Label(
            type_frame,
            text="Repeat:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT)

        # Get current recurrence type
        current_recur_type = "daily"
        if task and task.get("recurrence"):
            current_recur_type = task["recurrence"].get("type", "daily")

        recur_type_var = tk.StringVar(value=current_recur_type)
        recur_types = ["daily", "weekly", "monthly", "yearly", "custom"]

        recur_type_dropdown = ttk.Combobox(
            type_frame,
            textvariable=recur_type_var,
            values=recur_types,
            font=self.theme.small_font,
            width=10,
        )
        recur_type_dropdown.pack(side=tk.LEFT, padx=10)

        # Container for specific recurrence options
        specific_recur_frame = tk.Frame(recur_options_frame, bg=self.theme.bg_color)
        specific_recur_frame.pack(fill=tk.X, pady=5)

        # Weekly options (checkboxes for days)
        weekly_frame = tk.Frame(specific_recur_frame, bg=self.theme.bg_color)

        days_frame = tk.Frame(weekly_frame, bg=self.theme.bg_color)
        days_frame.pack(fill=tk.X, pady=5)

        days_vars = []
        days_of_week = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]

        # Get current days selection
        current_days = []
        if (
            task
            and task.get("recurrence")
            and task["recurrence"].get("type") == "weekly"
        ):
            current_days = task["recurrence"].get("days", [])

        for i, day in enumerate(days_of_week):
            var = tk.BooleanVar(value=i in current_days)
            days_vars.append(var)

            cb = tk.Checkbutton(
                days_frame,
                text=day,
                variable=var,
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
                selectcolor=self.theme.secondary_color,
            )
            cb.grid(row=i // 4, column=i % 4, sticky="w", padx=5, pady=2)

        # Custom interval options
        custom_frame = tk.Frame(specific_recur_frame, bg=self.theme.bg_color)

        interval_var = tk.StringVar(value="1")
        if (
            task
            and task.get("recurrence")
            and task["recurrence"].get("type") == "custom"
        ):
            interval_var.set(str(task["recurrence"].get("interval", 1)))

        interval_frame = tk.Frame(custom_frame, bg=self.theme.bg_color)
        interval_frame.pack(fill=tk.X, pady=5)

        tk.Label(
            interval_frame,
            text="Every",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT)

        vcmd = (
            dialog.register(lambda P: P.isdigit() and int(P) > 0 if P else True),
            "%P",
        )
        interval_entry = tk.Entry(
            interval_frame,
            textvariable=interval_var,
            validate="key",
            validatecommand=vcmd,
            font=self.theme.small_font,
            bg=self.theme.primary_color,
            fg=self.theme.text_color,
            width=3,
        )
        interval_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(
            interval_frame,
            text="days",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT)

        # End date options
        end_date_frame = tk.Frame(recur_options_frame, bg=self.theme.bg_color)
        end_date_frame.pack(fill=tk.X, pady=5)

        tk.Label(
            end_date_frame,
            text="End Date:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT)

        # End date option (with or without end date)
        has_end_date_var = tk.BooleanVar(value=False)
        if task and task.get("recurrence") and task["recurrence"].get("end_date"):
            has_end_date_var.set(True)

        has_end_date_cb = tk.Checkbutton(
            end_date_frame,
            text="Set End Date",
            variable=has_end_date_var,
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            selectcolor=self.theme.secondary_color,
        )
        has_end_date_cb.pack(side=tk.LEFT, padx=10)

        # End date entry fields
        end_date_inputs_frame = tk.Frame(end_date_frame, bg=self.theme.bg_color)
        end_date_inputs_frame.pack(side=tk.LEFT, padx=10)

        # Default end date (3 months from now)
        end_date = today + timedelta(days=90)

        if task and task.get("recurrence") and task["recurrence"].get("end_date"):
            try:
                end_date = datetime.strptime(
                    task["recurrence"]["end_date"], "%Y-%m-%d"
                ).date()
            except ValueError:
                pass

        # Year
        end_year_var = tk.StringVar(value=str(end_date.year))
        end_year_entry = tk.Entry(
            end_date_inputs_frame,
            textvariable=end_year_var,
            validate="key",
            validatecommand=year_vcmd,
            font=self.theme.small_font,
            bg=self.theme.primary_color,
            fg=self.theme.text_color,
            width=6,
        )
        end_year_entry.grid(row=0, column=0, padx=2)

        # Month
        end_month_var = tk.StringVar(value=str(end_date.month))
        end_month_dropdown = ttk.Combobox(
            end_date_inputs_frame,
            textvariable=end_month_var,
            values=months,
            font=self.theme.small_font,
            width=3,
        )
        end_month_dropdown.grid(row=0, column=1, padx=2)

        # Day
        end_day_var = tk.StringVar(value=str(end_date.day))
        end_day_dropdown = ttk.Combobox(
            end_date_inputs_frame,
            textvariable=end_day_var,
            values=days,
            font=self.theme.small_font,
            width=3,
        )
        end_day_dropdown.grid(row=0, column=2, padx=2)

        # Update end day dropdown when month changes
        def update_end_days(*args):
            try:
                month = int(end_month_var.get())
                year = int(end_year_var.get())

                # Get the last day of the month
                last_day = calendar.monthrange(year, month)[1]

                # Update days dropdown
                days = [str(i) for i in range(1, last_day + 1)]
                end_day_dropdown["values"] = days

                # If current day is invalid, set to last day
                if int(end_day_var.get()) > last_day:
                    end_day_var.set(str(last_day))
            except ValueError:
                pass

        end_month_var.trace_add("write", update_end_days)
        end_year_var.trace_add("write", update_end_days)

        # Show the appropriate recurrence options frame based on type
        def update_recurrence_options(*args):
            # Hide all frames
            weekly_frame.pack_forget()
            custom_frame.pack_forget()

            # Show frame based on selection
            recur_type = recur_type_var.get()
            if recur_type == "weekly":
                weekly_frame.pack(fill=tk.X, pady=5)
            elif recur_type == "custom":
                custom_frame.pack(fill=tk.X, pady=5)

        # Initial update
        update_recurrence_options()

        # Add trace to update when recurrence type changes
        recur_type_var.trace_add("write", update_recurrence_options)

        # Control buttons at the bottom
        button_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=20)

        # Cancel button
        cancel_button = self.theme.create_pixel_button(
            button_frame,
            "Cancel",
            dialog.destroy,
            color="#F44336",  # Red
        )
        cancel_button.pack(side=tk.RIGHT, padx=10)

        # Save button
        save_text = "Add Task" if not task else "Update Task"
        save_button = self.theme.create_pixel_button(
            button_frame,
            save_text,
            lambda: self.save_task(
                dialog,
                task,
                title_var.get(),
                desc_text.get("1.0", "end-1c"),
                group_var.get(),
                priority_var.get(),
                has_date_var.get(),
                year_var.get(),
                month_var.get(),
                day_var.get(),
                recur_var.get(),
                recur_type_var.get(),
                days_vars,
                interval_var.get(),
                has_end_date_var.get(),
                end_year_var.get(),
                end_month_var.get(),
                end_day_var.get(),
            ),
            color="#4CAF50",  # Green
        )
        save_button.pack(side=tk.RIGHT, padx=10)

        # Focus on title field
        title_entry.focus_set()

    def save_task(
        self,
        dialog,
        task,
        title,
        description,
        group,
        priority,
        has_date,
        year,
        month,
        day,
        is_recurring,
        recur_type,
        days_vars,
        interval,
        has_end_date,
        end_year,
        end_month,
        end_day,
    ):
        """
        Save a new task or update an existing one.

        Args:
            dialog: The dialog window to close on success
            task: Existing task to update, or None for a new task
            (... other parameters for task properties ...)
        """
        # Validate inputs
        if not title:
            messagebox.showerror("Error", "Task title is required.")
            return

        # Prepare task data
        task_data = {}

        # If editing, start with the existing task data
        if task:
            task_data = task.copy()
        else:
            # Generate a new task ID for new tasks
            task_data["id"] = f"task_{len(self.data['todo'].get('tasks', [])) + 1}"
            task_data["created_date"] = datetime.now().strftime("%Y-%m-%d")
            task_data["status"] = "active"
            task_data["completed_date"] = None

        # Update task data with form values
        task_data["title"] = title
        task_data["description"] = description
        task_data["group"] = group
        task_data["priority"] = priority

        # Due date
        if has_date:
            try:
                due_date = datetime(int(year), int(month), int(day)).date()
                task_data["due_date"] = due_date.strftime("%Y-%m-%d")
            except (ValueError, TypeError):
                messagebox.showerror("Error", "Invalid due date.")
                return
        else:
            task_data["due_date"] = None

        # Recurrence
        if is_recurring:
            recurrence = {}
            recurrence["type"] = recur_type

            if recur_type == "weekly":
                # Get selected days
                selected_days = [i for i, var in enumerate(days_vars) if var.get()]
                if not selected_days:
                    messagebox.showerror(
                        "Error", "Please select at least one day for weekly recurrence."
                    )
                    return

                recurrence["days"] = selected_days

            elif recur_type == "custom":
                try:
                    interval_val = int(interval)
                    if interval_val < 1:
                        messagebox.showerror(
                            "Error", "Interval must be at least 1 day."
                        )
                        return

                    recurrence["interval"] = interval_val
                except ValueError:
                    messagebox.showerror("Error", "Invalid interval value.")
                    return

            # End date
            if has_end_date:
                try:
                    end_date = datetime(
                        int(end_year), int(end_month), int(end_day)
                    ).date()
                    recurrence["end_date"] = end_date.strftime("%Y-%m-%d")
                except (ValueError, TypeError):
                    messagebox.showerror("Error", "Invalid end date.")
                    return
            else:
                recurrence["end_date"] = None

            task_data["recurrence"] = recurrence
        else:
            task_data["recurrence"] = None

        # Save to data store
        if not task:
            # New task
            self.data["todo"]["tasks"].append(task_data)
        else:
            # Update existing task
            for i, t in enumerate(self.data["todo"]["tasks"]):
                if t.get("id") == task["id"]:
                    self.data["todo"]["tasks"][i] = task_data
                    break

        # Save data
        self.data_manager.save_data()

        # Close dialog
        dialog.destroy()

        # Refresh display
        self.todo_list.refresh_display()

        # Show confirmation
        action = "updated" if task else "added"
        messagebox.showinfo("Success", f"Task '{title}' has been {action}!")

    def complete_task(self, task_id):
        """Mark a task as completed."""
        if self.todo_list.complete_task(task_id):
            self.todo_list.refresh_display()
        else:
            messagebox.showerror("Error", "Failed to complete task.")

    def delete_task(self, task_id):
        """Delete a task."""
        # Confirm deletion
        confirm = messagebox.askyesno(
            "Confirm Deletion",
            "Are you sure you want to delete this task? This action cannot be undone.",
        )

        if confirm:
            if self.todo_list.delete_task(task_id):
                self.todo_list.refresh_display()
            else:
                messagebox.showerror("Error", "Failed to delete task.")

    def show_recurrence_info(self, task_id):
        """Show information about a recurring task."""
        # Find the task
        task = None
        for t in self.data["todo"].get("tasks", []):
            if t.get("id") == task_id:
                task = t
                break

        if not task or not task.get("recurrence"):
            messagebox.showerror("Error", "Recurrence information not available.")
            return

        # Get recurrence details
        recurrence = task["recurrence"]
        recur_type = recurrence.get("type", "unknown")

        # Format recurrence information
        if recur_type == "daily":
            recur_text = "This task repeats every day"
        elif recur_type == "weekly":
            days = recurrence.get("days", [])
            day_names = [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
            ]
            selected_days = [day_names[i] for i in days]
            recur_text = f"This task repeats weekly on: {', '.join(selected_days)}"
        elif recur_type == "monthly":
            recur_text = "This task repeats monthly"
        elif recur_type == "yearly":
            recur_text = "This task repeats yearly"
        elif recur_type == "custom":
            interval = recurrence.get("interval", 1)
            recur_text = f"This task repeats every {interval} days"
        else:
            recur_text = "Unknown recurrence pattern"

        # Add end date if present
        if recurrence.get("end_date"):
            try:
                end_date = datetime.strptime(recurrence["end_date"], "%Y-%m-%d").date()
                recur_text += f"\nEnds on: {end_date.strftime('%b %d, %Y')}"
            except ValueError:
                pass

        # Show info dialog
        messagebox.showinfo("Recurrence Information", recur_text)
