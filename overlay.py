# overlay.py — 透明・最前面のオーバーレイウィンドウ

import threading
import tkinter as tk
from config import (
    OVERLAY_ALPHA, OVERLAY_WIDTH_RATIO, OVERLAY_HEIGHT,
    OVERLAY_BOTTOM_MARGIN, OVERLAY_BG, HIDE_DELAY_SEC,
    KEYBOARD_HEIGHT, SHORTCUT_BAR_HEIGHT, RELEASE_HOLD_SEC,
)
from keyboard_widget import KeyboardWidget
from shortcut_bar_widget import ShortcutBarWidget
from shortcuts import lookup


class OverlayWindow:
    """
    画面下部に表示する半透明キーボードオーバーレイ。
    上段: キーボードウィジェット（押下キーをハイライト）
    下段: ショートカット説明バー（Win / Mac 両表記 + 説明文を色分け表示）

    キー離放後 RELEASE_HOLD_SEC 秒間はハイライトとショートカット表示を維持し、
    その後クリアする。
    """

    def __init__(self, root: tk.Tk):
        self._root = root
        self._visible = False
        self._hide_timer: threading.Timer | None = None
        self._lock = threading.Lock()
        self._pressed_keys: set[str] = set()          # 現在押下中のキー名セット（生の key_name）
        self._release_timers: dict[str, threading.Timer] = {}  # キー別の離放遅延タイマー

        # --- Toplevel ウィンドウ作成 ---
        self._win = tk.Toplevel(root)
        self._win.overrideredirect(True)       # タイトルバーなし
        self._win.wm_attributes("-topmost", True)
        self._win.wm_attributes("-alpha", OVERLAY_ALPHA)
        self._win.configure(bg=OVERLAY_BG)
        self._win.withdraw()                   # 起動時は非表示

        # 画面サイズから位置・サイズを計算
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        ow = int(sw * OVERLAY_WIDTH_RATIO)
        oh = OVERLAY_HEIGHT                    # KEYBOARD_HEIGHT + SHORTCUT_BAR_HEIGHT
        ox = (sw - ow) // 2
        oy = sh - oh - OVERLAY_BOTTOM_MARGIN
        self._win.geometry(f"{ow}x{oh}+{ox}+{oy}")

        # --- 上段: キーボードウィジェット ---
        self._kb = KeyboardWidget(self._win, width=ow, height=KEYBOARD_HEIGHT)
        self._kb.pack(side="top", fill="x")

        # --- 下段: ショートカット説明バー ---
        self._shortcut_bar = ShortcutBarWidget(self._win, width=ow, height=SHORTCUT_BAR_HEIGHT)
        self._shortcut_bar.pack(side="top", fill="x")

    # ------------------------------------------------------------------
    # 公開 API（別スレッドから呼び出し可能）
    # ------------------------------------------------------------------

    def on_key_press(self, key_name: str):
        """キー押下イベントをメインスレッドに転送する。"""
        self._root.after(0, self._handle_press, key_name)

    def on_key_release(self, key_name: str):
        """キー離放イベントをメインスレッドに転送する。"""
        self._root.after(0, self._handle_release, key_name)

    def hide(self):
        """オーバーレイを非表示にする（メインスレッドに転送）。"""
        self._root.after(0, self._do_hide)

    # ------------------------------------------------------------------
    # 内部処理（メインスレッドのみ呼び出す）
    # ------------------------------------------------------------------

    def _handle_press(self, key_name: str):
        # 離放タイマーが残っていたらキャンセル（キー連打・長押し対応）
        timer = self._release_timers.pop(key_name, None)
        if timer is not None:
            timer.cancel()

        if not self._visible:
            self._do_show()
        self._kb.press(key_name)
        self._pressed_keys.add(key_name)
        self._update_shortcut()
        self._reset_hide_timer()

    def _handle_release(self, key_name: str):
        """
        キー離放時: 即座にクリアせず RELEASE_HOLD_SEC 秒後に _do_release を呼ぶ。
        同じキーの既存タイマーがあれば上書き（連打対策）。
        """
        # 既存タイマーがあればキャンセル
        existing = self._release_timers.pop(key_name, None)
        if existing is not None:
            existing.cancel()

        # RELEASE_HOLD_SEC 秒後にメインスレッドで _do_release を実行
        timer = threading.Timer(
            RELEASE_HOLD_SEC,
            lambda: self._root.after(0, self._do_release, key_name),
        )
        timer.daemon = True
        timer.start()
        self._release_timers[key_name] = timer

    def _do_release(self, key_name: str):
        """離放タイマー発火後の実際のクリア処理（メインスレッドで実行）。"""
        self._release_timers.pop(key_name, None)
        self._kb.release(key_name)
        self._pressed_keys.discard(key_name)
        self._update_shortcut()

    def _do_show(self):
        self._win.deiconify()
        self._visible = True

    def _do_hide(self):
        # 全ての離放遅延タイマーを即キャンセル
        for timer in self._release_timers.values():
            timer.cancel()
        self._release_timers.clear()

        self._kb.release_all()
        self._pressed_keys.clear()
        self._shortcut_bar.update(None)   # バーをクリア
        self._win.withdraw()
        self._visible = False

    def _update_shortcut(self):
        """
        現在の押下キーセットからショートカットを検索し、バーを更新する。
        ShortcutBarWidget 側で差分チェックを行うため、未変化なら再描画しない。
        """
        entry = lookup(self._pressed_keys)
        self._shortcut_bar.update(entry)

    def _reset_hide_timer(self):
        """タイマーをリセットして HIDE_DELAY_SEC 秒後に非表示にする。"""
        with self._lock:
            if self._hide_timer is not None:
                self._hide_timer.cancel()
            self._hide_timer = threading.Timer(HIDE_DELAY_SEC, self.hide)
            self._hide_timer.daemon = True
            self._hide_timer.start()
