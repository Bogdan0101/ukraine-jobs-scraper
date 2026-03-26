import re
from textblob import TextBlob


def get_level(*args: str) -> str:
    senior = {"senior", "lead", "architect", "expert", "principal"}
    senior_pattern = (
        r"(exp|опыт|досвід|від)?\s*.{0,50}?"
        r"\b([5-9]|1[0-5])\+?"
        r"\s*(years?|лет|рок|год|experience|опыт|досвід)"
    )
    middle = {"middle", "mid"}
    middle_pattern = (
        r"(exp|опыт|досвід|від)?\s*.{0,50}?"
        r"\b([2-4])\+?"
        r"\s*(years?|лет|рок|год|experience|опыт|досвід)"
    )
    junior = {
        "junior", "trainee", "intern",
        "strong", "entry", "internship", "стажер"
    }
    junior_pattern = (
        r"(exp|опыт|досвід|від)?\s*.{0,50}?"
        r"\b([0-1]|no|without|без|6\+?\s*(мес|mon))\+?"
        r"\s*(years?|experience|год|опыт|рок|року|рік|досвід)"
    )

    stop_words = {
        "викладач",
        "викладання",
        "вчитель",
        "дітьми",
        "дітей",
        "дітям",
        "school",
        "academy",
        "преподаватель",
    }

    for arg in args:
        if not arg or not str(arg).strip():
            continue

        text = (str(arg)
                .lower()
                .replace("/", " ")
                .replace("(", " ")
                .replace(")", " ")
                )
        words = set(TextBlob(text).words)

        if not stop_words.isdisjoint(words):
            return "not specified"

        if not senior.isdisjoint(words) or re.search(senior_pattern, text):
            return "senior"
        if not middle.isdisjoint(words) or re.search(middle_pattern, text):
            return "middle"
        if not junior.isdisjoint(words) or re.search(junior_pattern, text):
            return "junior"

    return "not specified"
