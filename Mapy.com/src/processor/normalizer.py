thonfrom typing import Any, Dict, Optional

def _ensure_coordinates(raw: Any) -> Optional[Dict[str, float]]:
    if raw is None:
        return None

    if isinstance(raw, dict) and "lat" in raw and "lng" in raw:
        try:
            lat = float(raw["lat"])
            lng = float(raw["lng"])
            return {"lat": lat, "lng": lng}
        except (TypeError, ValueError):
            return None

    # Accept tuple or list [lat, lng]
    if isinstance(raw, (list, tuple)) and len(raw) == 2:
        try:
            lat = float(raw[0])
            lng = float(raw[1])
            return {"lat": lat, "lng": lng}
        except (TypeError, ValueError):
            return None

    return None

def normalize_record(raw: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize a raw scraped record into a stable, predictable schema used by
    downstream tools and clients.

    The schema is:
    {
        "name": str or None,
        "address": str or None,
        "phone": str or None,
        "email": str or None,
        "website": str or None,
        "openingHours": str or None,
        "coordinates": { "lat": float, "lng": float } or None,
        "category": str or None,
        "url": str or None,
        "source": "mapy.com",
        "rawJob": { ... }   # original job metadata where available
    }
    """
    name = (raw.get("name") or "").strip() or None
    address = (raw.get("address") or "").strip() or None
    phone = (raw.get("phone") or "").strip() or None
    email = (raw.get("email") or "").strip() or None
    website = (raw.get("website") or "").strip() or None
    opening_hours = (raw.get("openingHours") or "").strip() or None
    category = (raw.get("category") or "").strip() or None
    url = (raw.get("url") or "").strip() or None

    coords = _ensure_coordinates(raw.get("coordinates"))

    normalized = {
        "name": name,
        "address": address,
        "phone": phone,
        "email": email,
        "website": website,
        "openingHours": opening_hours,
        "coordinates": coords,
        "category": category,
        "url": url,
        "source": raw.get("source") or "mapy.com",
        "rawJob": raw.get("rawJob") or None,
    }

    return normalized