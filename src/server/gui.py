import threading
import tkinter as tk
from tkinter import messagebox
import webbrowser

from .core import (
    CONTAINER_NAME,
    get_server_status,
    get_tailscale_ip,
    start_docker,
    start_tailscale,
    stop_server,
)
from .installer import install_docker, install_tailscale
from .utils import (
    is_installed,
    start_app_if_not_running,
    wait_for_docker_ready,
    wait_for_minecraft_ready,
)


class MinecraftServerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Minecraft Server Launcher")
        self.root.geometry("580x560")

        self.create_widgets()
        self.update_install_buttons()

        # ウィンドウを閉じたらサーバー停止
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        # STEP 0: インストール関連
        step0_label = tk.Label(
            self.root,
            text="STEP 0: 前提ソフトのインストール",
            font=("Arial", 12, "bold"),
        )
        step0_label.pack(pady=(10, 2))

        install_frame = tk.Frame(self.root)
        install_frame.pack(pady=(0, 10))

        self.tailscale_button = tk.Button(
            install_frame,
            text="Tailscale をインストール",
            command=self.install_tailscale_threaded,
            width=28,
        )
        self.tailscale_button.pack(side=tk.LEFT, padx=10)

        self.docker_button = tk.Button(
            install_frame,
            text="Docker をインストール",
            command=self.install_docker_threaded,
            width=28,
        )
        self.docker_button.pack(side=tk.LEFT, padx=10)

        # STEP 1: サーバー制御
        step1_label = tk.Label(
            self.root, text="STEP 1: サーバーを起動", font=("Arial", 12, "bold")
        )
        step1_label.pack(pady=(5, 5))

        self.start_button = tk.Button(
            self.root,
            text="サーバーを起動",
            command=self.start_server,
            height=2,
            width=30,
        )
        self.start_button.pack(pady=5)

        self.status_label = tk.Label(self.root, text="サーバー状態を確認中…")
        self.status_label.pack(pady=5)

        self.stop_button = tk.Button(
            self.root, text="サーバーを停止", command=self.stop_server
        )
        self.stop_button.pack(pady=5)

        # ログ表示エリア
        self.log_box = tk.Text(self.root, height=15, width=70, wrap="word")
        self.log_box.pack(padx=10, pady=10)

        # STEP 2: サーバー共有
        step2_label = tk.Label(
            self.root, text="STEP 2: サーバーを共有する", font=("Arial", 12, "bold")
        )
        step2_label.pack(pady=(5, 5))

        share_frame = tk.Frame(self.root)
        share_frame.pack(pady=(0, 10))

        tk.Button(
            share_frame,
            text="📘 共有方法を見る",
            command=self.show_share_guide,
            width=20,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            share_frame,
            text="🌐 Tailscale管理画面を開く",
            command=self.open_tailscale_share_page,
            width=20,
        ).pack(side=tk.LEFT, padx=5)

        # 定期的なステータス更新を開始
        self.update_server_status()

    def log(self, text):
        self.log_box.insert(tk.END, text + "\n")
        self.log_box.see(tk.END)

    def update_install_buttons(self):
        if is_installed("tailscale"):
            self.tailscale_button.config(
                text="✔ Tailscale インストール済", state="disabled"
            )
        else:
            self.tailscale_button.config(
                text="Tailscale をインストール", state="normal"
            )

        if is_installed("docker"):
            self.docker_button.config(text="✔ Docker インストール済", state="disabled")
        else:
            self.docker_button.config(text="Docker をインストール", state="normal")

    def update_server_status(self):
        is_running = get_server_status()
        if is_running:
            self.status_label.config(text="🟢 サーバー起動中", foreground="green")
        else:
            self.status_label.config(text="🔴 サーバー停止中", foreground="red")
        self.root.after(3000, self.update_server_status)

    def install_tailscale_threaded(self):
        threading.Thread(target=lambda: install_tailscale(self.log)).start()
        self.update_install_buttons()

    def install_docker_threaded(self):
        threading.Thread(target=lambda: install_docker(self.log)).start()
        self.update_install_buttons()

    def start_server(self):
        self.start_button.config(state="disabled")
        threading.Thread(target=self.run_server).start()

    def run_server(self):
        if not is_installed("tailscale"):
            self.log("Tailscale が見つかりません。インストールしてください。")
            messagebox.showwarning(
                "未インストール",
                "Tailscale が見つかりません。インストールしてください。",
            )
            self.start_button.config(state="normal")
            return
        if not is_installed("docker"):
            self.log("Docker が見つかりません。インストールしてください。")
            messagebox.showwarning(
                "未インストール", "Docker が見つかりません。インストールしてください。"
            )
            self.start_button.config(state="normal")
            return

        start_app_if_not_running(
            "tailscale-ipn.exe", r"C:\Program Files\Tailscale IPN\tailscale-ipn.exe"
        )
        start_app_if_not_running(
            "Docker Desktop.exe", r"C:\Program Files\Docker\Docker\Docker Desktop.exe"
        )

        if not wait_for_docker_ready(self.log):
            messagebox.showerror("エラー", "Docker Engine の起動に失敗しました")
            self.start_button.config(state="normal")
            return

        if not start_tailscale(self.log):
            self.start_button.config(state="normal")
            return
        ip = get_tailscale_ip(self.log)
        if not ip:
            self.start_button.config(state="normal")
            return
        if not start_docker(self.log):
            self.start_button.config(state="normal")
            return

        if not wait_for_minecraft_ready(CONTAINER_NAME, self.log):
            messagebox.showerror(
                "エラー", "Minecraft サーバーの準備完了を検出できませんでした。"
            )
            self.start_button.config(state="normal")
            return

        self.log(f"\nサーバー起動完了！\n接続アドレス: {ip}")
        messagebox.showinfo(
            "成功", f"Minecraft サーバーが起動しました！\n接続アドレス: {ip}"
        )
        self.start_button.config(state="normal")

    def open_tailscale_share_page(self):
        self.log("🌐 Tailscale管理画面を開きます...")
        webbrowser.open("https://login.tailscale.com/admin/machines")

    def show_share_guide(self):
        guide = (
            "🧑‍🤝‍🧑 サーバーを友達と共有する方法\n\n"
            "① 「🌐 Tailscale管理画面を開く」ボタンをクリック\n"
            "② Minecraftサーバーを起動している端末を探す（例：desktop-**など）\n"
            "③ 「Share...」を選択\n"
            "④ 「Copy share link」を選択してコピー\n"
            "⑤ 友達にLINEやDiscordでリンクを送信！\n\n"
        )
        self.log(guide)

    def stop_server(self):
        if stop_server(self.log):
            self.log("サーバーを停止しました。")
        else:
            messagebox.showerror("エラー", "サーバーの停止中にエラーが発生しました。")

    def on_closing(self):
        # サーバーが実行中なら停止を試みる
        if get_server_status():
            self.stop_server()
        self.root.destroy()

    def run(self):
        self.root.mainloop()
