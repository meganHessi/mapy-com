thonimport re
from typing import List, Optional
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

_EMAIL_RE = re.compile(
    r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
    flags=re.IGNORECASE,
)

_PHONE_RE = re.compile(
    r"\+?\d[\d\s\-().]{7,}\d"
)

def extract_emails_from_text(text: str) -> List[str]:
    if not text:
        return []
    matches = _EMAIL_RE.findall(text)
    # Remove duplicates while preserving order
    seen = set()
    unique: List[str] = []
    for m in matches:
        m_lower = m.lower()
        if m_lower not in seen:
            seen.add(m_lower)
            unique.append(m)
    return unique

def extract_phone_numbers_from_text(text: str) -> List[str]:
    if not text:
        return []
    matches = _PHONE_RE.findall(text)
    cleaned_numbers: List[str] = []
    seen = set()
    for m in matches:
        cleaned = re.sub(r"[^\d+]", "", m)
        if len(cleaned) < 7:
            continue
        if cleaned in seen:
            continue
        seen.add(cleaned)
        cleaned_numbers.append(cleaned)
    return cleaned_numbers

def extract_website_from_text(soup: BeautifulSoup, base_url: Optional[str]) -> Optional[str]:
    """
    Look for a website link in common contact areas or anchor tags that look like external sites.
    """
    # Try explicit contact sections first
    for selector in [
        "a.website",
        ".contact a[href]",
        ".contact-info a[href]",
        ".contacts a[href]",
    ]:
        link = soup.select_one(selector)
        if link and link.get("href"):
            href = link["href"]
            full = _normalize_href(href, base_url)
            if full:
                return full

    # Fallback: check all links and pick the first external one not pointing to the map service.
    for a in soup.find_all("a", href=True):
        href = a["href"]
        full = _normalize_href(href, base_url)
        if not full:
            continue

        parsed = urlparse(full)
        if not parsed.netloc:
            continue

        # Basic heuristic to avoid self-links
        if base_url and parsed.netloc in urlparse(base_url).netloc:
            continue

        return full

    return None

def _normalize_href(href: str, base_url: Optional[str]) -> Optional[str]:
    if not href:
        return None
    if href.startswith("mailto:") or href.startswith("tel:"):
        return None
    if href.startswith("http://") or href.startswith("https://"):
        return href
    if base_url:
        return urljoin(base_url.rstrip("/") + "/", href.lstrip("/"))
    return href