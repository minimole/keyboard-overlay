# shortcut_bar_widget.py — ショートカット説明を色分け1行で表示する Canvas ウィジェット

from __future__ import annotations
import tkinter as tk
import tkinter.font as tkfont
from typing import TYPE_CHECKING

from config import (
    SHORTCUT_BAR_BG,
    SHORTCUT_BAR_PADDING_X,
    SHORTCUT_BAR_FONT,
    SHORTCUT_BAR_FONT_SMALL,
    SHORTCUT_COLOR_CATEGORY,
    SHORTCUT_COLOR_WIN,
    SHORTCUT_COLOR_SEPARATOR,
    SHORTCUT_COLOR_MAC,
    SHORTCUT_COLOR_EQUALS,
    SHORTCUT_COLOR_DESCRIPTION,
)

if TYPE_CHECKING:
    from shortcuts import ShortcutEntry


# 6スロットのデフォルト設定（テキスト・色・フォント）
_EMPTY_SEGMENTS = [
    ("", SHORTCUT_COLOR_CATEGORY,    SHORTCUT_BAR_FONT),
    ("", SHORTCUT_COLOR_WIN,         SHORTCUT_BAR_FONT),
    ("", SHORTCUT_COLOR_SEPARATOR,   SHORTCUT_BAR_FONT_SMALL),
    ("", SHORTCUT_COLOR_MAC,         SHORTCUT_BAR_FONT),
    ("", SHORTCUT_COLOR_EQUALS,      SHORTCUT_BAR_FONT),
    ("", SHORTCUT_COLOR_DESCRIPTION, SHORTCUT_BAR_FONT),
]


class ShortcutBarWidget(tk.Canvas):
    """
    ショートカット説明を色分け1行で表示するウィジェット。

    起動時に6つの Canvas テキストアイテムを生成しておき、
    update() ごとに itemconfig + coords で差分更新のみ行う。
    全再描画は行わないため低負荷で動作する。
    """

    def __init__(self, master, width: int, height: int, **kwargs):
        super().__init__(
            master,
            width=width,
            height=height,
            bg=SHORTCUT_BAR_BG,
            highlightthickness=0,
            **kwargs,
        )
        self._width = width
        self._height = height
        self._text_ids: list[int] = []
        self._last_entry: "ShortcutEntry | None" = None   # 差分チェック用

        # フォントオブジェクトをキャッシュ（measure に使用）
        self._font_cache: dict[tuple, tkfont.Font] = {}

        self._build_slots()

    # ------------------------------------------------------------------
    # 公開 API
    # ------------------------------------------------------------------

    def update(self, entry: "ShortcutEntry | None"):
        """
        ショートカットエントリに基づいてバーを更新する。
        entry が前回と同一（is 比較）なら何もしない（差分更新）。
        """
        if entry is self._last_entry:
            return
        self._last_entry = entry

        if entry is None:
            self._clear_all()
            return

        segments = [
            (f"{entry.category}  ",  SHORTCUT_COLOR_CATEGORY,    SHORTCUT_BAR_FONT),
            (entry.win_label,        SHORTCUT_COLOR_WIN,          SHORTCUT_BAR_FONT),
            ("   ／   ",             SHORTCUT_COLOR_SEPARATOR,    SHORTCUT_BAR_FONT_SMALL),
            (entry.mac_label,        SHORTCUT_COLOR_MAC,          SHORTCUT_BAR_FONT),
            ("   ＝   ",             SHORTCUT_COLOR_EQUALS,       SHORTCUT_BAR_FONT),
            (entry.description,      SHORTCUT_COLOR_DESCRIPTION,  SHORTCUT_BAR_FONT),
        ]
        self._render_segments(segments)

    # ------------------------------------------------------------------
    # 内部処理
    # ------------------------------------------------------------------

    def _build_slots(self):
        """テキストスロットを6個生成（起動時1回のみ）。"""
        cy = self._height // 2
        for text, color, font in _EMPTY_SEGMENTS:
            tid = self.create_text(
                0, cy,
                text=text,
                fill=color,
                anchor="w",
                font=font,
            )
            self._text_ids.append(tid)

    def _clear_all(self):
        """全スロットを空文字・透明色にする。"""
        for tid in self._text_ids:
            self.itemconfig(tid, text="", fill="")

    def _render_segments(self, segments: list[tuple[str, str, tuple]]):
        """
        各セグメントを左から順に配置する。
        テキスト幅は tkfont.Font.measure() で計算（非表示状態でも動作する）。
        """
        x = SHORTCUT_BAR_PADDING_X
        cy = self._height // 2

        for i, (text, color, font) in enumerate(segments):
            tid = self._text_ids[i]
            self.itemconfig(tid, text=text, fill=color, font=font, anchor="w")
            self.coords(tid, x, cy)
            # テキスト幅を測定して次のスロットの x 座標を決定
            x += self._measure_text(text, font)

    def _measure_text(self, text: str, font: tuple) -> int:
        """フォントに応じたテキスト幅を返す（px）。"""
        if font not in self._font_cache:
            self._font_cache[font] = tkfont.Font(font=font)
        return self._font_cache[font].measure(text)
