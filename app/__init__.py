from __future__ import annotations

from pathlib import Path
import typing as t
import asyncio
from ollama import AsyncClient
import rio

from . import components as comps

def on_app_start(app: rio.App) -> None:
    """
    This function is called when the app starts up. It can be used to perform
    any initialization tasks that need to be done before the app is ready to
    use.
    """
    app.default_attachments.append(AsyncClient(host="http://localhost:11434"))
    print("App is starting up!")

# Define a theme for Rio to use.
#
# You can modify the colors here to adapt the appearance of your app or website.
# The most important parameters are listed, but more are available! You can find
# them all in the docs
#
# https://rio.dev/docs/api/theme
theme = rio.Theme.from_colors(
    primary_color=rio.Color.from_hex("01dffdff"),
    secondary_color=rio.Color.from_hex("0083ffff"),
    mode="dark",
)


# Create the Rio app
app = rio.App(
    name='app',
    theme=theme,
    assets_dir=Path(__file__).parent / "assets",
)

