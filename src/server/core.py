from tkinter import messagebox

from .utils import (
    is_installed,
    run_silently,
    start_app_if_not_running,
    wait_for_docker_ready,
    wait_for_minecraft_ready,
)

# コンテナ名の共通定義
CONTAINER_NAME = "minecraft-server"


def start_tailscale(log_callback=None):
    if log_callback:
        log_callback("[1/3] Tailscale に接続中...")
    result = run_silently(["tailscale", "up"])
    if result.returncode != 0:
        if log_callback:
            log_callback("Tailscale の起動に失敗しました")
        messagebox.showerror("エラー", "Tailscale の起動に失敗しました")
        return False
    return True


def get_tailscale_ip(log_callback=None):
    if log_callback:
        log_callback("[2/3] IP アドレス取得中...")
    result = run_silently(["tailscale", "ip", "--4"])
    if result.returncode != 0 or not result.stdout.strip():
        if log_callback:
            log_callback("IP アドレスの取得に失敗しました")
        messagebox.showerror("エラー", "IP アドレスの取得に失敗しました")
        return None
    return result.stdout.strip()


def start_docker(log_callback=None):
    if log_callback:
        log_callback("[3/3] Docker でサーバー起動中...")
    result = run_silently(["docker-compose", "up", "-d"])
    if result.returncode != 0:
        if log_callback:
            log_callback("Docker の起動に失敗しました")
        messagebox.showerror("エラー", "Docker の起動に失敗しました")
        return False
    return True


def stop_server(log_callback=None):
    try:
        run_silently(["docker", "stop", CONTAINER_NAME])
        if log_callback:
            log_callback("サーバーを停止しました。")
        return True
    except Exception as e:
        if log_callback:
            log_callback(f"サーバー停止中にエラー: {e}")
        return False


def get_server_status():
    try:
        result = run_silently(
            ["docker", "inspect", "-f", "{{.State.Running}}", CONTAINER_NAME]
        )
        return result.stdout.strip() == "true"
    except:
        return False


def run_server(log_callback=None) -> tuple[bool, str]:
    """
    Minecraftサーバーを起動する

    Args:
        log_callback: ログ出力用のコールバック関数

    Returns:
        tuple[bool, str]: (成功したかどうか, IPアドレスまたはエラーメッセージ)
    """
    # 前提条件チェック
    if not is_installed("tailscale"):
        message = "Tailscale が見つかりません。インストールしてください。"
        if log_callback:
            log_callback(message)
        messagebox.showwarning("未インストール", message)
        return False, message

    if not is_installed("docker"):
        message = "Docker が見つかりません。インストールしてください。"
        if log_callback:
            log_callback(message)
        messagebox.showwarning("未インストール", message)
        return False, message

    # アプリケーションの起動
    start_app_if_not_running(
        "tailscale-ipn.exe", r"C:\Program Files\Tailscale IPN\tailscale-ipn.exe"
    )
    start_app_if_not_running(
        "Docker Desktop.exe", r"C:\Program Files\Docker\Docker\Docker Desktop.exe"
    )

    # Docker Engineの準備待ち
    if not wait_for_docker_ready(log_callback):
        message = "Docker Engine の起動に失敗しました"
        messagebox.showerror("エラー", message)
        return False, message

    # Tailscaleの起動と接続
    if not start_tailscale(log_callback):
        return False, "Tailscaleの起動に失敗しました"

    ip = get_tailscale_ip(log_callback)
    if not ip:
        return False, "Tailscale IPの取得に失敗しました"

    # Dockerコンテナの起動
    if not start_docker(log_callback):
        return False, "Dockerの起動に失敗しました"

    # Minecraftサーバーの準備待ち
    if not wait_for_minecraft_ready(CONTAINER_NAME, log_callback):
        message = "Minecraft サーバーの準備完了を検出できませんでした"
        messagebox.showerror("エラー", message)
        return False, message

    return True, ip
