import datetime
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scraper.spiders.douua import DouUaSpider
from scraper.spiders.rabotaua import RabotaUaSpider
from scraper.spiders.workua import WorkUaSpider
from scraper.collector import stats_storage
from scraper.db import save_to_db


def run_spiders():
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    # WorkUaSpider must always run first to seed the cache_skills
    process.crawl(WorkUaSpider)
    process.crawl(DouUaSpider)
    process.crawl(RabotaUaSpider)

    process.start()


if __name__ == "__main__":
    start_time = datetime.datetime.now()

    run_spiders()
    save_to_db(data=stats_storage.data)

    result_time = datetime.datetime.now() - start_time
    total_seconds = int(result_time.total_seconds())
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    print(f"Scraper completion time: {minutes} minutes {seconds} seconds")
