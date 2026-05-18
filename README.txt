#  Escape from the Procedural Mansion

A lightweight, procedural text-adventure game built entirely with Python's standard library. Features a custom pseudo-3D vector graphics engine rendered dynamically on a Tkinter Canvas.

##  Key Features (Architecture Highlights)
* **Zero Dependencies:** Runs out-of-the-box using only built-in Python modules (`tkinter`, `json`, `random`, `os`).
* **Procedural Vector Engine:** No external `.png` or `.jpg` assets are used. The game mathematically calculates and draws 3D-perspective rooms based on JSON configuration.
* **Data-Driven Architecture:** Storylines, rooms, and dialogue are loaded from auto-generated `data/rooms.json` and `data/locales.json`.
* **State Serialization (Save/Load):** Fully functional Save/Load system utilizing JSON serialization.
* **Event-Driven UI:** Custom Typewriter effect with asynchronous callback handling using `root.after()`.
* **i18n (Internationalization):** Full support for English and Russian languages.
* **Modern Python:** Developed with strict **Type Hints** (`typing`) and proper OOP practices.

## How to Run

1. Make sure you have Python 3 installed.
2. Clone the repository and run:
   ```bash
   python main.py