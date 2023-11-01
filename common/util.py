import uuid


def is_vali_uuid(value):
    try:
        uuid.UUID(value)
        return True
    except ValueError:
        return False
