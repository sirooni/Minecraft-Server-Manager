"""
インストーラー関連の共通ユーティリティ関数
"""

import subprocess
from tkinter import messagebox

from .system import is_installed, run_silently


def install_with_winget(package_id: str, scope: str = "user") -> bool:
    """
    wingetを使用してパッケージをインストールする

    Args:
        package_id: インストールするパッケージのID
        scope: インストールスコープ（"user" または "machine"）

    Returns:
        bool: インストールに成功したかどうか
    """
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


def install_tailscale() -> bool:
    """
    Tailscaleをインストールする

    Returns:
        bool: インストールに成功したかどうか
    """
    if is_installed("tailscale"):
        return True

    return install_with_winget("Tailscale.Tailscale")
