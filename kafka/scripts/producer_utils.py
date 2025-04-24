import json
import yaml
from datetime import datetime
from decimal import Decimal


def json_serializer(obj):
    """Custom serializer for json encoding."""
    if isinstance(obj, Decimal):
        return float(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type{type(obj)} not serializable")

def load_config(path):
    import yaml
    with open(path, 'r') as file:
        return yaml.safe_load(file)