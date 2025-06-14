"""
Docker と Tailscale のインストール管理
"""

from ..shared.utils.installer import install_tailscale, install_with_winget
from ..shared.utils.system import is_installed


def install_docker():
    """
    Dockerをインストールする
    """
    if is_installed("docker"):
        return True

    return install_with_winget("Docker.DockerDesktop")
