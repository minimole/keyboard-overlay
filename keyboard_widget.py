# keyboard_widget.py — tkinter Canvas でキーボードを描画するウィジェット

import tkinter as tk
from config import (
    KEYBOARD_ROWS, KEY_NORMAL_BG, KEY_PRESSED_BG,
    KEY_NORMAL_FG, KEY_PRESSED_FG, KEY_BORDER_COLOR,
    KEY_FONT, KEY_SMALL_FONT, KEY_PADDING, OVERLAY_BG,
    KEY_CORNER_RADIUS,
)


def _rounded_rect(canvas, x1, y1, x2, y2, r, **kwargs):
    """Canvas に角丸矩形を描画するヘルパー。"""
    points = [
        x1 + r, y1,
        x2 - r, y1,
        x2, y1,
        x2, y1 + r,
        x2, y2 - r,
        x2, y2,
        x2 - r, y2,
        x1 + r, y2,
        x1, y2,
        x1, y2 - r,
        x1, y1 + r,
        x1, y1,
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)


class KeyboardWidget(tk.Canvas):
    """QWERTY キーボードを Canvas 上に描画し、押下キーをハイライトするウィジェット。"""

    def __init__(self, master, width, height, **kwargs):
        super().__init__(
            master,
            width=width,
            height=height,
            bg=OVERLAY_BG,
            highlightthickness=0,
            **kwargs,
        )
        self._width = width
        self._height = height

        # key_name → (rect_id, text_id) のマッピング
        self._key_items: dict[str, tuple[int, int]] = {}
        # 現在ハイライト中の key_name セット
        self._pressed: set[str] = set()

        self._build_keyboard()

    def _build_keyboard(self):
        """レイアウト定義に従って全キーを描画する（一度だけ呼ぶ）。"""
        rows = KEYBOARD_ROWS
        n_rows = len(rows)

        # 各行の合計幅（単位）を計算して最大値を得る
        max_units = max(sum(w for _, _, w in row) for row in rows)

        # 1単位あたりのピクセル幅
        unit_w = (self._width - KEY_PADDING) / max_units

        row_h = (self._height - KEY_PADDING * (n_rows + 1)) / n_rows

        y = KEY_PADDING
        for row in rows:
            x = KEY_PADDING
            for label, key_name, rel_w in row:
                key_w = unit_w * rel_w - KEY_PADDING
                self._draw_key(x, y, x + key_w, y + row_h, label, key_name)
                x += unit_w * rel_w
            y += row_h + KEY_PADDING

    def _draw_key(self, x1, y1, x2, y2, label, key_name):
        """単一キーを描画し、IDを登録する。"""
        r = KEY_CORNER_RADIUS
        rect_id = _rounded_rect(
            self, x1, y1, x2, y2, r,
            fill=KEY_NORMAL_BG,
            outline=KEY_BORDER_COLOR,
        )
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2
        font = KEY_SMALL_FONT if len(label) > 3 else KEY_FONT
        text_id = self.create_text(
            cx, cy,
            text=label,
            fill=KEY_NORMAL_FG,
            font=font,
        )
        # 同名キーが複数ある場合（左右Shiftなど）はリストで保持
        if key_name not in self._key_items:
            self._key_items[key_name] = []
        self._key_items[key_name].append((rect_id, text_id))

    def press(self, key_name: str):
        """指定キーをハイライトする。"""
        if key_name in self._pressed:
            return
        self._pressed.add(key_name)
        self._set_key_style(key_name, pressed=True)

    def release(self, key_name: str):
        """指定キーのハイライトを解除する。"""
        self._pressed.discard(key_name)
        self._set_key_style(key_name, pressed=False)

    def release_all(self):
        """全キーのハイライトを解除する。"""
        for key_name in list(self._pressed):
            self.release(key_name)

    def _set_key_style(self, key_name: str, pressed: bool):
        items = self._key_items.get(key_name)
        if not items:
            return
        bg = KEY_PRESSED_BG if pressed else KEY_NORMAL_BG
        fg = KEY_PRESSED_FG if pressed else KEY_NORMAL_FG
        for rect_id, text_id in items:
            self.itemconfig(rect_id, fill=bg)
            self.itemconfig(text_id, fill=fg)
