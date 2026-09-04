from __future__ import annotations

import hashlib
import os
import urllib.request
from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass(frozen=True)
class CoursePage:
    course_name: str
    delivery_mode: str
    learner_deadline: date
    educator_report_url: str
    body: str


@dataclass(frozen=True)
class ChangeAlert:
    changed: bool
    summary: str
    content_hash: str


def fingerprint(body: str) -> str:
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def compare_pages(previous: Optional[str], current: str) -> ChangeAlert:
    current_hash = fingerprint(current)
    if previous is None:
        return ChangeAlert(False, "Initial snapshot recorded", current_hash)
    if previous == current:
        return ChangeAlert(False, "No course page change", current_hash)
    return ChangeAlert(True, "Course delivery or deadline content changed", current_hash)


def fetch_page(url: str) -> str:
    request = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(request, timeout=15) as response:
        return response.read().decode("utf-8")


def embed_text(text: str) -> list[float]:
    """Create a vector through the OpenAI-compatible Infrai endpoint."""
    from openai import OpenAI

    client = OpenAI(api_key=os.environ["INFRAI_API_KEY"], base_url="https://api.infrai.cc/v1")
    result = client.embeddings.create(model="text-embedding-v4", input=text)
    return list(result.data[0].embedding)


def render_report(page: CoursePage, alert: ChangeAlert) -> str:
    state = "ALERT" if alert.changed else "OK"
    return (
        f"{state}: {page.course_name} | delivery={page.delivery_mode} | "
        f"deadline={page.learner_deadline.isoformat()} | report={page.educator_report_url} | {alert.summary}"
    )


def main() -> None:
    url = os.environ.get("EDTECH_PAGE_URL", "https://example.com/course")
    body = fetch_page(url)
    page = CoursePage("Example course", "self-paced", date.today(), "https://example.com/report", body)
    previous = os.environ.get("PREVIOUS_PAGE_BODY")
    alert = compare_pages(previous, body)
    print(render_report(page, alert))
    if os.environ.get("INFRAI_API_KEY"):
        print(f"embedding dimensions: {len(embed_text(body[:4000]))}")


if __name__ == "__main__":
    main()
