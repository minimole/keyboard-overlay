# window_watcher.py — アクティブウィンドウを監視して Sheets 検出を通知するスレッド

from __future__ import annotations
import threading
import win32gui
import win32process
import psutil
from typing import Callable
from config import SHEETS_TITLE_KEYWORDS, WINDOW_POLL_INTERVAL_SEC


# Sheets を表示するブラウザの実行ファイル名（小文字）
_BROWSER_EXES = {"chrome.exe", "msedge.exe", "firefox.exe", "brave.exe", "opera.exe"}


def _is_sheets_active() -> bool:
    """現在のフォアグラウンドウィンドウが Sheets かどうかを判定する。"""
    hwnd = win32gui.GetForegroundWindow()
    if not hwnd:
        return False

    # タイトルに Sheets キーワードが含まれるか確認
    title = win32gui.GetWindowText(hwnd)
    if not any(kw in title for kw in SHEETS_TITLE_KEYWORDS):
        return False

    # 念のためブラウザプロセスか確認
    try:
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        proc = psutil.Process(pid)
        exe = proc.name().lower()
        return exe in _BROWSER_EXES
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        # プロセス情報が取れない場合はタイトル一致のみで判断
        return True


class WindowWatcher:
    """
    バックグラウンドスレッドで定期的にアクティブウィンドウを監視し、
    Sheets のアクティブ状態の変化をコールバックで通知する。
    """

    def __init__(
        self,
        on_sheets_active: Callable[[], None],
        on_sheets_inactive: Callable[[], None],
    ):
        self._on_active = on_sheets_active
        self._on_inactive = on_sheets_inactive
        self._running = False
        self._thread: threading.Thread | None = None
        self._last_state: bool | None = None  # 前回の状態（変化検出用）

    def start(self):
        """監視スレッドを開始する。"""
        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True, name="WindowWatcher")
        self._thread.start()

    def stop(self):
        """監視スレッドを停止する。"""
        self._running = False
        if self._thread:
            self._thread.join(timeout=2.0)
            self._thread = None

    def _run(self):
        import time
        while self._running:
            current = _is_sheets_active()
            if current != self._last_state:
                self._last_state = current
                if current:
                    self._on_active()
                else:
                    self._on_inactive()
            time.sleep(WINDOW_POLL_INTERVAL_SEC)
