# keyboard_listener.py — pynput によるグローバルキーボードフック管理

from __future__ import annotations
import threading
from typing import Callable
from pynput import keyboard


# pynput の Key/KeyCode → config.py の key_name へ変換するマッピング
_SPECIAL_KEY_MAP: dict[keyboard.Key, str] = {
    # --- 修飾キー ---
    keyboard.Key.space:         "space",
    keyboard.Key.enter:         "enter",
    keyboard.Key.backspace:     "backspace",
    keyboard.Key.tab:           "tab",
    keyboard.Key.caps_lock:     "caps_lock",
    keyboard.Key.shift:         "shift_l",
    keyboard.Key.shift_l:       "shift_l",
    keyboard.Key.shift_r:       "shift_r",
    keyboard.Key.ctrl:          "ctrl_l",
    keyboard.Key.ctrl_l:        "ctrl_l",
    keyboard.Key.ctrl_r:        "ctrl_r",
    keyboard.Key.alt:           "alt_l",
    keyboard.Key.alt_l:         "alt_l",
    keyboard.Key.alt_r:         "alt_r",
    keyboard.Key.alt_gr:        "alt_r",
    keyboard.Key.cmd:           "cmd",
    keyboard.Key.cmd_l:         "cmd",
    keyboard.Key.cmd_r:         "cmd_r",
    keyboard.Key.menu:          "menu",
    # --- ナビゲーションキー ---
    keyboard.Key.right:         "right",
    keyboard.Key.left:          "left",
    keyboard.Key.up:            "up",
    keyboard.Key.down:          "down",
    keyboard.Key.home:          "home",
    keyboard.Key.end:           "end",
    keyboard.Key.page_up:       "page_up",
    keyboard.Key.page_down:     "page_down",
    keyboard.Key.delete:        "delete",
    keyboard.Key.insert:        "insert",
    keyboard.Key.esc:           "esc",
    # --- ファンクションキー ---
    keyboard.Key.f1:            "f1",
    keyboard.Key.f2:            "f2",
    keyboard.Key.f3:            "f3",
    keyboard.Key.f4:            "f4",
    keyboard.Key.f5:            "f5",
    keyboard.Key.f6:            "f6",
    keyboard.Key.f7:            "f7",
    keyboard.Key.f8:            "f8",
    keyboard.Key.f9:            "f9",
    keyboard.Key.f10:           "f10",
    keyboard.Key.f11:           "f11",
    keyboard.Key.f12:           "f12",
}


def _resolve_key_name(key: keyboard.Key | keyboard.KeyCode) -> str | None:
    """
    pynput のキーオブジェクトを config の key_name 文字列に変換する。

    【修正】Windows では Ctrl を押しながら文字キーを押すと、OS が key.char を
    制御文字（例: Ctrl+C → '\x03'、Ctrl+A → '\x01'）に変換して報告する。
    この場合 key.char.lower() は '\x03' を返してしまいショートカット辞書と
    一致しなくなるため、vk（仮想キーコード）から正規の文字を復元する。
    """
    if isinstance(key, keyboard.Key):
        return _SPECIAL_KEY_MAP.get(key)

    # KeyCode（通常文字キー）
    vk = getattr(key, 'vk', None)
    if vk is not None:
        # 英字キー A(65)〜Z(90) → 'a'〜'z'
        # Ctrl 押下時に char が制御文字になっても vk は常に正しい値を返す
        if 65 <= vk <= 90:
            return chr(vk + 32)   # 例: vk=67(C) → 'c'
        # 数字キー 0(48)〜9(57) → '0'〜'9'
        if 48 <= vk <= 57:
            return chr(vk)        # 例: vk=49(1) → '1'

    # 記号・その他: char が制御文字（ord < 0x20）でなければそのまま返す
    if key.char and ord(key.char) >= 0x20:
        return key.char.lower()

    return None


class KeyboardListener:
    """
    グローバルキーボードフックを管理するクラス。
    enable()/disable() でフックを動的に ON/OFF できる。
    フックは別スレッドで動作し、イベントはコールバックで通知する。
    """

    def __init__(
        self,
        on_press: Callable[[str], None],
        on_release: Callable[[str], None],
    ):
        self._on_press = on_press
        self._on_release = on_release
        self._listener: keyboard.Listener | None = None
        self._enabled = False
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # 公開 API
    # ------------------------------------------------------------------

    def enable(self):
        """フックを開始する。既に有効なら何もしない。"""
        with self._lock:
            if self._enabled:
                return
            self._enabled = True
            self._start_listener()

    def disable(self):
        """フックを停止する。既に無効なら何もしない。"""
        with self._lock:
            if not self._enabled:
                return
            self._enabled = False
            self._stop_listener()

    def shutdown(self):
        """アプリ終了時に呼ぶ。フックを確実に停止する。"""
        with self._lock:
            self._enabled = False
            self._stop_listener()

    # ------------------------------------------------------------------
    # 内部処理
    # ------------------------------------------------------------------

    def _start_listener(self):
        self._listener = keyboard.Listener(
            on_press=self._handle_press,
            on_release=self._handle_release,
            suppress=False,   # キー入力を横取りしない（シートへ届ける）
        )
        self._listener.daemon = True
        self._listener.start()

    def _stop_listener(self):
        if self._listener is not None:
            self._listener.stop()
            self._listener = None

    def _handle_press(self, key):
        if not self._enabled:
            return
        name = _resolve_key_name(key)
        if name:
            self._on_press(name)

    def _handle_release(self, key):
        if not self._enabled:
            return
        name = _resolve_key_name(key)
        if name:
            self._on_release(name)
