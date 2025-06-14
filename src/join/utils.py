"""
ユーティリティ関数
"""

import shutil
import subprocess


def is_installed(command):
    """
    コマンドがインストールされているかチェック

    Args:
        command: チェックするコマンド名

    Returns:
        bool: コマンドが利用可能かどうか
    """
    return shutil.which(command) is not None


def run_silently(command):
    """
    ウィンドウを表示せずにコマンドを実行

    Args:
        command: 実行するコマンドのリスト

    Returns:
        subprocess.CompletedProcess: 実行結果
    """
    return subprocess.run(
        command,
        creationflags=subprocess.CREATE_NO_WINDOW,
        capture_output=True,
        text=True,
    )
