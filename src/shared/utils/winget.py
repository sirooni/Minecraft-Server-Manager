"""
wingetのインストール管理用モジュール
"""

import os
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path
from tkinter import messagebox


def is_winget_installed():
    """
    wingetがインストールされているかチェック
    """
    try:
        result = subprocess.run(
            ["winget", "--version"],
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def install_winget():
    """
    wingetをインストール
    """
    try:
        # Microsoft Storeのリンクを表示
        messagebox.showinfo(
            "wingetのインストール",
            "このツールの実行には「アプリインストーラー」（winget）が必要です。\n"
            "Microsoft Storeが開くので、「入手」ボタンをクリックしてインストールしてください。\n\n"
            "その後、このメッセージを閉じて再度操作を行ってください。",
        )
        # Microsoft StoreでのApp Installerページを開く
        os.system("start ms-windows-store://pdp/?ProductId=9NBLGGH4NNS1")
        return False

    except Exception as e:
        messagebox.showerror(
            "エラー",
            f"wingetのインストールに失敗しました:\n{str(e)}\n\n"
            "Microsoft Storeで「アプリインストーラー」を検索してインストールしてください。",
        )
        return False
