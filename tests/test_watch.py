from datetime import date

from src.edtech_watch import CoursePage, compare_pages, render_report


def test_deadline_change_triggers_alert_and_report_context() -> None:
    old = "Course: Algebra\nDeadline: 2026-09-10"
    new = "Course: Algebra\nDeadline: 2026-09-17"
    alert = compare_pages(old, new)
    page = CoursePage("Algebra", "cohort", date(2026, 9, 17), "https://school.test/report", new)

    assert alert.changed is True
    assert "deadline=2026-09-17" in render_report(page, alert)


def test_same_page_does_not_alert() -> None:
    alert = compare_pages("unchanged", "unchanged")
    assert alert.changed is False
