#!/usr/bin/env python3
"""
Pixel Quest - A gamified skill development tracking application.
Main entry point for the application.
"""

import tkinter as tk
from src.gui import QuestGame

def main():
    """Initialize and run the application."""
    root = tk.Tk()
    app = QuestGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
