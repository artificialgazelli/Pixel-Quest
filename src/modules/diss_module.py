"""
Dissertation module for the Pixel Quest application.
Handles dissertation task tracking and logging with time-sensitive features.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from src.utils import update_streak, check_level_up, create_pixel_progress_bar


class DissModule:
    """
    Manages the dissertation module functionality.
    Tracks time-sensitive dissertation tasks with completion goals.
    """

    def __init__(self, app, data_manager, theme):
        """
        Initialize the dissertation module.

        Args:
            app: Main application instance
            data_manager: Data manager instance
            theme: Theme manager instance
        """
        self.app = app
        self.data_manager = data_manager
        self.data = data_manager.data
        self.theme = theme

    def show_module(self, parent_frame):
        """
        Show the dissertation module interface.

        Args:
            parent_frame: Parent frame to place module content
        """
        # Title
        title_label = tk.Label(
            parent_frame,
            text="DISSERTATION QUEST",
            font=self.theme.heading_font,
            bg=self.theme.bg_color,
            fg=self.theme.diss_color,
        )
        title_label.pack(pady=20)

        # Stats frame
        stats_frame = tk.Frame(
            parent_frame, bg=self.theme.bg_color, relief=tk.RIDGE, bd=3
        )
        stats_frame.pack(pady=10, fill=tk.X, padx=20)

        level_label = tk.Label(
            stats_frame,
            text=f"Level: {self.data['diss']['level']}",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        )
        level_label.grid(row=0, column=0, padx=20, pady=10)

        points_label = tk.Label(
            stats_frame,
            text=f"Points: {self.data['diss']['points']}",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        )
        points_label.grid(row=0, column=1, padx=20, pady=10)

        streak_label = tk.Label(
            stats_frame,
            text=f"Streak: {self.data['diss']['streak']} days",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg="#FF5722",
        )
        streak_label.grid(row=0, column=2, padx=20, pady=10)

        # Projects frame
        phases_frame = tk.Frame(parent_frame, bg=self.theme.bg_color)
        phases_frame.pack(pady=20, fill=tk.BOTH, expand=True, padx=20)

        # Show dissertation phases
        self.show_diss_phases(phases_frame)

        # Back button
        back_button = self.theme.create_pixel_button(
            parent_frame,
            "Back to Main Menu",
            self.app.show_main_menu,
            color="#9E9E9E",
        )
        back_button.pack(pady=20)

    def show_diss_phases(self, parent_frame):
        """
        Show dissertation module phases with pixel art styling.

        Args:
            parent_frame: Parent frame to place the phases
        """
        # Phase selection frame
        phase_select_frame = tk.Frame(parent_frame, bg=self.theme.bg_color)
        phase_select_frame.pack(pady=10, fill=tk.X, padx=10)

        tk.Label(
            phase_select_frame,
            text="Select Phase:",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT, padx=5)

        phases = [
            "Preparation Phase",
            "Empirical Analysis Phase",
            "Integration Phase",
            "Finalization Phase",
        ]
        self.selected_diss_phase = tk.StringVar(value=phases[0])

        phase_dropdown = ttk.Combobox(
            phase_select_frame,
            textvariable=self.selected_diss_phase,
            values=phases,
            state="readonly",
            width=30,
            font=self.theme.pixel_font,
        )
        phase_dropdown.pack(side=tk.LEFT, padx=5)
        phase_dropdown.bind(
            "<<ComboboxSelected>>", lambda e: self.update_diss_phase_view(parent_frame)
        )

        # Create a container frame for phase content
        self.diss_phase_container = tk.Frame(parent_frame, bg=self.theme.bg_color)
        self.diss_phase_container.pack(pady=10, fill=tk.BOTH, expand=True)

        # Show the first phase by default
        self.show_preparation_phase(self.diss_phase_container)

    def update_diss_phase_view(self, parent_frame):
        """
        Update the displayed phase based on dropdown selection.

        Args:
            parent_frame: Parent frame containing the phases
        """
        # Clear the container
        for widget in self.diss_phase_container.winfo_children():
            widget.destroy()

        # Show the selected phase
        phase = self.selected_diss_phase.get()
        if phase == "Preparation Phase":
            self.show_preparation_phase(self.diss_phase_container)
        elif phase == "Empirical Analysis Phase":
            self.show_empirical_phase(self.diss_phase_container)
        elif phase == "Integration Phase":
            self.show_integration_phase(self.diss_phase_container)
        elif phase == "Finalization Phase":
            self.show_finalization_phase(self.diss_phase_container)

    def show_preparation_phase(self, parent_frame):
        """
        Show preparation phase tasks with pixel art styling.
        Only shows tasks that are currently active based on date.

        Args:
            parent_frame: Parent frame to place the preparation phase content
        """
        # Phase frame
        phase_frame = tk.LabelFrame(
            parent_frame,
            text="Preparation Phase",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            relief=tk.RIDGE,
            bd=3,
        )
        phase_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)

        # Get current tasks based on date
        current_date = datetime.now().date()
        active_tasks = []
        for task in self.data["diss"]["tasks"]["preparation"]:
            start_date = datetime.strptime(task["start_date"], "%d.%m.%Y").date()
            end_date = datetime.strptime(task["end_date"], "%d.%m.%Y").date()

            if start_date <= current_date <= end_date:
                active_tasks.append(task)

        if not active_tasks:
            # No active tasks
            tk.Label(
                phase_frame,
                text="No active preparation tasks for the current date.",
                font=self.theme.pixel_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
            ).pack(pady=20)
            return

        # Task selection
        selection_frame = tk.LabelFrame(
            phase_frame,
            text="Active Tasks",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            relief=tk.RIDGE,
            bd=3,
        )
        selection_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)

        # Display active tasks
        active_task_names = [task["name"] for task in active_tasks]
        self.selected_diss_task = tk.StringVar()

        if active_task_names:
            self.selected_diss_task.set(active_task_names[0])

        # Task dropdown
        task_frame = tk.Frame(selection_frame, bg=self.theme.bg_color)
        task_frame.pack(pady=10, fill=tk.X)

        tk.Label(
            task_frame,
            text="Select task:",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
        ).pack(side=tk.LEFT, padx=5)

        task_dropdown = ttk.Combobox(
            task_frame,
            textvariable=self.selected_diss_task,
            values=active_task_names,
            width=40,
            font=self.theme.small_font,
        )
        task_dropdown.pack(side=tk.LEFT, padx=5)
        task_dropdown.bind("<<ComboboxSelected>>", lambda e: self.update_task_details())

        # Task details frame
        self.task_details_frame = tk.LabelFrame(
            selection_frame,
            text="Task Details",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            relief=tk.RIDGE,
            bd=3,
        )
        self.task_details_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)

        # Update task details for the first selected task
        self.update_task_details()

        # Progress tracking frame
        progress_frame = tk.LabelFrame(
            phase_frame,
            text="Log Progress",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            relief=tk.RIDGE,
            bd=3,
        )
        progress_frame.pack(pady=10, fill=tk.X, padx=10)

        # Hours worked entry
        hours_frame = tk.Frame(progress_frame, bg=self.theme.bg_color)
        hours_frame.pack(pady=10, fill=tk.X)

        tk.Label(
            hours_frame,
            text="Hours worked:",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
        ).pack(side=tk.LEFT, padx=5)

        self.hours_var = tk.DoubleVar(value=1.0)
        hours_values = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]

        hours_dropdown = ttk.Combobox(
            hours_frame,
            textvariable=self.hours_var,
            values=hours_values,
            width=5,
            font=self.theme.small_font,
        )
        hours_dropdown.pack(side=tk.LEFT, padx=5)

        # Progress description
        tk.Label(
            progress_frame,
            text="Progress notes (optional):",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
        ).pack(anchor="w", padx=10, pady=5)

        self.progress_notes = tk.Text(
            progress_frame,
            height=4,
            width=50,
            font=self.theme.small_font,
            bg=self.theme.primary_color,
            fg=self.theme.text_color,
        )
        self.progress_notes.pack(padx=10, pady=5, fill=tk.X)

        # Log button
        log_button = self.theme.create_pixel_button(
            progress_frame,
            "Log Progress",
            self.log_diss_progress,
            color=self.theme.diss_color,
        )
        log_button.pack(pady=10)

    def show_empirical_phase(self, parent_frame):
        """
        Show empirical analysis phase tasks with pixel art styling.
        Only shows tasks that are currently active based on date.

        Args:
            parent_frame: Parent frame to place the empirical phase content
        """
        # Phase frame
        phase_frame = tk.LabelFrame(
            parent_frame,
            text="Empirical Analysis Phase",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            relief=tk.RIDGE,
            bd=3,
        )
        phase_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)

        # Get current tasks based on date
        current_date = datetime.now().date()
        active_tasks = []
        for task in self.data["diss"]["tasks"]["empirical"]:
            start_date = datetime.strptime(task["start_date"], "%d.%m.%Y").date()
            end_date = datetime.strptime(task["end_date"], "%d.%m.%Y").date()

            if start_date <= current_date <= end_date:
                active_tasks.append(task)

        if not active_tasks:
            # No active tasks
            tk.Label(
                phase_frame,
                text="No active empirical analysis tasks for the current date.",
                font=self.theme.pixel_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
            ).pack(pady=20)
            return

        # Task selection
        selection_frame = tk.LabelFrame(
            phase_frame,
            text="Active Tasks",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            relief=tk.RIDGE,
            bd=3,
        )
        selection_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)

        # Display active tasks
        active_task_names = [task["name"] for task in active_tasks]
        self.selected_diss_task = tk.StringVar()

        if active_task_names:
            self.selected_diss_task.set(active_task_names[0])

        # Task dropdown
        task_frame = tk.Frame(selection_frame, bg=self.theme.bg_color)
        task_frame.pack(pady=10, fill=tk.X)

        tk.Label(
            task_frame,
            text="Select task:",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
        ).pack(side=tk.LEFT, padx=5)

        task_dropdown = ttk.Combobox(
            task_frame,
            textvariable=self.selected_diss_task,
            values=active_task_names,
            width=40,
            font=self.theme.small_font,
        )
        task_dropdown.pack(side=tk.LEFT, padx=5)
        task_dropdown.bind("<<ComboboxSelected>>", lambda e: self.update_task_details())

        # Task details frame
        self.task_details_frame = tk.LabelFrame(
            selection_frame,
            text="Task Details",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            relief=tk.RIDGE,
            bd=3,
        )
        self.task_details_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)

        # Update task details for the first selected task
        self.update_task_details()

        # Progress tracking frame
        progress_frame = tk.LabelFrame(
            phase_frame,
            text="Log Progress",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            relief=tk.RIDGE,
            bd=3,
        )
        progress_frame.pack(pady=10, fill=tk.X, padx=10)

        # Hours worked entry
        hours_frame = tk.Frame(progress_frame, bg=self.theme.bg_color)
        hours_frame.pack(pady=10, fill=tk.X)

        tk.Label(
            hours_frame,
            text="Hours worked:",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
        ).pack(side=tk.LEFT, padx=5)

        self.hours_var = tk.DoubleVar(value=1.0)
        hours_values = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]

        hours_dropdown = ttk.Combobox(
            hours_frame,
            textvariable=self.hours_var,
            values=hours_values,
            width=5,
            font=self.theme.small_font,
        )
        hours_dropdown.pack(side=tk.LEFT, padx=5)

        # Progress description
        tk.Label(
            progress_frame,
            text="Progress notes (optional):",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
        ).pack(anchor="w", padx=10, pady=5)

        self.progress_notes = tk.Text(
            progress_frame,
            height=4,
            width=50,
            font=self.theme.small_font,
            bg=self.theme.primary_color,
            fg=self.theme.text_color,
        )
        self.progress_notes.pack(padx=10, pady=5, fill=tk.X)

        # Log button
        log_button = self.theme.create_pixel_button(
            progress_frame,
            "Log Progress",
            self.log_diss_progress,
            color=self.theme.diss_color,
        )
        log_button.pack(pady=10)

    def show_integration_phase(self, parent_frame):
        """
        Show integration phase tasks with pixel art styling.
        Only shows tasks that are currently active based on date.

        Args:
            parent_frame: Parent frame to place the integration phase content
        """
        # Phase frame
        phase_frame = tk.LabelFrame(
            parent_frame,
            text="Integration Phase",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            relief=tk.RIDGE,
            bd=3,
        )
        phase_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)

        # Get current tasks based on date
        current_date = datetime.now().date()
        active_tasks = []
        for task in self.data["diss"]["tasks"]["integration"]:
            start_date = datetime.strptime(task["start_date"], "%d.%m.%Y").date()
            end_date = datetime.strptime(task["end_date"], "%d.%m.%Y").date()

            if start_date <= current_date <= end_date:
                active_tasks.append(task)

        if not active_tasks:
            # No active tasks
            tk.Label(
                phase_frame,
                text="No active integration tasks for the current date.",
                font=self.theme.pixel_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
            ).pack(pady=20)
            return

        # Task selection
        selection_frame = tk.LabelFrame(
            phase_frame,
            text="Active Tasks",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            relief=tk.RIDGE,
            bd=3,
        )
        selection_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)

        # Display active tasks
        active_task_names = [task["name"] for task in active_tasks]
        self.selected_diss_task = tk.StringVar()

        if active_task_names:
            self.selected_diss_task.set(active_task_names[0])

        # Task dropdown
        task_frame = tk.Frame(selection_frame, bg=self.theme.bg_color)
        task_frame.pack(pady=10, fill=tk.X)

        tk.Label(
            task_frame,
            text="Select task:",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
        ).pack(side=tk.LEFT, padx=5)

        task_dropdown = ttk.Combobox(
            task_frame,
            textvariable=self.selected_diss_task,
            values=active_task_names,
            width=40,
            font=self.theme.small_font,
        )
        task_dropdown.pack(side=tk.LEFT, padx=5)
        task_dropdown.bind("<<ComboboxSelected>>", lambda e: self.update_task_details())

        # Task details frame
        self.task_details_frame = tk.LabelFrame(
            selection_frame,
            text="Task Details",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            relief=tk.RIDGE,
            bd=3,
        )
        self.task_details_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)

        # Update task details for the first selected task
        self.update_task_details()

        # Progress tracking frame
        progress_frame = tk.LabelFrame(
            phase_frame,
            text="Log Progress",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            relief=tk.RIDGE,
            bd=3,
        )
        progress_frame.pack(pady=10, fill=tk.X, padx=10)

        # Hours worked entry
        hours_frame = tk.Frame(progress_frame, bg=self.theme.bg_color)
        hours_frame.pack(pady=10, fill=tk.X)

        tk.Label(
            hours_frame,
            text="Hours worked:",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
        ).pack(side=tk.LEFT, padx=5)

        self.hours_var = tk.DoubleVar(value=1.0)
        hours_values = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]

        hours_dropdown = ttk.Combobox(
            hours_frame,
            textvariable=self.hours_var,
            values=hours_values,
            width=5,
            font=self.theme.small_font,
        )
        hours_dropdown.pack(side=tk.LEFT, padx=5)

        # Progress description
        tk.Label(
            progress_frame,
            text="Progress notes (optional):",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
        ).pack(anchor="w", padx=10, pady=5)

        self.progress_notes = tk.Text(
            progress_frame,
            height=4,
            width=50,
            font=self.theme.small_font,
            bg=self.theme.primary_color,
            fg=self.theme.text_color,
        )
        self.progress_notes.pack(padx=10, pady=5, fill=tk.X)

        # Log button
        log_button = self.theme.create_pixel_button(
            progress_frame,
            "Log Progress",
            self.log_diss_progress,
            color=self.theme.diss_color,
        )
        log_button.pack(pady=10)

    def show_finalization_phase(self, parent_frame):
        """
        Show finalization phase tasks with pixel art styling.
        Only shows tasks that are currently active based on date.

        Args:
            parent_frame: Parent frame to place the finalization phase content
        """
        # Phase frame
        phase_frame = tk.LabelFrame(
            parent_frame,
            text="Finalization Phase",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            relief=tk.RIDGE,
            bd=3,
        )
        phase_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)

        # Get current tasks based on date
        current_date = datetime.now().date()
        active_tasks = []
        for task in self.data["diss"]["tasks"]["finalization"]:
            start_date = datetime.strptime(task["start_date"], "%d.%m.%Y").date()
            end_date = datetime.strptime(task["end_date"], "%d.%m.%Y").date()

            if start_date <= current_date <= end_date:
                active_tasks.append(task)

        if not active_tasks:
            # No active tasks
            tk.Label(
                phase_frame,
                text="No active finalization tasks for the current date.",
                font=self.theme.pixel_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
            ).pack(pady=20)
            return

        # Task selection
        selection_frame = tk.LabelFrame(
            phase_frame,
            text="Active Tasks",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            relief=tk.RIDGE,
            bd=3,
        )
        selection_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)

        # Display active tasks
        active_task_names = [task["name"] for task in active_tasks]
        self.selected_diss_task = tk.StringVar()

        if active_task_names:
            self.selected_diss_task.set(active_task_names[0])

        # Task dropdown
        task_frame = tk.Frame(selection_frame, bg=self.theme.bg_color)
        task_frame.pack(pady=10, fill=tk.X)

        tk.Label(
            task_frame,
            text="Select task:",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
        ).pack(side=tk.LEFT, padx=5)

        task_dropdown = ttk.Combobox(
            task_frame,
            textvariable=self.selected_diss_task,
            values=active_task_names,
            width=40,
            font=self.theme.small_font,
        )
        task_dropdown.pack(side=tk.LEFT, padx=5)
        task_dropdown.bind("<<ComboboxSelected>>", lambda e: self.update_task_details())

        # Task details frame
        self.task_details_frame = tk.LabelFrame(
            selection_frame,
            text="Task Details",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            relief=tk.RIDGE,
            bd=3,
        )
        self.task_details_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)

        # Update task details for the first selected task
        self.update_task_details()

        # Progress tracking frame
        progress_frame = tk.LabelFrame(
            phase_frame,
            text="Log Progress",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            relief=tk.RIDGE,
            bd=3,
        )
        progress_frame.pack(pady=10, fill=tk.X, padx=10)

        # Hours worked entry
        hours_frame = tk.Frame(progress_frame, bg=self.theme.bg_color)
        hours_frame.pack(pady=10, fill=tk.X)

        tk.Label(
            hours_frame,
            text="Hours worked:",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
        ).pack(side=tk.LEFT, padx=5)

        self.hours_var = tk.DoubleVar(value=1.0)
        hours_values = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]

        hours_dropdown = ttk.Combobox(
            hours_frame,
            textvariable=self.hours_var,
            values=hours_values,
            width=5,
            font=self.theme.small_font,
        )
        hours_dropdown.pack(side=tk.LEFT, padx=5)

        # Progress description
        tk.Label(
            progress_frame,
            text="Progress notes (optional):",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
        ).pack(anchor="w", padx=10, pady=5)

        self.progress_notes = tk.Text(
            progress_frame,
            height=4,
            width=50,
            font=self.theme.small_font,
            bg=self.theme.primary_color,
            fg=self.theme.text_color,
        )
        self.progress_notes.pack(padx=10, pady=5, fill=tk.X)

        # Log button
        log_button = self.theme.create_pixel_button(
            progress_frame,
            "Log Progress",
            self.log_diss_progress,
            color=self.theme.diss_color,
        )
        log_button.pack(pady=10)

    def update_task_details(self):
        """Update the task details display based on the selected task."""
        # Clear previous details
        for widget in self.task_details_frame.winfo_children():
            widget.destroy()

        # Get selected task
        task_name = self.selected_diss_task.get()
        if not task_name:
            return

        # Find task in data
        selected_task = None
        for phase in ["preparation", "empirical", "integration", "finalization"]:
            for task in self.data["diss"]["tasks"][phase]:
                if task["name"] == task_name:
                    selected_task = task
                    break
            if selected_task:
                break

        if not selected_task:
            return

        # Calculate task progress percentage
        progress = 0
        if selected_task["total_hours"] > 0:
            progress = min(
                100,
                (selected_task["hours_worked"] / selected_task["total_hours"]) * 100,
            )

        # Display task details
        tk.Label(
            self.task_details_frame,
            text=f"Task: {selected_task['name']}",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            anchor="w",
        ).pack(fill=tk.X, padx=10, pady=5)

        tk.Label(
            self.task_details_frame,
            text=f"Timeframe: {selected_task['start_date']} to {selected_task['end_date']}",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            anchor="w",
        ).pack(fill=tk.X, padx=10, pady=5)

        tk.Label(
            self.task_details_frame,
            text=f"Hours worked: {selected_task['hours_worked']} / {selected_task['total_hours']} hours",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            anchor="w",
        ).pack(fill=tk.X, padx=10, pady=5)

        # Progress bar
        progress_frame = tk.Frame(self.task_details_frame, bg=self.theme.bg_color)
        progress_frame.pack(pady=5, fill=tk.X, padx=10)

        tk.Label(
            progress_frame,
            text="Progress: ",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
        ).pack(side=tk.LEFT, padx=5)

        # Create pixel art progress bar
        create_pixel_progress_bar(
            progress_frame,
            progress,
            self.theme.diss_color,
            self.theme.bg_color,
            self.theme.text_color,
            self.theme.darken_color,
        )

        tk.Label(
            progress_frame,
            text=f"{progress:.1f}%",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
        ).pack(side=tk.LEFT, padx=5)

        # Last session
        if "last_session" in selected_task and selected_task["last_session"]:
            last_session = selected_task["last_session"]
            tk.Label(
                self.task_details_frame,
                text=f"Last session: {last_session['date']} - {last_session['hours']} hours",
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
                anchor="w",
            ).pack(fill=tk.X, padx=10, pady=5)

            if last_session["notes"]:
                notes_frame = tk.LabelFrame(
                    self.task_details_frame,
                    text="Last session notes",
                    font=self.theme.small_font,
                    bg=self.theme.bg_color,
                    fg=self.theme.text_color,
                )
                notes_frame.pack(fill=tk.X, padx=10, pady=5)

                notes_text = tk.Text(
                    notes_frame,
                    height=3,
                    width=40,
                    font=self.theme.small_font,
                    bg=self.theme.bg_color,
                    fg=self.theme.text_color,
                    wrap=tk.WORD,
                )
                notes_text.insert(tk.END, last_session["notes"])
                notes_text.config(state=tk.DISABLED)
                notes_text.pack(padx=5, pady=5, fill=tk.X)

    def log_diss_progress(self):
        """Log progress for dissertation task."""
        if not self.data["health_status"]:
            messagebox.showinfo(
                "Health Check Required",
                "Please complete your daily health check before logging progress.",
            )
            return

        # Get selected task
        task_name = self.selected_diss_task.get()
        if not task_name:
            messagebox.showwarning("No Task Selected", "Please select a task.")
            return

        # Find task in data
        selected_task = None
        task_phase = None
        task_index = -1
        for phase in ["preparation", "empirical", "integration", "finalization"]:
            for i, task in enumerate(self.data["diss"]["tasks"][phase]):
                if task["name"] == task_name:
                    selected_task = task
                    task_phase = phase
                    task_index = i
                    break
            if selected_task:
                break

        if not selected_task:
            messagebox.showwarning("Task Not Found", "Selected task not found in data.")
            return

        # Get hours and notes
        hours = self.hours_var.get()
        notes = self.progress_notes.get("1.0", tk.END).strip()

        # Update task data
        self.data["diss"]["tasks"][task_phase][task_index]["hours_worked"] += hours

        # Record session
        self.data["diss"]["tasks"][task_phase][task_index]["last_session"] = {
            "date": datetime.now().strftime("%d.%m.%Y"),
            "hours": hours,
            "notes": notes,
        }

        # Add to sessions log if it doesn't exist
        if "sessions" not in self.data["diss"]["tasks"][task_phase][task_index]:
            self.data["diss"]["tasks"][task_phase][task_index]["sessions"] = []

        # Add session to log
        self.data["diss"]["tasks"][task_phase][task_index]["sessions"].append(
            {
                "date": datetime.now().strftime("%d.%m.%Y"),
                "hours": hours,
                "notes": notes,
            }
        )

        # Add points (10 points per hour)
        points = int(hours * 10)
        self.data["diss"]["points"] += points

        # Update streak
        update_streak(self.data, "diss")

        # Save data
        self.data_manager.save_data()

        # Show confirmation
        messagebox.showinfo(
            "Progress Logged",
            f"You worked on {task_name} for {hours} hours! +{points} points",
        )

        # Clear form fields
        self.progress_notes.delete("1.0", tk.END)

        # Check for task completion
        task_completed = False
        if (
            self.data["diss"]["tasks"][task_phase][task_index]["hours_worked"]
            >= self.data["diss"]["tasks"][task_phase][task_index]["total_hours"]
        ):
            task_completed = True
            # Award bonus points for task completion
            completion_bonus = 50
            self.data["diss"]["points"] += completion_bonus
            self.data_manager.save_data()
            messagebox.showinfo(
                "Task Completed!",
                f"Congratulations! You've completed the '{task_name}' task!\n\nCompletion Bonus: +{completion_bonus} points",
            )

        # Check if level up is needed
        new_level, level_increased, streak_bonus = check_level_up(self.data, "diss")
        if level_increased:
            if streak_bonus > 0:
                messagebox.showinfo(
                    "Level Up!",
                    f"Congratulations! You advanced to Level {new_level}!\n\nStreak Bonus: +{streak_bonus} points",
                )
            else:
                messagebox.showinfo(
                    "Level Up!", f"Congratulations! You advanced to Level {new_level}!"
                )

    def create_activity_breakdown(self, parent):
        """
        Create activity breakdown for dissertation module for statistics display.

        Args:
            parent: Parent widget for the dissertation activity breakdown
        """
        # Calculate statistics for phases
        phase_totals = {
            "preparation": 0,
            "empirical": 0,
            "integration": 0,
            "finalization": 0,
        }

        total_hours_worked = 0

        # Calculate hours worked per phase
        for phase in phase_totals.keys():
            for task in self.data["diss"]["tasks"][phase]:
                phase_totals[phase] += task["hours_worked"]
                total_hours_worked += task["hours_worked"]

        if total_hours_worked == 0:
            # No activities yet
            tk.Label(
                parent,
                text="No dissertation activities recorded yet. Start working on your dissertation tasks to see your breakdown!",
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
                wraplength=400,
                justify="center",
            ).pack(pady=20)
            return

        # Calculate percentages
        phase_percentages = {}
        for phase, hours in phase_totals.items():
            phase_percentages[phase] = (
                (hours / total_hours_worked * 100) if total_hours_worked > 0 else 0
            )

        # Create chart frame
        chart_frame = tk.Frame(parent, bg=self.theme.bg_color)
        chart_frame.pack(pady=10, fill=tk.X)

        # Left side - Text stats
        stats_frame = tk.Frame(chart_frame, bg=self.theme.bg_color)
        stats_frame.pack(side=tk.LEFT, padx=20, fill=tk.Y)

        tk.Label(
            stats_frame,
            text=f"Total Hours Worked: {total_hours_worked}",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(anchor="w", pady=5)

        # Phase colors
        phase_colors = {
            "preparation": "#4CAF50",  # Green
            "empirical": "#2196F3",  # Blue
            "integration": "#FF9800",  # Orange
            "finalization": "#9C27B0",  # Purple
        }

        # Show hours worked per phase
        for phase, hours in phase_totals.items():
            phase_display = phase.capitalize()
            tk.Label(
                stats_frame,
                text=f"{phase_display}: {hours} hours ({phase_percentages[phase]:.1f}%)",
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=phase_colors[phase],
            ).pack(anchor="w", pady=5)

        # Recent dissertation activities
        recent_frame = tk.LabelFrame(
            parent,
            text="Recent Dissertation Activities",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            padx=10,
            pady=10,
        )
        recent_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Collect all dissertation activities
        diss_activities = []

        for phase in phase_totals.keys():
            for task in self.data["diss"]["tasks"][phase]:
                if "sessions" in task:
                    for session in task["sessions"]:
                        diss_activities.append(
                            {
                                "phase": phase.capitalize(),
                                "task": task["name"],
                                "hours": session["hours"],
                                "notes": session["notes"] if "notes" in session else "",
                                "date": session["date"],
                                "points": int(session["hours"] * 10),
                            }
                        )

        # Sort by date (most recent first)
        diss_activities.sort(key=lambda x: x["date"], reverse=True)

        # If no activities
        if not diss_activities:
            tk.Label(
                recent_frame,
                text="No recent dissertation activities recorded.",
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
            ).pack(pady=10)
            return

        # Create scrollable frame for activities
        canvas = tk.Canvas(recent_frame, bg=self.theme.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(recent_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.theme.bg_color)

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Show up to 15 most recent activities
        max_to_show = min(15, len(diss_activities))
        for i in range(max_to_show):
            activity = diss_activities[i]

            # Activity row
            row_frame = tk.Frame(scrollable_frame, bg=self.theme.bg_color)
            row_frame.pack(fill=tk.X, pady=2)

            # Apply alternating row colors
            if i % 2 == 0:
                row_bg = self.theme.bg_color
            else:
                row_bg = self.theme.darken_color(self.theme.bg_color)

            # Phase indicator
            type_label = tk.Label(
                row_frame,
                text=activity["phase"],
                font=self.theme.small_font,
                bg=row_bg,
                fg=phase_colors[activity["phase"].lower()],
                width=12,
                anchor="w",
            )
            type_label.pack(side=tk.LEFT, padx=5)

            # Description
            description = tk.Label(
                row_frame,
                text=f"Worked on '{activity['task']}' for {activity['hours']} hours",
                font=self.theme.small_font,
                bg=row_bg,
                fg=self.theme.text_color,
                anchor="w",
            )
            description.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

            # Points
            points = tk.Label(
                row_frame,
                text=f"+{activity['points']}",
                font=self.theme.small_font,
                bg=row_bg,
                fg="#4CAF50",
                width=4,
                anchor="e",
            )
            points.pack(side=tk.RIGHT, padx=5)

            # Date
            timestamp = tk.Label(
                row_frame,
                text=activity["date"],
                font=self.theme.small_font,
                bg=row_bg,
                fg=self.theme.text_color,
                width=10,
                anchor="e",
            )
            timestamp.pack(side=tk.RIGHT, padx=5)

        # Refresh display
        self.update_task_details()
