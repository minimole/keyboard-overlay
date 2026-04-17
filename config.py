# config.py — アプリ全体の設定値

# --- タイミング ---
HIDE_DELAY_SEC = 3.0          # 最後のキー操作からオーバーレイを消すまでの秒数
RELEASE_HOLD_SEC = 1.0        # キーを離した後もハイライト・ショートカットを保持する秒数
WINDOW_POLL_INTERVAL_SEC = 0.5  # Sheetsウィンドウ監視のポーリング間隔

# --- 検出対象ウィンドウタイトル（部分一致） ---
SHEETS_TITLE_KEYWORDS = [
    "Google スプレッドシート",
    "Google Sheets",
]

# --- オーバーレイウィンドウ ---
OVERLAY_ALPHA = 0.85          # 透明度 (0.0〜1.0)
OVERLAY_WIDTH_RATIO = 0.82    # 画面幅に対するオーバーレイ幅の割合
KEYBOARD_HEIGHT = 170         # キーボード部分の高さ (px)
SHORTCUT_BAR_HEIGHT = 38      # ショートカット説明バーの高さ (px)
OVERLAY_HEIGHT = KEYBOARD_HEIGHT + SHORTCUT_BAR_HEIGHT  # 合計高さ = 208px
OVERLAY_BOTTOM_MARGIN = 10    # 画面下端からのマージン (px)

# --- ショートカット説明バー ---
SHORTCUT_BAR_BG            = "#0a1f0a"              # バー背景（深い緑）
SHORTCUT_BAR_PADDING_X     = 20                      # バー内左右パディング (px)
SHORTCUT_BAR_FONT          = ("Segoe UI", 13, "bold")
SHORTCUT_BAR_FONT_SMALL    = ("Segoe UI", 11)
SHORTCUT_COLOR_CATEGORY    = "#f0f0f0"              # カテゴリラベル: 白
SHORTCUT_COLOR_WIN         = "#5bc8e8"              # Windows ショートカット: 水色
SHORTCUT_COLOR_SEPARATOR   = "#888888"              # " ／ " セパレータ: グレー
SHORTCUT_COLOR_MAC         = "#e8c84b"              # Mac ショートカット: 金色
SHORTCUT_COLOR_EQUALS      = "#ffffff"              # " ＝ ": 白
SHORTCUT_COLOR_DESCRIPTION = "#4de88e"              # 説明文: 明るい緑

# --- キーボード描画 ---
KEY_NORMAL_BG = "#2b2b2b"     # 通常キーの背景色
KEY_PRESSED_BG = "#e8b84b"    # 押下キーの背景色
KEY_NORMAL_FG = "#e0e0e0"     # 通常キーの文字色
KEY_PRESSED_FG = "#1a1a1a"    # 押下キーの文字色
KEY_BORDER_COLOR = "#555555"  # キー枠線の色
KEY_CORNER_RADIUS = 5         # キーの角丸半径 (px)
KEY_FONT = ("Segoe UI", 10, "bold")
KEY_SMALL_FONT = ("Segoe UI", 8)
KEY_PADDING = 4               # キー間のパディング (px)
OVERLAY_BG = "#1a1a1a"        # オーバーレイ背景色（透過色と一致させる）

# --- QWERTY キーレイアウト定義 ---
# 各行: (表示ラベル, key_name, 相対幅)
# key_name は pynput の Key 属性名 or 文字そのまま
KEYBOARD_ROWS = [
    # 数字行
    [
        ("`", "grave", 1.0), ("1", "1", 1.0), ("2", "2", 1.0), ("3", "3", 1.0),
        ("4", "4", 1.0), ("5", "5", 1.0), ("6", "6", 1.0), ("7", "7", 1.0),
        ("8", "8", 1.0), ("9", "9", 1.0), ("0", "0", 1.0), ("-", "minus", 1.0),
        ("=", "equal", 1.0), ("⌫", "backspace", 2.0),
    ],
    # QWERTY行
    [
        ("Tab", "tab", 1.5), ("Q", "q", 1.0), ("W", "w", 1.0), ("E", "e", 1.0),
        ("R", "r", 1.0), ("T", "t", 1.0), ("Y", "y", 1.0), ("U", "u", 1.0),
        ("I", "i", 1.0), ("O", "o", 1.0), ("P", "p", 1.0), ("[", "bracketleft", 1.0),
        ("]", "bracketright", 1.0), ("\\", "backslash", 1.5),
    ],
    # ASDF行
    [
        ("Caps", "caps_lock", 1.75), ("A", "a", 1.0), ("S", "s", 1.0), ("D", "d", 1.0),
        ("F", "f", 1.0), ("G", "g", 1.0), ("H", "h", 1.0), ("J", "j", 1.0),
        ("K", "k", 1.0), ("L", "l", 1.0), (";", "semicolon", 1.0),
        ("'", "apostrophe", 1.0), ("Enter", "enter", 2.25),
    ],
    # ZXCV行
    [
        ("Shift", "shift_l", 2.25), ("Z", "z", 1.0), ("X", "x", 1.0), ("C", "c", 1.0),
        ("V", "v", 1.0), ("B", "b", 1.0), ("N", "n", 1.0), ("M", "m", 1.0),
        (",", "comma", 1.0), (".", "period", 1.0), ("/", "slash", 1.0),
        ("Shift", "shift_r", 2.75),
    ],
    # スペース行
    [
        ("Ctrl", "ctrl_l", 1.25), ("Win", "cmd", 1.25), ("Alt", "alt_l", 1.25),
        ("Space", "space", 6.25),
        ("Alt", "alt_r", 1.25), ("Win", "cmd_r", 1.25), ("Menu", "menu", 1.25),
        ("Ctrl", "ctrl_r", 1.25),
    ],
]
