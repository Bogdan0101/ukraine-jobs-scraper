import scrapy
from typing import Generator
from scrapy.http import Response
from scraper.utils import get_level


class WorkUaSpider(scrapy.Spider):
    name = "workua"
    allowed_domains = ["www.work.ua"]
    start_urls = ["https://www.work.ua/jobs-python/"]

    def parse(self, res: Response, **kwargs) -> Generator:
        print("Work Ua Spider started-----------------------")
        print("@@@@@@@@@@@@@@@@@Page@@@@@@@@@@@@@@@@@@@@")
        links_detail_pref = res.css(
            "#pjax-jobs-list > div > div > h2 > a::attr(href)"
        ).getall()
        for prefix in links_detail_pref:
            yield res.follow(prefix, callback=self.parse_detail)

        next_pref = res.css(
            "nav > ul.visible-xs-block > li.ml-sm > a::attr(href)"
        ).get()
        if next_pref:
            print(f"{next_pref}----------------------------")
            yield res.follow(next_pref, callback=self.parse)

    def parse_detail(self, res: Response) -> Generator:
        title_raw = res.css("div.wordwrap > div > div > h1 *::text").getall()
        title = " ".join(title_raw).strip()

        job_requirements_raw = res.xpath(
            '//li[span[@title="Умови й вимоги"]]//text()'
        ).getall()
        job_requirements = " ".join(
            [t.strip() for t in job_requirements_raw if t.strip()]
        )

        description_raw = res.css("div#job-description *::text").getall()
        description = " ".join(
            [t.strip() for t in description_raw if t.strip()]
        )
        print(title)

        level = get_level(title, job_requirements, description)
        print(level)

        techs_requirements = res.css(
            "div.flex-wrap > ul > li > span.ellipsis::text"
        ).getall()

        techs = {
            "requirements": techs_requirements,
            "description": description,
        }

        yield {
            "level": level,
            "techs": techs,
        }
