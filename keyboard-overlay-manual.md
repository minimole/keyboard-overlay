# キーボードオーバーレイ ツール マニュアル

> 最終更新: 2026-04-16  
> バージョン: 1.3（キー離放後1秒表示保持機能追加版）  
> 対象OS: Windows 10 / 11

---

## 目次

1. [概要](#1-概要)
2. [動作環境・必要条件](#2-動作環境必要条件)
3. [インストール手順](#3-インストール手順)
4. [起動方法](#4-起動方法)
5. [画面の見かた](#5-画面の見かた)
6. [対応ショートカット一覧](#6-対応ショートカット一覧)
7. [カスタマイズ設定](#7-カスタマイズ設定-configpy)
8. [ファイル構成](#8-ファイル構成)
9. [トラブルシューティング](#9-トラブルシューティング)
10. [アンインストール](#10-アンインストール)

---

## 1. 概要

**キーボードオーバーレイ**は、Google スプレッドシートを使用中にキーボード操作を画面下部へリアルタイム表示するツールです。

### 主な機能

| 機能 | 詳細 |
|------|------|
| キーボード表示 | 画面下部にQWERTYキーボードを半透明で常時最前面表示 |
| キーハイライト | 押下中のキーをリアルタイムで黄色にハイライト |
| 離放後保持 | キーから指を離した後も**1秒間**ハイライトとショートカット説明を表示し続ける |
| ショートカット説明 | 押したキー組み合わせに対応するスプレッドシートの操作説明を表示 |
| Win / Mac 両対応 | Windows と Mac のショートカット表記を並列で表示 |
| 自動非表示 | 最後のキー入力から3秒後に自動でオーバーレイを非表示にする |
| 条件付き有効化 | Google スプレッドシートがアクティブな時だけ動作し、PC 負荷を最小化 |

### 用途

- 発表・デモ時に視聴者へキー操作を見せる
- スプレッドシート講座・レクチャーでのショートカット解説
- 操作の録画・配信での視認性向上

---

## 2. 動作環境・必要条件

| 項目 | 要件 |
|------|------|
| OS | Windows 10 / 11（64bit 推奨） |
| Python | 3.10 以上 |
| ブラウザ | Chrome / Edge / Firefox / Brave / Opera |
| 対象サービス | Google スプレッドシート（ブラウザ版） |

### 必要な Python ライブラリ

| ライブラリ | バージョン | 役割 |
|-----------|-----------|------|
| `pynput` | 1.7.6 以上 | グローバルキーボードフック |
| `pywin32` | 306 以上 | Windows アクティブウィンドウ検出 |
| `psutil` | 5.9.0 以上 | ブラウザプロセス確認 |
| `tkinter` | Python 標準 | オーバーレイウィンドウ描画 |

---

## 3. インストール手順

### ステップ 1：Python のインストール確認

コマンドプロンプトを開いて以下を実行します。

```
python --version
```

`Python 3.10.x` 以上が表示されれば OK です。  
表示されない場合は [python.org](https://www.python.org/downloads/) からインストールしてください。  
インストール時に **「Add Python to PATH」にチェックを入れること**が重要です。

---

### ステップ 2：ライブラリのインストール

コマンドプロンプトで以下を実行します。（初回のみ）

```
pip install -r C:\Claude\keyboard-overlay\requirements.txt
```

成功するとライブラリが自動インストールされます。

---

### ステップ 3：動作確認

```
cd C:\Claude\keyboard-overlay
python main.py
```

コンソールに以下のメッセージが表示されれば起動成功です。

```
[INFO] キーボードオーバーレイを起動しました。Google Sheets を開くと有効になります。
[INFO] 終了するには Ctrl+C を押してください。
```

---

## 4. 起動方法

### 方法 A：バッチファイルでダブルクリック起動（推奨）

`C:\Claude\keyboard-overlay\起動.bat` というファイルを作成し、  
以下の内容を書いて保存します。

```batch
@echo off
cd /d C:\Claude\keyboard-overlay
python main.py
pause
```

次回からは **このファイルをダブルクリック**するだけで起動できます。  
（`pause` があるためエラー時もメッセージを確認できます）

---

### 方法 B：コンソールなしのショートカットで起動（運用時向け）

デスクトップに静かに起動するショートカットを作る方法です。

1. デスクトップで右クリック → 「新規作成」→「ショートカット」
2. リンク先に以下を入力：
   ```
   pythonw.exe C:\Claude\keyboard-overlay\main.py
   ```
3. 名前を「キーボードオーバーレイ」として保存

> **注意:** `pythonw.exe` はコンソール画面なしで起動します。  
> エラーが発生しても表示されないため、最初は方法 A で動作確認を行ってください。

---

### 方法 C：コマンドプロンプトから起動（デバッグ時向け）

```
cd C:\Claude\keyboard-overlay
python main.py
```

動作ログがコンソールに表示されるため、問題の調査に役立ちます。

---

### 終了方法

| 起動方法 | 終了方法 |
|---------|---------|
| 方法 A / C（コンソールあり） | `Ctrl + C` を押す |
| 方法 B（コンソールなし） | タスクマネージャー → `python.exe` を終了 |

---

## 5. 画面の見かた

Google スプレッドシートをアクティブにしてキーを押すと、画面下部に以下のオーバーレイが表示されます。

```
╔══════════════════════════════════════════════════════════╗
║  Esc  F1  F2  F3  F4  F5  F6  F7  F8  F9  F10  F11  F12 ║
║   1    2    3    4    5   ...   0    -    =     ⌫        ║
║  Tab   Q    W    E    R   ...   P    [    ]     \         ║
║  Caps  A    S   [D]   F   ...   L    ;    '   Enter       ║ ← [D] が黄色ハイライト
║  Shift  Z    X    C    V  ...   /              Shift      ║
║  Ctrl  Win  Alt       Space      Alt  Win  Menu  Ctrl     ║
╠══════════════════════════════════════════════════════════╣
║ [セル操作]  Ctrl + D 💙  ／  ⌘ Cmd + D 💛  ＝  下のセルにコピー 💚 ║
╚══════════════════════════════════════════════════════════╝
```

### 上段：キーボードエリア

| 表示 | 意味 |
|------|------|
| 通常キー（暗い色） | 押していないキー |
| **黄色ハイライトのキー** | 現在押しているキー、またはキーを離してから1秒以内のキー |

### 下段：ショートカット説明バー

| パーツ | 色 | 例 |
|--------|----|----|
| カテゴリ | 白 | `[セル操作]` |
| Windows ショートカット | 水色 | `Ctrl + D` |
| セパレータ | グレー | `／` |
| Mac ショートカット | 金色 | `⌘ Cmd + D` |
| 区切り | 白 | `＝` |
| 操作説明 | 明るい緑 | `下のセルにコピー` |

> **ショートカット未登録のキー操作の場合**、バーは空欄（緑の背景のみ）になります。  
> **修飾キーのみ**（Ctrl・Shift・Alt 単独）では、誤表示を防ぐためバーは空欄のままです。

---

### 表示・非表示の動作タイミング

```
【キーを押した瞬間】
  → オーバーレイ表示
  → 押したキーが黄色にハイライト
  → ショートカット説明バーに操作名を表示
  → 3秒タイマーをリセット（押すたびにリセット）

【キーから指を離した瞬間】
  → ハイライト・ショートカット説明はそのまま維持
  → 1秒後 → ハイライト消去・ショートカット説明クリア

【最後のキー入力から3秒経過】
  → オーバーレイ全体を非表示
```

> **例：Ctrl + C を押してすぐ離した場合**
> ```
> Ctrl 押す → C 押す → [コピー 表示] → C 離す → Ctrl 離す
>                                              ↓ 1秒後
>                                         ハイライト消去・バークリア
>                                              ↓ 3秒後（最後のキー押下から）
>                                         オーバーレイ非表示
> ```

---

## 6. 対応ショートカット一覧

### 基本操作

| 操作 | Windows | Mac |
|------|---------|-----|
| コピー | `Ctrl + C` | `⌘ Cmd + C` |
| 切り取り | `Ctrl + X` | `⌘ Cmd + X` |
| 貼り付け | `Ctrl + V` | `⌘ Cmd + V` |
| 値のみ貼り付け | `Ctrl + Shift + V` | `⌘ Cmd + Shift + V` |
| 元に戻す | `Ctrl + Z` | `⌘ Cmd + Z` |
| やり直し | `Ctrl + Y` | `⌘ Cmd + Y` |
| すべて選択 | `Ctrl + A` | `⌘ Cmd + A` |
| 保存（自動保存） | `Ctrl + S` | `⌘ Cmd + S` |
| 印刷 | `Ctrl + P` | `⌘ Cmd + P` |
| 検索 | `Ctrl + F` | `⌘ Cmd + F` |
| 検索と置換 | `Ctrl + H` | `⌘ Cmd + H` |
| リンクを挿入 | `Ctrl + K` | `⌘ Cmd + K` |

### 書式設定

| 操作 | Windows | Mac |
|------|---------|-----|
| 太字 | `Ctrl + B` | `⌘ Cmd + B` |
| 斜体 | `Ctrl + I` | `⌘ Cmd + I` |
| 下線 | `Ctrl + U` | `⌘ Cmd + U` |
| 取り消し線 | `Alt + Shift + 5` | `⌘ Cmd + Shift + X` |
| 書式をクリア | `Ctrl + \` | `⌘ Cmd + \` |
| 中央揃え | `Ctrl + Shift + E` | `⌘ Cmd + Shift + E` |
| 右揃え | `Ctrl + Shift + R` | `⌘ Cmd + Shift + R` |
| 両端揃え | `Ctrl + Shift + J` | `⌘ Cmd + Shift + J` |
| 外枠ボーダー | `Ctrl + Shift + 7` | `⌘ Cmd + Shift + 7` |
| すべてのボーダー | `Ctrl + Shift + 6` | `⌘ Cmd + Shift + 6` |
| 数値書式 | `Ctrl + Shift + 1` | `⌘ Cmd + Shift + 1` |
| 時刻書式 | `Ctrl + Shift + 2` | `⌘ Cmd + Shift + 2` |
| 日付書式 | `Ctrl + Shift + 3` | `⌘ Cmd + Shift + 3` |
| 通貨書式 | `Ctrl + Shift + 4` | `⌘ Cmd + Shift + 4` |
| パーセント書式 | `Ctrl + Shift + 5` | `⌘ Cmd + Shift + 5` |

### セル操作

| 操作 | Windows | Mac |
|------|---------|-----|
| 下のセルにコピー | `Ctrl + D` | `⌘ Cmd + D` |
| 右のセルにコピー | `Ctrl + R` | `⌘ Cmd + R` |
| 選択範囲に同じ内容を入力 | `Ctrl + Enter` | `⌘ Cmd + Enter` |
| セル内で改行 | `Alt + Enter` | `Option + Enter` |
| 行・列を挿入 | `Ctrl + Shift + +` | `⌘ Cmd + Shift + +` |
| 行・列を削除 | `Ctrl + −` | `⌘ Cmd + −` |
| コメントを挿入 | `Ctrl + Shift + K` | `⌘ Cmd + Shift + K` |
| メモを挿入 | `Ctrl + Alt + M` | `⌘ Cmd + Alt + M` |

### ナビゲーション

| 操作 | Windows | Mac |
|------|---------|-----|
| シートの先頭へ | `Ctrl + Home` | `⌘ Cmd + Home` |
| データ末尾へ | `Ctrl + End` | `⌘ Cmd + End` |
| 右端のセルへ | `Ctrl + →` | `⌘ Cmd + →` |
| 左端のセルへ | `Ctrl + ←` | `⌘ Cmd + ←` |
| 上端のセルへ | `Ctrl + ↑` | `⌘ Cmd + ↑` |
| 下端のセルへ | `Ctrl + ↓` | `⌘ Cmd + ↓` |
| 右端まで選択拡張 | `Ctrl + Shift + →` | `⌘ Cmd + Shift + →` |
| 左端まで選択拡張 | `Ctrl + Shift + ←` | `⌘ Cmd + Shift + ←` |
| 下端まで選択拡張 | `Ctrl + Shift + ↓` | `⌘ Cmd + Shift + ↓` |
| 上端まで選択拡張 | `Ctrl + Shift + ↑` | `⌘ Cmd + Shift + ↑` |
| 行全体を選択 | `Shift + Space` | `Shift + Space` |
| 列全体を選択 | `Ctrl + Shift + Space` | `⌘ Cmd + Shift + Space` |

### データ

| 操作 | Windows | Mac |
|------|---------|-----|
| 今日の日付を入力 | `Ctrl + ;` | `⌘ Cmd + ;` |
| 現在の時刻を入力 | `Ctrl + Shift + ;` | `⌘ Cmd + Shift + ;` |
| フィルターの切り替え | `Ctrl + Shift + L` | `⌘ Cmd + Shift + L` |

### 表示・シート

| 操作 | Windows | Mac |
|------|---------|-----|
| 次のシートへ移動 | `Alt + Shift + K` | `Alt + Shift + K` |
| 前のシートへ移動 | `Alt + Shift + J` | `Alt + Shift + J` |
| 全画面表示の切り替え | `Ctrl + Shift + F` | `⌘ Cmd + Shift + F` |

---

## 7. カスタマイズ設定（config.py）

`C:\Claude\keyboard-overlay\config.py` を編集することで、動作・見た目を変更できます。  
変更後はツールを再起動してください。

### タイミング設定

```python
HIDE_DELAY_SEC = 3.0          # オーバーレイを非表示にするまでの秒数（デフォルト: 3秒）
RELEASE_HOLD_SEC = 1.0        # キーを離した後もハイライト・ショートカットを保持する秒数（デフォルト: 1秒）
WINDOW_POLL_INTERVAL_SEC = 0.5  # Sheetsウィンドウ監視の間隔（デフォルト: 0.5秒）
```

> **`RELEASE_HOLD_SEC` の調整例:**  
> - `0.5` → 素早く消えてテンポよく操作できる  
> - `1.0` → デフォルト。動画・発表でキーを見せるのに適切  
> - `2.0` → 長めに表示。ゆっくり操作を確認したい場面向け

### オーバーレイウィンドウ設定

```python
OVERLAY_ALPHA = 0.85          # 透明度（0.0=完全透明 〜 1.0=不透明）
OVERLAY_WIDTH_RATIO = 0.82    # 画面幅の何割をオーバーレイ幅にするか（0.6〜0.95 推奨）
KEYBOARD_HEIGHT = 170         # キーボード部分の高さ（px）
SHORTCUT_BAR_HEIGHT = 38      # ショートカット説明バーの高さ（px）
OVERLAY_BOTTOM_MARGIN = 10    # 画面下端からのマージン（px）
```

### キーの色設定

```python
KEY_NORMAL_BG = "#2b2b2b"     # 通常キーの背景色
KEY_PRESSED_BG = "#e8b84b"    # 押下キーの背景色（黄系）
KEY_NORMAL_FG = "#e0e0e0"     # 通常キーの文字色
KEY_PRESSED_FG = "#1a1a1a"    # 押下キーの文字色
```

### ショートカット説明バーの色設定

```python
SHORTCUT_BAR_BG            = "#0a1f0a"   # バー背景（深い緑）
SHORTCUT_COLOR_CATEGORY    = "#f0f0f0"   # カテゴリラベルの色（白）
SHORTCUT_COLOR_WIN         = "#5bc8e8"   # Windowsショートカットの色（水色）
SHORTCUT_COLOR_MAC         = "#e8c84b"   # Macショートカットの色（金色）
SHORTCUT_COLOR_DESCRIPTION = "#4de88e"   # 説明文の色（明るい緑）
```

> **色の指定方法:** `#RRGGBB` 形式の16進数カラーコードを使用します。  
> 例: `"#ff0000"` = 赤、`"#ffffff"` = 白、`"#000000"` = 黒

---

## 8. ファイル構成

```
C:\Claude\keyboard-overlay\
│
├── main.py                  # エントリポイント（起動・終了処理）
├── window_watcher.py        # Google Sheets ウィンドウ監視スレッド
├── keyboard_listener.py     # グローバルキーボードフック（pynput）
├── overlay.py               # オーバーレイウィンドウ全体の管理
├── keyboard_widget.py       # キーボード描画ウィジェット（Canvas）
├── shortcut_bar_widget.py   # ショートカット説明バーウィジェット（Canvas）
├── shortcuts.py             # ショートカット定義データベース（45件）
├── config.py                # 全設定値（色・サイズ・タイミング）
└── requirements.txt         # 依存ライブラリ一覧
```

---

## 9. トラブルシューティング

### Q: ダブルクリックしても何も起動しない

**原因:** Python が PATH に登録されていないか、`.py` ファイルが Python に関連付けられていない可能性があります。

**対処:**
1. コマンドプロンプトで `python --version` を実行し、Python が認識されているか確認
2. 認識されない場合は Python を再インストールし、「Add Python to PATH」にチェックを入れる
3. `.bat` ファイルから起動する方法（[方法 A](#方法-aバッチファイルでダブルクリック起動推奨)）に切り替える

---

### Q: Google Sheets を開いてもオーバーレイが出ない

**原因1:** ウィンドウタイトルにキーワードが含まれていない

**対処:** `config.py` の `SHEETS_TITLE_KEYWORDS` を確認し、使用しているブラウザの言語設定に合わせてキーワードを追加します。

```python
SHEETS_TITLE_KEYWORDS = [
    "Google スプレッドシート",   # 日本語
    "Google Sheets",             # 英語
]
```

**原因2:** ブラウザが対応リストにない

**対処:** `window_watcher.py` の `_BROWSER_EXES` に使用ブラウザの実行ファイル名を追加します。

```python
_BROWSER_EXES = {"chrome.exe", "msedge.exe", "firefox.exe", "brave.exe", "opera.exe"}
```

---

### Q: セキュリティソフトにブロックされる

**原因:** `pynput` のグローバルキーボードフックがキーロガーと誤検知される場合があります。

**対処:**
1. セキュリティソフトの除外リストに `python.exe` または `C:\Claude\keyboard-overlay` を追加
2. または管理者として実行（`起動.bat` を右クリック → 「管理者として実行」）

---

### Q: キーが正しくハイライトされない

**原因:** 一部の特殊キー（テンキー、メディアキーなど）は `keyboard_listener.py` の変換マップに含まれていない場合があります。

**対処:** `keyboard_listener.py` の `_SPECIAL_KEY_MAP` に対象キーを追加します。

---

### Q: テキストが画面に収まらず途切れる

**原因:** `config.py` の `SHORTCUT_BAR_HEIGHT` が小さすぎる、またはフォントサイズが大きい。

**対処:** 以下の値を調整します。

```python
SHORTCUT_BAR_HEIGHT = 38      # 値を増やす（例: 45）
SHORTCUT_BAR_FONT = ("Segoe UI", 13, "bold")  # フォントサイズを小さくする（例: 11）
```

---

### Q: PC の負荷が気になる

**確認方法:** タスクマネージャーで `python.exe` の CPU 使用率を確認します。  
待機時（Google Sheets 非アクティブ時）は **0.1% 以下**が正常です。

**設計上の低負荷対策:**
- Google Sheets がアクティブな時のみキーボードフックが動作
- キー入力はイベント駆動（ポーリングなし）
- オーバーレイの描画は変化したキーのみ差分更新

---

## 10. アンインストール

1. フォルダごと削除します。

```
C:\Claude\keyboard-overlay\
```

2. 作成したショートカットや `.bat` ファイルを削除します。

3. インストールしたライブラリを削除する場合（任意）：

```
pip uninstall pynput pywin32 psutil
```

---

## 付録：アーキテクチャ概要（技術参考）

```
起動
│
├── WindowWatcher スレッド（500ms ポーリング）
│     └── アクティブウィンドウのタイトルを確認
│           ├── Sheets アクティブ → KeyboardListener.enable()
│           └── Sheets 非アクティブ → KeyboardListener.disable() + overlay.hide()
│
├── KeyboardListener（pynput、イベント駆動）
│     ├── 押下イベント → overlay.on_key_press(key_name)
│     └── 離放イベント → overlay.on_key_release(key_name)
│
└── OverlayWindow（tkinter メインスレッド）
      ├── KeyboardWidget（Canvas：キーボード描画・差分ハイライト）
      ├── ShortcutBarWidget（Canvas：色分けテキスト差分更新）
      │     └── shortcuts.lookup(pressed_keys) でショートカット検索
      ├── HideTimer（threading.Timer：最後のキー押下から3秒後に withdraw()）
      └── ReleaseTimers（キー別 threading.Timer：各キー離放から1秒後にハイライト消去）
```

---

*このマニュアルは `C:\Claude\keyboard-overlay\keyboard-overlay-manual.md` に保存されています。*
