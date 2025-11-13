thonimport argparse
import json
import logging
from pathlib import Path
from typing import Any, Dict, List

from extractors.mapy_parser import MapyScraper, MapyJob
from processor.normalizer import normalize_record
from processor.dedupe import dedupe_records
from outputs.dataset_exporter import export_to_json

def load_settings(settings_path: Path) -> Dict[str, Any]:
    if not settings_path.exists():
        logging.warning("Settings file %s not found. Falling back to defaults.", settings_path)
        return {}

    with settings_path.open("r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as exc:
            logging.error("Failed to parse settings JSON: %s", exc)
            return {}

def load_jobs(input_path: Path) -> List[Dict[str, Any]]:
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    with input_path.open("r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Invalid JSON in input file: {exc}") from exc

    if not isinstance(data, list):
        raise ValueError("Input JSON must be an array of job objects.")
    return data

def build_scraper_from_settings(settings: Dict[str, Any]) -> MapyScraper:
    base_url = settings.get("baseUrl", "https://mapy.com")
    timeout = settings.get("timeoutSeconds", 15)
    user_agent = settings.get("userAgent", "MapyScraper/1.0 (+https://bitbash.dev)")
    max_retries = settings.get("maxRetries", 3)
    sleep_ms = settings.get("sleepBetweenRequestsMs", 500)

    return MapyScraper(
        base_url=base_url,
        timeout_seconds=timeout,
        user_agent=user_agent,
        max_retries=max_retries,
        sleep_between_requests_ms=sleep_ms,
    )

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Mapy.com Places & Business Data Scraper (Bitbash demo implementation)"
    )
    parser.add_argument(
        "--input",
        type=str,
        default=str(Path("data") / "sample_input.json"),
        help="Path to input JSON describing scraping jobs.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=str(Path("data") / "sample_output.json"),
        help="Path where output JSON dataset will be written.",
    )
    parser.add_argument(
        "--settings",
        type=str,
        default=str(Path("src") / "config" / "settings.example.json"),
        help="Path to settings JSON file.",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        help="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).",
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=getattr(logging, args.log_level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    )

    input_path = Path(args.input)
    output_path = Path(args.output)
    settings_path = Path(args.settings)

    logging.info("Loading settings from %s", settings_path)
    settings = load_settings(settings_path)
    scraper = build_scraper_from_settings(settings)

    logging.info("Loading jobs from %s", input_path)
    job_dicts = load_jobs(input_path)

    all_raw_records: List[Dict[str, Any]] = []
    for idx, job_dict in enumerate(job_dicts, start=1):
        job = MapyJob(
            query=job_dict.get("query"),
            city=job_dict.get("city"),
            urls=job_dict.get("urls") or [],
            fast_mode=bool(job_dict.get("fastMode", False)),
            exact_match=bool(job_dict.get("exactMatch", False)),
            max_results=int(job_dict.get("maxResults", 100)),
        )

        logging.info(
            "Running job %d/%d: query=%r city=%r urls=%d fast_mode=%s exact_match=%s max_results=%d",
            idx,
            len(job_dicts),
            job.query,
            job.city,
            len(job.urls),
            job.fast_mode,
            job.exact_match,
            job.max_results,
        )

        try:
            records = scraper.run_job(job)
            logging.info("Job %d produced %d raw records", idx, len(records))
            all_raw_records.extend(records)
        except Exception as exc:  # noqa: BLE001
            logging.exception("Job %d failed: %s", idx, exc)

    logging.info("Normalizing %d records", len(all_raw_records))
    normalized_records = [normalize_record(rec) for rec in all_raw_records]

    logging.info("Deduplicating records")
    deduped_records = dedupe_records(normalized_records)
    logging.info("After deduplication: %d records", len(deduped_records))

    logging.info("Exporting dataset to %s", output_path)
    export_to_json(deduped_records, output_path)

    logging.info("Done.")

if __name__ == "__main__":
    main()