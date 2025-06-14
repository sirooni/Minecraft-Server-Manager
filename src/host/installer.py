from tkinter import messagebox

from .utils import run_silently


def install_tailscale(log_callback=None):
    if log_callback:
        log_callback("Tailscale を CLI からインストールします…")
    result = run_silently(["winget", "install", "--id=Tailscale.Tailscale", "-e"])
    if result.returncode == 0:
        messagebox.showinfo(
            "Tailscale",
            "Tailscale のインストールが完了しました。再起動が必要な場合があります。",
        )
    else:
        if log_callback:
            log_callback(result.stderr)
        messagebox.showerror("エラー", "Tailscale のインストールに失敗しました")


def install_docker(log_callback=None):
    if log_callback:
        log_callback("Docker Desktop を CLI からインストールします…")
    result = run_silently(["winget", "install", "--id=Docker.DockerDesktop", "-e"])
    if result.returncode == 0:
        messagebox.showinfo(
            "Docker", "Docker のインストールが完了しました。PCを再起動してください。"
        )
    else:
        if log_callback:
            log_callback(result.stderr)
        messagebox.showerror("エラー", "Docker のインストールに失敗しました")
