# Snake

Classic Snake game on `pygame`, written as an exercise in object-oriented design: a `GameObject` base class with `Apple` and `Snake` subclasses, a game loop with key handling, and a test suite that checks both behaviour and code structure.

Built during the *Python Developer* course at Yandex Practicum (2025–2026). Every project was reviewed and accepted by a course mentor.

## Tech stack

Python 3 · pygame · pytest

## Run

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
python the_snake.py
```

Controls: arrow keys. The snake wraps around the screen edges; eating an apple makes it longer, running into its own body restarts the game.

## Tests

```bash
pytest          # 37 tests
```

## Author

Roman Tanashkin — [github.com/RomanTanashkin](https://github.com/RomanTanashkin)
