"""
Utility functions for the Pixel Quest application.
"""

import tkinter as tk
from datetime import datetime, timedelta

def create_pixel_progress_bar(parent, percent, color, bg_color, text_color, darken_color_func):
    """
    Create a pixel art styled progress bar.
    
    Args:
        parent: Parent widget
        percent: Percent complete (0-100)
        color: Fill color
        bg_color: Background color
        text_color: Text color
        darken_color_func: Function to darken colors
        
    Returns:
        The frame containing the progress bar
    """
    # Create frame for the progress bar
    bar_frame = tk.Frame(parent, bg=text_color, bd=2, relief=tk.RIDGE)
    bar_frame.pack(pady=5, fill=tk.X)

    # Create canvas for drawing the progress bar
    progress_width = 300
    progress_height = 20
    progress_canvas = tk.Canvas(
        bar_frame,
        width=progress_width,
        height=progress_height,
        bg=bg_color,
        highlightthickness=0,
    )
    progress_canvas.pack(fill=tk.X)

    # Calculate filled width based on percentage
    filled_width = int((percent / 100) * progress_width)

    # Draw the filled part of the progress bar
    progress_canvas.create_rectangle(
        0, 0, filled_width, progress_height, fill=color, outline=""
    )

    # Add pixelated edge effect (optional)
    for i in range(0, filled_width, 4):
        darker_color = darken_color_func(color)
        progress_canvas.create_rectangle(
            i, 0, i + 3, 3, fill=darker_color, outline=""
        )
        progress_canvas.create_rectangle(
            i,
            progress_height - 3,
            i + 3,
            progress_height,
            fill=darker_color,
            outline="",
        )
    
    return bar_frame

def update_streak(data, module):
    """
    Update streak for the given module.
    
    Args:
        data: The game data dictionary
        module: Module name ('art', 'korean', or 'french')
        
    Returns:
        The updated streak value
    """
    last_practice = data[module]["last_practice"]
    today = datetime.now().strftime("%Y-%m-%d")

    if last_practice is None:
        # First time logging progress
        data[module]["streak"] = 1
    elif last_practice == today:
        # Already logged today, no streak change
        pass
    else:
        # Check if the last practice was yesterday
        last_date = datetime.strptime(last_practice, "%Y-%m-%d")
        yesterday = datetime.now() - timedelta(days=1)

        if last_date.date() == yesterday.date():
            # Practiced yesterday, increase streak
            data[module]["streak"] += 1
        else:
            # Streak broken, reset to 1
            data[module]["streak"] = 1

    # Update last practice date
    data[module]["last_practice"] = today
    
    return data[module]["streak"]

def check_level_up(data, module):
    """
    Check if the module level should increase.
    
    Args:
        data: The game data dictionary
        module: Module name ('art', 'korean', or 'french')
        
    Returns:
        Tuple of (new_level, level_increased, streak_bonus)
    """
    # Points required for each level
    points_per_level = 100

    # Calculate level based on points
    new_level = (data[module]["points"] // points_per_level) + 1
    
    # Check if level increased
    level_increased = new_level > data[module]["level"]
    streak_bonus = 0
    
    if level_increased:
        # Add streak bonus points
        streak_bonus = data[module]["streak"]
        data[module]["points"] += streak_bonus
        
        # Update level
        data[module]["level"] = new_level
    
    return (new_level, level_increased, streak_bonus)
