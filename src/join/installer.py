"""
Tailscaleのインストールと起動を管理するモジュール
"""

from ..shared.utils.installer import install_tailscale
from ..shared.utils.system import is_installed

# 既存の関数をsharedモジュールからインポートして使用するように変更
__all__ = ["install_tailscale", "is_tailscale_installed"]


def is_tailscale_installed():
    """Tailscaleがインストールされているか確認"""
    return is_installed("tailscale")
