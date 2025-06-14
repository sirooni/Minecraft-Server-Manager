"""
Tailscaleの起動と招待URLの処理を行うコアモジュール
"""

import webbrowser
from tkinter import messagebox

from ..shared.utils.system import run_silently, start_app_if_not_running


def start_tailscale():
    """
    Tailscaleを起動する

    Returns:
        bool: 起動に成功したかどうか
    """
    try:
        # Tailscaleアプリケーションを起動
        if not start_app_if_not_running(
            "tailscale-ipn.exe",
            r"C:\Program Files\Tailscale IPN\tailscale-ipn.exe",
        ):
            return False

        # Tailscaleのネットワークに接続
        result = run_silently(["tailscale", "up"])
        return result.returncode == 0

    except Exception as e:
        messagebox.showerror("エラー", f"Tailscaleの起動中にエラーが発生しました: {e}")
        return False


def open_invite_url(url: str):
    """
    招待URLをブラウザで開く

    Args:
        url: 招待URL

    Returns:
        bool: 成功したかどうか
    """
    try:
        if not url.startswith("https://login.tailscale.com/"):
            raise ValueError("無効なTailscale招待URLです")

        webbrowser.open(url)
        return True

    except Exception as e:
        messagebox.showerror("エラー", f"URLを開く際にエラーが発生しました: {e}")
        return False
