import pytest
from scraper.pipelines import ScraperPipeline
from scraper.collector import stats_storage
from scraper.utils import get_level


def test_scraper_pipeline():
    stats_storage.data = {k: {} for k in stats_storage.data}
    pipeline = ScraperPipeline()

    items = [
        {
            "level": get_level("Strong junior"),
            "techs": {
                "requirements": ["Python", "JS", "SQL"],
                "description": "We are looking for a Python developer who knows FastAPI and Docker.",
            },
        },
        {
            "level": get_level("Потрібен досвідченний Middle"),
            "techs": {
                "requirements": ["Django", "AWS", "PostgreSQL"],
                "description": "Middle Django dev. Ми використовуемо Redis та Celery в роботі.",
            },
        },
        {
            "level": get_level("Junior/Senior python developer"),
            "techs": {
                "requirements": ["Python", "JS", "SQL"],
                "description": "Junior/Senior position. Python and Linux.",
            },
        },
    ]

    for item in items:
        pipeline.process_item(item, spider=None)

    junior = stats_storage.data["junior"]
    assert junior["python"] == 1
    assert junior["sql"] == 1
    assert junior["javascript"] == 1

    middle = stats_storage.data["middle"]
    assert middle["django"] == 1
    assert middle["amazon web services"] == 1
    assert middle["postgresql"] == 1

    senior = stats_storage.data["senior"]
    assert senior["python"] == 1
    assert senior["sql"] == 1
    assert senior["javascript"] == 1
