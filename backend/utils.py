def parse_bool(inp: str | None, default: bool) -> bool:
    if inp is None or inp == "":
        return default
    if inp.lower() in ("1", "true"):
        return True
    return False
