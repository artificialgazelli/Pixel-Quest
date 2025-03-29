"""
To Do List module for the Pixel Quest application.
Manages tasks, due dates, and recurring tasks with various frequency options.
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import calendar

# Import tab module
from todo_tab import TodoTab


class TodoList:
    """
    Manages the to-do list functionality.
    Allows users to create, organize, and track tasks with various options
    for scheduling, recurrence, duration, and grouping.
    """

    def __init__(self, app, data_manager, theme):
        """
        Initialize the to-do list module.

        Args:
            app: Main application instance
            data_manager: Data manager instance
            theme: Theme manager instance
        """
        self.app = app
        self.data_manager = data_manager
        self.data = data_manager.data
        self.theme = theme

        # Current date 
        self.current_date = datetime.now().date()
        
        # Make sure the to-do structure exists
        self.initialize_todo_data()

        # Initialize tabs
        self.todo_tab = TodoTab(self, app, data_manager, theme)

    def initialize_todo_data(self):
        """
        Ensure that the to-do data structure exists in the data.
        If not, initialize it with default values.
        """
        if "todo" not in self.data:
            self.data["todo"] = {
                "groups": [
                    {"name": "Work", "color": "#4CAF50"},  # Green
                    {"name": "Personal", "color": "#2196F3"},  # Blue
                    {"name": "Dissertation", "color": "#9C27B0"},  # Purple
                    {"name": "Shopping", "color": "#FF9800"},  # Orange
                ],
                "tasks": [
                    {
                        "id": "task_1",
                        "title": "Complete project proposal",
                        "description": "Write and submit the project proposal document",
                        "created_date": datetime.now().strftime("%Y-%m-%d"),
                        "due_date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
                        "group": "Work",
                        "priority": "high",
                        "status": "active",
                        "completed_date": None,
                        "recurrence": None,
                    },
                    {
                        "id": "task_2",
                        "title": "Buy groceries",
                        "description": "Buy vegetables, fruits, and other essentials",
                        "created_date": datetime.now().strftime("%Y-%m-%d"),
                        "due_date": datetime.now().strftime("%Y-%m-%d"),
                        "group": "Shopping",
                        "priority": "medium",
                        "status": "active",
                        "completed_date": None,
                        "recurrence": None,
                    },
                    {
                        "id": "task_3",
                        "title": "Work on dissertation",
                        "description": "Write at least 500 words for the dissertation",
                        "created_date": datetime.now().strftime("%Y-%m-%d"),
                        "due_date": datetime.now().strftime("%Y-%m-%d"),
                        "group": "Dissertation",
                        "priority": "high",
                        "status": "active",
                        "completed_date": None,
                        "recurrence": {
                            "type": "weekly",
                            "days": [0, 1, 2, 3, 4],  # Monday to Friday
                            "end_date": None
                        }
                    },
                ]
            }
            # Save the initialized data
            self.data_manager.save_data()
        else:
            # Update the data structure if it already exists
            self._update_existing_data()

    def _update_existing_data(self):
        """Update existing data structure with new features."""
        needs_save = False

        # Ensure default groups exist
        if "groups" not in self.data["todo"]:
            self.data["todo"]["groups"] = [
                {"name": "Work", "color": "#4CAF50"},
                {"name": "Personal", "color": "#2196F3"},
                {"name": "Dissertation", "color": "#9C27B0"},
                {"name": "Shopping", "color": "#FF9800"},
            ]
            needs_save = True

        # Add dissertation task if it doesn't exist
        if "tasks" in self.data["todo"]:
            has_diss_task = False
            for task in self.data["todo"]["tasks"]:
                if (task.get("title") == "Work on dissertation" and 
                    task.get("group") == "Dissertation" and 
                    task.get("recurrence") is not None):
                    has_diss_task = True
                    break
            
            if not has_diss_task:
                self.data["todo"]["tasks"].append({
                    "id": f"task_{len(self.data['todo']['tasks']) + 1}",
                    "title": "Work on dissertation",
                    "description": "Write at least 500 words for the dissertation",
                    "created_date": datetime.now().strftime("%Y-%m-%d"),
                    "due_date": datetime.now().strftime("%Y-%m-%d"),
                    "group": "Dissertation",
                    "priority": "high",
                    "status": "active",
                    "completed_date": None,
                    "recurrence": {
                        "type": "weekly",
                        "days": [0, 1, 2, 3, 4],  # Monday to Friday
                        "end_date": None
                    }
                })
                needs_save = True

        # Save if changes were made
        if needs_save:
            self.data_manager.save_data()

    def show_module(self, parent_frame):
        """
        Show the to-do list interface.

        Args:
            parent_frame: Parent frame to place to-do list content
        """
        # Title
        title_label = tk.Label(
            parent_frame,
            text="TO DO LIST",
            font=self.theme.heading_font,
            bg=self.theme.bg_color,
            fg=self.theme.todo_color,  # Use theme's todo color
        )
        title_label.pack(pady=20)

        # Create tab for to-do list
        tab_control = ttk.Notebook(parent_frame)
        tab_control.pack(expand=1, fill="both", padx=10, pady=10)

        # Create tab
        todo_tab = tk.Frame(tab_control, bg=self.theme.bg_color)
        tab_control.add(todo_tab, text="Tasks")

        # Fill the tab with content
        self.todo_tab.create_todo_view(todo_tab)

        # Back button
        back_button = self.theme.create_pixel_button(
            parent_frame,
            "Back to Main Menu",
            self.app.show_main_menu,
            color="#9E9E9E",
        )
        back_button.pack(pady=20)

    def refresh_display(self):
        """Refresh the to-do list display."""
        # Get the current notebook tab
        current_tab = self.app.main_frame.winfo_children()[1].index("current")

        # Clear the main frame
        self.app.clear_frame()

        # Recreate the to-do list
        self.show_module(self.app.main_frame)

        # Set the active tab back to what it was
        self.app.main_frame.winfo_children()[1].select(current_tab)

    def get_active_tasks(self, group_filter=None):
        """
        Get all active tasks, optionally filtered by group.
        
        Args:
            group_filter: Optional group name to filter by
            
        Returns:
            List of active tasks
        """
        tasks = self.data.get("todo", {}).get("tasks", [])
        active_tasks = [task for task in tasks if task.get("status") == "active"]
        
        if group_filter and group_filter != "All":
            active_tasks = [task for task in active_tasks if task.get("group") == group_filter]
            
        return active_tasks
    
    def get_completed_tasks(self, group_filter=None):
        """
        Get all completed tasks, optionally filtered by group.
        
        Args:
            group_filter: Optional group name to filter by
            
        Returns:
            List of completed tasks
        """
        tasks = self.data.get("todo", {}).get("tasks", [])
        completed_tasks = [task for task in tasks if task.get("status") == "completed"]
        
        if group_filter and group_filter != "All":
            completed_tasks = [task for task in completed_tasks if task.get("group") == group_filter]
            
        return completed_tasks
    
    def complete_task(self, task_id):
        """
        Mark a task as completed.
        
        Args:
            task_id: ID of the task to complete
        """
        tasks = self.data.get("todo", {}).get("tasks", [])
        for i, task in enumerate(tasks):
            if task.get("id") == task_id:
                # Check if the task is recurring
                if task.get("recurrence"):
                    # Create a new instance of the task for the next occurrence
                    self._create_next_occurrence(task)
                
                # Mark the current task as completed
                self.data["todo"]["tasks"][i]["status"] = "completed"
                self.data["todo"]["tasks"][i]["completed_date"] = datetime.now().strftime("%Y-%m-%d")
                self.data_manager.save_data()
                return True
        
        return False
    
    def _create_next_occurrence(self, task):
        """
        Create the next occurrence of a recurring task.
        
        Args:
            task: The recurring task to create a new instance of
        """
        recurrence = task.get("recurrence")
        if not recurrence:
            return
        
        new_task = task.copy()
        
        # Generate a new ID
        new_task["id"] = f"task_{len(self.data['todo']['tasks']) + 1}"
        
        # Determine the next due date
        current_due_date = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
        next_due_date = None
        
        if recurrence["type"] == "daily":
            next_due_date = current_due_date + timedelta(days=1)
        
        elif recurrence["type"] == "weekly":
            # Find the next weekday in the list
            recurrence_days = recurrence.get("days", [])
            if recurrence_days:
                # Current weekday (0=Monday)
                current_weekday = current_due_date.weekday()
                
                # Find the next weekday in the list
                next_day_index = None
                for day in recurrence_days:
                    if day > current_weekday:
                        next_day_index = day
                        break
                
                if next_day_index is not None:
                    # Next day is in the same week
                    days_ahead = next_day_index - current_weekday
                    next_due_date = current_due_date + timedelta(days=days_ahead)
                else:
                    # Next day is in the next week
                    days_ahead = 7 - current_weekday + recurrence_days[0]
                    next_due_date = current_due_date + timedelta(days=days_ahead)
        
        elif recurrence["type"] == "monthly":
            # Move to the next month, keeping the same day
            next_month = current_due_date.month + 1
            next_year = current_due_date.year
            
            if next_month > 12:
                next_month = 1
                next_year += 1
            
            # Handle month length differences (e.g., Jan 31 -> Feb 28)
            last_day = calendar.monthrange(next_year, next_month)[1]
            next_day = min(current_due_date.day, last_day)
            
            next_due_date = datetime(next_year, next_month, next_day).date()
        
        elif recurrence["type"] == "yearly":
            next_due_date = datetime(current_due_date.year + 1, 
                                    current_due_date.month, 
                                    current_due_date.day).date()
        
        elif recurrence["type"] == "custom":
            # Custom interval in days
            interval_days = recurrence.get("interval", 1)
            next_due_date = current_due_date + timedelta(days=interval_days)
        
        # Check if the task should still recur (end date check)
        if recurrence.get("end_date") and next_due_date:
            end_date = datetime.strptime(recurrence["end_date"], "%Y-%m-%d").date()
            if next_due_date > end_date:
                return  # Don't create a new task if past the end date
        
        # Update the new task with the next due date
        if next_due_date:
            new_task["due_date"] = next_due_date.strftime("%Y-%m-%d")
            new_task["status"] = "active"
            new_task["completed_date"] = None
            
            # Add the new task to the task list
            self.data["todo"]["tasks"].append(new_task)
            
    def delete_task(self, task_id):
        """
        Delete a task from the to-do list.
        
        Args:
            task_id: ID of the task to delete
            
        Returns:
            True if the task was deleted, False otherwise
        """
        tasks = self.data.get("todo", {}).get("tasks", [])
        for i, task in enumerate(tasks):
            if task.get("id") == task_id:
                del self.data["todo"]["tasks"][i]
                self.data_manager.save_data()
                return True
        
        return False
