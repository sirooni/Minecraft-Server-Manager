import shutil
import subprocess
import time


def is_installed(command):
    return shutil.which(command) is not None


def run_silently(command):
    return subprocess.run(
        command,
        creationflags=subprocess.CREATE_NO_WINDOW,
        capture_output=True,
        text=True,
    )


def start_app_if_not_running(process_name, exe_path):
    try:
        tasks = subprocess.check_output(
            ["tasklist"], text=True, creationflags=subprocess.CREATE_NO_WINDOW
        )
        if process_name not in tasks:
            return subprocess.Popen(
                [exe_path], shell=True, creationflags=subprocess.CREATE_NO_WINDOW
            )
    except Exception as e:
        raise Exception(f"{process_name} の起動に失敗しました: {e}")


def wait_for_docker_ready(log_callback=None, timeout=60):
    if log_callback:
        log_callback("Docker Engine の起動を待機中…")
    start_time = time.time()
    while time.time() - start_time < timeout:
        result = run_silently(["docker", "info"])
        if result.returncode == 0:
            if log_callback:
                log_callback("Docker Engine が起動しました。")
            return True
        time.sleep(2)
    if log_callback:
        log_callback("Docker Engine の起動にタイムアウトしました。")
    return False


def wait_for_minecraft_ready(
    container_name="minecraft-server", log_callback=None, timeout=120
):
    if log_callback:
        log_callback("Minecraft サーバーの準備完了を待機中…")
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            logs = subprocess.check_output(
                ["docker", "logs", "--since", "5s", container_name],
                text=True,
                stderr=subprocess.STDOUT,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
            if "Done" in logs and "For help" in logs:
                if log_callback:
                    log_callback("Minecraft サーバーが起動しました！")
                return True
        except Exception as e:
            if log_callback:
                log_callback(f"ログ取得中にエラー: {e}")
        time.sleep(3)
    if log_callback:
        log_callback("Minecraft サーバーの起動にタイムアウトしました。")
    return False
