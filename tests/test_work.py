from scrapy.http import Request, HtmlResponse
from scraper.spiders.workua import WorkUaSpider


def test_douua_parse_vacancy():
    with open("tests/responses/work_vacancy.html", "r", encoding="utf-8") as f:
        html_content = f.read()

    url = "https://www.work.ua/jobs/7891821/"
    response = HtmlResponse(
        url=url, body=html_content, encoding="utf-8", request=Request(url=url)
    )
    spider = WorkUaSpider()
    result = list(spider.parse_detail(response))
    assert len(result) > 0
    item = result[0]

    assert item["level"] == "junior"
    assert "JavaScript" in item["techs"]["requirements"]
    assert "Python" in item["techs"]["requirements"]
    assert "Python" in item["techs"]["requirements"]
