# PyGame Project Template

A comprehensive PyGame project template with state management, asset handling, and utility functions.

## Features

- 🎮 Game state management (Menu, Play, Pause)
- 🎨 Asset management system
- ⌨️ Input handling utilities
- 🎯 Sprite management and collision detection
- ⚙️ Configuration system
- 📁 Organized project structure

## Project Structure

```
pygame-project/
├── assets/
│   ├── images/
│   ├── sounds/
│   └── fonts/
├── states/
│   └── game_state.py
├── utils/
│   ├── asset_loader.py
│   ├── input_handler.py
│   └── sprite_utils.py
├── config.py
├── main.py
└── requirements.txt
```

## Setup

1. Clone the repository:
```bash
git clone https://github.com/RCS-KBD/pygame-project.git
cd pygame-project
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the game:
```bash
python main.py
```

## Controls

- Arrow keys / WASD: Movement
- ESC: Pause game
- Menu navigation: Arrow keys + Enter

## Development

### Adding New States

1. Create a new class inheriting from `GameState` in `states/game_state.py`
2. Implement the required methods: `update()`, `draw()`, and `handle_event()`
3. Add the state to the `states` dictionary in `Game.__init__()`

### Adding Assets

1. Place assets in the appropriate directory under `assets/`
2. Use the `AssetLoader` class to load and manage assets
3. Access assets through the game's asset loader instance

### Sprite Creation

1. Inherit from `GameSprite` in `utils/sprite_utils.py`
2. Initialize with an image and position
3. Implement custom update logic as needed

## License

This project is open source and available under the MIT License.