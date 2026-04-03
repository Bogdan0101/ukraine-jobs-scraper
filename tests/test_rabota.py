from scrapy.http import Request, TextResponse
from scraper.spiders.rabotaua import RabotaUaSpider


def test_robota_parse_vacancy():
    with open("tests/responses/robota_vacancy.json", "r", encoding="utf-8") as f:
        json_data = f.read()

    url = "https://dracula.robota.ua/?q=getPublishedVacancy"
    response = TextResponse(
        url=url, body=json_data, encoding="utf-8", request=Request(url=url)
    )
    spider = RabotaUaSpider()
    result = list(spider.parse_detail(response))
    assert len(result) > 0
    item = result[0]
    assert item["level"] == "senior"
    assert "<p>" not in item["techs"]["description"]
    assert "FastAPI" in item["techs"]["description"]
    assert "PostgreSQL" in item["techs"]["description"]
