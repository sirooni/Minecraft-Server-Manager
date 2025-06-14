"""
Minecraft Server Join GUI
サーバー参加用のGUIアプリケーション
"""

import tkinter as tk
from tkinter import messagebox, ttk
import threading

from .core import start_tailscale, open_invite_url
from .installer import install_tailscale, is_tailscale_installed


class JoinGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Minecraft Server Joiner")
        self.root.geometry("580x400")  # host側と同じ幅に変更

        self.create_widgets()
        self.update_install_button()

    def create_widgets(self):
        # STEP 1: Tailscaleのインストール
        step1_label = tk.Label(
            self.root,
            text="STEP 1: Tailscaleのインストール",
            font=("Arial", 12, "bold"),
        )
        step1_label.pack(pady=(10, 2))

        self.install_button = tk.Button(
            self.root,
            text="Tailscaleをインストール",
            command=self.install_tailscale_threaded,
            width=28,
        )
        self.install_button.pack(pady=(0, 10))

        # STEP 2: 招待URLの入力
        step2_label = tk.Label(
            self.root, text="STEP 2: 招待URLを入力", font=("Arial", 12, "bold")
        )
        step2_label.pack(pady=(5, 5))

        # 説明テキスト
        instruction = (
            "1. サーバー管理者から受け取った招待URLをペーストしてください。\n"
            "2. 「Tailscaleを起動して接続」ボタンを押してください。\n"
            "3. ブラウザが開くので、指示に従って接続を許可してください。"
        )
        tk.Label(
            self.root,
            text=instruction,
            justify=tk.LEFT,
            wraplength=540,  # host側と同じ幅に合わせる
        ).pack(padx=20, pady=5)

        # URL入力欄
        url_frame = ttk.LabelFrame(self.root, text="招待URL", padding=5)
        url_frame.pack(fill=tk.X, padx=20, pady=5)

        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(
            url_frame, textvariable=self.url_var, width=70  # host側と同じ幅に合わせる
        )
        self.url_entry.pack(fill=tk.X, padx=5)

        # STEP 3: 接続ボタン
        step3_label = tk.Label(
            self.root, text="STEP 3: Tailscaleに接続", font=("Arial", 12, "bold")
        )
        step3_label.pack(pady=(15, 5))

        self.connect_button = tk.Button(
            self.root,
            text="Tailscaleを起動して接続",
            command=self.connect_tailscale,
            width=28,
            height=2,  # host側と同じように高さを2に設定
        )
        self.connect_button.pack(pady=5)

    def update_install_button(self):
        """インストールボタンの状態を更新"""
        if is_tailscale_installed():
            self.install_button.config(
                text="✔ Tailscaleインストール済", state="disabled"
            )
        else:
            self.install_button.config(text="Tailscaleをインストール", state="normal")

    def install_tailscale_threaded(self):
        """Tailscaleのインストールを別スレッドで実行"""
        self.install_button.config(state="disabled")
        threading.Thread(target=self._install_tailscale, daemon=True).start()

    def _install_tailscale(self):
        """Tailscaleをインストール"""
        if install_tailscale():  # ログコールバックを削除
            self.update_install_button()
        else:
            self.install_button.config(state="normal")

    def connect_tailscale(self):
        """Tailscaleを起動して接続"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("入力エラー", "招待URLを入力してください。")
            return

        self.connect_button.config(state="disabled")

        def connect_thread():
            if not start_tailscale():  # ログコールバックを削除
                self.connect_button.config(state="normal")
                return

            if not open_invite_url(url):  # ログコールバックを削除
                self.connect_button.config(state="normal")
                return

            messagebox.showinfo(
                "接続手順完了", "ブラウザの指示に従ってネットワークに参加してください。"
            )
            self.connect_button.config(state="normal")

        threading.Thread(target=connect_thread, daemon=True).start()

    def run(self):
        """GUIを実行"""
        self.root.mainloop()


if __name__ == "__main__":
    gui = JoinGUI()
    gui.run()
