"""
Theme management for the Pixel Quest application.
Provides theme setup, colors, fonts, and styled UI components.
"""

import tkinter as tk
from tkinter import ttk, font, TclError


class PixelTheme:
    """
    Manages the pixel art theme for the application including colors,
    fonts, and styled UI components.
    """

    def __init__(self, root):
        """
        Initialize the pixel art theme.

        Args:
            root: The root Tkinter window
        """
        self.root = root
        self.setup_colors()
        self.setup_fonts()
        self.configure_styles()

    def setup_colors(self):
        """Set up the color scheme for the pixel art theme."""
        # Main colors
        self.bg_color = "#FFF4C2"  # Light cream background
        self.primary_color = "#FFD34E"  # Yellow
        self.secondary_color = "#FF9843"  # Orange
        self.accent_color = "#9ED5C5"  # Teal
        self.text_color = "#543F32"  # Brown

        # Module-specific colors
        self.art_color = "#4CAF50"  # Green
        self.korean_color = "#2196F3"  # Blue
        self.french_color = "#FF9800"  # Orange
        self.diss_color = "#9C27B0"  # Purple for dissertation
        self.habit_color = "#673AB7"  # Purple for habit tracker
        self.todo_color = "#E91E63"  # Pink for to-do list

    def setup_fonts(self):
        """Set up fonts for the pixel art theme."""
        try:
            # If you have the Press Start 2P font installed, uncomment these lines
            # self.pixel_font = font.Font(family="Press Start 2P", size=12)
            # self.heading_font = font.Font(family="Press Start 2P", size=18)
            # self.small_font = font.Font(family="Press Start 2P", size=9)

            # Fallback fonts that might look somewhat pixelated
            self.pixel_font = font.Font(family="Courier New", size=12, weight="bold")
            self.heading_font = font.Font(family="Courier New", size=18, weight="bold")
            self.small_font = font.Font(family="Courier New", size=9, weight="bold")
        except (TclError, RuntimeError):
            # Fallback fonts
            self.pixel_font = font.Font(family="Courier New", size=12, weight="bold")
            self.heading_font = font.Font(family="Courier New", size=18, weight="bold")
            self.small_font = font.Font(family="Courier New", size=9, weight="bold")

    def configure_styles(self):
        """Configure ttk styles for the pixel art theme."""
        # Configure the root window
        self.root.configure(bg=self.bg_color)

        # Configure ttk styles
        self.style = ttk.Style()
        self.style.configure(
            "Pixel.TButton",
            font=self.pixel_font,
            background=self.primary_color,
            foreground=self.text_color,
        )

        self.style.configure("Pixel.TFrame", background=self.bg_color)

        self.style.configure(
            "Pixel.TLabel",
            font=self.pixel_font,
            background=self.bg_color,
            foreground=self.text_color,
        )

        self.style.configure(
            "Pixel.Progressbar", thickness=20, background=self.accent_color
        )

        # Style for the combobox to match pixel theme
        self.style.configure(
            "Pixel.TCombobox", background=self.bg_color, fieldbackground=self.bg_color
        )

        # Configure notebook styles for tabs
        self.style.configure("TNotebook", background=self.bg_color)
        self.style.configure(
            "TNotebook.Tab",
            background=self.primary_color,
            foreground=self.text_color,
            font=self.pixel_font,
        )
        self.style.map("TNotebook.Tab", background=[("selected", self.secondary_color)])

    def create_pixel_button(
        self, parent, text, command, color=None, width=None, height=None, small=False
    ):
        """
        Create a button with pixel art styling.

        Args:
            parent: Parent widget
            text: Button text
            command: Button command function
            color: Button color (defaults to primary color)
            width: Button width
            height: Button height
            small: If True, use smaller font and padding

        Returns:
            The created button widget
        """
        if color is None:
            color = self.primary_color

        # Choose font based on small parameter
        button_font = self.small_font if small else self.pixel_font

        # Adjust padding for small buttons
        padx_value = 5 if small else 10
        pady_value = 2 if small else 5

        button = tk.Button(
            parent,
            text=text,
            command=command,
            font=button_font,
            bg=color,
            fg=self.text_color,
            relief=tk.RIDGE,
            bd=3,
            padx=padx_value,
            pady=pady_value,
            width=width,
            height=height,
            activebackground=self.secondary_color,
        )

        # Add pixel-like border effect
        button.config(highlightbackground=self.text_color, highlightthickness=2)

        return button

    def darken_color(self, hex_color):
        """
        Darken a hex color for shading effects.

        Args:
            hex_color: Hex color code

        Returns:
            Darkened hex color code
        """
        # Convert hex to RGB
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)

        # Darken the color
        factor = 0.8
        r = int(r * factor)
        g = int(g * factor)
        b = int(b * factor)

        # Convert back to hex
        return f"#{r:02x}{g:02x}{b:02x}"
