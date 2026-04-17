# main.py — エントリポイント：各コンポーネントを初期化してアプリを起動する

import tkinter as tk
import signal
import sys

from overlay import OverlayWindow
from keyboard_listener import KeyboardListener
from window_watcher import WindowWatcher


def main():
    # --- tkinter ルートウィンドウ（非表示、イベントループ用） ---
    root = tk.Tk()
    root.withdraw()                         # メインウィンドウは非表示
    root.wm_attributes("-alpha", 0)         # 完全透明
    root.title("KeyboardOverlay")

    # --- オーバーレイウィンドウ ---
    overlay = OverlayWindow(root)

    # --- キーボードリスナー ---
    listener = KeyboardListener(
        on_press=overlay.on_key_press,
        on_release=overlay.on_key_release,
    )

    # --- ウィンドウウォッチャー ---
    def on_sheets_active():
        print("[INFO] Google Sheets がアクティブになりました。キーボードフックを有効化します。")
        listener.enable()

    def on_sheets_inactive():
        print("[INFO] Google Sheets が非アクティブになりました。キーボードフックを無効化します。")
        listener.disable()
        overlay.hide()

    watcher = WindowWatcher(
        on_sheets_active=on_sheets_active,
        on_sheets_inactive=on_sheets_inactive,
    )

    # --- 終了処理 ---
    def shutdown(*_):
        print("[INFO] アプリを終了します...")
        watcher.stop()
        listener.shutdown()
        root.quit()

    # Ctrl+C でも正常終了できるようにする
    signal.signal(signal.SIGINT, shutdown)
    root.protocol("WM_DELETE_WINDOW", shutdown)

    # --- 起動 ---
    print("[INFO] キーボードオーバーレイを起動しました。Google Sheets を開くと有効になります。")
    print("[INFO] 終了するには Ctrl+C を押してください。")
    watcher.start()

    try:
        root.mainloop()
    except KeyboardInterrupt:
        shutdown()


if __name__ == "__main__":
    main()
