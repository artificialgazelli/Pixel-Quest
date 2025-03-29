"""
Categories tab module for the Pixel Quest habit tracker.
Manages habit categories including creation, editing, and deletion.
"""

import tkinter as tk
from tkinter import ttk, messagebox


class CategoriesTab:
    """
    Manages the categories tab of the habit tracker.
    Allows users to create, edit, and delete habit categories.
    """

    def __init__(self, habit_tracker, app, data_manager, theme):
        """
        Initialize the categories tab module.

        Args:
            habit_tracker: Main habit tracker instance
            app: Main application instance
            data_manager: Data manager instance
            theme: Theme manager instance
        """
        self.habit_tracker = habit_tracker
        self.app = app
        self.data_manager = data_manager
        self.data = data_manager.data
        self.theme = theme

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
        canvas = tk.Canvas(
            categories_frame, bg=self.theme.bg_color, highlightthickness=0
        )
        scrollbar = ttk.Scrollbar(
            categories_frame, orient="vertical", command=canvas.yview
        )
        scrollable_frame = tk.Frame(canvas, bg=self.theme.bg_color)

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y")

        # Display each category
        for i, category in enumerate(categories):
            # Row background alternates for better readability
            row_bg = (
                self.theme.bg_color
                if i % 2 == 0
                else self.theme.darken_color(self.theme.bg_color)
            )

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
                bg="#F44336"
                if habits_count == 0
                else self.theme.darken_color(self.theme.bg_color),
                fg="white" if habits_count == 0 else self.theme.text_color,
                command=lambda c=category: self.delete_category(c)
                if habits_count == 0
                else messagebox.showinfo(
                    "Cannot Delete",
                    f"Can't delete category with {habits_count} habits assigned to it.",
                ),
                relief=tk.FLAT,
                state=tk.NORMAL if habits_count == 0 else tk.DISABLED,
            )
            delete_button.pack(side=tk.LEFT, padx=5)

    def add_new_category(self):
        """Open a dialog to add a new category."""
        # Create a dialog window
        dialog = tk.Toplevel(self.app.root)
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

        color_var = tk.StringVar(value="#4CAF50")  # Default green
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

        # Color presets
        color_presets_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        color_presets_frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(
            color_presets_frame,
            text="Color Presets:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT)
        
        # Common colors for quick selection
        preset_colors = [
            "#4CAF50",  # Green
            "#2196F3",  # Blue
            "#F44336",  # Red
            "#FF9800",  # Orange
            "#9C27B0",  # Purple
            "#E91E63",  # Pink
        ]
        
        for color in preset_colors:
            preset_button = tk.Frame(
                color_presets_frame,
                bg=color,
                width=20,
                height=20,
                cursor="hand2",
            )
            preset_button.pack(side=tk.LEFT, padx=5)
            
            # Bind click to set the color
            preset_button.bind(
                "<Button-1>",
                lambda e, c=color: color_var.set(c)
            )

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
            color=self.theme.habit_color,
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
            self.app.root.winfo_rgb(color)
        except:
            messagebox.showerror(
                "Error", "Invalid color format. Please use a valid hex code (#RRGGBB)."
            )
            return

        # Check if category name already exists
        for category in self.data["habits"].get("categories", []):
            if category["name"] == name:
                messagebox.showerror(
                    "Error", f"A category named '{name}' already exists."
                )
                return

        # Create new category
        new_category = {"name": name, "color": color}

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
        self.habit_tracker.refresh_display()

        # Show confirmation
        messagebox.showinfo("Success", f"Category '{name}' has been added!")

    def edit_category(self, category):
        """
        Open a dialog to edit an existing category.

        Args:
            category: Category to edit
        """
        # Create a dialog window
        dialog = tk.Toplevel(self.app.root)
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
        
        # Color presets
        color_presets_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        color_presets_frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(
            color_presets_frame,
            text="Color Presets:",
            font=self.theme.small_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(side=tk.LEFT)
        
        # Common colors for quick selection
        preset_colors = [
            "#4CAF50",  # Green
            "#2196F3",  # Blue
            "#F44336",  # Red
            "#FF9800",  # Orange
            "#9C27B0",  # Purple
            "#E91E63",  # Pink
        ]
        
        for color in preset_colors:
            preset_button = tk.Frame(
                color_presets_frame,
                bg=color,
                width=20,
                height=20,
                cursor="hand2",
            )
            preset_button.pack(side=tk.LEFT, padx=5)
            
            # Bind click to set the color
            preset_button.bind(
                "<Button-1>",
                lambda e, c=color: color_var.set(c)
            )

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
            color=self.theme.habit_color,
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
            self.app.root.winfo_rgb(new_color)
        except:
            messagebox.showerror(
                "Error", "Invalid color format. Please use a valid hex code (#RRGGBB)."
            )
            return

        # Check if category name already exists (unless it's the same name)
        if new_name != category["name"]:
            for cat in self.data["habits"].get("categories", []):
                if cat["name"] == new_name:
                    messagebox.showerror(
                        "Error", f"A category named '{new_name}' already exists."
                    )
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
        self.habit_tracker.refresh_display()

        # Show confirmation
        messagebox.showinfo("Success", f"Category '{new_name}' has been updated!")

    def delete_category(self, category):
        """
        Delete a category.

        Args:
            category: Category to delete
        """
        # Confirm deletion
        if not messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete the category '{category['name']}'?",
        ):
            return

        # Count habits in this category
        habits_count = 0
        for habit_type in ["daily_habits", "custom_habits"]:
            for habit in self.data["habits"].get(habit_type, []):
                if habit.get("category") == category["name"]:
                    habits_count += 1

        # Don't delete if habits are assigned
        if habits_count > 0:
            messagebox.showinfo(
                "Cannot Delete",
                f"Cannot delete category with {habits_count} habits assigned to it.",
            )
            return

        # Find the category and delete it
        for i, cat in enumerate(self.data["habits"].get("categories", [])):
            if cat["name"] == category["name"]:
                del self.data["habits"]["categories"][i]
                break

        # Save data
        self.data_manager.save_data()

        # Refresh display
        self.habit_tracker.refresh_display()

        # Show confirmation
        messagebox.showinfo(
            "Success", f"Category '{category['name']}' has been deleted!"
        )