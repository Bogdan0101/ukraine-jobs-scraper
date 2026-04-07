import scrapy
import json
from typing import Generator
from scrapy.http import Response, FormRequest
from scraper.utils import get_level


class DouUaSpider(scrapy.Spider):
    name = "douua"
    allowed_domains = ["dou.ua"]
    start_urls = ["https://jobs.dou.ua/vacancies/?search=python"]

    all_links_detail = []
    current_offset = 20
    csrf = ""

    def parse(self, res: Response, **kwargs) -> Generator:
        print("Dou Ua Spider started@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        first_page_links = res.css(
            "#vacancyListId > ul > li.l-vacancy > .title > a.vt::attr(href)"
        ).getall()
        self.all_links_detail.extend(first_page_links)

        self.csrf = (
            res
            .css("input[name=csrfmiddlewaretoken]::attr(value)")
            .get()
        )
        print("CSRF token:", self.csrf)

        yield FormRequest(
            url="https://jobs.dou.ua/vacancies/xhr-load/?search=python",
            method="POST",
            formdata={
                "csrfmiddlewaretoken": self.csrf if self.csrf else "",
                "count": str(self.current_offset),
            },
            headers={
                "X-Requested-With": "XMLHttpRequest",
                "Referer": res.url,
            },
            callback=self.parse_only_links,
        )

    def parse_only_links(self, res: Response) -> Generator:
        data = json.loads(res.text)
        html_str = data.get("html", "")

        if not html_str.strip():
            print(f"Total links {len(self.all_links_detail)}")
            for link in self.all_links_detail:
                print(link)
                yield res.follow(link, callback=self.parse_detail)
            return

        selector = scrapy.Selector(text=html_str)
        new_links = selector.css("div.title > a.vt::attr(href)").getall()

        if new_links:
            self.all_links_detail.extend(new_links)
            self.current_offset += len(new_links)

            yield FormRequest(
                url="https://jobs.dou.ua/vacancies/xhr-load/?search=python",
                method="POST",
                formdata={
                    "csrfmiddlewaretoken": self.csrf,
                    "count": str(self.current_offset),
                },
                callback=self.parse_only_links,
            )

    def parse_detail(self, res: Response) -> Generator:
        title_raw = res.css("div.l-vacancy > h1.g-h2::text").getall()
        title = " ".join(title_raw).strip()

        description_raw = res.css("div.vacancy-section *::text").getall()
        description = " ".join(
            [t.strip() for t in description_raw if t.strip()]
        )

        level = get_level(title, description)
        print(title)
        print(level)

        techs = {
            "requirements": [],
            "description": description,
        }

        yield {
            "level": level,
            "techs": techs,
        }
