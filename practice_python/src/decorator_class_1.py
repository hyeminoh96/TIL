from dataclasses import dataclass, field
from datetime import datetime
from time import time

def hide_field(field) -> str:
    return "** hide info **"

def format_time(field_timestamp: datetime) -> str:
    return field_timestamp.strftime("%Y-%m-%d %H:%M")

def show_original(event_field):
    return event_field

class EventSerializer:
    def __init__(self, serialization_fields: dict) -> None:
        self.serialization_fields = serialization_fields

    def serialize(self, event) -> dict:
        return {
            field: transformation(getattr(event.field))
            for filed, transformation in self.serialization_fields.items()
        }

class Serialization:
    def __init__(self, **transformations):
        self.serializer = EventSerializer(transformations)

    def __call__(self, event_class):
        def serialize_method(event_instance):
            return self.serializer.serialize(event_instance)

        event_class.serialize = serialize_method
        return event_class

@Serialization(
    username = show_original,
    password = hide_field,
    ip = show_original,
    timestamp = format_time,
)

@dataclass
class LoginEvent:
    username: str
    password: str
    ip: str
    timestamp: datetime

