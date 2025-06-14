from tkinter import messagebox

from .utils import run_silently, wait_for_docker_ready, wait_for_minecraft_ready

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
