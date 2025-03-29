"""
Habit tracker module for the Pixel Quest application.
Manages daily habits, check-ins, and streak tracking.
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, timedelta
import calendar
from src.utils import update_streak
import json

class HabitTracker:
    """
    Manages the habit tracking functionality.
    Allows users to track daily habits and important check-ins.
    """

    def __init__(self, app, data_manager, theme):
        """
        Initialize the habit tracker module.

        Args:
            app: Main application instance
            data_manager: Data manager instance
            theme: Theme manager instance
        """
        self.app = app
        self.data_manager = data_manager
        self.data = data_manager.data
        self.theme = theme
        
        # Current date for the calendar views
        self.current_date = datetime.now().date()
        self.selected_month = self.current_date.month
        self.selected_year = self.current_date.year
        
        # Make sure the habits structure exists
        self.initialize_habits_data()
        
    def initialize_habits_data(self):
        """
        Ensure that the habit data structure exists in the data.
        If not, initialize it with default values.
        """
        if "habits" not in self.data:
            self.data["habits"] = {
                "categories": [
                    {"name": "Health", "color": "#4CAF50"},  # Green
                    {"name": "Productivity", "color": "#2196F3"},  # Blue
                    {"name": "Learning", "color": "#FF9800"},  # Orange
                    {"name": "Personal", "color": "#E91E63"},  # Pink
                ],
                "daily_habits": [
                    {
                        "name": "Early wakeup",
                        "icon": "☀️",
                        "active": True,
                        "category": "Productivity",  # Add category
                        "frequency": "daily",
                        "streak": 0,
                        "completed_dates": []
                    },
                    {
                        "name": "Exercise",
                        "icon": "🏃",
                        "active": True,
                        "category": "Health",  # Add category
                        "frequency": "daily",
                        "streak": 0,
                        "completed_dates": []
                    },
                    {
                        "name": "Reading",
                        "icon": "📚",
                        "active": True,
                        "category": "Learning",  # Add category
                        "frequency": "daily",
                        "streak": 0,
                        "completed_dates": []
                    },
                    {
                        "name": "Meditation",
                        "icon": "🧘",
                        "active": True,
                        "category": "Health",  # Add category
                        "frequency": "daily", 
                        "streak": 0,
                        "completed_dates": []
                    },
                    {
                        "name": "Drink water",
                        "icon": "💧",
                        "active": True,
                        "category": "Health",  # Add category
                        "frequency": "daily",
                        "streak": 0,
                        "completed_dates": []
                    }
                ],
                "custom_habits": [],
                "check_ins": [
                    {
                        "name": "Doctor Appointments",
                        "icon": "🩺",
                        "category": "Health",  # Add category
                        "dates": [],
                        "notes": {}
                    },
                    {
                        "name": "Dentist",
                        "icon": "🦷",
                        "category": "Health",  # Add category
                        "dates": [],
                        "notes": {}
                    }
                ]
            }
            # Save the initialized data
            self.data_manager.save_data()
        else:
            # If the data exists but categories are missing, add them
            if "categories" not in self.data["habits"]:
                self.data["habits"]["categories"] = [
                    {"name": "Health", "color": "#4CAF50"},  # Green
                    {"name": "Productivity", "color": "#2196F3"},  # Blue
                    {"name": "Learning", "color": "#FF9800"},  # Orange
                    {"name": "Personal", "color": "#E91E63"},  # Pink
                ]
                
                # Ensure all habits have a category
                for habit_type in ["daily_habits", "custom_habits"]:
                    for habit in self.data["habits"].get(habit_type, []):
                        if "category" not in habit:
                            habit["category"] = "Personal"
                
                # Ensure all check-ins have a category
                for check_in in self.data["habits"].get("check_ins", []):
                    if "category" not in check_in:
                        check_in["category"] = "Health"
                        
                # Save the updated data
                self.data_manager.save_data()
        
    def show_module(self, parent_frame):
        """
        Show the habit tracker interface.
        
        Args:
            parent_frame: Parent frame to place habit tracker content
        """
        # Title
        title_label = tk.Label(
            parent_frame,
            text="HABIT TRACKER",
            font=self.theme.heading_font,
            bg=self.theme.bg_color,
            fg=self.theme.habit_color,  # Use the theme's habit color
        )
        title_label.pack(pady=20)
        
        # Create tabs for different views
        tab_control = ttk.Notebook(parent_frame)
        tab_control.pack(expand=1, fill="both", padx=10, pady=10)
        
        # Create tabs
        habits_tab = tk.Frame(tab_control, bg=self.theme.bg_color)
        check_ins_tab = tk.Frame(tab_control, bg=self.theme.bg_color)
        stats_tab = tk.Frame(tab_control, bg=self.theme.bg_color)
        categories_tab = tk.Frame(tab_control, bg=self.theme.bg_color)  # New categories tab
        
        tab_control.add(habits_tab, text="Daily Habits")
        tab_control.add(check_ins_tab, text="Check-ins")
        tab_control.add(stats_tab, text="Statistics")
        tab_control.add(categories_tab, text="Categories")  # Add categories tab
        
        # Fill the tabs with content
        self.create_habits_view(habits_tab)
        self.create_check_ins_view(check_ins_tab)
        self.create_stats_view(stats_tab)
        self.create_categories_view(categories_tab)  # Create categories view
        
        # Back button
        back_button = self.theme.create_pixel_button(
            parent_frame,
            "Back to Main Menu",
            self.app.show_main_menu,
            color="#9E9E9E",
        )
        back_button.pack(pady=20)
    
    def create_categories_view(self, parent):
        """
        Create the categories tab view for managing habit categories.
        
        Args:
            parent: Parent frame to place the categories view
        """
        # Top control panel
        control_frame = tk.Frame(parent, bg=self.theme.bg_color)
        control_frame.pack(pady=10, fill=tk.X)
        
        # Add category button
        add_category_button = self.theme.create_pixel_button(
            control_frame,
            "Add New Category",
            self.add_new_category,
            color=self.theme.habit_color,
        )
        add_category_button.pack(side=tk.LEFT, padx=10)
        
        # Create a frame for displaying categories
        categories_frame = tk.Frame(parent, bg=self.theme.bg_color)
        categories_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # If no categories exist yet, show a message
        if not self.data["habits"].get("categories", []):
            tk.Label(
                categories_frame,
                text="No categories defined yet. Click 'Add New Category' to get started!",
                font=self.theme.pixel_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
                pady=20,
            ).pack()
            return
        
        # Get all categories
        categories = self.data["habits"].get("categories", [])
        
        # Create a table header
        header_frame = tk.Frame(categories_frame, bg=self.theme.bg_color)
        header_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            header_frame,
            text="Category Name",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            width=20,
            anchor="w",
        ).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        tk.Label(
            header_frame,
            text="Color",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            width=10,
            anchor="w",
        ).grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        tk.Label(
            header_frame,
            text="Habits Count",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            width=15,
            anchor="w",
        ).grid(row=0, column=2, padx=5, pady=5, sticky="w")
        
        tk.Label(
            header_frame,
            text="Actions",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            width=15,
            anchor="w",
        ).grid(row=0, column=3, padx=5, pady=5, sticky="w")
        
        # Create scrollable frame for categories
        canvas = tk.Canvas(categories_frame, bg=self.theme.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(categories_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.theme.bg_color)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y")
        
        # Display each category
        for i, category in enumerate(categories):
            # Row background alternates for better readability
            row_bg = self.theme.bg_color if i % 2 == 0 else self.theme.darken_color(self.theme.bg_color)
            
            # Count habits in this category
            habits_count = 0
            for habit_type in ["daily_habits", "custom_habits"]:
                for habit in self.data["habits"].get(habit_type, []):
                    if habit.get("category") == category["name"]:
                        habits_count += 1
            
            # Category row
            row_frame = tk.Frame(scrollable_frame, bg=row_bg)
            row_frame.pack(fill=tk.X)
            
            # Category name
            tk.Label(
                row_frame,
                text=category["name"],
                font=self.theme.small_font,
                bg=row_bg,
                fg=self.theme.text_color,
                width=20,
                anchor="w",
            ).grid(row=0, column=0, padx=5, pady=5, sticky="w")
            
            # Color indicator
            color_frame = tk.Frame(row_frame, bg=row_bg)
            color_frame.grid(row=0, column=1, padx=5, pady=5)
            
            color_sample = tk.Frame(
                color_frame,
                bg=category["color"],
                width=20,
                height=20,
            )
            color_sample.pack(side=tk.LEFT, padx=5)
            
            color_label = tk.Label(
                color_frame,
                text=category["color"],
                font=self.theme.small_font,
                bg=row_bg,
                fg=self.theme.text_color,
            )
            color_label.pack(side=tk.LEFT, padx=5)
            
            # Habits count
            tk.Label(
                row_frame,
                text=str(habits_count),
                font=self.theme.small_font,
                bg=row_bg,
                fg=self.theme.text_color,
                width=15,
                anchor="w",
            ).grid(row=0, column=2, padx=5, pady=5, sticky="w")
            
            # Action buttons
            actions_frame = tk.Frame(row_frame, bg=row_bg)
            actions_frame.grid(row=0, column=3, padx=5, pady=5)
            
            # Edit button
            edit_button = tk.Button(
                actions_frame,
                text="✏️",
                font=self.theme.small_font,
                bg=self.theme.primary_color,
                fg=self.theme.text_color,
                command=lambda c=category: self.edit_category(c),
                relief=tk.FLAT,
            )
            edit_button.pack(side=tk.LEFT, padx=5)
            
            # Delete button (disabled if category has habits)
            delete_button = tk.Button(
                actions_frame,
                text="🗑️",
                font=self.theme.small_font,
                bg="#F44336" if habits_count == 0 else self.theme.darken_color(self.theme.bg_color),
                fg="white" if habits_count == 0 else self.theme.text_color,
                command=lambda c=category: self.delete_category(c) if habits_count == 0 else messagebox.showinfo("Cannot Delete", f"Can't delete category with {habits_count} habits assigned to it."),
                relief=tk.FLAT,
                state=tk.NORMAL if habits_count == 0 else tk.DISABLED,
            )
            delete_button.pack(side=tk.LEFT, padx=5)
    
    def add_new_category(self):
        """Open a dialog to add a new category."""
        # Create a dialog window
        dialog = tk.Toplevel()
        dialog.title("Add New Category")
        dialog.geometry("400x200")
        dialog.configure(bg=self.theme.bg_color)
        dialog.transient(self.app.root)
        dialog.grab_set()
        
        # Name input
        name_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        name_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            name_frame,
            text="Category Name:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT)
        
        name_var = tk.StringVar()
        name_entry = tk.Entry(
            name_frame,
            textvariable=name_var,
            font=self.theme.small_font,
            bg=self.theme.primary_color,
            fg=self.theme.text_color,
            width=30,
        )
        name_entry.pack(side=tk.LEFT, padx=10)
        
        # Color input
        color_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        color_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            color_frame,
            text="Color (Hex):",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT)
        
        color_var = tk.StringVar(value="#4CAF50")
        color_entry = tk.Entry(
            color_frame,
            textvariable=color_var,
            font=self.theme.small_font,
            bg=self.theme.primary_color,
            fg=self.theme.text_color,
            width=10,
        )
        color_entry.pack(side=tk.LEFT, padx=10)
        
        # Color preview
        color_preview = tk.Frame(
            color_frame,
            bg="#4CAF50",
            width=20,
            height=20,
        )
        color_preview.pack(side=tk.LEFT, padx=10)
        
        # Update color preview when color changes
        def update_preview(*args):
            try:
                color = color_var.get()
                color_preview.config(bg=color)
            except:
                pass
        
        color_var.trace_add("write", update_preview)
        
        # Button frame
        button_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        button_frame.pack(pady=20)
        
        # Cancel button
        cancel_button = self.theme.create_pixel_button(
            button_frame,
            "Cancel",
            dialog.destroy,
            color="#F44336",
        )
        cancel_button.pack(side=tk.LEFT, padx=10)
        
        # Add button
        add_button = self.theme.create_pixel_button(
            button_frame,
            "Add Category",
            lambda: self.save_new_category(
                name_var.get(),
                color_var.get(),
                dialog,
            ),
            color=self.theme.habit_color,  # Use theme's habit color
        )
        add_button.pack(side=tk.LEFT, padx=10)
        
        # Focus the name entry
        name_entry.focus_set()
    
    def save_new_category(self, name, color, dialog):
        """
        Save a new category to the data.
        
        Args:
            name: Category name
            color: Category color
            dialog: Dialog window to close after saving
        """
        # Validate input
        if not name:
            messagebox.showerror("Error", "Please enter a category name.")
            return
        
        # Validate color
        try:
            self.root.winfo_rgb(color)
        except:
            messagebox.showerror("Error", "Invalid color format. Please use a valid hex code (#RRGGBB).")
            return
        
        # Check if category name already exists
        for category in self.data["habits"].get("categories", []):
            if category["name"] == name:
                messagebox.showerror("Error", f"A category named '{name}' already exists.")
                return
        
        # Create new category
        new_category = {
            "name": name,
            "color": color
        }
        
        # Initialize categories if not exist
        if "categories" not in self.data["habits"]:
            self.data["habits"]["categories"] = []
        
        # Add to categories
        self.data["habits"]["categories"].append(new_category)
        
        # Save data
        self.data_manager.save_data()
        
        # Close dialog
        dialog.destroy()
        
        # Refresh display
        self.refresh_display()
        
        # Show confirmation
        messagebox.showinfo("Success", f"Category '{name}' has been added!")
    
    def edit_category(self, category):
        """
        Open a dialog to edit an existing category.
        
        Args:
            category: Category to edit
        """
        # Create a dialog window
        dialog = tk.Toplevel()
        dialog.title(f"Edit Category: {category['name']}")
        dialog.geometry("400x200")
        dialog.configure(bg=self.theme.bg_color)
        dialog.transient(self.app.root)
        dialog.grab_set()
        
        # Name input
        name_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        name_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            name_frame,
            text="Category Name:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT)
        
        name_var = tk.StringVar(value=category["name"])
        name_entry = tk.Entry(
            name_frame,
            textvariable=name_var,
            font=self.theme.small_font,
            bg=self.theme.primary_color,
            fg=self.theme.text_color,
            width=30,
        )
        name_entry.pack(side=tk.LEFT, padx=10)
        
        # Color input
        color_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        color_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            color_frame,
            text="Color (Hex):",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT)
        
        color_var = tk.StringVar(value=category["color"])
        color_entry = tk.Entry(
            color_frame,
            textvariable=color_var,
            font=self.theme.small_font,
            bg=self.theme.primary_color,
            fg=self.theme.text_color,
            width=10,
        )
        color_entry.pack(side=tk.LEFT, padx=10)
        
        # Color preview
        color_preview = tk.Frame(
            color_frame,
            bg=category["color"],
            width=20,
            height=20,
        )
        color_preview.pack(side=tk.LEFT, padx=10)
        
        # Update color preview when color changes
        def update_preview(*args):
            try:
                color = color_var.get()
                color_preview.config(bg=color)
            except:
                pass
        
        color_var.trace_add("write", update_preview)
        
        # Button frame
        button_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        button_frame.pack(pady=20)
        
        # Cancel button
        cancel_button = self.theme.create_pixel_button(
            button_frame,
            "Cancel",
            dialog.destroy,
            color="#F44336",
        )
        cancel_button.pack(side=tk.LEFT, padx=10)
        
        # Update button
        update_button = self.theme.create_pixel_button(
            button_frame,
            "Update Category",
            lambda: self.update_category(
                category,
                name_var.get(),
                color_var.get(),
                dialog,
            ),
            color=self.theme.habit_color,  # Use theme's habit color
        )
        update_button.pack(side=tk.LEFT, padx=10)
        
        # Focus the name entry
        name_entry.focus_set()
    
    def update_category(self, category, new_name, new_color, dialog):
        """
        Update an existing category.
        
        Args:
            category: Existing category to update
            new_name: New category name
            new_color: New category color
            dialog: Dialog window to close after saving
        """
        # Validate input
        if not new_name:
            messagebox.showerror("Error", "Please enter a category name.")
            return
        
        # Validate color
        try:
            self.root.winfo_rgb(new_color)
        except:
            messagebox.showerror("Error", "Invalid color format. Please use a valid hex code (#RRGGBB).")
            return
        
        # Check if category name already exists (unless it's the same name)
        if new_name != category["name"]:
            for cat in self.data["habits"].get("categories", []):
                if cat["name"] == new_name:
                    messagebox.showerror("Error", f"A category named '{new_name}' already exists.")
                    return
        
        # Find the category and update it
        for i, cat in enumerate(self.data["habits"].get("categories", [])):
            if cat["name"] == category["name"]:
                # Update category
                self.data["habits"]["categories"][i]["name"] = new_name
                self.data["habits"]["categories"][i]["color"] = new_color
                
                # Update habits that use this category
                old_name = category["name"]
                for habit_type in ["daily_habits", "custom_habits"]:
                    for habit in self.data["habits"].get(habit_type, []):
                        if habit.get("category") == old_name:
                            habit["category"] = new_name
                
                # Update check-ins that use this category
                for check_in in self.data["habits"].get("check_ins", []):
                    if check_in.get("category") == old_name:
                        check_in["category"] = new_name
                
                break
        
        # Save data
        self.data_manager.save_data()
        
        # Close dialog
        dialog.destroy()
        
        # Refresh display
        self.refresh_display()
        
        # Show confirmation
        messagebox.showinfo("Success", f"Category '{new_name}' has been updated!")
    
    def delete_category(self, category):
        """
        Delete a category.
        
        Args:
            category: Category to delete
        """
        # Confirm deletion
        if not messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the category '{category['name']}'?"):
            return
        
        # Count habits in this category
        habits_count = 0
        for habit_type in ["daily_habits", "custom_habits"]:
            for habit in self.data["habits"].get(habit_type, []):
                if habit.get("category") == category["name"]:
                    habits_count += 1
        
        # Don't delete if habits are assigned
        if habits_count > 0:
            messagebox.showinfo("Cannot Delete", f"Cannot delete category with {habits_count} habits assigned to it.")
            return
        
        # Find the category and delete it
        for i, cat in enumerate(self.data["habits"].get("categories", [])):
            if cat["name"] == category["name"]:
                del self.data["habits"]["categories"][i]
                break
        
        # Save data
        self.data_manager.save_data()
        
        # Refresh display
        self.refresh_display()
        
        # Show confirmation
        messagebox.showinfo("Success", f"Category '{category['name']}' has been deleted!")
        
    def create_habits_view(self, parent):
        """
        Create the habits tab view with a calendar and habit list.
        
        Args:
            parent: Parent frame to place the habits view
        """
        # Top control panel
        control_frame = tk.Frame(parent, bg=self.theme.bg_color)
        control_frame.pack(pady=5, fill=tk.X)
        
        # Add habit button
        add_habit_button = self.theme.create_pixel_button(
            control_frame,
            "Add New Habit",
            self.add_new_habit,
            color="#4CAF50",
        )
        add_habit_button.pack(side=tk.LEFT, padx=10)
        
        # Filter by category dropdown
        filter_frame = tk.Frame(control_frame, bg=self.theme.bg_color)
        filter_frame.pack(side=tk.LEFT, padx=20)
        
        tk.Label(
            filter_frame,
            text="Filter by Category:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT, padx=5)
        
        # Get categories for dropdown
        categories = ["All"] + [c["name"] for c in self.data["habits"].get("categories", [])]
        
        self.category_filter_var = tk.StringVar(value="All")
        category_dropdown = ttk.Combobox(
            filter_frame,
            textvariable=self.category_filter_var,
            values=categories,
            font=self.theme.small_font,
            width=15,
        )
        category_dropdown.pack(side=tk.LEFT, padx=5)
        
        # Add binding to refresh when filter changes
        category_dropdown.bind("<<ComboboxSelected>>", lambda e: self.refresh_display())
        
        # Current week display
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        
        week_label = tk.Label(
            control_frame,
            text=f"Week: {start_of_week.strftime('%b %d')} - {end_of_week.strftime('%b %d, %Y')}",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        )
        week_label.pack(side=tk.RIGHT, padx=10)
        
        # Main content frame
        content_frame = tk.Frame(parent, bg=self.theme.bg_color)
        content_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Calendar header with days of week
        days_frame = tk.Frame(content_frame, bg=self.theme.bg_color)
        days_frame.pack(fill=tk.X, pady=5)
        
        days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        # First column for habit names
        tk.Label(
            days_frame,
            text="Habit",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            width=16,
            anchor="w",
        ).grid(row=0, column=0, padx=5)
        
        # Day columns
        for i, day in enumerate(days):
            # Calculate date for this column
            date = start_of_week + timedelta(days=i)
            
            # Container frame for day header
            day_frame = tk.Frame(days_frame, bg=self.theme.bg_color)
            day_frame.grid(row=0, column=i+1, padx=2)
            
            # Day name
            tk.Label(
                day_frame,
                text=day,
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
            ).pack()
            
            # Day number
            date_color = "#FF5722" if date == today else self.theme.text_color
            tk.Label(
                day_frame,
                text=str(date.day),
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=date_color,
            ).pack()
        
        # Create scrollable frame for habits
        habits_canvas = tk.Canvas(content_frame, bg=self.theme.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=habits_canvas.yview)
        scrollable_frame = tk.Frame(habits_canvas, bg=self.theme.bg_color)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: habits_canvas.configure(scrollregion=habits_canvas.bbox("all"))
        )
        
        habits_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        habits_canvas.configure(yscrollcommand=scrollbar.set)
        
        habits_canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y")
        
        # Add habit rows
        self.display_habit_rows(scrollable_frame, start_of_week)
        
    def display_habit_rows(self, parent, start_date):
        """
        Display habit rows with toggles for each day of the week.
        
        Args:
            parent: Parent frame to place the habit rows
            start_date: Starting date of the displayed week
        """
        # Get all habits
        all_habits = (
            self.data.get("habits", {}).get("daily_habits", []) +
            self.data.get("habits", {}).get("custom_habits", [])
        )
        
        # Filter by category if needed
        selected_category = self.category_filter_var.get()
        if selected_category != "All":
            all_habits = [h for h in all_habits if h.get("category") == selected_category]
        
        # If no habits exist yet, show a message
        if not all_habits:
            message = "No habits added yet. Click 'Add New Habit' to get started!"
            if selected_category != "All":
                message = f"No habits in the '{selected_category}' category. Try a different filter or add new habits."
                
            tk.Label(
                parent,
                text=message,
                font=self.theme.pixel_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
                pady=20,
            ).grid(row=0, column=0, columnspan=8)
            return
        
        # Get category colors
        category_colors = {}
        for category in self.data["habits"].get("categories", []):
            category_colors[category["name"]] = category["color"]
        
        # Create a row for each habit
        for i, habit in enumerate(all_habits):
            # Skip inactive habits
            if not habit.get("active", True):
                continue
                
            # Row background alternates for better readability
            row_bg = self.theme.bg_color if i % 2 == 0 else self.theme.darken_color(self.theme.bg_color)
            
            # Get category color
            category = habit.get("category", "Personal")
            category_color = category_colors.get(category, self.theme.habit_color)
            
            # Habit info frame (first column)
            habit_frame = tk.Frame(parent, bg=row_bg, padx=5, pady=5)
            habit_frame.grid(row=i, column=0, sticky="ew")
            
            # Category color indicator
            category_indicator = tk.Frame(
                habit_frame,
                bg=category_color,
                width=5,
                height=20
            )
            category_indicator.pack(side=tk.LEFT, padx=2)
            
            # Habit icon and name
            icon_label = tk.Label(
                habit_frame,
                text=habit.get("icon", "📋"),
                font=self.theme.pixel_font,
                bg=row_bg,
                fg=self.theme.text_color,
            )
            icon_label.pack(side=tk.LEFT, padx=2)
            
            name_label = tk.Label(
                habit_frame,
                text=habit["name"],
                font=self.theme.small_font,
                bg=row_bg,
                fg=self.theme.text_color,
                anchor="w",
                width=12,
            )
            name_label.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
            
            # Streak display
            streak_frame = tk.Frame(habit_frame, bg=row_bg)
            streak_frame.pack(side=tk.RIGHT)
            
            streak_label = tk.Label(
                streak_frame,
                text=f"🔥 {habit.get('streak', 0)}",
                font=self.theme.small_font,
                bg=row_bg,
                fg="#FF5722",  # Orange for streak
            )
            streak_label.pack()
            
            # Toggle buttons for each day of the week
            for j in range(7):
                date = start_date + timedelta(days=j)
                date_str = date.strftime("%Y-%m-%d")
                
                # Check if habit was completed on this date
                completed = date_str in habit.get("completed_dates", [])
                
                # Cell background
                cell_frame = tk.Frame(
                    parent,
                    bg=row_bg,
                    padx=5,
                    pady=5,
                )
                cell_frame.grid(row=i, column=j+1)
                
                # Different button styles for completed vs not completed
                if completed:
                    # For completed habits, show a green checkmark button
                    button = tk.Button(
                        cell_frame,
                        text="✓",
                        font=self.theme.small_font,
                        bg="#4CAF50",  # Green
                        fg="white",
                        width=2,
                        height=1,
                        relief=tk.FLAT,
                        command=lambda h=habit["name"], d=date_str: self.toggle_habit(h, d),
                    )
                else:
                    # For incomplete habits, show an empty button
                    button = tk.Button(
                        cell_frame,
                        text=" ",
                        font=self.theme.small_font,
                        bg=self.theme.primary_color,
                        fg=self.theme.text_color,
                        width=2,
                        height=1,
                        relief=tk.FLAT,
                        command=lambda h=habit["name"], d=date_str: self.toggle_habit(h, d),
                    )
                
                # Disable buttons for future dates
                if date > datetime.now().date():
                    button.config(state=tk.DISABLED)
                    
                button.pack(padx=5, pady=5)
                
    def create_check_ins_view(self, parent):
        """
        Create the check-ins tab view with a calendar and event list.
        
        Args:
            parent: Parent frame to place the check-ins view
        """
        # Control panel with month navigation
        control_frame = tk.Frame(parent, bg=self.theme.bg_color)
        control_frame.pack(fill=tk.X, pady=5)
        
        # Previous month button
        prev_button = self.theme.create_pixel_button(
            control_frame,
            "<",
            self.prev_month,
            color="#9E9E9E",
            width=2,
        )
        prev_button.pack(side=tk.LEFT, padx=10)
        
        # Month/year label
        self.month_label = tk.Label(
            control_frame,
            text=f"{calendar.month_name[self.selected_month]} {self.selected_year}",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        )
        self.month_label.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        # Next month button
        next_button = self.theme.create_pixel_button(
            control_frame,
            ">",
            self.next_month,
            color="#9E9E9E",
            width=2,
        )
        next_button.pack(side=tk.RIGHT, padx=10)
        
        # Add check-in button
        add_checkin_button = self.theme.create_pixel_button(
            control_frame,
            "Add Check-in",
            self.add_new_check_in,
            color=self.theme.habit_color,  # Use the theme's habit color
        )
        add_checkin_button.pack(side=tk.RIGHT, padx=10)
        
        # Calendar frame
        calendar_frame = tk.Frame(parent, bg=self.theme.bg_color)
        calendar_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Days of week header
        days_frame = tk.Frame(calendar_frame, bg=self.theme.bg_color)
        days_frame.pack(fill=tk.X)
        
        days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        for i, day in enumerate(days):
            tk.Label(
                days_frame,
                text=day,
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
                width=8,
            ).grid(row=0, column=i, padx=2, pady=5)
        
        # Calendar grid
        self.month_frame = tk.Frame(calendar_frame, bg=self.theme.bg_color)
        self.month_frame.pack(fill=tk.BOTH, expand=True)
        
        # Display current month
        self.display_month()
        
        # Events frame
        events_frame = tk.LabelFrame(
            parent,
            text="Check-in Details",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.habit_color,  # Use the theme's habit color
            padx=10,
            pady=10,
        )
        events_frame.pack(fill=tk.X, pady=10, padx=10)
        
        # Create a frame for the events list that will be updated
        self.events_list_frame = tk.Frame(events_frame, bg=self.theme.bg_color)
        self.events_list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Display check-ins for current month
        self.display_check_ins()
    
    def create_stats_view(self, parent):
        """
        Create the statistics tab view with habit performance metrics.
        
        Args:
            parent: Parent frame to place the statistics view
        """
        # Stats overview
        overview_frame = tk.LabelFrame(
            parent,
            text="Habit Overview",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.habit_color,  # Use the theme's habit color
        )
        overview_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Calculate stats
        habits = (
            self.data.get("habits", {}).get("daily_habits", []) +
            self.data.get("habits", {}).get("custom_habits", [])
        )
        
        total_habits = len(habits)
        active_habits = sum(1 for h in habits if h.get("active", True))
        
        # Today's date
        today = datetime.now().date().strftime("%Y-%m-%d")
        
        # Count habits completed today
        completed_today = sum(
            1 for h in habits 
            if h.get("active", True) and today in h.get("completed_dates", [])
        )
        
        completion_rate = (
            int((completed_today / active_habits) * 100) 
            if active_habits > 0 else 0
        )
        
        # Calculate longest streak
        longest_streak = max([h.get("streak", 0) for h in habits], default=0)
        
        # Stats grid
        stats_grid = tk.Frame(overview_frame, bg=self.theme.bg_color)
        stats_grid.pack(fill=tk.X, padx=10, pady=10)
        
        # Total habits
        stat_frame = tk.Frame(stats_grid, bg=self.theme.bg_color, padx=10, pady=10)
        stat_frame.grid(row=0, column=0, padx=10, pady=10)
        
        tk.Label(
            stat_frame,
            text="📋 Total Habits",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack()
        
        tk.Label(
            stat_frame,
            text=str(total_habits),
            font=self.theme.heading_font,
            bg=self.theme.bg_color,
            fg=self.theme.habit_color,  # Use the theme's habit color
        ).pack()
        
        # Active habits
        stat_frame = tk.Frame(stats_grid, bg=self.theme.bg_color, padx=10, pady=10)
        stat_frame.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(
            stat_frame,
            text="✅ Active Habits",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack()
        
        tk.Label(
            stat_frame,
            text=str(active_habits),
            font=self.theme.heading_font,
            bg=self.theme.bg_color,
            fg="#4CAF50",  # Green
        ).pack()
        
        # Today's completion
        stat_frame = tk.Frame(stats_grid, bg=self.theme.bg_color, padx=10, pady=10)
        stat_frame.grid(row=0, column=2, padx=10, pady=10)
        
        tk.Label(
            stat_frame,
            text="🔄 Today's Completion",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack()
        
        tk.Label(
            stat_frame,
            text=f"{completion_rate}%",
            font=self.theme.heading_font,
            bg=self.theme.bg_color,
            fg="#2196F3",  # Blue
        ).pack()
        
        # Longest streak
        stat_frame = tk.Frame(stats_grid, bg=self.theme.bg_color, padx=10, pady=10)
        stat_frame.grid(row=0, column=3, padx=10, pady=10)
        
        tk.Label(
            stat_frame,
            text="🔥 Longest Streak",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack()
        
        tk.Label(
            stat_frame,
            text=f"{longest_streak} days",
            font=self.theme.heading_font,
            bg=self.theme.bg_color,
            fg="#FF5722",  # Orange
        ).pack()
        
        # Category breakdown
        category_frame = tk.LabelFrame(
            parent,
            text="Habits by Category",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.habit_color,  # Use the theme's habit color
        )
        category_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Get categories and counts
        categories = self.data["habits"].get("categories", [])
        category_counts = {}
        category_completion = {}
        
        for habit in habits:
            if not habit.get("active", True):
                continue
                
            category = habit.get("category", "Personal")
            
            # Initialize counter if needed
            if category not in category_counts:
                category_counts[category] = 0
                category_completion[category] = 0
                
            # Increment count
            category_counts[category] += 1
            
            # Check if completed today
            if today in habit.get("completed_dates", []):
                category_completion[category] += 1
        
        # Display categories
        category_grid = tk.Frame(category_frame, bg=self.theme.bg_color)
        category_grid.pack(fill=tk.X, padx=10, pady=10)
        
        # If no categories, show message
        if not categories:
            tk.Label(
                category_grid,
                text="No categories defined yet. Go to the Categories tab to add some!",
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
            ).pack(pady=10)
        else:
            # Get category colors
            category_colors = {}
            for category in categories:
                category_colors[category["name"]] = category["color"]
            
            # Show categories in a grid
            for i, category in enumerate(categories):
                name = category["name"]
                count = category_counts.get(name, 0)
                
                if count == 0:
                    continue  # Skip categories with no active habits
                    
                # Calculate completion rate
                completed = category_completion.get(name, 0)
                completion_rate = int((completed / count) * 100) if count > 0 else 0
                
                # Category card
                card_frame = tk.Frame(
                    category_grid,
                    bg=self.theme.bg_color,
                    relief=tk.RIDGE,
                    bd=1,
                    padx=10,
                    pady=10,
                )
                card_frame.grid(
                    row=i//2,
                    column=i%2,
                    padx=10,
                    pady=10,
                    sticky="news",
                )
                
                # Color indicator and name
                header_frame = tk.Frame(card_frame, bg=self.theme.bg_color)
                header_frame.pack(fill=tk.X)
                
                color_indicator = tk.Frame(
                    header_frame,
                    bg=category_colors.get(name, self.theme.habit_color),
                    width=15,
                    height=15,
                )
                color_indicator.pack(side=tk.LEFT, padx=5)
                
                name_label = tk.Label(
                    header_frame,
                    text=name,
                    font=self.theme.small_font,
                    bg=self.theme.bg_color,
                    fg=self.theme.text_color,
                )
                name_label.pack(side=tk.LEFT, padx=5)
                
                # Count
                tk.Label(
                    card_frame,
                    text=f"Habits: {count}",
                    font=self.theme.small_font,
                    bg=self.theme.bg_color,
                    fg=self.theme.text_color,
                ).pack(anchor="w")
                
                # Completion
                completion_color = "#4CAF50" if completion_rate >= 80 else "#FFC107" if completion_rate >= 50 else "#F44336"
                
                tk.Label(
                    card_frame,
                    text=f"Today: {completed}/{count} ({completion_rate}%)",
                    font=self.theme.small_font,
                    bg=self.theme.bg_color,
                    fg=completion_color,
                ).pack(anchor="w")
        
        # Habit performance chart
        performance_frame = tk.LabelFrame(
            parent,
            text="Habit Performance",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.habit_color,  # Use the theme's habit color
        )
        performance_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # If no habits, show a message
        if not habits:
            tk.Label(
                performance_frame,
                text="No habits added yet. Add some habits to see statistics!",
                font=self.theme.pixel_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
                pady=30,
            ).pack()
            return
        
        # Create a canvas for the habit performance bars
        performance_canvas = tk.Canvas(
            performance_frame,
            bg=self.theme.bg_color,
            highlightthickness=0,
        )
        scrollbar = ttk.Scrollbar(
            performance_frame,
            orient="vertical",
            command=performance_canvas.yview,
        )
        scrollable_frame = tk.Frame(performance_canvas, bg=self.theme.bg_color)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: performance_canvas.configure(scrollregion=performance_canvas.bbox("all"))
        )
        
        performance_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        performance_canvas.configure(yscrollcommand=scrollbar.set)
        
        performance_canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y")
        
        # Get category colors
        category_colors = {}
        for category in self.data["habits"].get("categories", []):
            category_colors[category["name"]] = category["color"]
        
        # Display habit performance bars
        for i, habit in enumerate(habits):
            if not habit.get("active", True):
                continue
                
            # Calculate completion rate for the last 30 days
            today = datetime.now().date()
            dates_to_check = [
                (today - timedelta(days=i)).strftime("%Y-%m-%d")
                for i in range(30)
            ]
            
            completed_dates = habit.get("completed_dates", [])
            recent_completed = [d for d in dates_to_check if d in completed_dates]
            completion_rate = (len(recent_completed) / len(dates_to_check)) * 100
            
            # Get category and color
            category = habit.get("category", "Personal")
            category_color = category_colors.get(category, self.theme.habit_color)
            
            # Create a row for this habit
            row_bg = self.theme.bg_color if i % 2 == 0 else self.theme.darken_color(self.theme.bg_color)
            row_frame = tk.Frame(scrollable_frame, bg=row_bg, padx=5, pady=8)
            row_frame.pack(fill=tk.X)
            
            # Habit name and icon
            name_frame = tk.Frame(row_frame, bg=row_bg, width=150)
            name_frame.pack(side=tk.LEFT, padx=5)
            
            # Category color indicator
            category_indicator = tk.Frame(
                name_frame,
                bg=category_color,
                width=5,
                height=20
            )
            category_indicator.pack(side=tk.LEFT, padx=2)
            
            tk.Label(
                name_frame,
                text=f"{habit.get('icon', '📋')} {habit['name']}",
                font=self.theme.small_font,
                bg=row_bg,
                fg=self.theme.text_color,
                anchor="w",
                width=20,
            ).pack(side=tk.LEFT)
            
            # Progress bar
            bar_frame = tk.Frame(row_frame, bg=row_bg)
            bar_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
            
            bar_bg = tk.Frame(
                bar_frame,
                bg=self.theme.darken_color(self.theme.primary_color),
                height=20,
                width=300,
            )
            bar_bg.pack(fill=tk.X)
            
            # Calculate progress bar width
            bar_width = int((completion_rate / 100) * 300)
            
            # Determine color based on completion rate
            if completion_rate >= 80:
                bar_color = "#4CAF50"  # Green for high completion
            elif completion_rate >= 50:
                bar_color = "#FFC107"  # Yellow for medium completion
            else:
                bar_color = "#F44336"  # Red for low completion
            
            bar = tk.Frame(
                bar_bg,
                bg=bar_color,
                height=20,
                width=bar_width,
            )
            bar.place(x=0, y=0)
            
            # Percentage label
            tk.Label(
                row_frame,
                text=f"{int(completion_rate)}%",
                font=self.theme.small_font,
                bg=row_bg,
                fg=self.theme.text_color,
                width=5,
            ).pack(side=tk.LEFT, padx=5)
    
    def toggle_habit(self, habit_name, date_str):
        """
        Toggle a habit's completion status for a specific date.
        
        Args:
            habit_name: Name of the habit to toggle
            date_str: Date string in YYYY-MM-DD format
        """
        # Find the habit
        habit = None
        habit_list = None
        habit_index = -1
        
        # Check in daily habits
        for i, h in enumerate(self.data.get("habits", {}).get("daily_habits", [])):
            if h["name"] == habit_name:
                habit = h
                habit_list = "daily_habits"
                habit_index = i
                break
        
        # If not found in daily habits, check custom habits
        if habit is None:
            for i, h in enumerate(self.data.get("habits", {}).get("custom_habits", [])):
                if h["name"] == habit_name:
                    habit = h
                    habit_list = "custom_habits"
                    habit_index = i
                    break
        
        if habit is None:
            messagebox.showerror("Error", f"Habit '{habit_name}' not found.")
            return
        
        # Get completed dates list
        completed_dates = habit.get("completed_dates", [])
        
        # Toggle the date
        if date_str in completed_dates:
            # Remove date if already completed
            completed_dates.remove(date_str)
        else:
            # Add date if not completed
            completed_dates.append(date_str)
        
        # Update the habit
        self.data["habits"][habit_list][habit_index]["completed_dates"] = completed_dates
        
        # Update the streak
        self.update_habit_streak(habit_list, habit_index)
        
        # Save data
        self.data_manager.save_data()
        
        # Refresh the display
        self.refresh_display()
    
    def update_habit_streak(self, habit_list, habit_index):
        """
        Update a habit's streak based on completion history.
        
        Args:
            habit_list: Which list the habit belongs to (daily_habits or custom_habits)
            habit_index: Index of the habit in the list
        """
        habit = self.data["habits"][habit_list][habit_index]
        completed_dates = habit.get("completed_dates", [])
        
        # Sort dates
        date_objects = [datetime.strptime(d, "%Y-%m-%d").date() for d in completed_dates]
        date_objects.sort(reverse=True)
        
        # Calculate streak
        streak = 0
        today = datetime.now().date()
        
        # If today is completed, start streak from today
        if today in date_objects:
            streak = 1
            check_date = today - timedelta(days=1)
        else:
            # If today is not completed, start from yesterday
            check_date = today - timedelta(days=1)
            if check_date in date_objects:
                streak = 1
            else:
                # No recent completions
                self.data["habits"][habit_list][habit_index]["streak"] = 0
                return
        
        # Check consecutive days
        while True:
            if check_date in date_objects:
                streak += 1
                check_date -= timedelta(days=1)
            else:
                break
        
        # Update streak
        self.data["habits"][habit_list][habit_index]["streak"] = streak
    
    def refresh_display(self):
        """Refresh the habit tracker display."""
        # Get the current notebook tab
        current_tab = self.app.main_frame.winfo_children()[-2].index("current")
        
        # Clear the main frame
        self.app.clear_frame()
        
        # Recreate the habit tracker
        self.show_module(self.app.main_frame)
        
        # Set the active tab back to what it was
        self.app.main_frame.winfo_children()[-2].select(current_tab)
    
    def add_new_habit(self):
        """Open a dialog to add a new custom habit."""
        # Create a dialog window
        dialog = tk.Toplevel()
        dialog.title("Add New Habit")
        dialog.geometry("400x350")  # Increased height for category dropdown
        dialog.configure(bg=self.theme.bg_color)
        dialog.transient(self.app.root)
        dialog.grab_set()
        
        # Name input
        name_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        name_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            name_frame,
            text="Habit Name:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT)
        
        name_var = tk.StringVar()
        name_entry = tk.Entry(
            name_frame,
            textvariable=name_var,
            font=self.theme.small_font,
            bg=self.theme.primary_color,
            fg=self.theme.text_color,
            width=30,
        )
        name_entry.pack(side=tk.LEFT, padx=10)
        
        # Icon selection
        icon_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        icon_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            icon_frame,
            text="Icon:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT)
        
        icon_var = tk.StringVar(value="📋")
        icons = ["📋", "🏃", "📚", "💪", "🎨", "🎵", "💻", "🧘", "🥗", "💤", "💧", "🧠"]
        
        icon_dropdown = ttk.Combobox(
            icon_frame,
            textvariable=icon_var,
            values=icons,
            font=self.theme.small_font,
            width=5,
        )
        icon_dropdown.pack(side=tk.LEFT, padx=10)
        
        # Category selection
        category_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        category_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            category_frame,
            text="Category:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT)
        
        # Get categories
        categories = [c["name"] for c in self.data["habits"].get("categories", [])]
        if not categories:
            categories = ["Personal"]  # Default if no categories
            
        category_var = tk.StringVar(value=categories[0] if categories else "Personal")
        
        category_dropdown = ttk.Combobox(
            category_frame,
            textvariable=category_var,
            values=categories,
            font=self.theme.small_font,
            width=15,
        )
        category_dropdown.pack(side=tk.LEFT, padx=10)
        
        # Frequency selection (for future use)
        freq_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        freq_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            freq_frame,
            text="Frequency:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT)
        
        freq_var = tk.StringVar(value="daily")
        frequencies = ["daily", "weekly"]
        
        freq_dropdown = ttk.Combobox(
            freq_frame,
            textvariable=freq_var,
            values=frequencies,
            font=self.theme.small_font,
            width=10,
        )
        freq_dropdown.pack(side=tk.LEFT, padx=10)
        
        # Button frame
        button_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        button_frame.pack(pady=20)
        
        # Cancel button
        cancel_button = self.theme.create_pixel_button(
            button_frame,
            "Cancel",
            dialog.destroy,
            color="#F44336",
        )
        cancel_button.pack(side=tk.LEFT, padx=10)
        
        # Add button
        add_button = self.theme.create_pixel_button(
            button_frame,
            "Add Habit",
            lambda: self.save_new_habit(
                name_var.get(),
                icon_var.get(),
                category_var.get(),
                freq_var.get(),
                dialog,
            ),
            color=self.theme.habit_color,  # Use the theme's habit color
        )
        add_button.pack(side=tk.LEFT, padx=10)
        
        # Focus the name entry
        name_entry.focus_set()
    
    def save_new_habit(self, name, icon, category, frequency, dialog):
        """
        Save a new custom habit to the data.
        
        Args:
            name: Habit name
            icon: Habit icon
            category: Habit category
            frequency: Habit frequency
            dialog: Dialog window to close after saving
        """
        # Validate input
        if not name:
            messagebox.showerror("Error", "Please enter a habit name.")
            return
        
        # Initialize habits if not exist
        if "habits" not in self.data:
            self.data["habits"] = {
                "daily_habits": [],
                "custom_habits": [],
                "check_ins": []
            }
        
        # Check if habit name already exists
        all_habits = (
            self.data["habits"].get("daily_habits", []) +
            self.data["habits"].get("custom_habits", [])
        )
        
        for habit in all_habits:
            if habit["name"] == name:
                messagebox.showerror("Error", f"A habit named '{name}' already exists.")
                return
        
        # Create new habit
        new_habit = {
            "name": name,
            "icon": icon,
            "category": category,  # Add category
            "frequency": frequency,
            "active": True,
            "streak": 0,
            "completed_dates": []
        }
        
        # Add to custom habits
        self.data["habits"]["custom_habits"].append(new_habit)
        
        # Save data
        self.data_manager.save_data()
        
        # Close dialog
        dialog.destroy()
        
        # Refresh display
        self.refresh_display()
        
        # Show confirmation
        messagebox.showinfo("Success", f"Habit '{name}' has been added!")
    
    def prev_month(self):
        """Move to the previous month in the calendar."""
        if self.selected_month == 1:
            self.selected_month = 12
            self.selected_year -= 1
        else:
            self.selected_month -= 1
            
        self.update_calendar_view()
    
    def next_month(self):
        """Move to the next month in the calendar."""
        if self.selected_month == 12:
            self.selected_month = 1
            self.selected_year += 1
        else:
            self.selected_month += 1
            
        self.update_calendar_view()
    
    def update_calendar_view(self):
        """Update the calendar view with the selected month."""
        # Update month label
        self.month_label.config(text=f"{calendar.month_name[self.selected_month]} {self.selected_year}")
        
        # Clear calendar grid
        for widget in self.month_frame.winfo_children():
            widget.destroy()
            
        # Display the month
        self.display_month()
        
        # Update check-ins list
        self.display_check_ins()
    
    def display_month(self):
        """Display the selected month in the calendar grid."""
        # Get calendar for selected month
        cal = calendar.monthcalendar(self.selected_year, self.selected_month)
        
        # Today's date for highlighting
        today = datetime.now().date()
        
        # Get all check-in dates
        check_in_dates = []
        for check_in in self.data.get("habits", {}).get("check_ins", []):
            for date_str in check_in.get("dates", []):
                date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
                check_in_dates.append(date_str)
        
        # Display calendar
        for week_idx, week in enumerate(cal):
            for day_idx, day in enumerate(week):
                if day == 0:
                    # Empty cell for days not in this month
                    frame = tk.Frame(self.month_frame, bg=self.theme.bg_color, width=80, height=80)
                    frame.grid(row=week_idx, column=day_idx, padx=2, pady=2)
                    frame.grid_propagate(False)
                else:
                    # Create frame for this day
                    date_obj = datetime.date(self.selected_year, self.selected_month, day)
                    date_str = date_obj.strftime("%Y-%m-%d")
                    
                    # Check if this is today
                    is_today = (date_obj == today)
                    
                    # Check if there are check-ins on this day
                    has_check_in = date_str in check_in_dates
                    
                    # Set frame color based on conditions
                    if is_today:
                        bg_color = "#FFF9C4"  # Light yellow for today
                    elif has_check_in:
                        bg_color = "#E3F2FD"  # Light blue for check-in days
                    else:
                        bg_color = self.theme.bg_color
                    
                    frame = tk.Frame(
                        self.month_frame,
                        bg=bg_color,
                        width=80,
                        height=80,
                        relief=tk.RIDGE if is_today else tk.FLAT,
                        bd=2 if is_today else 0,
                    )
                    frame.grid(row=week_idx, column=day_idx, padx=2, pady=2)
                    frame.grid_propagate(False)
                    
                    # Day number
                    day_label = tk.Label(
                        frame,
                        text=str(day),
                        font=self.theme.small_font,
                        bg=bg_color,
                        fg="#FF5722" if is_today else self.theme.text_color,
                    )
                    day_label.pack(anchor="nw", padx=5, pady=2)
                    
                    # If there are check-ins on this day, show indicators
                    if has_check_in:
                        # Find all check-ins for this day
                        day_check_ins = []
                        for check_in in self.data.get("habits", {}).get("check_ins", []):
                            if date_str in check_in.get("dates", []):
                                day_check_ins.append(check_in)
                        
                        # Show up to 3 check-in icons with tooltips
                        for i, check_in in enumerate(day_check_ins[:3]):
                            icon_label = tk.Label(
                                frame,
                                text=check_in.get("icon", "🩺"),
                                font=("TkDefaultFont", 9),
                                bg=bg_color,
                                fg=self.theme.text_color,
                            )
                            icon_label.pack(anchor="w", padx=5, pady=0)
                            
                            # Add binding for click to show details
                            icon_label.bind(
                                "<Button-1>",
                                lambda e, d=date_str: self.show_check_in_details(d)
                            )
                        
                        # If more than 3, show a "more" indicator
                        if len(day_check_ins) > 3:
                            more_label = tk.Label(
                                frame,
                                text=f"+{len(day_check_ins) - 3} more",
                                font=("TkDefaultFont", 7),
                                bg=bg_color,
                                fg="#2196F3",
                            )
                            more_label.pack(anchor="w", padx=5, pady=0)
                            
                            # Add binding for click to show details
                            more_label.bind(
                                "<Button-1>",
                                lambda e, d=date_str: self.show_check_in_details(d)
                            )
                    
                    # Make the entire day clickable to add check-in
                    frame.bind(
                        "<Button-1>",
                        lambda e, d=date_str: self.show_check_in_details(d)
                    )
                    day_label.bind(
                        "<Button-1>",
                        lambda e, d=date_str: self.show_check_in_details(d)
                    )
    
    def show_check_in_details(self, date_str):
        """
        Show details for check-ins on a specific date.
        
        Args:
            date_str: Date string in YYYY-MM-DD format
        """
        # Clear the events list frame
        for widget in self.events_list_frame.winfo_children():
            widget.destroy()
        
        # Format date for display
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            formatted_date = date_obj.strftime("%A, %B %d, %Y")
        except:
            formatted_date = date_str
        
        # Title with date
        title_frame = tk.Frame(self.events_list_frame, bg=self.theme.bg_color)
        title_frame.pack(fill=tk.X, pady=5)
        
        date_label = tk.Label(
            title_frame,
            text=formatted_date,
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        )
        date_label.pack(side=tk.LEFT)
        
        # Add check-in button
        add_button = self.theme.create_pixel_button(
            title_frame,
            "Add Check-in",
            lambda: self.add_check_in_for_date(date_str),
            color=self.theme.habit_color,  # Use the theme's habit color
        )
        add_button.pack(side=tk.RIGHT)
        
        # Find check-ins for this date
        day_check_ins = []
        for check_in in self.data.get("habits", {}).get("check_ins", []):
            if date_str in check_in.get("dates", []):
                day_check_ins.append({
                    "name": check_in["name"],
                    "category": check_in.get("category", "Health"),  # Get category
                    "icon": check_in.get("icon", "🩺"),
                    "notes": check_in.get("notes", {}).get(date_str, "")
                })
        
        # If no check-ins, show a message
        if not day_check_ins:
            tk.Label(
                self.events_list_frame,
                text="No check-ins recorded for this date.",
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
                pady=10,
            ).pack()
            return
        
        # Get category colors
        category_colors = {}
        for category in self.data["habits"].get("categories", []):
            category_colors[category["name"]] = category["color"]
        
        # Display check-ins
        for check_in in day_check_ins:
            check_in_frame = tk.Frame(
                self.events_list_frame,
                bg=self.theme.bg_color,
                relief=tk.RIDGE,
                bd=1,
                padx=10,
                pady=5,
            )
            check_in_frame.pack(fill=tk.X, pady=5)
            
            # Header with icon and name
            header_frame = tk.Frame(check_in_frame, bg=self.theme.bg_color)
            header_frame.pack(fill=tk.X)
            
            # Category color indicator
            category = check_in.get("category", "Health")
            category_color = category_colors.get(category, self.theme.habit_color)
            
            color_indicator = tk.Frame(
                header_frame,
                bg=category_color,
                width=5,
                height=20
            )
            color_indicator.pack(side=tk.LEFT, padx=2)
            
            icon_label = tk.Label(
                header_frame,
                text=check_in["icon"],
                font=self.theme.pixel_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
            )
            icon_label.pack(side=tk.LEFT)
            
            name_label = tk.Label(
                header_frame,
                text=check_in["name"],
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=self.theme.text_color,
            )
            name_label.pack(side=tk.LEFT, padx=5)
            
            # Category label on the right
            category_label = tk.Label(
                header_frame,
                text=category,
                font=self.theme.small_font,
                bg=self.theme.bg_color,
                fg=category_color,
            )
            category_label.pack(side=tk.RIGHT, padx=5)
            
            # Notes if any
            if check_in["notes"]:
                notes_frame = tk.Frame(check_in_frame, bg=self.theme.bg_color, pady=5)
                notes_frame.pack(fill=tk.X)
                
                notes_text = tk.Text(
                    notes_frame,
                    height=3,
                    width=40,
                    font=self.theme.small_font,
                    bg=self.theme.primary_color,
                    fg=self.theme.text_color,
                    wrap=tk.WORD,
                )
                notes_text.insert(tk.END, check_in["notes"])
                notes_text.config(state=tk.DISABLED)
                notes_text.pack(fill=tk.X, padx=5)
    
    def add_check_in_for_date(self, date_str):
        """
        Add a check-in for a specific date.
        
        Args:
            date_str: Date string in YYYY-MM-DD format
        """
        # Format date for display
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            formatted_date = date_obj.strftime("%B %d, %Y")
        except:
            formatted_date = date_str
        
        # Create a dialog window
        dialog = tk.Toplevel()
        dialog.title(f"Add Check-in for {formatted_date}")
        dialog.geometry("400x400")  # Increased height for category dropdown
        dialog.configure(bg=self.theme.bg_color)
        dialog.transient(self.app.root)
        dialog.grab_set()
        
        # Check-in type selection
        type_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        type_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            type_frame,
            text="Check-in Type:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT)
        
        # Get existing check-in types
        check_in_types = []
        for check_in in self.data.get("habits", {}).get("check_ins", []):
            check_in_types.append(check_in["name"])
        
        if not check_in_types:
            # Default check-in types if none exist
            check_in_types = ["Doctor Appointment", "Dentist", "New check-in..."]
        elif "New check-in..." not in check_in_types:
            check_in_types.append("New check-in...")
        
        type_var = tk.StringVar(value=check_in_types[0])
        
        type_dropdown = ttk.Combobox(
            type_frame,
            textvariable=type_var,
            values=check_in_types,
            font=self.theme.small_font,
            width=20,
        )
        type_dropdown.pack(side=tk.LEFT, padx=10)
        
        # When "New check-in..." is selected, show a field to enter new type
        new_type_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        new_type_frame.pack(fill=tk.X, padx=20, pady=5)
        new_type_frame.pack_forget()  # Hide initially
        
        new_type_label = tk.Label(
            new_type_frame,
            text="New Type Name:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        )
        new_type_label.pack(side=tk.LEFT)
        
        new_type_var = tk.StringVar()
        new_type_entry = tk.Entry(
            new_type_frame,
            textvariable=new_type_var,
            font=self.theme.small_font,
            bg=self.theme.primary_color,
            fg=self.theme.text_color,
            width=20,
        )
        new_type_entry.pack(side=tk.LEFT, padx=10)
        
        # Category selection
        category_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        category_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            category_frame,
            text="Category:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT)
        
        # Get categories
        categories = [c["name"] for c in self.data["habits"].get("categories", [])]
        if not categories:
            categories = ["Health"]  # Default if no categories
            
        category_var = tk.StringVar(value=categories[0] if categories else "Health")
        
        category_dropdown = ttk.Combobox(
            category_frame,
            textvariable=category_var,
            values=categories,
            font=self.theme.small_font,
            width=15,
        )
        category_dropdown.pack(side=tk.LEFT, padx=10)
        
        # Icon selection
        icon_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        icon_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            icon_frame,
            text="Icon:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT)
        
        icon_var = tk.StringVar(value="🩺")
        icons = ["🩺", "🦷", "💉", "🧠", "👁️", "🫀", "💊", "🔬", "🧪", "📋"]
        
        icon_dropdown = ttk.Combobox(
            icon_frame,
            textvariable=icon_var,
            values=icons,
            font=self.theme.small_font,
            width=5,
        )
        icon_dropdown.pack(side=tk.LEFT, padx=10)
        
        # Notes
        notes_frame = tk.LabelFrame(
            dialog,
            text="Notes",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        )
        notes_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        notes_text = tk.Text(
            notes_frame,
            height=6,
            width=40,
            font=self.theme.small_font,
            bg=self.theme.primary_color,
            fg=self.theme.text_color,
            wrap=tk.WORD,
        )
        notes_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Button frame
        button_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        button_frame.pack(pady=20)
        
        # Cancel button
        cancel_button = self.theme.create_pixel_button(
            button_frame,
            "Cancel",
            dialog.destroy,
            color="#F44336",
        )
        cancel_button.pack(side=tk.LEFT, padx=10)
        
        # Add button
        add_button = self.theme.create_pixel_button(
            button_frame,
            "Save Check-in",
            lambda: self.save_check_in(
                type_var.get() if type_var.get() != "New check-in..." else new_type_var.get(),
                category_var.get(),
                icon_var.get(),
                date_str,
                notes_text.get("1.0", tk.END).strip(),
                dialog,
            ),
            color=self.theme.habit_color,  # Use the theme's habit color
        )
        add_button.pack(side=tk.LEFT, padx=10)
        
        # Function to show/hide new type field based on dropdown selection
        def on_type_change(*args):
            if type_var.get() == "New check-in...":
                new_type_frame.pack(fill=tk.X, padx=20, pady=5)
                new_type_entry.focus_set()
            else:
                new_type_frame.pack_forget()
        
        # Bind dropdown change
        type_var.trace_add("write", on_type_change)
    
    def save_check_in(self, check_in_type, category, icon, date_str, notes, dialog):
        """
        Save a check-in to the data.
        
        Args:
            check_in_type: Type of check-in
            category: Category of check-in
            icon: Icon for the check-in
            date_str: Date string in YYYY-MM-DD format
            notes: Notes for the check-in
            dialog: Dialog window to close after saving
        """
        # Validate input
        if not check_in_type:
            messagebox.showerror("Error", "Please enter a check-in type.")
            return
        
        # Initialize habits if not exist
        if "habits" not in self.data:
            self.data["habits"] = {
                "daily_habits": [],
                "custom_habits": [],
                "check_ins": []
            }
        
        # Find or create check-in type
        check_in = None
        for c in self.data["habits"]["check_ins"]:
            if c["name"] == check_in_type:
                check_in = c
                break
        
        if check_in is None:
            # Create new check-in type
            check_in = {
                "name": check_in_type,
                "category": category,  # Add category
                "icon": icon,
                "dates": [],
                "notes": {}
            }
            self.data["habits"]["check_ins"].append(check_in)
        else:
            # Update category and icon if it already exists
            check_in["category"] = category
            check_in["icon"] = icon
        
        # Add date if not already there
        if date_str not in check_in["dates"]:
            check_in["dates"].append(date_str)
        
        # Add notes if any
        if notes:
            if "notes" not in check_in:
                check_in["notes"] = {}
            check_in["notes"][date_str] = notes
        
        # Save data
        self.data_manager.save_data()
        
        # Close dialog
        dialog.destroy()
        
        # Refresh display
        self.refresh_display()
        
        # Show confirmation
        messagebox.showinfo("Success", f"Check-in recorded for {date_str}!")
    
    def add_new_check_in(self):
        """Open a dialog to add a new check-in type."""
        self.add_check_in_for_date(datetime.now().date().strftime("%Y-%m-%d"))
    
    def display_check_ins(self):
        """Display check-ins for the current month."""
        pass
        
    # Quick action methods for the main GUI
    def quick_toggle_today(self, habit_name):
        """
        Quick toggle a habit for today from the main screen.
        
        Args:
            habit_name: Name of the habit to toggle
        """
        today = datetime.now().date().strftime("%Y-%m-%d")
        self.toggle_habit(habit_name, today)
