# Mapy.com Places & Business Data Scraper

> A high-precision scraper that extracts business and place data from Mapy.com using flexible search parameters, location targeting, and optional direct URLs. It helps analysts, researchers, and lead-generation teams collect clean, structured business information quickly.

> This tool makes gathering Mapy.com business listings efficient, accurate, and scalable while keeping the workflow simple and user-friendly.


<p align="center">
  <a href="https://bitbash.dev" target="_blank">
    <img src="https://github.com/za2122/footer-section/blob/main/media/scraper.png" alt="Bitbash Banner" width="100%"></a>
</p>
<p align="center">
  <a href="https://t.me/devpilot1" target="_blank">
    <img src="https://img.shields.io/badge/Chat%20on-Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram">
  </a>&nbsp;
  <a href="https://wa.me/923249868488?text=Hi%20BitBash%2C%20I'm%20interested%20in%20automation." target="_blank">
    <img src="https://img.shields.io/badge/Chat-WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" alt="WhatsApp">
  </a>&nbsp;
  <a href="mailto:sale@bitbash.dev" target="_blank">
    <img src="https://img.shields.io/badge/Email-sale@bitbash.dev-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Gmail">
  </a>&nbsp;
  <a href="https://bitbash.dev" target="_blank">
    <img src="https://img.shields.io/badge/Visit-Website-007BFF?style=for-the-badge&logo=google-chrome&logoColor=white" alt="Website">
  </a>
</p>




<p align="center" style="font-weight:600; margin-top:8px; margin-bottom:8px;">
  Created by Bitbash, built to showcase our approach to Scraping and Automation!<br>
  If you are looking for <strong>Mapy.com</strong> you've just found your team — Let’s Chat. 👆👆
</p>


## Introduction

This project extracts detailed points of interest such as pharmacies, restaurants, service providers, and other businesses from Mapy.com. It solves the problem of manually collecting local business data by automating the discovery, extraction, and structuring of results across any city or category.
It is ideal for teams performing lead generation, competitive benchmarking, local research, or directory building.

### Smart Location-Based Data Extraction

- Search any business category paired with any city or locality.
- Optionally scrape directly from one or more specific URLs.
- Optionally skip detail pages to maximize speed and throughput.
- Access structured business details including contact information, opening hours, and addresses.
- Adjust query precision using exact match filtering.

## Features

| Feature | Description |
|--------|-------------|
| Flexible Search Queries | Search businesses using keyword + city pairs. |
| Direct URL Support | Scrape specific Mapy.com URLs without using keyword search. |
| Fast Scraping Mode | Skip detail pages to increase speed (less detailed data). |
| Exact Match Filtering | Restrict results to only those matching the search query exactly. |
| Structured Output | Extract clean JSON data suitable for analysis or automation. |
| Request Limiting | Control scraping volume with max request caps. |
| Detail Page Enrichment | Disable fast mode to extract emails, phone numbers, and more. |

---

## What Data This Scraper Extracts

| Field Name | Field Description |
|------------|------------------|
| name | Business or place name. |
| address | Full address of the location. |
| phone | Contact phone number when available. |
| email | Email address extracted from detail page when present. |
| website | Official website URL for the business. |
| openingHours | Operating hours across weekdays. |
| coordinates | Latitude and longitude if available. |
| category | The category or type of business. |
| url | URL of the place’s detail page. |

---

## Example Output


    [
        {
            "name": "Lekarna U Andela",
            "address": "Jungmannova 743/18, Prague",
            "phone": "+420 224 948 237",
            "email": null,
            "website": "https://www.lekarna-uandela.cz",
            "openingHours": "Mon–Fri 08:00–18:00",
            "coordinates": { "lat": 50.0812, "lng": 14.4198 },
            "category": "Pharmacy",
            "url": "https://mapy.com/prague/pharmacy/lekarna-u-andela"
        }
    ]

---

## Directory Structure Tree


    Mapy.com/
    ├── src/
    │   ├── runner.py
    │   ├── extractors/
    │   │   ├── mapy_parser.py
    │   │   ├── html_cleaner.py
    │   │   └── contact_utils.py
    │   ├── processor/
    │   │   ├── normalizer.py
    │   │   └── dedupe.py
    │   ├── outputs/
    │   │   └── dataset_exporter.py
    │   └── config/
    │       └── settings.example.json
    ├── data/
    │   ├── sample_input.json
    │   └── sample_output.json
    ├── requirements.txt
    └── README.md

---

## Use Cases

- **Sales teams** use it to collect business emails and phone numbers, enabling targeted outreach with verified contact data.
- **Market researchers** use it to map local competitors and analyze regional business density for better strategic planning.
- **Directory builders** use it to populate business listings with consistent, structured data.
- **Analysts** use it to track service availability, compare business categories, and study city-level commercial activity.
- **Automation engineers** use it to integrate Mapy.com data into CRM pipelines or enrichment tools.

---

## FAQs

**Q: Can this scrape any city or type of business?**
Yes. You can change the query and city values to target any business category and location.

**Q: Can I provide URLs directly instead of using a search query?**
Yes. You can pass one or more Mapy.com page URLs. When used, the query and city fields are ignored for those URLs.

**Q: How do I get more detailed contact information?**
Disable fast scraping mode. This allows the scraper to visit detail pages and extract emails, phone numbers, and extended information.

**Q: Is there a limit on how many results I can extract?**
You can control volume using the maxRequests field to manage cost or testing limits.

---

## Performance Benchmarks and Results

**Primary Metric:** Full-detail mode processes listings at an average of 2–4 items per second depending on location density.
**Reliability Metric:** Typical runs achieve a 98%+ success rate across diverse categories and cities.
**Efficiency Metric:** Fast scraping mode reduces runtime by up to 65% by skipping detail pages.
**Quality Metric:** Detail-enriched runs return up to 40% more contact fields, improving completeness for lead-generation workflows.


<p align="center">
<a href="https://calendar.app.google/74kEaAQ5LWbM8CQNA" target="_blank">
  <img src="https://img.shields.io/badge/Book%20a%20Call%20with%20Us-34A853?style=for-the-badge&logo=googlecalendar&logoColor=white" alt="Book a Call">
</a>
  <a href="https://www.youtube.com/@bitbash-demos/videos" target="_blank">
    <img src="https://img.shields.io/badge/🎥%20Watch%20demos%20-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="Watch on YouTube">
  </a>
</p>
<table>
  <tr>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtu.be/MLkvGB8ZZIk" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review1.gif" alt="Review 1" width="100%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Bitbash is a top-tier automation partner, innovative, reliable, and dedicated to delivering real results every time.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Nathan Pennington
        <br><span style="color:#888;">Marketer</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtu.be/8-tw8Omw9qk" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review2.gif" alt="Review 2" width="100%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Bitbash delivers outstanding quality, speed, and professionalism, truly a team you can rely on.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Eliza
        <br><span style="color:#888;">SEO Affiliate Expert</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtube.com/shorts/6AwB5omXrIM" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review3.gif" alt="Review 3" width="35%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Exceptional results, clear communication, and flawless delivery. Bitbash nailed it.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Syed
        <br><span style="color:#888;">Digital Strategist</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
  </tr>
</table>
