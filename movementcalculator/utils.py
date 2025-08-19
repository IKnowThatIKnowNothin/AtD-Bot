def normalize_location(name):
    """Lowercase, remove spaces and apostrophes for node matching."""
    return name.lower().replace(" ", "").replace("'", "")