# scraper.py
from typing import Dict
import cloudscraper
from bs4 import BeautifulSoup
import trafilatura

UA_CHROME = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
             "AppleWebKit/537.36 (KHTML, like Gecko) "
             "Chrome/120.0.0.0 Safari/537.36")
UA_FIREFOX = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) "
              "Gecko/20100101 Firefox/128.0")

def _extract_title(soup: BeautifulSoup) -> str:
    for sel in [
        ("meta", {"property": "og:title"}),
        ("meta", {"name": "twitter:title"}),
    ]:
        tag = soup.find(*sel)
        if tag and tag.get("content"):
            return tag["content"].strip()
    h1 = soup.find("h1")
    if h1:
        return h1.get_text(strip=True)
    if soup.title and soup.title.string:
        return soup.title.string.strip()
    return "Untitled"

def fetch_article(url: str) -> Dict[str, str]:
    # Cloudflare-friendly HTTP client
    scraper = cloudscraper.create_scraper(
        browser={"browser": "chrome", "platform": "windows", "mobile": False}
    )
    headers = {
        "User-Agent": UA_CHROME,
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": "https://www.google.com/",
    }

    # Try once with Chrome UA, then once with Firefox UA if needed (avoid raise_for_status)
    r = scraper.get(url, headers=headers, timeout=25)
    if r.status_code != 200:
        headers["User-Agent"] = UA_FIREFOX
        r = scraper.get(url, headers=headers, timeout=25)

    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    title = _extract_title(soup)

    # Best extractor first
    extracted = trafilatura.extract(html, url=url, include_comments=False, favor_recall=True)
    if extracted and extracted.strip():
        return {"url": url, "title": title, "text": extracted}

    # Fallback: join visible paragraphs (inside <article> if present)
    article_tag = soup.find("article")
    if article_tag:
        paragraphs = [p.get_text(" ", strip=True) for p in article_tag.find_all("p")]
    else:
        paragraphs = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
    text = " ".join([p for p in paragraphs if p])

    return {"url": url, "title": title, "text": text}
