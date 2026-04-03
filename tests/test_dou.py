from scrapy.http import Request, HtmlResponse
from scraper.spiders.douua import DouUaSpider


def test_douua_parse_vacancy():
    with open("tests/responses/dou_vacancy.html", "r", encoding="utf-8") as f:
        html_content = f.read()

    url = "https://jobs.dou.ua/companies/samawatt-sa/vacancies/340628/"
    response = HtmlResponse(
        url=url, body=html_content, encoding="utf-8", request=Request(url=url)
    )
    spider = DouUaSpider()
    result = list(spider.parse_detail(response))
    assert len(result) > 0
    item = result[0]

    assert item["level"] == "senior"
    assert "FastAPI" in item["techs"]["description"]
    assert "Python" in item["techs"]["description"]
