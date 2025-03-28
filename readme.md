# Pixel Quest - Gamified Skill Development

A gamified skill tracking application to help you develop skills through regular practice and structured learning.

## Overview

Pixel Quest turns skill development into a game with points, levels, streaks, and rewards. Track your progress in multiple skill areas:

- **Art** - Track fundamentals, sketchbook practice, and accountability posts
- **Korean** - Track language learning, immersion, and practical application
- **French** - Track language learning, immersion, and practical application

The application uses a pixel art aesthetic and gamification principles to make skill development more engaging and fun.

## Features

- **Multiple Skill Modules**: Track art and language learning progress
- **Points & Levels**: Earn points for completed activities and level up
- **Daily Streaks**: Maintain streaks by practicing regularly
- **Rewards System**: Cash in points for customizable rewards
- **Health Check**: Daily wellness check to monitor your health status
- **Statistics**: Detailed stats and progress tracking
- **Data Management**: Backup, restore, and export your data

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd pixel-quest
   ```

2. Install requirements:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python main.py
   ```

## Project Structure

```
pixel_quest/
├── main.py                  # Main execution file
├── requirements.txt         # Dependencies
├── src/                     # Source code folder
│   ├── __init__.py          # Makes src a package
│   ├── gui.py               # Main GUI components
│   ├── data_manager.py      # Data loading/saving
│   ├── theme.py             # Theme management
│   ├── modules/             # Individual modules
│   │   ├── __init__.py      # Makes modules a package
│   │   ├── art_module.py    # Art module functionality
│   │   ├── french_module.py # French module functionality
│   │   ├── korean_module.py # Korean module functionality
│   │   ├── rewards.py       # Rewards functionality
│   │   ├── settings.py      # Settings functionality
│   │   ├── statistics.py    # Statistics functionality
│   │   └── health.py        # Health check functionality
│   └── utils.py             # Utility functions
```

## Extending the Application

### Adding a New Skill Module

1. Create a new module file in `src/modules/`, following the pattern of existing modules
2. Update the main GUI in `src/gui.py` to include the new module
3. Add the module data structure in `src/data_manager.py`
4. Implement the module interface similar to existing modules

### Adding New Features to Existing Modules

1. Locate the module file in `src/modules/`
2. Add new methods or extend existing ones
3. Update the module's UI components as needed
4. If needed, update the data structure in `src/data_manager.py`

### Customizing the Theme

1. Open `src/theme.py`
2. Modify the color schemes and fonts in the `setup_colors` and `setup_fonts` methods

### Adding New Reward Types

1. Open `src/modules/rewards.py`
2. Extend the rewards management functionality
3. Update the data structure in `src/data_manager.py` if needed

## Data Storage

The application stores all data in a JSON file (`quest_data.json`) in the application directory. You can:

- Backup your data using the settings tab
- Restore from backups
- Export statistics
- Reset all data if needed

## License

[Insert appropriate license here]

## Contributing

Contributions are welcome! Please feel free to submit pull requests.

1. Fork the repository
2. Create a new branch for your feature
3. Add your feature or enhancement
4. Submit a pull request
