# shortcuts.py — Google スプレッドシートのショートカット定義 + ルックアップ関数

from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class ShortcutEntry:
    """1件のショートカット情報。frozen=True により同一キーなら同一オブジェクト。"""
    category: str       # "[基本操作]" など括弧込み
    win_label: str      # "Ctrl + C"
    mac_label: str      # "⌘ Cmd + C"
    description: str    # "コピー"


# ------------------------------------------------------------------
# キー名正規化（ctrl_l/ctrl_r → ctrl など）
# ------------------------------------------------------------------

_NORMALIZE: dict[str, str] = {
    "ctrl_l":  "ctrl",
    "ctrl_r":  "ctrl",
    "shift_l": "shift",
    "shift_r": "shift",
    "alt_l":   "alt",
    "alt_r":   "alt",
    "cmd":     "cmd",
    "cmd_r":   "cmd",
}

# 修飾キーのみのセット（このセットのサブセットはショートカットとして扱わない）
_MODIFIER_ONLY: frozenset[str] = frozenset({"ctrl", "shift", "alt", "cmd"})


def normalize(key_name: str) -> str:
    """左右修飾キーを統一する。その他はそのまま返す。"""
    return _NORMALIZE.get(key_name, key_name)


# ------------------------------------------------------------------
# Google スプレッドシート ショートカット辞書（45件）
# キー: frozenset of normalized key_name
# ------------------------------------------------------------------

SHORTCUTS: dict[frozenset, ShortcutEntry] = {

    # ═══════════════════════════════════════════════════════════════
    # 基本操作
    # ═══════════════════════════════════════════════════════════════
    frozenset({"ctrl", "c"}): ShortcutEntry(
        "[基本操作]", "Ctrl + C", "⌘ Cmd + C", "コピー"),
    frozenset({"ctrl", "x"}): ShortcutEntry(
        "[基本操作]", "Ctrl + X", "⌘ Cmd + X", "切り取り"),
    frozenset({"ctrl", "v"}): ShortcutEntry(
        "[基本操作]", "Ctrl + V", "⌘ Cmd + V", "貼り付け"),
    frozenset({"ctrl", "shift", "v"}): ShortcutEntry(
        "[基本操作]", "Ctrl + Shift + V", "⌘ Cmd + Shift + V", "値のみ貼り付け"),
    frozenset({"ctrl", "z"}): ShortcutEntry(
        "[基本操作]", "Ctrl + Z", "⌘ Cmd + Z", "元に戻す"),
    frozenset({"ctrl", "y"}): ShortcutEntry(
        "[基本操作]", "Ctrl + Y", "⌘ Cmd + Y", "やり直し"),
    frozenset({"ctrl", "a"}): ShortcutEntry(
        "[基本操作]", "Ctrl + A", "⌘ Cmd + A", "すべて選択"),
    frozenset({"ctrl", "s"}): ShortcutEntry(
        "[基本操作]", "Ctrl + S", "⌘ Cmd + S", "保存（自動保存）"),
    frozenset({"ctrl", "p"}): ShortcutEntry(
        "[基本操作]", "Ctrl + P", "⌘ Cmd + P", "印刷"),
    frozenset({"ctrl", "f"}): ShortcutEntry(
        "[基本操作]", "Ctrl + F", "⌘ Cmd + F", "検索"),
    frozenset({"ctrl", "h"}): ShortcutEntry(
        "[基本操作]", "Ctrl + H", "⌘ Cmd + H", "検索と置換"),
    frozenset({"ctrl", "k"}): ShortcutEntry(
        "[基本操作]", "Ctrl + K", "⌘ Cmd + K", "リンクを挿入"),

    # ═══════════════════════════════════════════════════════════════
    # 書式設定
    # ═══════════════════════════════════════════════════════════════
    frozenset({"ctrl", "b"}): ShortcutEntry(
        "[書式設定]", "Ctrl + B", "⌘ Cmd + B", "太字"),
    frozenset({"ctrl", "i"}): ShortcutEntry(
        "[書式設定]", "Ctrl + I", "⌘ Cmd + I", "斜体"),
    frozenset({"ctrl", "u"}): ShortcutEntry(
        "[書式設定]", "Ctrl + U", "⌘ Cmd + U", "下線"),
    frozenset({"alt", "shift", "5"}): ShortcutEntry(
        "[書式設定]", "Alt + Shift + 5", "⌘ Cmd + Shift + X", "取り消し線"),
    frozenset({"ctrl", "backslash"}): ShortcutEntry(
        "[書式設定]", "Ctrl + \\", "⌘ Cmd + \\", "書式をクリア"),
    frozenset({"ctrl", "shift", "e"}): ShortcutEntry(
        "[書式設定]", "Ctrl + Shift + E", "⌘ Cmd + Shift + E", "中央揃え"),
    frozenset({"ctrl", "shift", "r"}): ShortcutEntry(
        "[書式設定]", "Ctrl + Shift + R", "⌘ Cmd + Shift + R", "右揃え"),
    frozenset({"ctrl", "shift", "j"}): ShortcutEntry(
        "[書式設定]", "Ctrl + Shift + J", "⌘ Cmd + Shift + J", "両端揃え"),
    frozenset({"ctrl", "shift", "7"}): ShortcutEntry(
        "[書式設定]", "Ctrl + Shift + 7", "⌘ Cmd + Shift + 7", "外枠ボーダーを適用"),
    frozenset({"ctrl", "shift", "6"}): ShortcutEntry(
        "[書式設定]", "Ctrl + Shift + 6", "⌘ Cmd + Shift + 6", "すべてのボーダーを適用"),
    frozenset({"ctrl", "shift", "1"}): ShortcutEntry(
        "[書式設定]", "Ctrl + Shift + 1", "⌘ Cmd + Shift + 1", "数値書式"),
    frozenset({"ctrl", "shift", "2"}): ShortcutEntry(
        "[書式設定]", "Ctrl + Shift + 2", "⌘ Cmd + Shift + 2", "時刻書式"),
    frozenset({"ctrl", "shift", "3"}): ShortcutEntry(
        "[書式設定]", "Ctrl + Shift + 3", "⌘ Cmd + Shift + 3", "日付書式"),
    frozenset({"ctrl", "shift", "4"}): ShortcutEntry(
        "[書式設定]", "Ctrl + Shift + 4", "⌘ Cmd + Shift + 4", "通貨書式"),
    frozenset({"ctrl", "shift", "5"}): ShortcutEntry(
        "[書式設定]", "Ctrl + Shift + 5", "⌘ Cmd + Shift + 5", "パーセント書式"),

    # ═══════════════════════════════════════════════════════════════
    # セル操作
    # ═══════════════════════════════════════════════════════════════
    frozenset({"ctrl", "d"}): ShortcutEntry(
        "[セル操作]", "Ctrl + D", "⌘ Cmd + D", "下のセルにコピー"),
    frozenset({"ctrl", "r"}): ShortcutEntry(
        "[セル操作]", "Ctrl + R", "⌘ Cmd + R", "右のセルにコピー"),
    frozenset({"ctrl", "enter"}): ShortcutEntry(
        "[セル操作]", "Ctrl + Enter", "⌘ Cmd + Enter", "選択範囲に同じ内容を入力"),
    frozenset({"alt", "enter"}): ShortcutEntry(
        "[セル操作]", "Alt + Enter", "Option + Enter", "セル内で改行"),
    frozenset({"ctrl", "shift", "equal"}): ShortcutEntry(
        "[セル操作]", "Ctrl + Shift + +", "⌘ Cmd + Shift + +", "行・列を挿入"),
    frozenset({"ctrl", "minus"}): ShortcutEntry(
        "[セル操作]", "Ctrl + −", "⌘ Cmd + −", "行・列を削除"),
    frozenset({"ctrl", "shift", "k"}): ShortcutEntry(
        "[セル操作]", "Ctrl + Shift + K", "⌘ Cmd + Shift + K", "コメントを挿入"),
    frozenset({"ctrl", "alt", "m"}): ShortcutEntry(
        "[セル操作]", "Ctrl + Alt + M", "⌘ Cmd + Alt + M", "メモを挿入"),

    # ═══════════════════════════════════════════════════════════════
    # ナビゲーション
    # ═══════════════════════════════════════════════════════════════
    frozenset({"ctrl", "home"}): ShortcutEntry(
        "[ナビゲーション]", "Ctrl + Home", "⌘ Cmd + Home", "シートの先頭へ移動"),
    frozenset({"ctrl", "end"}): ShortcutEntry(
        "[ナビゲーション]", "Ctrl + End", "⌘ Cmd + End", "データ末尾へ移動"),
    frozenset({"ctrl", "right"}): ShortcutEntry(
        "[ナビゲーション]", "Ctrl + →", "⌘ Cmd + →", "右端のセルへ移動"),
    frozenset({"ctrl", "left"}): ShortcutEntry(
        "[ナビゲーション]", "Ctrl + ←", "⌘ Cmd + ←", "左端のセルへ移動"),
    frozenset({"ctrl", "up"}): ShortcutEntry(
        "[ナビゲーション]", "Ctrl + ↑", "⌘ Cmd + ↑", "上端のセルへ移動"),
    frozenset({"ctrl", "down"}): ShortcutEntry(
        "[ナビゲーション]", "Ctrl + ↓", "⌘ Cmd + ↓", "下端のセルへ移動"),
    frozenset({"ctrl", "shift", "right"}): ShortcutEntry(
        "[ナビゲーション]", "Ctrl + Shift + →", "⌘ Cmd + Shift + →", "右端まで選択を拡張"),
    frozenset({"ctrl", "shift", "left"}): ShortcutEntry(
        "[ナビゲーション]", "Ctrl + Shift + ←", "⌘ Cmd + Shift + ←", "左端まで選択を拡張"),
    frozenset({"ctrl", "shift", "down"}): ShortcutEntry(
        "[ナビゲーション]", "Ctrl + Shift + ↓", "⌘ Cmd + Shift + ↓", "下端まで選択を拡張"),
    frozenset({"ctrl", "shift", "up"}): ShortcutEntry(
        "[ナビゲーション]", "Ctrl + Shift + ↑", "⌘ Cmd + Shift + ↑", "上端まで選択を拡張"),
    frozenset({"shift", "space"}): ShortcutEntry(
        "[ナビゲーション]", "Shift + Space", "Shift + Space", "行全体を選択"),
    frozenset({"ctrl", "shift", "space"}): ShortcutEntry(
        "[ナビゲーション]", "Ctrl + Shift + Space", "⌘ Cmd + Shift + Space", "列全体を選択"),

    # ═══════════════════════════════════════════════════════════════
    # データ
    # ═══════════════════════════════════════════════════════════════
    frozenset({"ctrl", "semicolon"}): ShortcutEntry(
        "[データ]", "Ctrl + ;", "⌘ Cmd + ;", "今日の日付を入力"),
    frozenset({"ctrl", "shift", "semicolon"}): ShortcutEntry(
        "[データ]", "Ctrl + Shift + ;", "⌘ Cmd + Shift + ;", "現在の時刻を入力"),
    frozenset({"ctrl", "shift", "l"}): ShortcutEntry(
        "[データ]", "Ctrl + Shift + L", "⌘ Cmd + Shift + L", "フィルターの切り替え"),

    # ═══════════════════════════════════════════════════════════════
    # 表示・シート
    # ═══════════════════════════════════════════════════════════════
    frozenset({"alt", "shift", "k"}): ShortcutEntry(
        "[表示・シート]", "Alt + Shift + K", "Alt + Shift + K", "次のシートへ移動"),
    frozenset({"alt", "shift", "j"}): ShortcutEntry(
        "[表示・シート]", "Alt + Shift + J", "Alt + Shift + J", "前のシートへ移動"),
    frozenset({"ctrl", "shift", "f"}): ShortcutEntry(
        "[表示・シート]", "Ctrl + Shift + F", "⌘ Cmd + Shift + F", "全画面表示の切り替え"),
}


# ------------------------------------------------------------------
# ルックアップ関数
# ------------------------------------------------------------------

def lookup(raw_keys: set[str]) -> ShortcutEntry | None:
    """
    押下中の key_name セットからショートカットエントリを返す。
    修飾キーのみのセット（例: {"ctrl"}）は None を返す（誤ヒット防止）。
    """
    if not raw_keys:
        return None
    normalized = frozenset(normalize(k) for k in raw_keys)
    # 修飾キーのみのサブセットなら None
    if normalized <= _MODIFIER_ONLY:
        return None
    return SHORTCUTS.get(normalized)
