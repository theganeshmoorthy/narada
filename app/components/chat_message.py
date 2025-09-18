from __future__ import annotations

import typing as t
from dataclasses import KW_ONLY, field

import rio

from .. import components as comps
from .. import conversation

class ChatMessage(rio.Component):
    """
    This component displays a single chat message. Using this you can create a
    message history by stacking multiple ChatMessage components vertically.
    """

    model: conversation.ChatMessage

    def build(self) -> rio.Component:
        # User messages look different from the bot's responses. This
        # makes it easy to distinguish between the two.

        if self.model.role == "user":
            icon = "material/emoji-people"
            color = "neutral"
        else:
            icon = "material/computer"
            color = "background"

        return rio.Row(
            # Display an icon on the left side of the message. It is wrapped
            # inside of a card to give it a circular shape.
            rio.Card(
                rio.Icon(icon, min_width=2, min_height=2, margin=0.8),
                # Using an enormous corner radius makes the card circular
                corner_radius=99999,
                color="neutral",
                margin=0.5,
                align_y=0,
            ),
            # The message content is displayed inside the second card. By using markdown,
            # we can easily format the text to include bold, italics, lists, etc.
            rio.Card(
                rio.Markdown(self.model.text, margin=1.5),
                grow_x=True,
                color=color,
            ),
        )