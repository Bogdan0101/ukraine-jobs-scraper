import json
import scrapy
from typing import Generator
from scrapy.http import Response
from scraper.utils import get_level
from w3lib.html import remove_tags


class RabotaUaSpider(scrapy.Spider):
    name = "rabotaua"
    allowed_domains = ["dracula.robota.ua", "ua-api.robota.ua", "robota.ua"]

    def start_requests(self):
        print("Rabota Ua Spider started")

        url = "https://dracula.robota.ua/?q=getPublishedVacanciesList"
        payload = {
            "operationName": "getPublishedVacanciesList",
            "query": "query getPublishedVacanciesList($filter: PublishedVacanciesFilterInput!, $pagination: PublishedVacanciesPaginationInput!, $sort: PublishedVacanciesSortType!, $isBrowser: Boolean!) {\n  publishedVacancies(filter: $filter, pagination: $pagination, sort: $sort) {\n    totalCount\n    items {\n      ...PublishedVacanciesItem\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment PublishedVacanciesItem on Vacancy {\n  id\n  schedules {\n    id\n    __typename\n  }\n  title\n  distanceText\n  description\n  showLogo\n  sortDateText\n  hot\n  designBannerUrl\n  isPublicationInAllCities\n  badges {\n    name\n    __typename\n  }\n  salary {\n    amount\n    comment\n    amountFrom\n    amountTo\n    __typename\n  }\n  company {\n    id\n    logoUrl\n    name\n    honors {\n      badge {\n        iconUrl\n        tooltipDescription\n        locations\n        isFavorite\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  city {\n    id\n    name\n    __typename\n  }\n  showProfile\n  seekerFavorite @include(if: $isBrowser) {\n    isFavorite\n    __typename\n  }\n  seekerDisliked @include(if: $isBrowser) {\n    isDisliked\n    __typename\n  }\n  formApplyCustomUrl\n  anonymous\n  isActive\n  publicationType\n  branding {\n    ...PublishedVacancyBranding\n    ...PublishedVacancyBrandingByStudio\n    __typename\n  }\n  __typename\n}\n\nfragment PublishedVacancyBranding on VacancyBranding {\n  id\n  name\n  banner {\n    media {\n      ...PublishedVacancyBrandingMediaImage\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment PublishedVacancyBrandingMediaImage on MediaImage {\n  fileName\n  url\n  __typename\n}\n\nfragment PublishedVacancyBrandingByStudio on VacancyBrandingByStudio {\n  id\n  name\n  bannerByStudio: banner {\n    media {\n      ...PublishedVacancyBrandingMediaImage\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n",
            "variables": {
                "filter": {
                    "additionalKeywords": "",
                    "branchIds": [],
                    "clusterKeywords": [],
                    "districtIds": [],
                    "gender": None,
                    "isForVeterans": False,
                    "isMilitary": False,
                    "isOfficeWithGenerator": False,
                    "isOfficeWithShelter": False,
                    "isReservation": False,
                    "keywords": "python",
                    "location": {"latitude": 0, "longitude": 0},
                    "metroBranches": [],
                    "microDistrictIds": [],
                    "rubrics": [],
                    "salary": 0,
                    "scheduleIds": [],
                    "showAgencies": True,
                    "showMilitary": True,
                    "showOnlyNoCvApplyVacancies": False,
                    "showOnlyNotViewed": False,
                    "showOnlySpecialNeeds": False,
                    "showOnlyWithoutExperience": False,
                    "showWithoutSalary": True,
                },
                "isBrowser": True,
                "pagination": {
                    "count": 20,
                    "page": 0,
                },
                "sort": "BY_BUSINESS_SCORE",
            },
        }

        yield scrapy.Request(
            url=url,
            method="POST",
            body=json.dumps(payload),
            headers={
                "Content-Type": "application/json",
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/146.0.0.0 Safari/537.36"
                ),
            },
            meta={"page": 0},
        )

    def parse(self, res: Response, **kwargs) -> Generator:
        current_page = res.meta.get("page")
        if current_page is None:
            self.logger.error("Rabota Ua Spider did not return a page in meta data")
            return
        print(f"Page: {current_page}")
        data = json.loads(res.text)
        result = data.get("data", {}).get("publishedVacancies", {})
        items = result.get("items", [])
        total_count = result.get("totalCount", 0)

        for item in items:
            id_vacancy = item.get("id", "")
            payload = {
                "operationName": "getPublishedVacancy",
                "query": "query getPublishedVacancy($id: ID!, $isBrowser: Boolean!, $trackView: Boolean) {\n  publishedVacancy(id: $id, trackView: $trackView) {\n    ...PublishedVacancyPage\n    __typename\n  }\n}\n\nfragment PublishedVacancyPage on Vacancy {\n  id\n  title\n  anonymous\n  showLogo\n  city {\n    id\n    name\n    __typename\n  }\n  company {\n    ...CompanyInfo\n    __typename\n  }\n  salary {\n    comment\n    amount\n    amountFrom\n    amountTo\n    __typename\n  }\n  isPublicationInAllCities\n  sortDateText\n  sortDate\n  address {\n    name\n    district {\n      name\n      __typename\n    }\n    metro {\n      name\n      __typename\n    }\n    longitude\n    latitude\n    __typename\n  }\n  distanceText\n  badges {\n    ...Badge\n    __typename\n  }\n  description\n  fullDescription\n  contacts {\n    name\n    phones\n    photo\n    socials\n    __typename\n  }\n  seekerDisliked @include(if: $isBrowser) {\n    isDisliked\n    __typename\n  }\n  seekerFavorite @include(if: $isBrowser) {\n    isFavorite\n    __typename\n  }\n  seekerApplication @include(if: $isBrowser) {\n    isApplied\n    lastTimeAppliedAt\n    __typename\n  }\n  isActive\n  hasDesign\n  designType\n  design {\n    ...HeaderInfo\n    id\n    backgroundHtml\n    footerInfo {\n      ...DesignFooterInfo\n      __typename\n    }\n    __typename\n  }\n  branch {\n    id\n    name\n    __typename\n  }\n  schedules {\n    id\n    name\n    __typename\n  }\n  hot\n  media {\n    ...MediaObject\n    __typename\n  }\n  ...KeyTagGroups\n  supportApplicationWithoutResume\n  formApplyCustomUrl\n  publicationType\n  languageQuestions @include(if: $isBrowser) {\n    language {\n      id\n      __typename\n    }\n    __typename\n  }\n  candidatesScreening @include(if: $isBrowser) {\n    questionnaire {\n      id\n      __typename\n    }\n    isEnabled\n    __typename\n  }\n  experienceQuestions @include(if: $isBrowser) {\n    id\n    __typename\n  }\n  status\n  branding {\n    ...VacancyBrandingItemByStudio\n    ...VacancyBrandingItem\n    __typename\n  }\n  __typename\n}\n\nfragment CompanyInfo on Company {\n  id\n  logoUrl\n  name\n  isVerified\n  companyUrl\n  miniProfile {\n    ...CompanyMiniProfileInfo\n    __typename\n  }\n  honors {\n    ...CompanyHonors\n    __typename\n  }\n  __typename\n}\n\nfragment CompanyMiniProfileInfo on CompanyMiniProfile {\n  isEnabled\n  description\n  images\n  years\n  benefits {\n    name\n    id\n    __typename\n  }\n  staffSize {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment CompanyHonors on CompanyHonors {\n  badge {\n    iconUrl\n    locations\n    isFavorite\n    __typename\n  }\n  __typename\n}\n\nfragment Badge on PublishedVacancyBadge {\n  name\n  id\n  __typename\n}\n\nfragment HeaderInfo on VacancyDesign {\n  headerInfo {\n    ...DesignHeaderInfo\n    __typename\n  }\n  __typename\n}\n\nfragment DesignHeaderInfo on VacancyDesignHeader {\n  mediaItems {\n    type\n    url\n    videoCoverImageUrl\n    __typename\n  }\n  videoPlayButtonImageUrl\n  __typename\n}\n\nfragment DesignFooterInfo on VacancyDesignFooter {\n  imageUrl\n  __typename\n}\n\nfragment MediaObject on VacancyMedia {\n  url\n  description\n  type\n  __typename\n}\n\nfragment KeyTagGroups on Vacancy {\n  keyTagGroups {\n    name\n    id\n    __typename\n  }\n  __typename\n}\n\nfragment VacancyBrandingItemByStudio on VacancyBrandingByStudio {\n  id\n  name\n  background {\n    ...VacancyBrandingBackgroundColorItem\n    ...VacancyBrandingBackgroundImageItem\n    ...VacancyBrandingBackgroundHtmlItem\n    __typename\n  }\n  footer {\n    media {\n      ...VacancyBrandingMediaImage\n      __typename\n    }\n    __typename\n  }\n  headerByStudio: header {\n    media {\n      ...VacancyBrandingMediaImage\n      ...VacancyBrandingMediaVideo\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment VacancyBrandingBackgroundColorItem on VacancyBrandingBackgroundColor {\n  color {\n    color\n    __typename\n  }\n  __typename\n}\n\nfragment VacancyBrandingBackgroundImageItem on VacancyBrandingBackgroundImage {\n  fillingType\n  image {\n    fileName\n    url\n    __typename\n  }\n  __typename\n}\n\nfragment VacancyBrandingBackgroundHtmlItem on VacancyBrandingBackgroundHtml {\n  html\n  __typename\n}\n\nfragment VacancyBrandingMediaImage on MediaImage {\n  fileName\n  url\n  __typename\n}\n\nfragment VacancyBrandingMediaVideo on MediaVideo {\n  videoUrl: url\n  cover {\n    url\n    fileName\n    __typename\n  }\n  __typename\n}\n\nfragment VacancyBrandingItem on VacancyBranding {\n  id\n  name\n  background {\n    ...VacancyBrandingBackgroundColorItem\n    ...VacancyBrandingBackgroundImageItem\n    __typename\n  }\n  footer {\n    media {\n      ...VacancyBrandingMediaImage\n      __typename\n    }\n    __typename\n  }\n  header {\n    media {\n      ...VacancyBrandingMediaImage\n      ...VacancyBrandingMediaVideo\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n",
                "variables": {
                    "id": str(id_vacancy),
                    "isBrowser": True,
                    "trackView": False,
                },
            }
            yield scrapy.Request(
                url="https://dracula.robota.ua/?q=getPublishedVacancy",
                method="POST",
                body=json.dumps(payload),
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": (
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/146.0.0.0 Safari/537.36"
                    ),
                },
                callback=self.parse_detail,
            )

        if (current_page + 1) * 20 < total_count:
            next_page = current_page + 1
            new_payload = json.loads(res.request.body)
            new_payload["variables"]["pagination"]["page"] = next_page

            yield scrapy.Request(
                url=res.url,
                method="POST",
                body=json.dumps(new_payload),
                headers=res.request.headers,
                callback=self.parse,
                meta={"page": next_page},
            )

    def parse_detail(self, res: Response, **kwargs) -> Generator:
        data = json.loads(res.text)
        result = data.get("data", {}).get("publishedVacancy", {})
        if not result:
            print("Error: vacancy not found")

        title_raw = result.get("title", "")
        title = " ".join(title_raw.split()).strip()
        description_raw = result.get("fullDescription", "")
        description_clean = remove_tags(description_raw)
        description = " ".join(description_clean.split()).strip()
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
