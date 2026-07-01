"""
gui.py — Professional GUI inspired by OpenAI Platform (Dark & Blue Theme)
"""
import sys
import collections
import collections.abc

try:
    collections.Mapping  # noqa: B018
except AttributeError:
    collections.Mapping = collections.abc.Mapping

import io
import re
from datetime import datetime

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTabWidget, QTextEdit, QPushButton,
    QListWidget, QListWidgetItem, QMessageBox, QFrame,
    QSizePolicy, QScrollArea, QSlider, QSpinBox, QCheckBox,
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QTextCharFormat, QColor, QTextCursor

from core import Symptom
from symptom_mapper import map_text_to_symptoms
from main import ENGINES

C = {
    # Sidebar (Deep Dark)
    "sb_bg":          "#0a0b0e",
    "sb_hover":       "#14151a",
    "sb_active":      "#1e2028",
    "sb_border":      "#1a1b22",
    "sb_text":        "#a1a1aa",
    "sb_text_dim":    "#52525b",

    # Main Content
    "bg":             "#0f1115",
    "card":           "#181a20",
    "border":         "#272a35",
    "border_focus":   "#3b82f6",

    # Text
    "text":           "#e4e4e7",
    "text_muted":     "#a1a1aa",
    "text_hint":      "#71717a",

    # Primary Accent (Professional Blue)
    "blue":           "#3b82f6",
    "blue_hover":     "#2563eb",
    "blue_light":     "#172554",
    "blue_text":      "#60a5fa",
    "blue_border":    "#1e3a8a",

    # Status
    "amber":          "#f59e0b",
    "red":            "#ef4444",

    # Terminal Output
    "out_bg":         "#090a0c",
    "out_text":       "#cbd5e1",
    "out_blue":       "#60a5fa",
    "out_purple":     "#c084fc",
    "out_yellow":     "#fcd34d",
    "out_red":        "#fca5a5",
    "out_dim":        "#64748b",
    "out_border":     "#1e293b",
}

STYLESHEET = f"""
/* ═══ Base ═══ */
* {{ font-family: "Inter", "Segoe UI", "Arial", sans-serif; }}

QMainWindow {{ background: {C['bg']}; }}
QWidget#root {{ background: {C['bg']}; }}

/* ═══ Header ═══ */
QWidget#header {{
    background: {C['card']};
    border-bottom: 1px solid {C['border']};
}}

QLabel#app_title {{
    color: {C['text']};
    font-size: 17px;
    font-weight: 700;
    letter-spacing: -0.3px;
}}

QLabel#app_sub {{
    color: {C['text_muted']};
    font-size: 11px;
}}

/* ═══ Sidebar ═══ */
QWidget#sidebar {{
    background: {C['sb_bg']};
}}

QLabel#sb_section {{
    color: {C['sb_text_dim']};
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.5px;
    padding: 18px 16px 6px 16px;
}}

QListWidget#crop_list {{
    background: transparent;
    border: none;
    padding: 4px 8px;
    outline: none;
}}
QListWidget#crop_list::item {{
    color: {C['sb_text']};
    font-size: 13px;
    padding: 9px 12px;
    border-radius: 7px;
    margin: 1px 0;
}}
QListWidget#crop_list::item:hover {{
    background: {C['sb_hover']};
}}
QListWidget#crop_list::item:selected {{
    background: {C['blue']};
    color: #ffffff;
    font-weight: 600;
}}

QLabel#sb_footer {{
    color: {C['sb_text_dim']};
    font-size: 11px;
    padding: 12px 16px;
}}

/* ═══ Content ═══ */
QWidget#content {{
    background: {C['bg']};
}}

/* ═══ Cards ═══ */
QFrame#card {{
    background: {C['card']};
    border: 1px solid {C['border']};
    border-radius: 12px;
}}

QLabel#card_title {{
    color: {C['text']};
    font-size: 14px;
    font-weight: 700;
}}

QLabel#hint {{
    color: {C['text_muted']};
    font-size: 12px;
}}

/* ═══ Tabs ═══ */
QTabWidget#tabs::pane {{
    border: none;
    background: transparent;
}}

QTabBar::tab {{
    background: transparent;
    color: {C['text_muted']};
    font-size: 13px;
    font-weight: 600;
    padding: 7px 18px;
    border-bottom: 2px solid transparent;
    margin-bottom: -1px;
}}
QTabBar::tab:selected {{
    color: {C['blue']};
    border-bottom: 2px solid {C['blue']};
}}
QTabBar::tab:hover:!selected {{
    color: {C['text']};
}}

/* ═══ Text Input ═══ */
QTextEdit#nlp_input {{
    background: {C['bg']};
    border: 1.5px solid {C['border']};
    border-radius: 10px;
    padding: 12px 14px;
    font-size: 13px;
    color: {C['text']};
    line-height: 1.5;
    selection-background-color: {C['blue_light']};
}}
QTextEdit#nlp_input:focus {{
    border: 1.5px solid {C['blue']};
    background: {C['card']};
}}

/* ═══ Symptoms List ═══ */
QListWidget#sym_list {{
    background: {C['bg']};
    border: 1.5px solid {C['border']};
    border-radius: 10px;
    padding: 4px;
    outline: none;
    font-size: 13px;
    color: {C['text']};
}}
QListWidget#sym_list::item {{
    padding: 8px 10px;
    border-radius: 6px;
    margin: 1px 2px;
}}
QListWidget#sym_list::item:hover {{
    background: {C['blue_light']};
}}
QListWidget#sym_list::indicator {{
    width: 15px;
    height: 15px;
    border-radius: 3px;
    border: 2px solid {C['border']};
}}
QListWidget#sym_list::indicator:checked {{
    background: {C['blue']};
    border: 2px solid {C['blue']};
}}

/* ═══ Buttons ═══ */
QPushButton#btn_primary {{
    background: {C['blue']};
    color: #ffffff;
    font-size: 13px;
    font-weight: 700;
    padding: 10px 24px;
    border-radius: 8px;
    border: none;
    min-width: 130px;
}}
QPushButton#btn_primary:hover {{ background: {C['blue_hover']}; }}
QPushButton#btn_primary:pressed {{ background: #1d4ed8; }}

QPushButton#btn_ghost {{
    background: transparent;
    color: {C['text_muted']};
    font-size: 13px;
    font-weight: 600;
    padding: 9px 18px;
    border-radius: 8px;
    border: 1.5px solid {C['border']};
}}
QPushButton#btn_ghost:hover {{
    background: {C['bg']};
    color: {C['text']};
    border-color: #3f3f46;
}}

QPushButton#btn_chip {{
    background: transparent;
    color: {C['blue_text']};
    font-size: 11px;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 10px;
    border: 1px solid {C['blue_border']};
    min-height: 22px;
}}
QPushButton#btn_chip:hover {{ background: {C['blue_light']}; }}

/* ═══ Terminal Output ═══ */
QTextEdit#output {{
    background: {C['out_bg']};
    color: {C['out_text']};
    font-family: "Cascadia Code", "JetBrains Mono", "Consolas", monospace;
    font-size: 13px;
    padding: 20px;
    border: 1px solid {C['out_border']};
    border-radius: 12px;
    line-height: 1.7;
    selection-background-color: #1e293b;
}}

/* ═══ History List ═══ */
QListWidget#hist_list {{
    background: {C['bg']};
    border: 1.5px solid {C['border']};
    border-radius: 10px;
    padding: 4px;
    outline: none;
    font-size: 12px;
    color: {C['text']};
}}
QListWidget#hist_list::item {{
    padding: 7px 10px;
    border-radius: 6px;
    margin: 1px 2px;
}}
QListWidget#hist_list::item:hover {{
    background: {C['blue_light']};
}}

/* ═══ Symptom Chips ═══ */
QLabel#chip {{
    background: {C['blue_light']};
    color: {C['blue_text']};
    font-size: 11px;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 10px;
    border: 1px solid {C['blue_border']};
}}

/* ═══ Status Bar ═══ */
QLabel#status {{
    color: {C['text_hint']};
    font-size: 11px;
    padding: 2px 0;
}}

/* ═══ CF SpinBox ═══ */
QSpinBox#cf_spin {{
    background: {C['card']};
    border: 1.5px solid {C['border']};
    border-radius: 5px;
    padding: 1px 4px;
    font-size: 12px;
    font-weight: 700;
    color: {C['blue_text']};
    min-width: 46px;
    max-width: 46px;
}}
QSpinBox#cf_spin:focus {{
    border-color: {C['blue']};
}}

/* ═══ Symptoms CheckBox ═══ */
QCheckBox#sym_check {{
    color: {C['text']};
    font-size: 13px;
    spacing: 8px;
}}
QCheckBox#sym_check::indicator {{
    width: 16px;
    height: 16px;
    border-radius: 3px;
    border: 2px solid {C['border']};
}}
QCheckBox#sym_check::indicator:checked {{
    background: {C['blue']};
    border: 2px solid {C['blue']};
}}

/* ═══ Dividers ═══ */
QFrame#hdiv {{
    background: {C['border']};
    min-height: 1px;
    max-height: 1px;
}}
QFrame#vdiv {{
    background: {C['sb_border']};
    min-width: 1px;
    max-width: 1px;
}}

/* ═══ Scrollbar ═══ */
QScrollBar:vertical {{
    background: transparent;
    width: 5px;
}}
QScrollBar::handle:vertical {{
    background: #3f3f46;
    border-radius: 2px;
    min-height: 24px;
}}
QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {{ height: 0; }}
"""

CROP_EMOJIS = {
    # English Mappings
    "Apple": "🍎", "Cherry": "🍒", "Grape": "🍇", "Tomato": "🍅",
    "Potato": "🥔", "Citrus": "🍊", "Zucchini": "🥒",
    "Eggplant": "🍆", "Onion": "🧅", "Garlic": "🧄",
    # Arabic Fallbacks (in case backend is not translated)
    "تفاح": "🍎", "كرز": "🍒", "عنب": "🍇", "طماطم": "🍅",
    "بطاطا": "🥔", "حمضيات": "🍊", "كوسا": "🥒",
    "باذنجان": "🍆", "البصل": "🧅", "الثوم": "🧄",
}


class PlantDiseaseGUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Plant Disease Diagnosis System")
        self.setMinimumSize(1020, 680)
        self.resize(1120, 740)
        self.setLayoutDirection(Qt.LeftToRight)
        self.setStyleSheet(STYLESHEET)

        self.history = []

        root = QWidget()
        root.setObjectName("root")
        self.setCentralWidget(root)
        main_v = QVBoxLayout(root)
        main_v.setContentsMargins(0, 0, 0, 0)
        main_v.setSpacing(0)

        main_v.addWidget(self._make_header())
        main_v.addWidget(self._make_hdiv())

        body = QWidget()
        body.setObjectName("root")
        body_h = QHBoxLayout(body)
        body_h.setContentsMargins(0, 0, 0, 0)
        body_h.setSpacing(0)

        body_h.addWidget(self._make_sidebar())
        body_h.addWidget(self._make_vdiv())
        body_h.addWidget(self._make_content(), 1)

        main_v.addWidget(body, 1)

        # Select first crop by default
        self.crop_list.setCurrentRow(0)
        self._refresh_crop()

    # ─────────────────────── Header ──────────────────────────────────────────

    def _make_header(self) -> QWidget:
        w = QWidget()
        w.setObjectName("header")
        w.setFixedHeight(58)
        h = QHBoxLayout(w)
        h.setContentsMargins(22, 0, 22, 0)
        h.setSpacing(10)

        icon = QLabel("🌿")
        icon.setFont(QFont("Segoe UI Emoji", 22))
        icon.setFixedWidth(30)
        h.addWidget(icon)

        col = QVBoxLayout()
        col.setSpacing(1)

        title = QLabel("Plant Disease Diagnosis System")
        title.setObjectName("app_title")
        col.addWidget(title)

        sub = QLabel("Plant Disease Expert System  ·  NLP + Rule-Based Diagnosis")
        sub.setObjectName("app_sub")
        col.addWidget(sub)

        h.addLayout(col)
        h.addStretch()

        badge = QLabel("NLP v2.0")
        badge.setStyleSheet(f"""
            background: {C['blue_light']};
            color: {C['blue_text']};
            font-size: 11px;
            font-weight: 700;
            padding: 5px 12px;
            border-radius: 8px;
            border: 1px solid {C['blue_border']};
        """)
        h.addWidget(badge)
        return w

    # ─────────────────────── Sidebar ─────────────────────────────────────────

    def _make_sidebar(self) -> QWidget:
        w = QWidget()
        w.setObjectName("sidebar")
        w.setFixedWidth(210)
        v = QVBoxLayout(w)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(0)

        lbl = QLabel("CROP / PLANT")
        lbl.setObjectName("sb_section")
        v.addWidget(lbl)

        self.crop_list = QListWidget()
        self.crop_list.setObjectName("crop_list")
        self.crop_list.setFocusPolicy(Qt.NoFocus)
        self.crop_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        for _, (name, cls) in ENGINES.items():
            em = CROP_EMOJIS.get(name, "🌱")
            item = QListWidgetItem(f"  {em}  {name}")
            item.setData(Qt.UserRole, cls)
            item.setSizeHint(QSize(190, 38))
            self.crop_list.addItem(item)

        self.crop_list.currentItemChanged.connect(lambda *_: self._refresh_crop())
        v.addWidget(self.crop_list, 1)

        # Footer
        v.addWidget(self._make_hdiv_dark())
        footer = QLabel(f"  🌾  {len(ENGINES)} Crops · 35+ Diseases")
        footer.setObjectName("sb_footer")
        footer.setAlignment(Qt.AlignCenter)
        v.addWidget(footer)

        return w

    # ─────────────────────── Main Content ────────────────────────────────────

    def _make_content(self) -> QWidget:
        w = QWidget()
        w.setObjectName("content")
        v = QVBoxLayout(w)
        v.setContentsMargins(22, 18, 22, 16)
        v.setSpacing(14)

        v.addWidget(self._make_input_card())

        # Detected Chips Row
        chips_row = QHBoxLayout()
        chips_row.setSpacing(8)
        chips_row.setAlignment(Qt.AlignLeft)

        self.lbl_chips_prefix = QLabel("✅ Detected Symptoms:")
        self.lbl_chips_prefix.setObjectName("hint")
        self.lbl_chips_prefix.setVisible(False)
        chips_row.addWidget(self.lbl_chips_prefix)

        self.chips_container = QWidget()
        self.chips_h = QHBoxLayout(self.chips_container)
        self.chips_h.setContentsMargins(0, 0, 0, 0)
        self.chips_h.setSpacing(6)
        self.chips_container.setVisible(False)
        chips_row.addWidget(self.chips_container)
        chips_row.addStretch()

        v.addLayout(chips_row)

        # ─ Divider ─
        v.addWidget(self._make_hdiv())

        # ─ Output Area ─
        out_header = QHBoxLayout()
        out_lbl = QLabel("📊 Result & Diagnosis")
        out_lbl.setObjectName("card_title")
        out_header.addWidget(out_lbl)
        out_header.addStretch()

        self.lbl_status = QLabel("Ready · Select crop then enter symptoms")
        self.lbl_status.setObjectName("status")
        out_header.addWidget(self.lbl_status)
        v.addLayout(out_header)

        self.output = QTextEdit()
        self.output.setObjectName("output")
        self.output.setReadOnly(True)
        self.output.setPlaceholderText(
            "Diagnosis result will appear here after clicking 'Diagnose' ..."
        )
        v.addWidget(self.output, 1)

        # ─ History ─
        hist_header = QHBoxLayout()
        hist_header.setSpacing(10)

        hist_lbl = QLabel("📜 Diagnosis History")
        hist_lbl.setObjectName("card_title")
        hist_header.addWidget(hist_lbl)

        self.history_toggle_btn = QPushButton("Show")
        self.history_toggle_btn.setObjectName("btn_chip")
        self.history_toggle_btn.setCursor(Qt.PointingHandCursor)
        self.history_toggle_btn.clicked.connect(self._toggle_history)
        hist_header.addWidget(self.history_toggle_btn)

        self.history_count_lbl = QLabel("0 Diagnoses")
        self.history_count_lbl.setObjectName("hint")
        hist_header.addWidget(self.history_count_lbl)

        hist_header.addStretch()
        v.addLayout(hist_header)

        self.history_list = QListWidget()
        self.history_list.setObjectName("hist_list")
        self.history_list.setFixedHeight(120)
        self.history_list.setVisible(False)
        self.history_list.setFocusPolicy(Qt.NoFocus)
        self.history_list.clicked.connect(self._show_history_item)
        v.addWidget(self.history_list)

        return w

    # ─────────────────────── Input Card ──────────────────────────────────────

    def _make_input_card(self) -> QFrame:
        card = QFrame()
        card.setObjectName("card")
        v = QVBoxLayout(card)
        v.setContentsMargins(18, 14, 18, 14)
        v.setSpacing(10)

        # Card Header
        top_row = QHBoxLayout()
        top_lbl = QLabel("Symptom Input")
        top_lbl.setObjectName("card_title")
        top_row.addWidget(top_lbl)
        top_row.addStretch()

        self.lbl_crop_badge = QLabel("")
        self.lbl_crop_badge.setStyleSheet(f"""
            background: {C['blue_light']};
            color: {C['blue_text']};
            font-size: 12px;
            font-weight: 700;
            padding: 4px 12px;
            border-radius: 9px;
            border: 1px solid {C['blue_border']};
        """)
        top_row.addWidget(self.lbl_crop_badge)
        v.addLayout(top_row)

        # ─ Tabs ─
        self.tabs = QTabWidget()
        self.tabs.setObjectName("tabs")
        self.tabs.setStyleSheet("QTabWidget::tab-bar { alignment: left; }")

        # NLP Tab
        tab_nlp = QWidget()
        tn = QVBoxLayout(tab_nlp)
        tn.setContentsMargins(0, 10, 0, 0)
        tn.setSpacing(8)

        hint_nlp = QLabel(
            "✍️  Describe symptoms in your own words"
        )
        hint_nlp.setObjectName("hint")
        tn.addWidget(hint_nlp)

        self.nlp_input = QTextEdit()
        self.nlp_input.setObjectName("nlp_input")
        self.nlp_input.setFixedHeight(82)
        self.nlp_input.setPlaceholderText(
            "Example: Leaves are yellowing and falling, there are shiny oily spots..."
        )
        tn.addWidget(self.nlp_input)

        # Quick Examples
        ex_row = QHBoxLayout()
        ex_row.setSpacing(6)
        ex_row.setAlignment(Qt.AlignLeft)
        ex_lbl = QLabel("Try:")
        ex_lbl.setObjectName("hint")
        ex_row.addWidget(ex_lbl)

        # Translated Quick Examples (feel free to change based on the crop context)
        for sample in ["الورق اصفر", "تعفن الثمار", "بقع بيضاء", "ذبول مفاجئ"]:
            btn = QPushButton(sample)
            btn.setObjectName("btn_chip")
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(
                lambda checked, t=sample: self._inject_example(t)
            )
            ex_row.addWidget(btn)
        ex_row.addStretch()
        tn.addLayout(ex_row)

        # ─ NLP Detected Symptoms CF Area ─
        self._nlp_cf_widget = QWidget()
        self._nlp_cf_widget.setVisible(False)
        nlp_cf_lay = QVBoxLayout(self._nlp_cf_widget)
        nlp_cf_lay.setContentsMargins(0, 4, 0, 0)
        nlp_cf_lay.setSpacing(3)

        nlp_cf_hdr = QLabel("✅ Detected Symptoms — set confidence factor (CF) for each:")
        nlp_cf_hdr.setObjectName("hint")
        nlp_cf_lay.addWidget(nlp_cf_hdr)

        self._nlp_cf_scroll = QScrollArea()
        self._nlp_cf_scroll.setWidgetResizable(True)
        self._nlp_cf_scroll.setFixedHeight(90)
        self._nlp_cf_scroll.setStyleSheet(f"""
            QScrollArea {{
                border: 1.5px solid {C['blue_border']};
                border-radius: 8px;
                background: {C['blue_light']};
            }}
            QScrollArea > QWidget > QWidget {{
                background: {C['blue_light']};
            }}
        """)
        self._nlp_cf_inner = QWidget()
        self._nlp_cf_inner.setStyleSheet(f"background: {C['blue_light']};" )
        self._nlp_cf_vlay = QVBoxLayout(self._nlp_cf_inner)
        self._nlp_cf_vlay.setContentsMargins(6, 4, 6, 4)
        self._nlp_cf_vlay.setSpacing(2)
        self._nlp_cf_scroll.setWidget(self._nlp_cf_inner)
        nlp_cf_lay.addWidget(self._nlp_cf_scroll)
        tn.addWidget(self._nlp_cf_widget)

        self._nlp_cf_widgets: dict[str, QSpinBox] = {}

        # Manual Tab
        tab_manual = QWidget()
        tm = QVBoxLayout(tab_manual)
        tm.setContentsMargins(0, 10, 0, 0)
        tm.setSpacing(4)

        hint_m = QLabel("📋  Select symptoms and set confidence factor (CF) for each")
        hint_m.setObjectName("hint")
        tm.addWidget(hint_m)

        self._sym_scroll = QScrollArea()
        self._sym_scroll.setWidgetResizable(True)
        self._sym_scroll.setFixedHeight(155)
        self._sym_scroll.setStyleSheet(f"""
            QScrollArea {{
                border: 1.5px solid {C['border']};
                border-radius: 10px;
                background: {C['bg']};
            }}
            QScrollArea > QWidget > QWidget {{
                background: {C['bg']};
            }}
        """)

        self._sym_container = QWidget()
        self._sym_container.setStyleSheet(f"background: {C['bg']};" )
        self._sym_vlay = QVBoxLayout(self._sym_container)
        self._sym_vlay.setContentsMargins(6, 4, 6, 4)
        self._sym_vlay.setSpacing(2)
        self._sym_vlay.addStretch()

        self._sym_scroll.setWidget(self._sym_container)
        tm.addWidget(self._sym_scroll)

        self._sym_widgets: dict[str, tuple] = {}

        self.tabs.addTab(tab_nlp, "🤖  Smart Analysis (NLP)")
        self.tabs.addTab(tab_manual, "📋  Manual Selection")
        v.addWidget(self.tabs)

        # Action Buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        btn_clr = QPushButton("Clear")
        btn_clr.setObjectName("btn_ghost")
        btn_clr.setCursor(Qt.PointingHandCursor)
        btn_clr.clicked.connect(self._clear)
        btn_row.addStretch()
        btn_row.addWidget(btn_clr)

        self.btn_detect = QPushButton("🔎  Detect Symptoms")
        self.btn_detect.setObjectName("btn_ghost")
        self.btn_detect.setCursor(Qt.PointingHandCursor)
        self.btn_detect.clicked.connect(self._detect_only)
        btn_row.addWidget(self.btn_detect)

        btn_diag = QPushButton("🩺  Diagnose")
        btn_diag.setObjectName("btn_primary")
        btn_diag.setCursor(Qt.PointingHandCursor)
        btn_diag.clicked.connect(self._diagnose)
        btn_row.addWidget(btn_diag)

        self.tabs.currentChanged.connect(
            lambda i: self.btn_detect.setVisible(i == 0)
        )

        v.addLayout(btn_row)
        return card

    # ─────────────────────── Helpers ─────────────────────────────────────────

    def _make_hdiv(self) -> QFrame:
        f = QFrame()
        f.setObjectName("hdiv")
        return f

    def _make_hdiv_dark(self) -> QFrame:
        f = QFrame()
        f.setFrameShape(QFrame.HLine)
        f.setStyleSheet(f"background: {C['sb_border']}; min-height: 1px; max-height: 1px;")
        return f

    def _make_vdiv(self) -> QFrame:
        f = QFrame()
        f.setObjectName("vdiv")
        return f

    def _engine_class(self):
        item = self.crop_list.currentItem()
        return item.data(Qt.UserRole) if item else None

    def _crop_name(self) -> str:
        item = self.crop_list.currentItem()
        if not item:
            return ""
        return re.sub(r"[\s🍎🍒🍇🍅🥔🍊🥒🍆🧅🧄🌱]+", " ", item.text()).strip()

    def _refresh_crop(self):
        cls = self._engine_class()
        name = self._crop_name()
        if not cls:
            return

        self.lbl_crop_badge.setText(f"🌿 {name}")

        self._sym_widgets.clear()
        while self._sym_vlay.count():
            item = self._sym_vlay.takeAt(0)
            w = item.widget()
            if w:
                w.setParent(None)
                w.deleteLater()

        for sym in cls.SYMPTOMS:
            row_w = QWidget()
            row_w.setObjectName("sym_row")
            row_h = QHBoxLayout(row_w)
            row_h.setContentsMargins(4, 2, 4, 2)
            row_h.setSpacing(6)

            chk = QCheckBox(sym)
            chk.setObjectName("sym_check")
            chk.setChecked(False)
            row_h.addWidget(chk, 1)

            sld = QSlider(Qt.Horizontal)
            sld.setRange(0, 100)
            sld.setValue(80)
            sld.setFixedWidth(80)
            sld.setFixedHeight(18)
            sld.setEnabled(False)
            sld.setStyleSheet(f"""
                QSlider::groove:horizontal {{
                    background: {C['border']};
                    height: 4px; border-radius: 2px;
                }}
                QSlider::handle:horizontal {{
                    background: {C['blue']};
                    width: 12px; height: 12px;
                    margin: -4px 0; border-radius: 6px;
                }}
                QSlider::sub-page:horizontal {{
                    background: {C['blue']};
                    border-radius: 2px;
                }}
                QSlider:disabled::groove:horizontal {{
                    background: {C['border']};
                }}
                QSlider:disabled::handle:horizontal {{
                    background: #3f3f46;
                }}
            """)
            row_h.addWidget(sld)

            spn = QSpinBox()
            spn.setObjectName("cf_spin")
            spn.setRange(0, 100)
            spn.setValue(80)
            spn.setEnabled(False)
            spn.setSuffix("%")
            spn.setButtonSymbols(QSpinBox.NoButtons)
            row_h.addWidget(spn)

            sld.valueChanged.connect(spn.setValue)
            spn.valueChanged.connect(sld.setValue)

            def _toggle(checked, s=sld, sp=spn):
                s.setEnabled(checked)
                sp.setEnabled(checked)

            chk.toggled.connect(_toggle)

            self._sym_vlay.addWidget(row_w)
            self._sym_widgets[sym] = (chk, spn)

        self._sym_vlay.addStretch()

        self._clear_chips()
        self._nlp_cf_widget.setVisible(False)
        self._nlp_cf_widgets.clear()
        while self._nlp_cf_vlay.count():
            item = self._nlp_cf_vlay.takeAt(0)
            w = item.widget()
            if w:
                w.setParent(None)
                w.deleteLater()
        self.lbl_status.setText(
            f"Crop: {name}  ·  {len(cls.SYMPTOMS)} available symptoms"
        )

    def _inject_example(self, text: str):
        cur = self.nlp_input.toPlainText().strip()
        self.nlp_input.setText(f"{cur}, {text}" if cur else text)
        self.nlp_input.setFocus()

    def _clear(self):
        self.nlp_input.clear()
        for sym, (chk, spn) in self._sym_widgets.items():
            chk.setChecked(False)
            spn.setValue(80)
        self._nlp_cf_widget.setVisible(False)
        self._nlp_cf_widgets.clear()
        while self._nlp_cf_vlay.count():
            item = self._nlp_cf_vlay.takeAt(0)
            w = item.widget()
            if w:
                w.setParent(None)
                w.deleteLater()
        self.output.clear()
        self._clear_chips()
        self.lbl_status.setText("Cleared · Ready for new diagnosis")

    def _clear_chips(self):
        while self.chips_h.count():
            w = self.chips_h.takeAt(0).widget()
            if w:
                w.deleteLater()
        self.chips_container.setVisible(False)
        self.lbl_chips_prefix.setVisible(False)

    def _show_chips(self, symptoms: list):
        self._clear_chips()
        if not symptoms:
            return
        self.lbl_chips_prefix.setVisible(True)
        self.chips_container.setVisible(True)
        for sym in symptoms[:6]:
            short = sym[:28] + "…" if len(sym) > 28 else sym
            chip = QLabel(short)
            chip.setObjectName("chip")
            chip.setToolTip(sym)
            self.chips_h.addWidget(chip)
        if len(symptoms) > 6:
            more = QLabel(f"+{len(symptoms)-6}")
            more.setObjectName("chip")
            self.chips_h.addWidget(more)

    # ─────────────────────── Engine Execution ────────────────────────────────

    def _run_engine(self, cls, facts: list) -> str:
        if not facts:
            return ""
        import sys as _sys
        buf = io.StringIO()
        old_stdout = _sys.stdout
        try:
            _sys.stdout = buf
            engine = cls()
            engine.reset()
            for f in facts:
                engine.declare(f)
            engine.run()
        except Exception as e:
            _sys.stdout = old_stdout
            return f"[Engine Error: {e}]"
        finally:
            _sys.stdout = old_stdout
        return buf.getvalue().strip()

    # ─────────────────────── Diagnosis ───────────────────────────────────────

    def _diagnose(self):
        cls = self._engine_class()
        name = self._crop_name()
        if not cls:
            QMessageBox.warning(self, "Warning", "Please select a crop first.")
            return

        if self.tabs.currentIndex() == 0:
            if self._nlp_cf_widgets:
                text = self.nlp_input.toPlainText().strip()
                self._run_nlp_diagnose(cls, name, text)
            else:
                self._run_nlp(cls, name)
        else:
            self._run_manual(cls, name)

    def _run_nlp(self, cls, name: str):
        text = self.nlp_input.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "Warning", "Please enter symptom description first.")
            return

        detected = map_text_to_symptoms(text, crop_symptoms=cls.SYMPTOMS)

        if not detected:
            self._clear_chips()
            self._nlp_cf_widget.setVisible(False)
            self._display_error(
                "No symptoms detected in text",
                "Try:\n"
                "  • Rephrasing with more details\n"
                "  • Using quick examples to start\n"
                "  • Switching to manual selection",
            )
            self.lbl_status.setText("No symptoms detected · Try another phrasing")
            return

        self._nlp_cf_widgets.clear()
        while self._nlp_cf_vlay.count():
            item = self._nlp_cf_vlay.takeAt(0)
            w = item.widget()
            if w:
                w.setParent(None)
                w.deleteLater()

        for sym in detected:
            row_w = QWidget()
            row_w.setStyleSheet("background: transparent;")
            row_h = QHBoxLayout(row_w)
            row_h.setContentsMargins(2, 1, 2, 1)
            row_h.setSpacing(6)

            lbl = QLabel(f"✔ {sym}")
            lbl.setStyleSheet(f"color: {C['blue_text']}; font-size: 12px; font-weight: 600;")
            row_h.addWidget(lbl, 1)

            sld = QSlider(Qt.Horizontal)
            sld.setRange(0, 100)
            sld.setValue(80)
            sld.setFixedWidth(70)
            sld.setFixedHeight(16)
            sld.setStyleSheet(f"""
                QSlider::groove:horizontal {{ background: {C['blue_border']}; height: 4px; border-radius: 2px; }}
                QSlider::handle:horizontal {{ background: {C['blue']}; width: 12px; height: 12px; margin: -4px 0; border-radius: 6px; }}
                QSlider::sub-page:horizontal {{ background: {C['blue']}; border-radius: 2px; }}
            """)
            row_h.addWidget(sld)

            spn = QSpinBox()
            spn.setRange(0, 100)
            spn.setValue(80)
            spn.setSuffix("%")
            spn.setButtonSymbols(QSpinBox.NoButtons)
            spn.setFixedWidth(52)
            spn.setStyleSheet(f"""
                QSpinBox {{
                    background: {C['card']}; border: 1px solid {C['blue']};
                    border-radius: 4px; padding: 1px 3px;
                    font-size: 12px; font-weight: 700; color: {C['blue_text']};
                }}
            """)
            sld.valueChanged.connect(spn.setValue)
            spn.valueChanged.connect(sld.setValue)
            row_h.addWidget(spn)

            self._nlp_cf_vlay.addWidget(row_w)
            self._nlp_cf_widgets[sym] = spn

        self._nlp_cf_widget.setVisible(True)
        self._show_chips(detected)
        self.lbl_status.setText(
            f"✅ {len(detected)} symptoms detected · Adjust CF then Diagnose"
        )

    def _detect_only(self):
        cls = self._engine_class()
        name = self._crop_name()
        if not cls:
            QMessageBox.warning(self, "Warning", "Please select a crop first.")
            return
        self._run_nlp(cls, name)

    def _run_nlp_diagnose(self, cls, name: str, text: str):
        if not self._nlp_cf_widgets:
            QMessageBox.warning(self, "Warning", "Enter text first to detect symptoms.")
            return

        facts = [Symptom(name=sym, cf=spn.value()) for sym, spn in self._nlp_cf_widgets.items()]
        raw = self._run_engine(cls, facts)
        self._display_output(
            crop=name,
            mode="NLP",
            extra=f"Text: {text[:70]}{'…' if len(text)>70 else ''}",
            symptoms_count=len(facts),
            raw=raw,
        )
        self.lbl_status.setText(f"✅ {len(facts)} symptoms · {name}")

    def _run_manual(self, cls, name: str):
        selected = []
        for sym, (chk, spn) in self._sym_widgets.items():
            if chk.isChecked():
                selected.append(Symptom(name=sym, cf=spn.value()))

        if not selected:
            QMessageBox.warning(self, "Warning", "Select at least one symptom.")
            return

        self._clear_chips()
        raw = self._run_engine(cls, selected)

        if not raw:
            self._display_error(
                "System could not diagnose the disease",
                "  • Ensure CF >= 60%\n"
                "  • Add more symptoms for better accuracy",
            )
            self.lbl_status.setText(f"⚠ No diagnosis · Check CF or add symptoms")
            return

        self._display_output(
            crop=name,
            mode="Manual",
            symptoms_count=len(selected),
            raw=raw,
        )
        self.lbl_status.setText(f"✅ {len(selected)} manual symptoms  ·  {name}")

    # ─────────────────────── Output Formatting ───────────────────────────────

    def _display_error(self, title: str, body: str):
        self.output.clear()
        cur = self.output.textCursor()

        def _write(text, color=C["out_red"], bold=False, nl=True):
            fmt = QTextCharFormat()
            fmt.setForeground(QColor(color))
            if bold:
                fmt.setFontWeight(QFont.Bold)
            cur.setCharFormat(fmt)
            cur.insertText(text + ("\n" if nl else ""))

        _write("⚠  " + title, color=C["out_yellow"], bold=True)
        _write("", color=C["out_dim"])
        for line in body.split("\n"):
            _write(line, color=C["out_text"])

    def _display_output(
        self,
        crop: str,
        mode: str,
        symptoms_count: int,
        raw: str,
        extra: str = "",
    ):
        self.output.clear()
        cur = self.output.textCursor()

        def _w(text, color=C["out_text"], bold=False, nl=True):
            fmt = QTextCharFormat()
            fmt.setForeground(QColor(color))
            if bold:
                fmt.setFontWeight(QFont.Bold)
            cur.setCharFormat(fmt)
            cur.insertText(text + ("\n" if nl else ""))

        crop_emoji = CROP_EMOJIS.get(crop, "🌱")
        _w("─" * 48, color=C["out_dim"])
        _w(f"  {crop_emoji}  Crop      :  {crop}", color=C["out_blue"], bold=True)
        _w(f"  📥  Input     :  {mode}", color=C["out_dim"])
        if extra:
            _w(f"  📝  {extra}", color=C["out_dim"])
        _w(f"  🔎  Symptoms  :  {symptoms_count}", color=C["out_dim"])
        _w("─" * 48, color=C["out_dim"])

        if not raw:
            _w("")
            _w("⚠  System could not determine a specific disease.", color=C["out_yellow"])
            _w("   Add more symptoms to improve accuracy.", color=C["out_dim"])
            return

        _w("")

        in_treatment = False
        for line in raw.split("\n"):
            stripped = line.strip()
            if not stripped:
                _w("")
                continue

            if "Diagnosis:" in stripped or "التشخيص:" in stripped:
                _w(stripped, color=C["out_blue"], bold=True)
            elif "Preliminary Diagnosis:" in stripped or "تشخيص مبدئي:" in stripped:
                _w(stripped, color=C["out_yellow"], bold=True)
            elif "Low Probability:" in stripped or "احتمال ضعيف:" in stripped:
                _w(stripped, color=C["out_red"])
            elif "Cause:" in stripped or "المسبب:" in stripped:
                _w(stripped, color=C["out_purple"])
            elif "Treatment" in stripped or "العلاج" in stripped:
                in_treatment = True
                _w("")
                _w("╌" * 36, color=C["out_dim"])
                _w(stripped, color=C["out_yellow"], bold=True)
            elif stripped.startswith("- ") and in_treatment:
                _w(f"    ◈  {stripped[2:]}", color=C["out_blue"])
            elif "Confidence" in stripped or "درجة الثقة" in stripped:
                m = re.search(r"(\d+)/(\d+)", stripped)
                if m:
                    val, total = int(m.group(1)), int(m.group(2))
                    filled = round(val / total * 10) if total else 0
                    bar = "█" * filled + "░" * (10 - filled)
                    if val >= 70:
                        bar_color = C["out_blue"]
                    elif val >= 50:
                        bar_color = C["out_yellow"]
                    else:
                        bar_color = C["out_red"]
                    _w(stripped, color=bar_color)
                    _w(f"    {bar}  {val}%", color=bar_color, bold=True)
                else:
                    _w(stripped, color=C["out_blue"])
            elif stripped.startswith("─"):
                _w(stripped, color=C["out_dim"])
            else:
                _w(stripped, color=C["out_dim"])

        start_cursor = self.output.textCursor()
        start_cursor.movePosition(QTextCursor.Start)
        self.output.setTextCursor(start_cursor)
        sc = self.output.verticalScrollBar()
        if sc:
            sc.setValue(0)

        if not getattr(self, '_from_history', False):
            ts = datetime.now().strftime("%H:%M:%S")
            self.history.append({
                "crop": crop, "mode": mode,
                "symptoms_count": symptoms_count,
                "raw": raw, "timestamp": ts,
                "extra": extra,
            })
            self.history_count_lbl.setText(f"{len(self.history)} Diagnoses")
            item = QListWidgetItem(
                f"{crop} · {mode} · {symptoms_count} symptoms · {ts}"
            )
            self.history_list.insertItem(0, item)

    def _toggle_history(self):
        visible = self.history_list.isVisible()
        self.history_list.setVisible(not visible)
        self.history_toggle_btn.setText("Hide" if not visible else "Show")

    def _show_history_item(self, index):
        if not index.isValid():
            return
        row = self.history_list.count() - 1 - index.row()
        entry = self.history[row]
        self._from_history = True
        try:
            self._display_output(
                crop=entry["crop"],
                mode=entry["mode"],
                symptoms_count=entry["symptoms_count"],
                raw=entry["raw"],
                extra=entry.get("extra", ""),
            )
        finally:
            self._from_history = False


# ── Entry Point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Inter", 10))

    win = PlantDiseaseGUI()
    win.show()
    sys.exit(app.exec_())