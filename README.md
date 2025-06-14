# Minecraft Server Manager

Minecraft サーバーの構築と参加を簡単にする GUI ツール

## 機能

### サーバーホスト側 (`src/host`)

- Docker ベースの Minecraft サーバーを簡単に起動
- Tailscale を使用した安全な P2P 接続
- 必要なソフトウェアの自動インストール
  - Docker Desktop
  - Tailscale

### クライアント側 (`src/join`)

- Tailscale の自動インストールと設定
- 招待 URL を使用した簡単な接続
- ステップバイステップのガイド付き UI

## 必要要件

- Windows 10/11
- Python 3.8 以上
- インターネット接続
- 管理者権限（インストール時）

## インストール方法

1. このリポジトリをクローン

```powershell
git clone <repository-url>
cd "Minecraft Server"
```

2. 必要な Python パッケージをインストール

```powershell
pip install -r requirements.txt
```

## 使用方法

### サーバーをホストする場合

1. `server.py`を実行

```powershell
python server.py
```

2. GUI の指示に従って：
   1. Docker と Tailscale をインストール
   2. サーバーを起動
   3. Tailscale 管理画面から招待リンクを作成
   4. 招待リンクを参加者に共有

### サーバーに参加する場合

1. `join.py`を実行

```powershell
python join.py
```

2. GUI の指示に従って：
   1. Tailscale をインストール
   2. 受け取った招待リンクを入力
   3. ブラウザの指示に従って接続を許可

## ディレクトリ構造

```
.
├── src/
│   ├── host/           # サーバーホスト側の機能
│   │   ├── gui.py      # ホストのGUI
│   │   └── core.py     # サーバー制御の中核機能
│   ├── join/           # クライアント側の機能
│   │   ├── gui.py      # 参加者用GUI
│   │   └── core.py     # 接続機能
│   └── shared/         # 共通機能
│       └── utils/      # ユーティリティ
├── server.py           # ホスト側エントリーポイント
├── join.py             # クライアント側エントリーポイント
└── requirements.txt    # 依存パッケージ
```

## 技術スタック

- **GUI**: tkinter
- **コンテナ**: Docker
- **ネットワーク**: Tailscale
- **パッケージ管理**: winget
- **開発ツール**:
  - flake8
  - black
  - isort

## ライセンス

MIT License

## 注意事項

- Minecraft サーバーの利用は、Mojang のガイドラインに従ってください
- Tailscale の利用は、無料アカウントの制限に従います
- サーバーのホストには十分な CPU、メモリ、ディスク容量が必要です
