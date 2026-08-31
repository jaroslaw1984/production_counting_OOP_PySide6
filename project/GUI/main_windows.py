from PySide6.QtCore import QObject, Qt, Signal
from PySide6.QtGui import QFontMetrics
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from assets.ui_metrics import (
    LEFT_PANEL_MARGINS,
    LEFT_PANEL_SPACING,
    LEFT_PANEL_WIDTH,
    MAIN_LAYOUT_MARGINS,
    MAIN_LAYOUT_SPACING,
    MAIN_WINDOW_SIZE,
    RIGHT_PANEL_MARGINS,
    WELCOME_CARD_HORIZONTAL_PADDING,
    WELCOME_CARD_MIN_HEIGHT,
    WELCOME_LOGO_BOTTOM_SPACING,
    WELCOME_SPACING,
    WELCOME_VERSION_TOP_SPACING,
)
from project.config.version import PROGRAM_NAME
from project.core.app_state import AppState
from project.GUI.ui_texts import ASCII_LOGO, HOME_DESC, HOME_SUBTITLE, HOME_VERSION


class MainWindowSignals(QObject):
    """Sygnały zastępujące bezpośrednie odwołania do kontrolera."""
    load_machines_requested = Signal()
    generate_report_requested = Signal()
    confirm_order_requested = Signal()
    clean_text_requested = Signal()
    open_settings_requested = Signal()
    show_help_requested = Signal()
    show_about_requested = Signal()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.signals = MainWindowSignals()

        self.setWindowTitle(PROGRAM_NAME)
        self.resize(MAIN_WINDOW_SIZE)

        # Wywołanie metod budujących interfejs (dokładnie jak u Ciebie)
        self._configure_layout()
        self._build_left_panel()
        self._build_right_panel()

    def _configure_layout(self):
        # Odpowiednik self.root.grid_columnconfigure z CTk
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(*MAIN_LAYOUT_MARGINS)
        self.main_layout.setSpacing(MAIN_LAYOUT_SPACING)

    def _build_left_panel(self):
        # Odpowiednik self.left = ctk.CTkFrame
        self.left_panel = QFrame()
        self.left_panel.setObjectName("LeftPanel")
        self.left_panel.setFixedWidth(LEFT_PANEL_WIDTH)

        self.left_layout = QVBoxLayout(self.left_panel)
        self.left_layout.setContentsMargins(*LEFT_PANEL_MARGINS)
        self.left_layout.setSpacing(LEFT_PANEL_SPACING)

        # --- Górne przyciski ---
        self.btn_load_machines = QPushButton("Wczytaj maszyny")
        self.btn_load_machines.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_generate_report = QPushButton("Generuj raport")
        self.btn_generate_report.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_confirm_order = QPushButton("Potwierdź termin")
        self.btn_confirm_order.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_clean_text = QPushButton("Wyczyść")
        self.btn_clean_text.setCursor(Qt.CursorShape.PointingHandCursor)

        # Emisja sygnałów
        self.btn_load_machines.clicked.connect(self.signals.load_machines_requested.emit)
        self.btn_generate_report.clicked.connect(self.signals.generate_report_requested.emit)
        self.btn_confirm_order.clicked.connect(self.signals.confirm_order_requested.emit)
        self.btn_clean_text.clicked.connect(self.signals.clean_text_requested.emit)

        self.left_layout.addWidget(self.btn_load_machines)
        self.left_layout.addWidget(self.btn_generate_report)
        self.left_layout.addWidget(self.btn_confirm_order)
        self.left_layout.addWidget(self.btn_clean_text)

        # Wypycha dolne przyciski na dół (odpowiednik grid_rowconfigure w CTk)
        self.left_layout.addStretch()

        # --- Dolne przyciski ---
        self.btn_settings = QPushButton("Ustawienia")
        self.btn_settings.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_help = QPushButton("Pomoc")
        self.btn_help.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_about = QPushButton("O programie")
        self.btn_about.setCursor(Qt.CursorShape.PointingHandCursor)

        self.btn_settings.clicked.connect(self.signals.open_settings_requested.emit)
        self.btn_help.clicked.connect(self.signals.show_help_requested.emit)
        self.btn_about.clicked.connect(self.signals.show_about_requested.emit)

        self.left_layout.addWidget(self.btn_settings)
        self.left_layout.addWidget(self.btn_help)
        self.left_layout.addWidget(self.btn_about)

        self.main_layout.addWidget(self.left_panel)

    def _build_right_panel(self):
        # Odpowiednik self.right = ctk.CTkFrame
        self.right_panel = QFrame()
        self.right_panel.setObjectName("RightPanel")

        self.right_layout = QVBoxLayout(self.right_panel)
        self.right_layout.setContentsMargins(*RIGHT_PANEL_MARGINS)

        # Zbudowanie ekranu powitalnego wewnątrz prawego panelu
        self._build_welcome_screen()

        self.main_layout.addWidget(self.right_panel)

    def _build_welcome_screen(self):
        # Odpowiednik self.welcome_inner = ctk.CTkFrame(corner_radius=15)
        self.welcome_inner = QFrame()
        self.welcome_inner.setObjectName("WelcomeCard")

        welcome_layout = QVBoxLayout(self.welcome_inner)
        welcome_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_layout.setSpacing(WELCOME_SPACING)

        # --- Logo ASCII ---
        self.lbl_logo = QLabel(ASCII_LOGO.strip("\n"))
        self.lbl_logo.setObjectName("WelcomeLogo")
        self.lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_logo.ensurePolished()

        font_metrics = QFontMetrics(self.lbl_logo.font())
        logo_width = max(
            font_metrics.horizontalAdvance(line)
            for line in self.lbl_logo.text().splitlines()
        )
        self.lbl_logo.setMinimumWidth(logo_width)
        self.welcome_inner.setMinimumSize(
            logo_width + WELCOME_CARD_HORIZONTAL_PADDING,
            WELCOME_CARD_MIN_HEIGHT,
        )

        # --- Tytuł ---
        self.lbl_title = QLabel(HOME_SUBTITLE)
        self.lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_title.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")

        # --- Opis ---
        self.lbl_desc = QLabel(HOME_DESC)
        self.lbl_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_desc.setStyleSheet("color: #9aa0a6; font-size: 14px;")

        # --- Wersja ---
        self.lbl_ver = QLabel(HOME_VERSION)
        self.lbl_ver.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_ver.setStyleSheet("color: #a86b47; font-size: 13px; font-weight: bold;")

        # Składanie elementów na karcie
        welcome_layout.addWidget(self.lbl_logo)
        welcome_layout.addSpacing(WELCOME_LOGO_BOTTOM_SPACING)
        welcome_layout.addWidget(self.lbl_title)
        welcome_layout.addWidget(self.lbl_desc)
        welcome_layout.addSpacing(WELCOME_VERSION_TOP_SPACING)
        welcome_layout.addWidget(self.lbl_ver)

        # Centrowanie karty w prawym panelu za pomocą addStretch
        self.right_layout.addStretch()
        self.right_layout.addWidget(self.welcome_inner, 0, Qt.AlignmentFlag.AlignCenter)
        self.right_layout.addStretch()

    def show_welcome_screen(self):
        self.welcome_inner.show()

    def hide_welcome_screen(self):
        self.welcome_inner.hide()
