thonimport logging
import time
import urllib.parse
from dataclasses import dataclass, asdict
from typing import Any, Dict, Iterable, List, Optional

import requests
from bs4 import BeautifulSoup

from .html_cleaner import clean_text
from .contact_utils import (
    extract_emails_from_text,
    extract_phone_numbers_from_text,
    extract_website_from_text,
)

logger = logging.getLogger(__name__)

@dataclass
class MapyJob:
    query: Optional[str] = None
    city: Optional[str] = None
    urls: List[str] = None
    fast_mode: bool = False
    exact_match: bool = False
    max_results: int = 100

    def __post_init__(self) -> None:
        if self.urls is None:
            self.urls = []

class MapyScraper:
    """
    High-level scraper responsible for orchestrating search-based and URL-based scraping
    against Mapy.com. This implementation is generic and may require selector updates
    if Mapy.com layout changes, but it is written to be robust and safe by default.
    """

    def __init__(
        self,
        base_url: str,
        timeout_seconds: int = 15,
        user_agent: str = "MapyScraper/1.0",
        max_retries: int = 3,
        sleep_between_requests_ms: int = 500,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds
        self.max_retries = max_retries
        self.sleep_between_requests_ms = sleep_between_requests_ms

        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": user_agent,
                "Accept-Language": "en-US,en;q=0.9",
            }
        )

    # ------------- Public API -------------

    def run_job(self, job: MapyJob) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []

        if job.query and job.city:
            logger.info("Running search-based scraping for query=%r city=%r", job.query, job.city)
            search_results = self._scrape_search(job)
            results.extend(search_results)

        if job.urls:
            logger.info("Running URL-based scraping for %d direct URLs", len(job.urls))
            url_results = self._scrape_urls(job)
            results.extend(url_results)

        # Attach metadata to each record
        for record in results:
            record.setdefault("source", "mapy.com")
            record.setdefault("rawJob", asdict(job))

        return results

    # ------------- Search-based scraping -------------

    def _build_search_url(self, query: str, city: str) -> str:
        # Approximate Mapy.com search URL (may need adjusting for real usage).
        q = urllib.parse.quote_plus(f"{query} {city}")
        return f"{self.base_url}/search?query={q}"

    def _scrape_search(self, job: MapyJob) -> List[Dict[str, Any]]:
        if not job.query or not job.city:
            return []

        url = self._build_search_url(job.query, job.city)
        logger.debug("Search URL built: %s", url)

        html = self._fetch_with_retries(url)
        if html is None:
            return []

        soup = BeautifulSoup(html, "html.parser")
        cards = self._find_listing_cards(soup)

        logger.info("Found %d potential listing cards on search page", len(cards))
        results: List[Dict[str, Any]] = []
        for card in cards:
            if len(results) >= job.max_results:
                break

            basic = self._parse_listing_card(card)
            if not basic:
                continue

            if job.exact_match and job.query:
                name_lower = (basic.get("name") or "").strip().lower()
                if job.query.strip().lower() not in name_lower:
                    continue

            if job.fast_mode:
                results.append(basic)
                continue

            detail_url = basic.get("url")
            if not detail_url:
                results.append(basic)
                continue

            detail_data = self._scrape_detail_page(detail_url)
            merged = {**basic, **detail_data}
            results.append(merged)

        return results

    def _find_listing_cards(self, soup: BeautifulSoup) -> List[Any]:
        # Try a couple of generic patterns to find listing cards.
        selectors = [
            "article",
            "div.search-result",
            "div.poi-result",
            "li",
        ]
        cards: List[Any] = []
        for selector in selectors:
            cards = soup.select(selector)
            if cards:
                break
        return cards

    def _parse_listing_card(self, card: Any) -> Optional[Dict[str, Any]]:
        name = clean_text(card.select_one("h2, h3, .title, .name"))
        if not name:
            # Fallback: try aria-label or title
            aria_label = card.get("aria-label")
            if aria_label:
                name = clean_text(aria_label)

        if not name:
            return None

        address = clean_text(card.select_one(".address, .location, .street"))
        category = clean_text(card.select_one(".category, .tag"))

        # Try to pick a link that looks like a detail URL.
        link_el = card.select_one("a[href]")
        url = None
        if link_el:
            href = link_el.get("href")
            if href:
                url = self._absolutize_url(href)

        return {
            "name": name,
            "address": address or None,
            "category": category or None,
            "url": url,
        }

    # ------------- URL-based scraping -------------

    def _scrape_urls(self, job: MapyJob) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        for raw_url in job.urls:
            url = self._absolutize_url(raw_url)
            logger.debug("Scraping detail URL: %s", url)
            basic = {"url": url, "name": None, "address": None, "category": None}

            if job.fast_mode:
                # Even in fast mode, we must load the page once to get basic info.
                detail_data = self._scrape_detail_page(url)
                merged = {**basic, **detail_data}
                results.append(merged)
            else:
                detail_data = self._scrape_detail_page(url)
                merged = {**basic, **detail_data}
                results.append(merged)

        return results

    # ------------- Detail page parsing -------------

    def _scrape_detail_page(self, url: str) -> Dict[str, Any]:
        html = self._fetch_with_retries(url)
        if html is None:
            return {}

        soup = BeautifulSoup(html, "html.parser")

        name = clean_text(
            soup.select_one("h1, h2, .poi-title, .business-name, [itemprop='name']")
        )
        address = clean_text(
            soup.select_one(
                ".address, .poi-address, [itemprop='address'], [data-testid='address']"
            )
        )
        category = clean_text(
            soup.select_one(".category, .poi-category, [itemprop='category']")
        )

        # Contact info
        contact_block_text = ""
        contact_candidates = soup.select(
            ".contact, .contact-info, .contacts, [itemprop='telephone'], [itemprop='email']"
        )
        for el in contact_candidates:
            contact_block_text += " " + el.get_text(" ", strip=True)

        emails = extract_emails_from_text(contact_block_text)
        phones = extract_phone_numbers_from_text(contact_block_text)
        website = extract_website_from_text(soup, base_url=self.base_url)

        # Coordinates (if present in meta or data attributes)
        lat, lng = self._extract_coordinates(soup)

        opening_hours = clean_text(
            soup.select_one(".opening-hours, .hours, [itemprop='openingHours']")
        )

        return {
            "name": name or None,
            "address": address or None,
            "category": category or None,
            "email": emails[0] if emails else None,
            "phone": phones[0] if phones else None,
            "website": website,
            "openingHours": opening_hours or None,
            "coordinates": {"lat": lat, "lng": lng} if lat is not None and lng is not None else None,
        }

    def _extract_coordinates(self, soup: BeautifulSoup) -> (Optional[float], Optional[float]):
        # Check common patterns for latitude/longitude in meta tags or attributes.
        meta_lat = soup.find("meta", attrs={"property": "place:location:latitude"})
        meta_lng = soup.find("meta", attrs={"property": "place:location:longitude"})
        if meta_lat and meta_lng:
            try:
                return float(meta_lat.get("content")), float(meta_lng.get("content"))
            except (TypeError, ValueError):
                pass

        meta_geo = soup.find("meta", attrs={"name": "geo.position"})
        if meta_geo and meta_geo.get("content"):
            parts = meta_geo["content"].split(";")
            if len(parts) == 2:
                try:
                    return float(parts[0]), float(parts[1])
                except (TypeError, ValueError):
                    pass

        # Fallback: check elements with data-lat, data-lng
        lat_attr = None
        lng_attr = None
        for attr in ("data-lat", "data-lng", "data-latitude", "data-longitude"):
            el = soup.find(attrs={attr: True})
            if el is not None:
                if "lat" in attr and lat_attr is None:
                    lat_attr = el.get(attr)
                if ("lng" in attr or "long" in attr) and lng_attr is None:
                    lng_attr = el.get(attr)

        if lat_attr is not None and lng_attr is not None:
            try:
                return float(lat_attr), float(lng_attr)
            except (TypeError, ValueError):
                return None, None

        return None, None

    # ------------- HTTP helpers -------------

    def _absolutize_url(self, href: str) -> str:
        if href.startswith("http://") or href.startswith("https://"):
            return href
        return urllib.parse.urljoin(self.base_url + "/", href.lstrip("/"))

    def _fetch_with_retries(self, url: str) -> Optional[str]:
        for attempt in range(1, self.max_retries + 1):
            try:
                logger.debug("Fetching %s (attempt %d/%d)", url, attempt, self.max_retries)
                resp = self.session.get(url, timeout=self.timeout_seconds)
                if resp.status_code >= 400:
                    logger.warning("Got HTTP %s for %s", resp.status_code, url)
                    if 500 <= resp.status_code < 600 and attempt < self.max_retries:
                        self._sleep()
                        continue
                    return None
                return resp.text
            except requests.RequestException as exc:
                logger.warning("Request to %s failed (%s)", url, exc)
                if attempt >= self.max_retries:
                    return None
                self._sleep()
        return None

    def _sleep(self) -> None:
        time.sleep(self.sleep_between_requests_ms / 1000.0)