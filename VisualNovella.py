import tkinter as tk
from tkinter import messagebox
import random
import json
import os
from typing import List, Dict, Set, Optional, Any

# ==========================================
# Исходные данные для генерации JSON-файлов
# ==========================================
DEFAULT_LOCALES: Dict[str, Dict[str, str]] = {
    "en": {
        "title": "Escape from the Procedural Mansion",
        "play": "Play Game", "quit": "Quit", "continue": "Continue", "yes": "Yes", "no": "No",
        "menu_file": "File", "menu_save": "Save Game", "menu_load": "Load Game",
        "menu_lang": "Language", "inventory_title": "Inventory: ", "empty": "Empty",
        "intro_text": "You wake up in a dark, unfamiliar room. Your memories are hazy. The air is cold and still. Before you stand two doors. You must find a way out.",
        "intro_opt1": "Take the left door", "intro_opt2": "Take the right door",
        "room_water_desc": "You enter a cozy room with wooden walls. A soft lamp illuminates a table. On it sits a glass of glowing water with a note: 'Do not drink'.",
        "room_water_opt1": "Drink the water", "room_water_opt2": "Leave it alone",
        "room_water_out1": "The water tastes unusually sweet. A surge of energy hits you! You suddenly see hidden glowing numbers on the wall: CODE 4827.",
        "room_water_out2": "You decide not to risk it and step away from the table.",
        "room_trash_desc": "You walk into a damp, dark room. The floor is littered with garbage and graffiti covers the walls. In the corner, you spot a surprisingly fresh-looking sandwich.",
        "room_trash_opt1": "Eat the sandwich", "room_trash_opt2": "Ignore it",
        "room_trash_out1": "You eat the sandwich. It's delicious! You feel incredibly strong and revitalized.",
        "room_trash_out2": "You smartly decide not to eat food off the floor.",
        "room_book_desc": "You enter a bright red room. In the center, an ancient book rests on a stone pedestal. The cover warns: 'Do not read'.",
        "room_book_opt1": "Read the book", "room_book_opt2": "Walk past it",
        "room_book_out1": "You open the book. A rusted, heavy key falls out from the pages! You take it with you.",
        "room_book_out2": "You ignore the creepy book and move on.",
        "room_chest_desc": "This spacious room is lit by cold blue neon lights. The walls are metallic. A dusty chest sits in the corner.",
        "room_chest_opt1": "Open the chest", "room_chest_opt2": "Leave it closed",
        "room_chest_out1": "Inside, you find a detailed blueprint map of the mansion's locking mechanisms!",
        "room_chest_out2": "You leave the chest closed, feeling you might have missed out on something.",
        "final_desc": "You finally reach the end of the corridor. A massive steel gate blocks your path to freedom. It has a digital keypad, a heavy keyhole, and exposed locking gears.",
        "final_opt1": "Enter code 4827 on the keypad", "final_opt2": "Insert the rusted key",
        "final_opt3": "Use sheer strength to force the gate open",
        "final_opt4": "Use the blueprint map to dismantle the gears",
        "final_win1": "The keypad beeps green! The heavy gate slides open, revealing the outside world. You escaped!",
        "final_win2": "You turn the rusted key. With a heavy clunk, the mechanism unlocks. You escaped!",
        "final_win3": "Empowered by the strange food you ate, you pull the doors apart with immense strength! You escaped!",
        "final_win4": "Following the blueprint, you find the weak point and disable the lock. You escaped!",
        "final_lose": "Your attempt fails. The gate remains sealed. Sirens blare as the room fills with gas... You are trapped forever.",
        "game_over_good": "Congratulations! You survived the procedural mansion.",
        "game_over_bad": "GAME OVER. You perished in the mansion.",
        "play_again": "Would you like to play again?"
    },
    "ru": {
        "title": "Побег из Процедурного Особняка",
        "play": "Играть", "quit": "Выйти", "continue": "Продолжить", "yes": "Да", "no": "Нет",
        "menu_file": "Файл", "menu_save": "Сохранить игру", "menu_load": "Загрузить игру",
        "menu_lang": "Язык", "inventory_title": "Инвентарь: ", "empty": "Пусто",
        "intro_text": "Вы просыпаетесь в темной незнакомой комнате. Ваши воспоминания туманны. Воздух холодный и неподвижный. Перед вами две двери. Вы должны найти выход.",
        "intro_opt1": "Пойти в левую дверь", "intro_opt2": "Пойти в правую дверь",
        "room_water_desc": "Вы попадаете в уютную комнату с деревянными стенами. Мягкий свет освещает стол. На нем стоит стакан со светящейся водой и запиской: 'Не пей меня'.",
        "room_water_opt1": "Выпить воду", "room_water_opt2": "Оставить стакан",
        "room_water_out1": "Вода на вкус сладкая. Вы чувствуете прилив сил! На стене проявляются цифры: КОД 4827.",
        "room_water_out2": "Вы решаете не рисковать и отходите от стола.",
        "room_trash_desc": "Вы заходите в сырую комнату. Пол усеян мусором. В углу вы замечаете удивительно свежий на вид бутерброд.",
        "room_trash_opt1": "Съесть бутерброд", "room_trash_opt2": "Игнорировать",
        "room_trash_out1": "Вы съедаете бутерброд. Очень вкусно! Вы чувствуете себя невероятно сильным и здоровым.",
        "room_trash_out2": "Вы благоразумно решаете не есть еду с пола.",
        "room_book_desc": "Вы входите в ярко-красную комнату. На каменном пьедестале покоится древняя книга. Надпись гласит: 'Не читай'.",
        "room_book_opt1": "Прочитать книгу", "room_book_opt2": "Пройти мимо",
        "room_book_out1": "Вы открываете книгу. Из страниц выпадает тяжелый ржавый ключ! Вы забираете его.",
        "room_book_out2": "Вы игнорируете жуткую книгу и идете дальше.",
        "room_chest_desc": "Комната освещена неоновым светом. Стены металлические. В углу стоит пыльный сундук.",
        "room_chest_opt1": "Открыть сундук", "room_chest_opt2": "Не трогать",
        "room_chest_out1": "Внутри вы находите детальные чертежи замковых механизмов этого особняка!",
        "room_chest_out2": "Вы оставляете сундук закрытым.",
        "final_desc": "Вы достигаете конца коридора. Массивные ворота преграждают путь. На них есть цифровой блок, замочная скважина и открытые шестеренки.",
        "final_opt1": "Ввести код 4827", "final_opt2": "Вставить ржавый ключ",
        "final_opt3": "Применить грубую силу", "final_opt4": "Использовать чертежи механизма",
        "final_win1": "Панель загорается зеленым! Ворота открываются. Вы выбрались!",
        "final_win2": "Вы поворачиваете ключ. Со щелчком механизм открывается. Вы выбрались!",
        "final_win3": "С невероятной силой вы раздвигаете ворота! Вы выбрались!",
        "final_win4": "Следуя чертежам, вы отключаете замок. Вы выбрались!",
        "final_lose": "Ваша попытка провалилась. Включается сирена, комната заполняется газом... Вы в ловушке навсегда.",
        "game_over_good": "Поздравляем! Вы успешно покинули особняк.",
        "game_over_bad": "ИГРА ОКОНЧЕНА. Вы погибли в стенах особняка.",
        "play_again": "Хотите сыграть еще раз?"
    }
}

DEFAULT_ROOMS: List[Dict[str, str]] = [
    {"id": "water", "env": "wood", "item": "table", "desc": "room_water_desc", "opt1": "room_water_opt1",
     "opt2": "room_water_opt2", "out1": "room_water_out1", "out2": "room_water_out2", "gain": "code"},
    {"id": "trash", "env": "dark", "item": "trash", "desc": "room_trash_desc", "opt1": "room_trash_opt1",
     "opt2": "room_trash_opt2", "out1": "room_trash_out1", "out2": "room_trash_out2", "gain": "health"},
    {"id": "book", "env": "red", "item": "pedestal", "desc": "room_book_desc", "opt1": "room_book_opt1",
     "opt2": "room_book_opt2", "out1": "room_book_out1", "out2": "room_book_out2", "gain": "key"},
    {"id": "chest", "env": "neon", "item": "chest", "desc": "room_chest_desc", "opt1": "room_chest_opt1",
     "opt2": "room_chest_opt2", "out1": "room_chest_out1", "out2": "room_chest_out2", "gain": "map"}
]

# Иконки для HUD инвентаря
INVENTORY_ICONS: Dict[str, str] = {
    "code": "🔢", "health": "🥪", "key": "🗝️", "map": "🗺️"
}


class TextAdventureGame:
    def __init__(self, root: tk.Tk) -> None:
        """Инициализация главного окна, загрузка данных и сборка UI."""
        self.root = root
        self.lang: str = "en"
        self.inventory: Set[str] = set()
        self.run_sequence: List[Dict[str, str]] = []
        self.current_room_index: int = 0
        self._type_timer: Optional[str] = None  # Таймер для эффекта печатной машинки
        self.locales: Dict[str, Dict[str, str]] = {}
        self.room_pools: List[Dict[str, str]] = []

        self._setup_window()
        self._ensure_data_files()
        self._load_data()
        self._build_ui()
        self._build_menu()

        self.show_language_screen()

    def _setup_window(self) -> None:
        """Настройка параметров окна Tkinter."""
        self.root.geometry("750x700")
        self.root.configure(bg="#0f0f13")
        self.root.minsize(600, 600)

    def _ensure_data_files(self) -> None:
        """Проверяет наличие файлов с данными. Если их нет - генерирует из дефолтных (Отказоустойчивость)."""
        if not os.path.exists("data"):
            os.makedirs("data")

        if not os.path.exists("data/locales.json"):
            with open("data/locales.json", "w", encoding="utf-8") as f:
                json.dump(DEFAULT_LOCALES, f, ensure_ascii=False, indent=4)

        if not os.path.exists("data/rooms.json"):
            with open("data/rooms.json", "w", encoding="utf-8") as f:
                json.dump(DEFAULT_ROOMS, f, ensure_ascii=False, indent=4)

    def _load_data(self) -> None:
        """Загрузка данных из JSON-файлов."""
        with open("data/locales.json", "r", encoding="utf-8") as f:
            self.locales = json.load(f)
        with open("data/rooms.json", "r", encoding="utf-8") as f:
            self.room_pools = json.load(f)

    def _build_ui(self) -> None:
        """Создание всех виджетов интерфейса (Canvas, HUD, Text, Buttons)."""
        self.canvas = tk.Canvas(self.root, height=250, bg="#0f0f13", highlightthickness=0)
        self.canvas.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # HUD Инвентаря
        self.hud_frame = tk.Frame(self.root, bg="#1a1a24", bd=2, relief=tk.GROOVE)
        self.hud_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=0)
        self.hud_label = tk.Label(self.hud_frame, text="", bg="#1a1a24", fg="#00e5ff", font=("Helvetica", 12, "bold"))
        self.hud_label.pack(side=tk.LEFT, padx=10, pady=5)

        self.text_display = tk.Text(
            self.root, wrap=tk.WORD, bg="#1a1a24", fg="#ffffff",
            font=("Helvetica", 14), state=tk.DISABLED, height=8,
            relief=tk.FLAT, padx=15, pady=15
        )
        self.text_display.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.choice_frame = tk.Frame(self.root, bg="#0f0f13")
        self.choice_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=15)

        self.choice_buttons: List[tk.Button] = []

    def _build_menu(self) -> None:
        """Создание верхнего системного меню (Save, Load, Lang)."""
        self.menu_bar = tk.Menu(self.root)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Save Game", command=self.save_game)
        self.file_menu.add_command(label="Load Game", command=self.load_game)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Quit", command=self.root.destroy)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        self.lang_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.lang_menu.add_command(label="English", command=lambda: self.change_language("en"))
        self.lang_menu.add_command(label="Русский", command=lambda: self.change_language("ru"))
        self.menu_bar.add_cascade(label="Language", menu=self.lang_menu)

        self.root.config(menu=self.menu_bar)

    def t(self, key: str) -> str:
        """Возвращает локализованную строку по ключу."""
        return self.locales.get(self.lang, {}).get(key, key)

    def update_hud(self) -> None:
        """Обновляет визуальный инвентарь (HUD)."""
        title = self.t("inventory_title")
        if not self.inventory:
            items = self.t("empty")
        else:
            items = "  ".join([INVENTORY_ICONS.get(item, item) for item in self.inventory])
        self.hud_label.config(text=f"{title} {items}")

    def update_menu_labels(self) -> None:
        """Обновляет язык в верхнем меню."""
        self.menu_bar.entryconfig(1, label=self.t("menu_file"))
        self.menu_bar.entryconfig(2, label=self.t("menu_lang"))
        self.file_menu.entryconfig(0, label=self.t("menu_save"))
        self.file_menu.entryconfig(1, label=self.t("menu_load"))
        self.file_menu.entryconfig(3, label=self.t("quit"))

    def display_text(self, text: str) -> None:
        """Инициализирует эффект 'печатной машинки'."""
        if self._type_timer:
            self.root.after_cancel(self._type_timer)

        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete(1.0, tk.END)
        self.text_display.config(state=tk.DISABLED)

        # Блокируем кнопки, чтобы игрок не кликал во время печати текста
        for btn in self.choice_buttons:
            btn.config(state=tk.DISABLED)

        self._typewriter_effect(text, 0)

    def _typewriter_effect(self, text: str, index: int) -> None:
        """Рекурсивный метод для посимвольного вывода текста (Анимация)."""
        if index < len(text):
            self.text_display.config(state=tk.NORMAL)
            self.text_display.insert(tk.END, text[index])
            self.text_display.see(tk.END)
            self.text_display.config(state=tk.DISABLED)
            # Скорость печати: 20мс на символ
            self._type_timer = self.root.after(20, self._typewriter_effect, text, index + 1)
        else:
            # Текст напечатан - разблокируем кнопки
            for btn in self.choice_buttons:
                btn.config(state=tk.NORMAL)

    def set_choices(self, choices: List[str], callback: Any) -> None:
        """Создает кнопки выбора действий."""
        for btn in self.choice_buttons:
            btn.destroy()
        self.choice_buttons.clear()

        for i, text in enumerate(choices):
            btn = tk.Button(
                self.choice_frame, text=text,
                bg="#2a2a35", fg="white", activebackground="#4e4e63", activeforeground="white",
                font=("Helvetica", 12, "bold"), relief=tk.FLAT, cursor="hand2",
                command=lambda idx=i: callback(idx),
                state=tk.DISABLED  # Блокируем до окончания печати текста
            )
            btn.pack(side=tk.TOP, fill=tk.X, pady=4)
            self.choice_buttons.append(btn)

    # --- SAVE / LOAD SYSTEM ---
    def save_game(self) -> None:
        """Сериализация текущего состояния игры в JSON."""
        state = {
            "lang": self.lang,
            "inventory": list(self.inventory),
            "run_sequence": self.run_sequence,
            "current_room_index": self.current_room_index
        }
        try:
            with open("savegame.json", "w", encoding="utf-8") as f:
                json.dump(state, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Success", "Game Saved Successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save game: {e}")

    def load_game(self) -> None:
        """Десериализация состояния игры из JSON."""
        if not os.path.exists("savegame.json"):
            messagebox.showwarning("Warning", "No save file found!")
            return

        try:
            with open("savegame.json", "r", encoding="utf-8") as f:
                state = json.load(f)

            self.lang = state.get("lang", "en")
            self.inventory = set(state.get("inventory", []))
            self.run_sequence = state.get("run_sequence", [])
            self.current_room_index = state.get("current_room_index", 0)

            self.update_menu_labels()
            self.update_hud()
            self.root.title(self.t("title"))

            if not self.run_sequence:
                self.show_main_menu()
            elif self.current_room_index >= len(self.run_sequence):
                self.play_finale()
            else:
                self.play_next_room(load_mode=True)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load game: {e}")

    def change_language(self, new_lang: str) -> None:
        self.lang = new_lang
        self.update_menu_labels()
        self.update_hud()
        self.root.title(self.t("title"))
        if not self.run_sequence:
            self.show_main_menu()

    # --- ПСЕВДО-3D ВЕКТОРНАЯ ГРАФИКА (SVG-LIKE) ---
    def draw_scene(self, env_type: str, item_type: str, doors_count: int) -> None:
        """Процедурная генерация визуала комнаты на Canvas."""
        self.canvas.delete("all")
        w, h = 730, 250

        themes = {
            "dark": {"wall": "#263238", "floor": "#101416", "line": "#37474f"},
            "wood": {"wall": "#5c4033", "floor": "#3e2723", "line": "#8d6e63"},
            "red": {"wall": "#7f0000", "floor": "#212121", "line": "#b71c1c"},
            "neon": {"wall": "#1a237e", "floor": "#000000", "line": "#00e5ff"}
        }
        theme = themes.get(env_type, themes["dark"])

        # Room Geometry
        self.canvas.create_polygon(0, 0, w, 0, w - 150, 50, 150, 50, fill="#111111", outline=theme["line"])
        self.canvas.create_polygon(0, h, w, h, w - 150, h - 50, 150, h - 50, fill=theme["floor"], outline=theme["line"])
        self.canvas.create_polygon(0, 0, 150, 50, 150, h - 50, 0, h, fill=theme["wall"], outline=theme["line"])
        self.canvas.create_polygon(w, 0, w - 150, 50, w - 150, h - 50, w, h, fill=theme["wall"], outline=theme["line"])
        self.canvas.create_rectangle(150, 50, w - 150, h - 50, fill=theme["wall"], outline=theme["line"])

        # Doors
        if doors_count == 2:
            self.canvas.create_rectangle(220, 80, 280, h - 50, fill="#3e2723", outline="#000")
            self.canvas.create_oval(265, 140, 275, 150, fill="#ffd54f")
            self.canvas.create_rectangle(w - 280, 80, w - 220, h - 50, fill="#3e2723", outline="#000")
            self.canvas.create_oval(w - 240, 140, w - 230, 150, fill="#ffd54f")
        elif doors_count == 1:
            cx = w / 2
            self.canvas.create_rectangle(cx - 40, 80, cx + 40, h - 50, fill="#4e342e", outline="#000")
            self.canvas.create_oval(cx + 20, 140, cx + 30, 150, fill="#ffd54f")

        # Items
        cx = w / 2
        if item_type == "table":
            self.canvas.create_rectangle(cx - 40, h - 80, cx + 40, h - 70, fill="#8d6e63")
            self.canvas.create_rectangle(cx - 30, h - 70, cx - 20, h - 40, fill="#5d4037")
            self.canvas.create_rectangle(cx + 20, h - 70, cx + 30, h - 40, fill="#5d4037")
            self.canvas.create_rectangle(cx - 5, h - 95, cx + 5, h - 80, fill="#81d4fa", outline="#e1f5fe")
        elif item_type == "trash":
            self.canvas.create_oval(cx - 60, h - 60, cx - 20, h - 40, fill="#4caf50")
            self.canvas.create_oval(cx + 10, h - 55, cx + 60, h - 35, fill="#9e9e9e")
            self.canvas.create_oval(cx - 15, h - 50, cx + 25, h - 30, fill="#795548")
        elif item_type == "pedestal":
            self.canvas.create_rectangle(cx - 20, h - 100, cx + 20, h - 40, fill="#757575", outline="#424242")
            self.canvas.create_polygon(cx - 15, h - 110, cx + 15, h - 110, cx + 10, h - 100, cx - 10, h - 100,
                                       fill="#b71c1c")
        elif item_type == "chest":
            self.canvas.create_rectangle(cx - 30, h - 80, cx + 30, h - 40, fill="#5d4037", outline="#3e2723")
            self.canvas.create_arc(cx - 30, h - 95, cx + 30, h - 65, start=0, extent=180, fill="#8d6e63",
                                   outline="#3e2723")
            self.canvas.create_rectangle(cx - 5, h - 75, cx + 5, h - 65, fill="#ffb300")

    # --- GAME LOGIC ---
    def show_language_screen(self) -> None:
        self.update_menu_labels()
        self.update_hud()
        self.canvas.delete("all")
        self.display_text("Select Language / Выберите язык")
        self.set_choices(["English", "Русский"],
                         lambda idx: self.change_language("en" if idx == 0 else "ru") or self.show_main_menu())

    def show_main_menu(self) -> None:
        self.run_sequence.clear()
        self.inventory.clear()
        self.update_hud()
        self.canvas.delete("all")
        self.display_text(self.t("title"))
        self.set_choices([self.t("play"), self.t("quit")],
                         lambda idx: self.start_game() if idx == 0 else self.root.destroy())

    def start_game(self) -> None:
        self.inventory.clear()
        self.update_hud()
        self.run_sequence = random.sample(self.room_pools, 3)
        self.current_room_index = 0

        self.draw_scene("dark", "none", 2)
        self.display_text(self.t("intro_text"))
        self.set_choices([self.t("intro_opt1"), self.t("intro_opt2")], lambda idx: self.play_next_room())

    def play_next_room(self, load_mode: bool = False) -> None:
        if self.current_room_index < len(self.run_sequence):
            room = self.run_sequence[self.current_room_index]
            self.draw_scene(room["env"], room["item"], 2)

            if load_mode:
                self.display_text(self.t(room["desc"]) + "\n[Game Loaded]")
            else:
                self.display_text(self.t(room["desc"]))

            self.set_choices(
                [self.t(room["opt1"]), self.t(room["opt2"])],
                lambda idx, r=room: self.handle_room_outcome(r, idx)
            )
        else:
            self.play_finale()

    def handle_room_outcome(self, room: Dict[str, str], choice_index: int) -> None:
        if choice_index == 0:
            self.inventory.add(room["gain"])
            self.update_hud()
            outcome_text = self.t(room["out1"])
        else:
            outcome_text = self.t(room["out2"])

        self.display_text(outcome_text)
        self.current_room_index += 1
        self.set_choices([self.t("continue")], lambda idx: self.play_next_room())

    def play_finale(self) -> None:
        self.draw_scene("dark", "none", 1)
        self.display_text(self.t("final_desc"))

        choices = [self.t("final_opt1"), self.t("final_opt2"), self.t("final_opt3"), self.t("final_opt4")]
        self.set_choices(choices, self.check_finale_outcome)

    def check_finale_outcome(self, index: int) -> None:
        has_won, win_text = False, ""

        if index == 0 and "code" in self.inventory:
            has_won, win_text = True, "final_win1"
        elif index == 1 and "key" in self.inventory:
            has_won, win_text = True, "final_win2"
        elif index == 2 and "health" in self.inventory:
            has_won, win_text = True, "final_win3"
        elif index == 3 and "map" in self.inventory:
            has_won, win_text = True, "final_win4"

        if has_won:
            self.display_text(self.t(win_text))
            self.set_choices([self.t("continue")], lambda idx: self.end_game(True))
        else:
            self.display_text(self.t("final_lose"))
            self.set_choices([self.t("continue")], lambda idx: self.end_game(False))

    def end_game(self, is_win: bool) -> None:
        self.canvas.delete("all")
        result = self.t("game_over_good") if is_win else self.t("game_over_bad")
        self.display_text(f"{result}\n\n{self.t('play_again')}")
        self.set_choices([self.t("yes"), self.t("no")],
                         lambda idx: self.start_game() if idx == 0 else self.root.destroy())


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Escape from the Procedural Mansion")
    app = TextAdventureGame(root)
    root.mainloop()