"""This module defines the Event class."""


class Event:
    """A class to represent an event with a name and associated data."""

    def __init__(self, name: str, data):
        """Initialize the Event with a name and data."""
        self.name = name
        self.data = data
