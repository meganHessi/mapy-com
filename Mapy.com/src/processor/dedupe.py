thonfrom typing import Dict, Iterable, List

def _build_key(record: Dict) -> str:
    """
    Build a stable, deterministic key for deduplication based on URL if present,
    otherwise on a normalized combination of name + address.
    """
    url = (record.get("url") or "").strip().lower()
    if url:
        return f"url:{url}"

    name = (record.get("name") or "").strip().lower()
    address = (record.get("address") or "").strip().lower()
    return f"nameaddr:{name}|{address}"

def dedupe_records(records: Iterable[Dict]) -> List[Dict]:
    """
    Remove duplicates while preserving the first occurrence of each logical entity.
    """
    seen_keys = set()
    deduped: List[Dict] = []

    for rec in records:
        key = _build_key(rec)
        if key in seen_keys:
            continue
        seen_keys.add(key)
        deduped.append(rec)

    return deduped