import re


def clean_title(title):

    title = title.replace("-", " ")
    title = re.sub(r"\d+", "", title)

    return title.strip().title()