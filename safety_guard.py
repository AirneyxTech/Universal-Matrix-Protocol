#!/usr/bin/env python3
# safety_guard.py  –  Termux-ready safety + sanity check for live Lagos data
# Airneyx 2026  –  MPL-2.0

_THRESHOLD = 0.9   # Toxic limit for Pollution

def _sanity_check(vector: dict) -> bool:
    """Return False if any value is outside 0-1 range."""
    for k, v in vector.items():
        if not (isinstance(v, (int, float)) and 0.0 <= v <= 1.0):
            print(f"⚠️  System Error: field '{k}' = {v} (must be 0-1)")
            return False
    return True

def validate_state(vector: dict) -> bool:
    """
    Live-data safety gate for Lagos State Vector.
    1. Sanity-check all values.
    2. Reject if Pollution > 0.9.
    Returns True only if both pass.
    """
    if not _sanity_check(vector):
        return False

    pollution = float(vector.get("Pollution", 0.0))
    if pollution > _THRESHOLD:
        print("⛔ BLOCK: Solution violates Human Safety Protocol.")
        return False
    return True


# ---- quick self-test ----
if __name__ == "__main__":
    print("Safe:",      validate_state({"Pollution": 0.65}))
    print("Toxic:",     validate_state({"Pollution": 0.91}))
    print("Bad range:", validate_state({"Pollution": -1}))
    print("Bad type:",  validate_state({"Pollution": "999"}))

