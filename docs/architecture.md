
FinalProject/
│
├── main.py
├── config.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── assets/
│   ├── images/
│   │   ├── backgrounds/
│   │   ├── icons/
│   │   ├── pieces/
│   │   │   ├── x.png
│   │   │   └── o.png
│   │   ├── buttons/
│   │   └── effects/
│   │
│   ├── sounds/
│   │   ├── click.wav
│   │   ├── place.wav
│   │   ├── win.wav
│   │   ├── lose.wav
│   │   └── draw.wav
│   │
│   └── fonts/
│
├── src/
│   ├── __init__.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── game.py
│   │   ├── states.py
│   │   ├── event_manager.py
│   │   └── scene_manager.py
│   │
│   ├── board/
│   │   ├── __init__.py
│   │   ├── board.py
│   │   ├── renderer.py
│   │   ├── input_handler.py
│   │   ├── coordinates.py
│   │   └── highlights.py
│   │
│   ├── logic/
│   │   ├── __init__.py
│   │   ├── game_logic.py
│   │   ├── turn_manager.py
│   │   ├── move_validator.py
│   │   ├── win_checker.py
│   │   └── draw_checker.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── player.py
│   │   ├── move.py
│   │   ├── game_data.py
│   │   └── game_settings.py
│   │
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── ai_player.py
│   │   ├── difficulty.py
│   │   ├── evaluation.py
│   │   ├── move_generator.py
│   │   └── algorithms/
│   │       ├── __init__.py
│   │       ├── minimax.py
│   │       ├── alpha_beta.py
│   │       └── heuristic.py
│   │
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── menu.py
│   │   ├── buttons.py
│   │   ├── renderer.py
│   │   ├── text_input.py
│   │   ├── game_over.py
│   │   ├── pause_menu.py
│   │   ├── settings_menu.py
│   │   ├── player_panel.py
│   │   ├── scoreboard.py
│   │   └── dialogs.py
│   │
│   ├── audio/
│   │   ├── __init__.py
│   │   └── sound_manager.py
│   │
│   ├── data/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── save_manager.py
│   │   ├── history_manager.py
│   │   └── statistics.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── helpers.py
│       ├── constants.py
│       └── timer.py
│
├── saves/
│   ├── settings.json
│   ├── history.json
│   └── statistics.json
│
├── tests/
│   ├── test_game_logic.py
│   ├── test_win_checker.py
│   ├── test_move_validator.py
│   ├── test_ai.py
│   └── test_save_manager.py
│
└── docs/
    ├── architecture.md
    ├── game_rules.md
    └── team_work.md
