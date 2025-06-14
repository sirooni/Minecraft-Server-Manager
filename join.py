"""
Minecraft Server Join Tool
サーバー参加用ツールのエントリーポイント
"""

from src.join.gui import JoinGUI


def main():
    gui = JoinGUI()
    gui.run()


if __name__ == "__main__":
    main()
