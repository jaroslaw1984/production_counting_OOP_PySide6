# app.py
import sys
from PySide6.QtWidgets import QApplication

from project.config.paths import STYLE_PATH
from project.GUI.main_windows import MainWindow # lub nowa nazwa pliku okna PySide6

def main() -> None:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Wczytanie globalnego wyglądu z pliku QSS za pomocą bezpiecznej ścieżki
    if STYLE_PATH.exists():
        app.setStyleSheet(STYLE_PATH.read_text(encoding="utf-8"))
    else:
        print(f"Ostrzeżenie: Nie odnaleziono pliku stylów w {STYLE_PATH}")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
