from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class MainWindowSignals(QObject):
    """
    Agregator zdarzeń dla MainWindow.
    Wymusza rygorystyczny kontrakt między widokiem a kontrolerem.
    """
    load_machines_requested = Signal()
    generate_report_requested = Signal()
    confirm_order_requested = Signal()
    clean_text_requested = Signal()
    open_settings_requested = Signal()
    show_help_requested = Signal()
    show_about_requested = Signal()


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.signals = MainWindowSignals()

        # --- Konfiguracja okna głównego ---
        self.setWindowTitle("Production Counter")
        self.resize(840, 640)

        # Inicjalizacja układu UI
        self._build_ui()

    def _build_ui(self) -> None:
        # 1. Główny widżet centralny, do którego przypniemy układ horyzontalny
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)  # Brak marginesów od krawędzi okna
        main_layout.setSpacing(0)

        # ==========================================
        # 2. LEWY PANEL (Menu bocznego)
        # ==========================================
        self.left_panel = QWidget()
        self.left_panel.setObjectName("LeftPanel")  # Powiązanie z plikiem .qss
        self.left_panel.setFixedWidth(220)  # Sztywna szerokość panelu, jak w CTk

        left_layout = QVBoxLayout(self.left_panel)
        left_layout.setContentsMargins(15, 20, 15, 20)
        left_layout.setSpacing(15)

        # --- Górna grupa przycisków ---
        self.btn_load_machines = QPushButton("Wczytaj maszyny")
        self.btn_generate_report = QPushButton("Generuj raport")
        self.btn_confirm_order = QPushButton("Potwierdź termin")
        self.btn_clean_text = QPushButton("Wyczyść")

        # Emisja sygnałów po kliknięciu
        self.btn_load_machines.clicked.connect(self.signals.load_machines_requested.emit)
        self.btn_generate_report.clicked.connect(self.signals.generate_report_requested.emit)
        self.btn_confirm_order.clicked.connect(self.signals.confirm_order_requested.emit)
        self.btn_clean_text.clicked.connect(self.signals.clean_text_requested.emit)

        # Dodanie przycisków do wertykalnego layoutu
        left_layout.addWidget(self.btn_load_machines)
        left_layout.addWidget(self.btn_generate_report)
        left_layout.addWidget(self.btn_confirm_order)
        left_layout.addWidget(self.btn_clean_text)

        # Pusty 'wypychacz' (addStretch), który spycha kolejne elementy na sam dół okna
        left_layout.addStretch()

        # --- Dolna grupa przycisków ---
        self.btn_settings = QPushButton("Ustawienia")
        self.btn_help = QPushButton("Pomoc")
        self.btn_about = QPushButton("O programie")

        self.btn_settings.clicked.connect(self.signals.open_settings_requested.emit)
        self.btn_help.clicked.connect(self.signals.show_help_requested.emit)
        self.btn_about.clicked.connect(self.signals.show_about_requested.emit)

        left_layout.addWidget(self.btn_settings)
        left_layout.addWidget(self.btn_help)
        left_layout.addWidget(self.btn_about)

        # ==========================================
        # 3. PRAWY PANEL (Główna zawartość)
        # ==========================================
        self.right_panel = QWidget()
        self.right_panel.setObjectName("RightPanel")

        # Przygotowany pod welcome screen i tabele w przyszłości
        self.right_layout = QVBoxLayout(self.right_panel)
        self.right_layout.setContentsMargins(20, 20, 20, 20)

        # ==========================================
        # 4. ZŁOŻENIE UKŁADU
        # ==========================================
        main_layout.addWidget(self.left_panel)
        main_layout.addWidget(self.right_panel)
