# app.py
import sys

from PySide6.QtWidgets import QApplication

from project.config.paths import STYLE_PATH
from project.GUI.main_windows import MainWindow
from project.core.app_state import AppState
from project.core.controllers import MainController


def main() -> None:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Wczytanie globalnego wyglądu z pliku QSS za pomocą bezpiecznej ścieżki
    if STYLE_PATH.exists():
        app.setStyleSheet(STYLE_PATH.read_text(encoding="utf-8"))
    else:
        print(f"Ostrzeżenie: Nie odnaleziono pliku stylów w {STYLE_PATH}")

    # 1. Tworzymy stan aplikacji (AppState)
    state = AppState()

    # 2. Tworzymy okno główne (MainWindow)
    window = MainWindow()

    # 3. Tworzymy kontroler i przekazujemy mu stan oraz widok
    controller = MainController(state=state, view=window)

    # 4. ŁĄCZENIE (WIRING): Sygnały widoku -> Metody kontrolera
    window.signals.load_machines_requested.connect(controller.handle_load_machines)
    window.signals.generate_report_requested.connect(controller.handle_generate_report)
    window.signals.confirm_order_requested.connect(controller.handle_confirm_order)
    window.signals.clean_text_requested.connect(controller.handle_clean_text)

    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
