def validate_isbn13(isbn: str) -> str:
    """Validate and normalize an ISBN-13 string.

    Strips hyphens and spaces, checks length and check digit.
    Returns the normalized (digits-only) ISBN.
    Raises ValueError if invalid.
    """
    normalized = isbn.replace("-", "").replace(" ", "")

    if len(normalized) != 13:
        raise ValueError("ISBN must be exactly 13 digits (after removing hyphens/spaces)")

    if not normalized.isdigit():
        raise ValueError("ISBN must contain only digits (and optional hyphens/spaces)")

    weights = [1, 3] * 6
    total = sum(int(d) * w for d, w in zip(normalized[:12], weights))
    check = (10 - (total % 10)) % 10

    if int(normalized[12]) != check:
        raise ValueError(f"Invalid ISBN-13 check digit: expected {check}, got {normalized[12]}")

    return normalized
