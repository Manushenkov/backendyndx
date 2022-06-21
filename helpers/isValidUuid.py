import uuid


def isValidUuid(value):
    try:
        uuid.UUID(value)

        return True
    except ValueError:
        return False
