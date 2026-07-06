import hashlib
from datetime import timezone


def make_id(url, existing_id=None):
    if existing_id is not None:
        return str(existing_id)
    return hashlib.sha256(url.encode("utf-8")).hexdigest()


def to_iso_z(dt):
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
