from .gui import MinecraftServerGUI


def start_server():
    app = MinecraftServerGUI()
    app.run()
