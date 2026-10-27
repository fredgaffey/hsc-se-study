import secrets


def generate_id(current_list, max_value=999999999):
    """Helper func - generates random num based on list using cryptographically secure random"""
    existing_ids = set(current_list)
    R = secrets.randbelow(max_value + 1)

    while R in existing_ids:
        R = secrets.randbelow(max_value + 1)
    return str(R)
