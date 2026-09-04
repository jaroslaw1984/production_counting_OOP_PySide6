from collections.abc import Callable
from datetime import date, datetime

from PySide6.QtWidgets import (
    QButtonGroup,
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QRadioButton,
    QVBoxLayout,
    QWidget,
)


class SchedulePopup(QDialog):
    def __init__(self, parent: QWidget, on_confirm: Callable) -> None:
        super().__init__(parent)
        self.setWindowTitle("Parametry liczenia grupy - harmonogram")
        self.setFixedSize(450, 260)
        self.setModal(True)

        self.on_confirm = on_confirm

        self._build_ui()

    def _build_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # --- WIERSZ 1: Zmiana ---
        shift_layout = QHBoxLayout()
        lbl_shift = QLabel("Start od zmiany:")
        lbl_shift.setFixedWidth(120)
        shift_layout.addWidget(lbl_shift)

        self.shift_group = QButtonGroup(self)
        self.radio_shift1 = QRadioButton("1")
        self.radio_shift2 = QRadioButton("2")
        self.radio_shift3 = QRadioButton("3")

        self.radio_shift1.setChecked(True) # Domyślnie zmiana 1

        self.shift_group.addButton(self.radio_shift1, 1)
        self.shift_group.addButton(self.radio_shift2, 2)
        self.shift_group.addButton(self.radio_shift3, 3)

        shift_layout.addWidget(self.radio_shift1)
        shift_layout.addWidget(self.radio_shift2)
        shift_layout.addWidget(self.radio_shift3)
        shift_layout.addStretch()
        main_layout.addLayout(shift_layout)

        # --- WIERSZ 2: Tryb startu (dziś/data) ---
        mode_layout = QHBoxLayout()
        lbl_mode = QLabel("Start liczenia:")
        lbl_mode.setFixedWidth(120)
        mode_layout.addWidget(lbl_mode)

        self.mode_group = QButtonGroup(self)
        self.radio_today = QRadioButton("od dziś")
        self.radio_date = QRadioButton("od daty")

        self.radio_today.setChecked(True)

        self.mode_group.addButton(self.radio_today, 1)
        self.mode_group.addButton(self.radio_date, 2)

        mode_layout.addWidget(self.radio_today)
        mode_layout.addWidget(self.radio_date)
        mode_layout.addStretch()
        main_layout.addLayout(mode_layout)

        # --- WIERSZ 3: Pole daty ---
        date_layout = QHBoxLayout()
        lbl_date = QLabel("Podaj datę:")
        lbl_date.setFixedWidth(120)
        date_layout.addWidget(lbl_date)

        self.date_entry = QLineEdit(date.today().isoformat())
        self.date_entry.setFixedWidth(140)
        date_layout.addWidget(self.date_entry)

        lbl_date_hint = QLabel("(YYYY-MM-DD)")
        lbl_date_hint.setStyleSheet("color: #aaaaaa;")
        date_layout.addWidget(lbl_date_hint)
        date_layout.addStretch()
        main_layout.addLayout(date_layout)

        main_layout.addStretch()

        # --- WIERSZ 4: Przyciski ---
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        btn_cancel = QPushButton("Anuluj")
        btn_cancel.setFixedWidth(100)
        btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(btn_cancel)

        btn_ok = QPushButton("OK")
        btn_ok.setFixedWidth(100)
        btn_ok.clicked.connect(self._on_ok)
        btn_layout.addWidget(btn_ok)

        main_layout.addLayout(btn_layout)

    def _on_ok(self) -> None:
        # Zbieranie danych z grup
        shift_val = self.shift_group.checkedId() # Zwróci 1, 2 lub 3

        mode = "today" if self.mode_group.checkedId() == 1 else "date"
        ds = self.date_entry.text().strip()

        # Walidacja daty
        if mode == "date":
            try:
                datetime.strptime(ds, "%Y-%m-%d")
            except ValueError:
                QMessageBox.critical(self, "Błąd daty", "Podaj datę w formacie YYYY-MM-DD.")
                return

        result = {
            "start_shift": shift_val,
            "start_mode": mode,
            "start_date": ds
        }

        self.accept() # Zamyka popup z wynikiem pozytywnym
        self.on_confirm(result)
