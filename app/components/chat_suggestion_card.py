from __future__ import annotations
from dataclasses import KW_ONLY, field
import typing as t
import rio
import asyncio
from .. import components as comps

class ChatSuggestionCard(rio.Component):
    """
    This component displays a single chat suggestion card. It is used to show
    suggested prompts or actions that the user can take.
    """

    icon: str
    text: str

    on_press: rio.EventHandler[str] = None

    async def _on_press(self) -> None:
        await self.call_event_handler(self.on_press, self.text)

    def build(self) -> rio.Component:
        # A suggestion is just an icon, text and button wrapped inside a card.
        return rio.Card(
            rio.Column(
                rio.Icon(self.icon, min_width=1.8, min_height=1.8, margin=0),
                rio.Text(
                    self.text,
                    justify="center",
                    overflow="wrap",
                    grow_y=True,
                    align_y=0.5,
                ),
                rio.Button(
                    "Ask",
                    icon="material/send",
                    on_press=self._on_press,
                    style="minor",
                ),
                spacing=0.6,
                margin=1,
            ),
        )