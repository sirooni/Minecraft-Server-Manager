"""
システム関連の共通ユーティリティ関数
"""

import os
import subprocess
from typing import List, Optional


def run_silently(
    command: List[str],
    check: bool = False,
    cwd: Optional[str] = None,
) -> subprocess.CompletedProcess:
    """
    コマンドをサイレントモードで実行する

    Args:
        command: 実行するコマンドとその引数のリスト
        check: Trueの場合、終了コードが0以外の場合に例外を発生させる
        cwd: コマンドを実行するディレクトリ

    Returns:
        subprocess.CompletedProcess: 実行結果
    """
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=check,
        cwd=cwd,
    )


def is_installed(command_name: str) -> bool:
    """
    指定されたコマンドがインストールされているか確認する

    Args:
        command_name: 確認するコマンド名

    Returns:
        bool: インストールされている場合はTrue
    """
    try:
        subprocess.run(
            ["where", command_name],
            capture_output=True,
            check=True,
        )
        return True
    except subprocess.CalledProcessError:
        return False


def start_app_if_not_running(process_name: str, exe_path: str) -> bool:
    """
    アプリケーションが実行されていない場合は起動する

    Args:
        process_name: プロセス名
        exe_path: 実行ファイルのパス

    Returns:
        bool: 起動に成功したかどうか
    """
    try:
        # タスクリストをチェック
        result = run_silently(["tasklist", "/FI", f"IMAGENAME eq {process_name}"])

        # プロセスが見つからない場合は起動
        if process_name not in result.stdout:
            if os.path.exists(exe_path):
                subprocess.Popen(exe_path)
                return True
            else:
                print(f"実行ファイルが見つかりません: {exe_path}")
                return False
        return True

    except Exception as e:
        print(f"アプリケーションの起動中にエラーが発生: {e}")
        return False
