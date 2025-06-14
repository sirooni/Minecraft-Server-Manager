"""
インストーラー関連の共通ユーティリティ関数
"""

import subprocess
from tkinter import messagebox, ttk, Toplevel, Label
import threading
import time

from .system import is_installed, run_silently
from .winget import is_winget_installed, install_winget


class InstallProgressDialog:
    def __init__(self, parent, title, package_name):
        self.window = Toplevel(parent)
        self.window.title(title)
        self.window.geometry("300x150")
        self.window.transient(parent)
        self.window.grab_set()

        # ウィンドウを中央に配置
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")

        Label(
            self.window, text=f"{package_name}をインストールしています...", pady=10
        ).pack()
        self.progress = ttk.Progressbar(self.window, mode="indeterminate", length=200)
        self.progress.pack(pady=20)
        self.status_label = Label(self.window, text="準備中...")
        self.status_label.pack(pady=10)

        self.progress.start()

    def update_status(self, text):
        self.status_label.config(text=text)

    def close(self):
        self.window.destroy()


def install_with_winget(package_id: str, scope: str = "user", parent=None) -> bool:
    """
    wingetを使用してパッケージをインストールする

    Args:
        package_id: インストールするパッケージのID
        scope: インストールスコープ（"user" または "machine"）
        parent: プログレスダイアログの親ウィンドウ

    Returns:
        bool: インストールに成功したかどうか
    """
    # wingetの存在確認
    if not is_winget_installed():
        answer = messagebox.askyesno(
            "wingetが必要です",
            "パッケージのインストールには「アプリインストーラー」(winget)が必要です。\n"
            "インストールしますか？",
        )
        if answer:
            if not install_winget():
                return False
        else:
            return False
    try:
        # wingetコマンドを構築
        command = [
            "winget",
            "install",
            "--id",
            package_id,
            "--scope",
            scope,
            "--accept-source-agreements",
            "--accept-package-agreements",
            "--silent",
        ]

        # インストールを実行
        result = run_silently(command)
        return result.returncode == 0

    except Exception as e:
        messagebox.showerror(
            "エラー", f"{package_id}のインストール中にエラーが発生しました: {e}"
        )
        return False


def install_tailscale(parent=None) -> bool:
    """
    Tailscaleをインストールする

    Args:
        parent: プログレスダイアログの親ウィンドウ（オプション）

    Returns:
        bool: インストールに成功したかどうか
    """
    if is_installed("tailscale"):
        return True

    return install_with_winget("Tailscale.Tailscale", parent=parent)
