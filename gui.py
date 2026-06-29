"""
gui.py — واجهة رسومية احترافية مستوحاة من OpenAI Platform
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
from contextlib import redirect_stdout

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTabWidget, QTextEdit, QPushButton,
    QListWidget, QListWidgetItem, QMessageBox, QFrame,
    QSizePolicy, QScrollArea, QSlider,
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QTextCharFormat, QColor, QTextCursor

from core import Symptom
from symptom_mapper import map_text_to_symptoms
from main import ENGINES


# ── لوحة الألوان ─────────────────────────────────────────────────────────────
C = {
    # الشريط الجانبي (داكن)
    "sb_bg":          "#1a1a2e",
    "sb_hover":       "#252540",
    "sb_active":      "#16213e",
    "sb_border":      "#2a2a4a",
    "sb_text":        "#c8c8e0",
    "sb_text_dim":    "#5a5a7a",

    # المحتوى الرئيسي
    "bg":             "#f7f7f9",
    "card":           "#ffffff",
    "border":         "#e8e8ef",
    "border_focus":   "#10a37f",

    # النصوص
    "text":           "#1a1a2e",
    "text_muted":     "#6e6e8e",
    "text_hint":      "#9090b0",

    # اللون الأساسي
    "green":          "#10a37f",
    "green_hover":    "#0d8f6e",
    "green_light":    "#e6f7f2",
    "green_text":     "#0b7a60",

    # الحالات
    "amber":          "#f59e0b",
    "amber_light":    "#fef3c7",
    "red":            "#ef4444",
    "red_light":      "#fee2e2",

    # منطقة الإخراج
    "out_bg":         "#0f0f1a",
    "out_text":       "#cdd6f4",
    "out_green":      "#a6e3a1",
    "out_blue":       "#89b4fa",
    "out_yellow":     "#f9e2af",
    "out_red":        "#f38ba8",
    "out_dim":        "#45475a",
    "out_border":     "#1e1e3a",
}

STYLESHEET = f"""
/* ═══ القاعدة ═══ */
* {{ font-family: "Segoe UI", "Tahoma", "Arial", sans-serif; }}

QMainWindow {{ background: {C['bg']}; }}
QWidget#root {{ background: {C['bg']}; }}

/* ═══ شريط العنوان ═══ */
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

/* ═══ الشريط الجانبي ═══ */
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
    background: {C['green']};
    color: #ffffff;
    font-weight: 600;
}}

QLabel#sb_footer {{
    color: {C['sb_text_dim']};
    font-size: 11px;
    padding: 12px 16px;
}}

/* ═══ المحتوى ═══ */
QWidget#content {{
    background: {C['bg']};
}}

/* ═══ البطاقات ═══ */
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

/* ═══ التبويبات ═══ */
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
    color: {C['green']};
    border-bottom: 2px solid {C['green']};
}}
QTabBar::tab:hover:!selected {{
    color: {C['text']};
}}

/* ═══ حقل النص ═══ */
QTextEdit#nlp_input {{
    background: {C['bg']};
    border: 1.5px solid {C['border']};
    border-radius: 10px;
    padding: 12px 14px;
    font-size: 13px;
    color: {C['text']};
    line-height: 1.5;
    selection-background-color: {C['green_light']};
}}
QTextEdit#nlp_input:focus {{
    border: 1.5px solid {C['green']};
    background: {C['card']};
}}

/* ═══ قائمة الأعراض ═══ */
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
    background: {C['green_light']};
}}
QListWidget#sym_list::indicator {{
    width: 15px;
    height: 15px;
    border-radius: 3px;
    border: 2px solid {C['border']};
}}
QListWidget#sym_list::indicator:checked {{
    background: {C['green']};
    border: 2px solid {C['green']};
}}

/* ═══ الأزرار ═══ */
QPushButton#btn_primary {{
    background: {C['green']};
    color: #ffffff;
    font-size: 13px;
    font-weight: 700;
    padding: 10px 24px;
    border-radius: 8px;
    border: none;
    min-width: 130px;
}}
QPushButton#btn_primary:hover {{ background: {C['green_hover']}; }}
QPushButton#btn_primary:pressed {{ background: #0b7a60; }}

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
    border-color: #c0c0d8;
}}

QPushButton#btn_chip {{
    background: transparent;
    color: {C['green']};
    font-size: 11px;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 10px;
    border: 1px solid {C['green']};
    min-height: 22px;
}}
QPushButton#btn_chip:hover {{ background: {C['green_light']}; }}

/* ═══ الإخراج (Terminal) ═══ */
QTextEdit#output {{
    background: {C['out_bg']};
    color: {C['out_text']};
    font-family: "Cascadia Code", "JetBrains Mono", "Consolas", monospace;
    font-size: 13px;
    padding: 20px;
    border: 1px solid {C['out_border']};
    border-radius: 12px;
    line-height: 1.7;
    selection-background-color: #2a2a45;
}}

/* ═══ سجل التشخيصات ═══ */
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
    background: {C['green_light']};
}}

/* ═══ شرائح الأعراض ═══ */
QLabel#chip {{
    background: {C['green_light']};
    color: {C['green_text']};
    font-size: 11px;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 10px;
    border: 1px solid #a0dfd0;
}}

/* ═══ شريط الحالة ═══ */
QLabel#status {{
    color: {C['text_hint']};
    font-size: 11px;
    padding: 2px 0;
}}

/* ═══ الفاصل ═══ */
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

/* ═══ شريط التمرير ═══ */
QScrollBar:vertical {{
    background: transparent;
    width: 5px;
}}
QScrollBar::handle:vertical {{
    background: #ccccdd;
    border-radius: 2px;
    min-height: 24px;
}}
QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {{ height: 0; }}
"""

CROP_EMOJIS = {
    "تفاح": "🍎", "كرز": "🍒", "عنب": "🍇", "طماطم": "🍅",
    "بطاطا": "🥔", "حمضيات": "🍊", "كوسا": "🥒",
    "باذنجان": "🍆", "البصل": "🧅", "الثوم": "🧄",
}


class PlantDiseaseGUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("نظام تشخيص الأمراض النباتية")
        self.setMinimumSize(1020, 680)
        self.resize(1120, 740)
        self.setLayoutDirection(Qt.RightToLeft)
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

        # تحديد المحصول الأول
        self.crop_list.setCurrentRow(0)
        self._refresh_crop()

    # ─────────────────────── الشريط العلوي ──────────────────────────────────

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

        title = QLabel("نظام تشخيص الأمراض النباتية")
        title.setObjectName("app_title")
        col.addWidget(title)

        sub = QLabel("Plant Disease Expert System  ·  NLP + Rule-Based Diagnosis")
        sub.setObjectName("app_sub")
        col.addWidget(sub)

        h.addLayout(col)
        h.addStretch()

        badge = QLabel("NLP v2.0")
        badge.setStyleSheet(f"""
            background: {C['green_light']};
            color: {C['green_text']};
            font-size: 11px;
            font-weight: 700;
            padding: 5px 12px;
            border-radius: 8px;
            border: 1px solid #a0dfd0;
        """)
        h.addWidget(badge)
        return w

    # ─────────────────────── الشريط الجانبي ─────────────────────────────────

    def _make_sidebar(self) -> QWidget:
        w = QWidget()
        w.setObjectName("sidebar")
        w.setFixedWidth(210)
        v = QVBoxLayout(w)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(0)

        lbl = QLabel("CROP / المحصول")
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

        # شريط التذييل
        v.addWidget(self._make_hdiv_dark())
        footer = QLabel(f"  🌾  {len(ENGINES)} محاصيل · 35+ مرض")
        footer.setObjectName("sb_footer")
        footer.setAlignment(Qt.AlignCenter)
        v.addWidget(footer)

        return w

    # ─────────────────────── منطقة المحتوى ─────────────────────────────────

    def _make_content(self) -> QWidget:
        w = QWidget()
        w.setObjectName("content")
        v = QVBoxLayout(w)
        v.setContentsMargins(22, 18, 22, 16)
        v.setSpacing(14)

        v.addWidget(self._make_input_card())

        # صف الشرائح
        chips_row = QHBoxLayout()
        chips_row.setSpacing(8)
        chips_row.setAlignment(Qt.AlignRight)

        self.lbl_chips_prefix = QLabel("✅ أعراض مكتشفة:")
        self.lbl_chips_prefix.setObjectName("hint")
        self.lbl_chips_prefix.setVisible(False)
        chips_row.addWidget(self.lbl_chips_prefix)

        # حاوية الشرائح
        self.chips_container = QWidget()
        self.chips_h = QHBoxLayout(self.chips_container)
        self.chips_h.setContentsMargins(0, 0, 0, 0)
        self.chips_h.setSpacing(6)
        self.chips_container.setVisible(False)
        chips_row.addWidget(self.chips_container)
        chips_row.addStretch()

        v.addLayout(chips_row)

        # ─ فاصل ─
        v.addWidget(self._make_hdiv())

        # ─ منطقة الإخراج ─
        out_header = QHBoxLayout()
        out_lbl = QLabel("📊 النتيجة والتشخيص")
        out_lbl.setObjectName("card_title")
        out_header.addWidget(out_lbl)
        out_header.addStretch()

        self.lbl_status = QLabel("جاهز · اختر المحصول ثم أدخل الأعراض")
        self.lbl_status.setObjectName("status")
        out_header.addWidget(self.lbl_status)
        v.addLayout(out_header)

        self.output = QTextEdit()
        self.output.setObjectName("output")
        self.output.setReadOnly(True)
        self.output.setPlaceholderText(
            "ستظهر نتيجة التشخيص هنا بعد الضغط على زر «تشخيص» ..."
        )
        v.addWidget(self.output, 1)

        # ─ سجل التشخيصات ─
        hist_header = QHBoxLayout()
        hist_header.setSpacing(10)

        hist_lbl = QLabel("📜 سجل التشخيصات")
        hist_lbl.setObjectName("card_title")
        hist_header.addWidget(hist_lbl)

        self.history_toggle_btn = QPushButton("عرض")
        self.history_toggle_btn.setObjectName("btn_chip")
        self.history_toggle_btn.setCursor(Qt.PointingHandCursor)
        self.history_toggle_btn.clicked.connect(self._toggle_history)
        hist_header.addWidget(self.history_toggle_btn)

        self.history_count_lbl = QLabel("0 تشخيص")
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

    # ─────────────────────── بطاقة الإدخال ─────────────────────────────────

    def _make_input_card(self) -> QFrame:
        card = QFrame()
        card.setObjectName("card")
        v = QVBoxLayout(card)
        v.setContentsMargins(18, 14, 18, 14)
        v.setSpacing(10)

        # رأس البطاقة
        top_row = QHBoxLayout()
        top_lbl = QLabel("إدخال الأعراض")
        top_lbl.setObjectName("card_title")
        top_row.addWidget(top_lbl)
        top_row.addStretch()

        self.lbl_crop_badge = QLabel("")
        self.lbl_crop_badge.setStyleSheet(f"""
            background: {C['green_light']};
            color: {C['green_text']};
            font-size: 12px;
            font-weight: 700;
            padding: 4px 12px;
            border-radius: 9px;
            border: 1px solid #b0e8d8;
        """)
        top_row.addWidget(self.lbl_crop_badge)
        v.addLayout(top_row)

        # ─ التبويبات ─
        self.tabs = QTabWidget()
        self.tabs.setObjectName("tabs")
        self.tabs.setStyleSheet("QTabWidget::tab-bar { alignment: right; }")

        # تبويب NLP
        tab_nlp = QWidget()
        tn = QVBoxLayout(tab_nlp)
        tn.setContentsMargins(0, 10, 0, 0)
        tn.setSpacing(8)

        hint_nlp = QLabel(
            "✍️  صِف الأعراض بكلماتك — فصيح أو عامي "
        )
        hint_nlp.setObjectName("hint")
        tn.addWidget(hint_nlp)

        self.nlp_input = QTextEdit()
        self.nlp_input.setObjectName("nlp_input")
        self.nlp_input.setFixedHeight(82)
        self.nlp_input.setPlaceholderText(
            "مثال: الأوراق عم تصفر وتتساقط، في بقع لامعة زيتية على الورق..."
        )
        tn.addWidget(self.nlp_input)

        # أمثلة سريعة
        ex_row = QHBoxLayout()
        ex_row.setSpacing(6)
        ex_row.setAlignment(Qt.AlignRight)
        ex_lbl = QLabel("جرّب:")
        ex_lbl.setObjectName("hint")
        ex_row.addWidget(ex_lbl)

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

        # تبويب يدوي
        tab_manual = QWidget()
        tm = QVBoxLayout(tab_manual)
        tm.setContentsMargins(0, 10, 0, 0)
        tm.setSpacing(6)

        hint_m = QLabel("📋  اختر الأعراض من القائمة — يمكن تحديد أكثر من عرض")
        hint_m.setObjectName("hint")
        tm.addWidget(hint_m)

        self.sym_list = QListWidget()
        self.sym_list.setObjectName("sym_list")
        self.sym_list.setSelectionMode(QListWidget.NoSelection)
        self.sym_list.setFixedHeight(118)
        tm.addWidget(self.sym_list)

        # ─ شريط عامل الثقة (CF) ─
        cf_row = QHBoxLayout()
        cf_row.setSpacing(8)
        cf_label = QLabel("عامل الثقة (CF):")
        cf_label.setObjectName("hint")
        cf_row.addWidget(cf_label)

        self.cf_slider = QSlider(Qt.Horizontal)
        self.cf_slider.setObjectName("cf_slider")
        self.cf_slider.setRange(0, 100)
        self.cf_slider.setValue(100)
        self.cf_slider.setFixedHeight(22)
        self.cf_slider.setStyleSheet(f"""
            QSlider#cf_slider::groove:horizontal {{
                background: {C['border']};
                height: 6px;
                border-radius: 3px;
            }}
            QSlider#cf_slider::handle:horizontal {{
                background: {C['green']};
                width: 16px;
                height: 16px;
                margin: -5px 0;
                border-radius: 8px;
            }}
            QSlider#cf_slider::sub-page:horizontal {{
                background: {C['green']};
                border-radius: 3px;
            }}
        """)
        cf_row.addWidget(self.cf_slider, 1)

        self.cf_value_lbl = QLabel("100")
        self.cf_value_lbl.setObjectName("hint")
        self.cf_value_lbl.setFixedWidth(30)
        self.cf_slider.valueChanged.connect(
            lambda v: self.cf_value_lbl.setText(str(v))
        )
        cf_row.addWidget(self.cf_value_lbl)

        tm.addLayout(cf_row)

        self.tabs.addTab(tab_nlp, "🤖  التحليل الذكي")
        self.tabs.addTab(tab_manual, "📋  الاختيار اليدوي")
        v.addWidget(self.tabs)

        # أزرار التشغيل
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        btn_clr = QPushButton("مسح")
        btn_clr.setObjectName("btn_ghost")
        btn_clr.setCursor(Qt.PointingHandCursor)
        btn_clr.clicked.connect(self._clear)
        btn_row.addStretch()
        btn_row.addWidget(btn_clr)

        btn_diag = QPushButton("🔍  تشخيص")
        btn_diag.setObjectName("btn_primary")
        btn_diag.setCursor(Qt.PointingHandCursor)
        btn_diag.clicked.connect(self._diagnose)
        btn_row.addWidget(btn_diag)

        v.addLayout(btn_row)
        return card

    # ─────────────────────── المساعدات ──────────────────────────────────────

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
        # اسم المحصول بدون الإيموجي والمسافات
        return re.sub(r"[\s🍎🍒🍇🍅🥔🍊🥒🍆🧅🧄🌱]+", " ", item.text()).strip()

    def _refresh_crop(self):
        cls = self._engine_class()
        name = self._crop_name()
        if not cls:
            return

        self.lbl_crop_badge.setText(f"🌿 {name}")

        self.sym_list.clear()
        for sym in cls.SYMPTOMS:
            item = QListWidgetItem(f"  {sym}")
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.sym_list.addItem(item)

        self._clear_chips()
        self.lbl_status.setText(
            f"محصول: {name}  ·  {len(cls.SYMPTOMS)} عرض متاح"
        )

    def _inject_example(self, text: str):
        cur = self.nlp_input.toPlainText().strip()
        self.nlp_input.setText(f"{cur}، {text}" if cur else text)
        self.nlp_input.setFocus()

    def _clear(self):
        self.nlp_input.clear()
        for i in range(self.sym_list.count()):
            self.sym_list.item(i).setCheckState(Qt.Unchecked)
        self.output.clear()
        self._clear_chips()
        self.lbl_status.setText("تم المسح · جاهز للتشخيص من جديد")

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
        for sym in symptoms[:6]:          # أقصى 6 شرائح
            short = sym[:28] + "…" if len(sym) > 28 else sym
            chip = QLabel(short)
            chip.setObjectName("chip")
            chip.setToolTip(sym)
            self.chips_h.addWidget(chip)
        if len(symptoms) > 6:
            more = QLabel(f"+{len(symptoms)-6}")
            more.setObjectName("chip")
            self.chips_h.addWidget(more)

    # ─────────────────────── تشغيل المحرك ───────────────────────────────────

    def _run_engine(self, cls, facts: list) -> str:
        if not facts:
            return ""
        engine = cls()
        engine.reset()
        for f in facts:
            engine.declare(f)
        buf = io.StringIO()
        with redirect_stdout(buf):
            engine.run()
        return buf.getvalue().strip()

    # ─────────────────────── التشخيص ────────────────────────────────────────

    def _diagnose(self):
        cls = self._engine_class()
        name = self._crop_name()
        if not cls:
            QMessageBox.warning(self, "تنبيه", "اختر محصولاً أولاً.")
            return

        if self.tabs.currentIndex() == 0:
            self._run_nlp(cls, name)
        else:
            self._run_manual(cls, name)

    def _run_nlp(self, cls, name: str):
        text = self.nlp_input.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "تنبيه", "أدخل وصف الأعراض أولاً.")
            return

        detected = map_text_to_symptoms(text, crop_symptoms=cls.SYMPTOMS)

        if not detected:
            self._clear_chips()
            self._display_error(
                "لم يُكتشف أي عرض في النص",
                "جرّب:\n"
                "  • إعادة الصياغة بتفصيل أكبر\n"
                "  • استخدام الأمثلة السريعة كبداية\n"
                "  • التبديل إلى الاختيار اليدوي",
            )
            self.lbl_status.setText("لم يُكتشف أعراض · جرّب صياغة أخرى")
            return

        self._show_chips(detected)
        raw = self._run_engine(cls, [Symptom(name=s, cf=80) for s in detected])

        self._display_output(
            crop=name,
            mode="NLP",
            extra=f"النص: {text[:70]}{'…' if len(text)>70 else ''}",
            symptoms_count=len(detected),
            raw=raw,
        )
        self.lbl_status.setText(
            f"✅ {len(detected)} عرض مكتشف  ·  {name}  ·  CF افتراضي 80"
        )

    def _run_manual(self, cls, name: str):
        selected = []
        for i in range(self.sym_list.count()):
            item = self.sym_list.item(i)
            if item.checkState() == Qt.Checked:
                selected.append(Symptom(name=item.text().strip(), cf=self.cf_slider.value()))

        if not selected:
            QMessageBox.warning(self, "تنبيه", "حدّد عرضاً واحداً على الأقل.")
            return

        self._clear_chips()
        raw = self._run_engine(cls, selected)

        self._display_output(
            crop=name,
            mode="يدوي",
            symptoms_count=len(selected),
            raw=raw,
        )
        self.lbl_status.setText(
            f"✅ {len(selected)} أعراض يدوية  ·  {name}  ·  CF = {self.cf_slider.value()}"
        )

    # ─────────────────────── تنسيق الإخراج ─────────────────────────────────

    def _display_error(self, title: str, body: str):
        self.output.clear()
        cur = self.output.textCursor()

        def _write(text, color="#ef4444", bold=False, nl=True):
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

        # رأس الجلسة
        crop_emoji = CROP_EMOJIS.get(crop, "🌱")
        _w("─" * 48, color=C["out_dim"])
        _w(f"  {crop_emoji}  المحصول   :  {crop}", color=C["out_blue"], bold=True)
        _w(f"  📥  الإدخال   :  {mode}", color=C["out_dim"])
        if extra:
            _w(f"  📝  {extra}", color=C["out_dim"])
        _w(f"  🔎  الأعراض   :  {symptoms_count}", color=C["out_dim"])
        _w("─" * 48, color=C["out_dim"])

        if not raw:
            _w("")
            _w("⚠  لم يتمكن النظام من تحديد مرض محدد.", color=C["out_yellow"])
            _w("   أضِف أعراضاً أكثر لتحسين الدقة.", color=C["out_dim"])
            return

        _w("")

        # تلوين سطر المخرجات
        in_treatment = False
        for line in raw.split("\n"):
            stripped = line.strip()
            if not stripped:
                _w("")
                continue

            if "التشخيص:" in stripped:
                _w(stripped, color=C["out_green"], bold=True)
            elif "تشخيص مبدئي:" in stripped:
                _w(stripped, color=C["out_yellow"], bold=True)
            elif "احتمال ضعيف:" in stripped:
                _w(stripped, color=C["out_red"])
            elif "المسبب:" in stripped:
                _w(stripped, color=C["out_blue"])
            elif "العلاج" in stripped:
                in_treatment = True
                _w("")
                _w("╌" * 36, color=C["out_dim"])
                _w(stripped, color=C["out_yellow"], bold=True)
            elif stripped.startswith("- ") and in_treatment:
                _w(f"    ◈  {stripped[2:]}", color=C["out_green"])
            elif "درجة الثقة" in stripped:
                # visual confidence bar
                m = re.search(r"(\d+)/(\d+)", stripped)
                if m:
                    val, total = int(m.group(1)), int(m.group(2))
                    filled = round(val / total * 10) if total else 0
                    bar = "█" * filled + "░" * (10 - filled)
                    if val >= 70:
                        bar_color = C["out_green"]
                    elif val >= 50:
                        bar_color = C["out_yellow"]
                    else:
                        bar_color = C["out_red"]
                    _w(stripped, color=bar_color)
                    _w(f"    {bar}  {val}%", color=bar_color, bold=True)
                else:
                    _w(stripped, color=C["out_green"])
            elif stripped.startswith("─"):
                _w(stripped, color=C["out_dim"])
            else:
                _w(stripped, color=C["out_dim"])

        self.output.setTextCursor(
            self.output.document().find("")
        )
        # اذهب للأعلى
        sc = self.output.verticalScrollBar()
        if sc:
            sc.setValue(0)

        # سجل التشخيصات
        if not getattr(self, '_from_history', False):
            ts = datetime.now().strftime("%H:%M:%S")
            self.history.append({
                "crop": crop, "mode": mode,
                "symptoms_count": symptoms_count,
                "raw": raw, "timestamp": ts,
                "extra": extra,
            })
            self.history_count_lbl.setText(f"{len(self.history)} تشخيص")
            item = QListWidgetItem(
                f"{crop} · {mode} · {symptoms_count} أعراض · {ts}"
            )
            self.history_list.insertItem(0, item)

    def _toggle_history(self):
        visible = self.history_list.isVisible()
        self.history_list.setVisible(not visible)
        self.history_toggle_btn.setText("إخفاء" if not visible else "عرض")

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


# ── نقطة الدخول ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))

    win = PlantDiseaseGUI()
    win.show()
    sys.exit(app.exec_())