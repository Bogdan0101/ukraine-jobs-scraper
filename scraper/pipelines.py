import re
from .collector import stats_storage


class ScraperPipeline:
    def __init__(self):
        pass

    def process_item(self, item: dict, spider):
        skills = set()
        level = item["level"]
        techs_req = item["techs"]["requirements"]
        description = item["techs"]["description"].lower()

        for tag in techs_req:
            clean_tag = tag.lower().strip().strip(".,")
            if re.search(r"[а-яіїєґ]", clean_tag):
                continue
            stats_storage.cache_skills.add(clean_tag)
            skills.add(clean_tag)

        for skill in stats_storage.cache_skills:
            skill_clean = re.escape(skill).replace(r"\-", r"[- _]")
            pattern = rf"\b{skill_clean}\b"

            if re.search(pattern, description):
                skills.add(skill)

        for skill in skills:
            stats_storage.add_skill(level=level, skill=skill)

        return item
