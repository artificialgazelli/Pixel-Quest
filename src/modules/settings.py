"""
Settings module for the Pixel Quest application.
Handles application settings and data management.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class SettingsModule:
    """
    Manages the settings functionality.
    """
    
    def __init__(self, app, data_manager, theme):
        """
        Initialize the settings module.
        
        Args:
            app: Main application instance
            data_manager: Data manager instance
            theme: Theme manager instance
        """
        self.app = app
        self.data_manager = data_manager
        self.data = data_manager.data
        self.theme = theme
        
    def create_settings_tab(self, parent):
        """
        Create the settings tab content with pixel art styling.
        
        Args:
            parent: Parent widget to place the settings tab
        """
        # Title
        tk.Label(
            parent,
            text="Settings",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
        ).pack(pady=10)

        # Application settings
        app_frame = tk.LabelFrame(
            parent,
            text="Application Settings",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            padx=10,
            pady=10,
            relief=tk.RIDGE,
            bd=3,
        )
        app_frame.pack(fill=tk.X, padx=10, pady=10)

        # Auto-save option (placeholder for future)
        autosave_var = tk.BooleanVar(value=True)
        check_frame = tk.Frame(app_frame, bg=self.theme.bg_color)
        check_frame.pack(anchor="w", pady=5)

        # Create a custom checkbox appearance
        autosave_check = tk.Checkbutton(
            check_frame,
            text="Auto-save progress",
            variable=autosave_var,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
            selectcolor=self.theme.secondary_color,
            relief=tk.FLAT,
        )
        autosave_check.pack(anchor="w")

        # Data management
        data_frame = tk.LabelFrame(
            parent,
            text="Data Management",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            padx=10,
            pady=10,
            relief=tk.RIDGE,
            bd=3,
        )
        data_frame.pack(fill=tk.X, padx=10, pady=10)

        # Backup and restore options
        backup_button = self.theme.create_pixel_button(
            data_frame, "Backup Data", self.backup_data, color="#607D8B"
        )
        backup_button.pack(pady=5)

        restore_button = self.theme.create_pixel_button(
            data_frame, "Restore from Backup", self.restore_data, color="#607D8B"
        )
        restore_button.pack(pady=5)

        reset_button = self.theme.create_pixel_button(
            data_frame, "Reset All Data", self.confirm_reset_data, color="#F44336"
        )
        reset_button.pack(pady=5)

        # About section
        about_frame = tk.LabelFrame(
            parent,
            text="About",
            font=self.theme.pixel_font,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            padx=10,
            pady=10,
            relief=tk.RIDGE,
            bd=3,
        )
        about_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        about_text = """Skill Quest 2025 - Gamification for Skill Development

Version 1.0.0

This application helps you track and gamify your progress in developing 
skills through regular practice and structured learning.

Based on the gamification principles outlined in the transcript, 
this tool turns skill development into a motivating game with 
points, levels, and rewards.

Created with Python and Tkinter."""

        tk.Label(
            about_frame,
            text=about_text,
            justify=tk.LEFT,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.small_font,
        ).pack(pady=10)
        
    def backup_data(self):
        """Create a backup of the current data."""
        try:
            backup_file = self.data_manager.backup_data()
            messagebox.showinfo(
                "Backup Successful", f"Data successfully backed up to {backup_file}"
            )
        except Exception as e:
            messagebox.showerror("Backup Error", f"Failed to create backup: {str(e)}")
            
    def restore_data(self):
        """Restore data from a backup file."""
        # Open file dialog to select backup file
        backup_file = filedialog.askopenfilename(
            title="Select Backup File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )

        if not backup_file:
            return

        # Confirm restoration
        if messagebox.askyesno(
            "Confirm Restore",
            "This will overwrite your current data. Are you sure you want to continue?",
        ):
            # Make a backup of current data just in case
            self.backup_data()

            # Attempt to restore
            if self.data_manager.restore_from_backup(backup_file):
                messagebox.showinfo(
                    "Restore Successful", "Data has been restored from backup"
                )
                
                # Refresh display
                self.app.show_main_menu()
            else:
                messagebox.showerror(
                    "Restore Error", "Failed to restore from backup. Invalid backup file."
                )
                
    def confirm_reset_data(self):
        """Confirm before resetting all data."""
        if messagebox.askyesno(
            "Confirm Reset",
            "This will reset ALL your data and progress. This cannot be undone. Are you absolutely sure?",
        ):
            # Double confirmation for safety
            if messagebox.askyesno(
                "Final Confirmation",
                "ALL YOUR PROGRESS WILL BE LOST. Are you really, really sure?",
            ):
                # Make a backup first
                self.backup_data()

                # Reset the data
                if self.data_manager.reset_data():
                    messagebox.showinfo("Reset Complete", "All data has been reset")

                    # Refresh display
                    self.app.show_main_menu()
