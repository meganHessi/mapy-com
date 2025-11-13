thonimport re
from typing import Optional

from bs4 import BeautifulSoup, Tag

_WHITESPACE_RE = re.compile(r"\s+")

def clean_text(node: Optional[Tag]) -> str:
    """
    Convert a BeautifulSoup node to stripped, normalized text.
    Returns an empty string if the node is None.
    """
    if node is None:
        return ""
    text = node.get_text(" ", strip=True)
    text = _WHITESPACE_RE.sub(" ", text)
    return text.strip()

def normalize_whitespace(text: str) -> str:
    """
    Normalize whitespace in an arbitrary string: collapse multiple spaces, strip edges.
    """
    text = _WHITESPACE_RE.sub(" ", text or "")
    return text.strip()

def safe_text_from_html(html: str) -> str:
    """
    Parse raw HTML and return stripped text for logging or fallback parsing.
    """
    soup = BeautifulSoup(html or "", "html.parser")
    return clean_text(soup)