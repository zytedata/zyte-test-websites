#!/usr/bin/python3

"""
Imports the CSV data from https://www.kaggle.com/datasets/jacopoferretti/bbc-articles-dataset/data (license: CC0)
into the format suitable for zyte_test_websites/articles/data.json, adding some more fields.
"""

from __future__ import annotations

import csv
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from zyte_test_websites.articles.models import Article, ArticleCategory, Author

DATES = [
    "2024-06-24",
    "2023-12-24",
    "2024-05-10",
    "2024-03-02",
    "2024-01-01",
    "2023-12-27",
    "2024-01-16",
    "2024-01-12",
    "2024-03-31",
    "2024-06-27",
    "2024-01-20",
    "2023-12-29",
    "2024-03-11",
    "2024-06-01",
    "2024-01-14",
    "2024-02-25",
    "2024-05-21",
    "2024-05-04",
    "2024-03-08",
    "2024-05-27",
    "2024-03-18",
    "2024-06-11",
    "2024-03-23",
    "2024-04-20",
    "2024-03-04",
    "2024-05-14",
    "2024-06-16",
    "2024-02-24",
    "2024-01-25",
    "2024-02-06",
    "2024-06-30",
    "2024-05-28",
    "2024-02-18",
    "2024-01-04",
    "2024-06-08",
    "2024-04-12",
    "2024-05-11",
    "2024-01-21",
    "2024-04-15",
    "2024-01-11",
    "2024-05-09",
    "2024-05-20",
    "2024-04-08",
    "2024-02-27",
    "2024-03-12",
    "2024-05-23",
    "2024-06-23",
    "2024-06-20",
    "2024-03-27",
    "2024-06-05",
    "2024-03-17",
    "2024-05-31",
    "2024-01-22",
    "2024-05-02",
    "2024-01-27",
    "2024-01-24",
    "2024-06-03",
    "2024-06-17",
    "2024-03-22",
    "2024-05-08",
    "2024-06-07",
    "2024-06-12",
    "2024-06-29",
    "2024-01-17",
    "2024-05-22",
    "2024-01-10",
    "2024-05-01",
    "2024-04-01",
    "2024-03-26",
    "2024-06-28",
    "2024-05-12",
    "2024-01-23",
    "2024-03-29",
    "2024-03-21",
    "2024-01-28",
    "2024-01-08",
    "2024-02-29",
    "2024-06-06",
    "2024-04-09",
    "2024-05-13",
    "2024-04-07",
    "2024-04-25",
    "2024-01-13",
    "2024-01-29",
    "2024-03-14",
    "2024-05-07",
    "2024-03-15",
    "2024-05-05",
    "2024-04-11",
    "2024-04-21",
    "2024-04-16",
    "2024-05-30",
    "2024-06-09",
    "2024-01-18",
    "2024-04-02",
    "2024-03-24",
    "2024-04-24",
    "2024-02-20",
    "2024-06-26",
    "2024-03-03",
    "2024-04-19",
    "2024-06-10",
    "2024-04-18",
    "2024-04-17",
    "2024-05-29",
    "2024-05-03",
    "2024-04-06",
    "2024-04-03",
    "2024-03-19",
    "2024-01-26",
    "2024-03-20",
    "2024-05-24",
    "2024-03-01",
    "2024-02-26",
    "2024-02-28",
    "2024-06-25",
    "2024-01-30",
    "2024-06-18",
    "2024-02-12",
    "2024-06-21",
    "2024-01-09",
    "2024-02-04",
    "2024-01-15",
    "2024-04-27",
    "2024-03-28",
    "2024-03-05",
    "2024-05-18",
    "2024-06-15",
    "2024-02-21",
    "2024-03-16",
    "2024-03-09",
    "2024-04-26",
    "2024-04-30",
    "2024-02-01",
    "2024-04-28",
    "2024-06-14",
    "2024-06-22",
    "2024-02-19",
    "2024-01-31",
    "2024-02-11",
    "2024-04-05",
    "2024-03-06",
    "2024-04-23",
    "2024-05-26",
    "2024-06-13",
    "2024-02-10",
    "2024-04-14",
    "2024-04-13",
    "2024-04-04",
    "2024-05-25",
    "2024-03-25",
    "2024-06-19",
    "2024-01-05",
    "2024-04-22",
    "2024-02-02",
    "2024-02-09",
    "2024-01-19",
    "2024-02-07",
    "2024-02-17",
    "2024-01-06",
    "2024-01-03",
    "2024-01-07",
    "2024-01-02",
    "2024-03-07",
    "2024-05-19",
    "2024-05-16",
    "2024-02-08",
    "2024-02-15",
    "2024-01-04",
    "2024-02-14",
    "2024-05-17",
    "2024-05-15",
    "2024-06-04",
    "2024-04-29",
    "2024-01-01",
    "2024-01-01",
    "2023-12-31",
    "2024-02-13",
    "2024-01-10",
]

AUTHORS = {
    "Alice Johnson": "Alice Johnson is a seasoned writer with a passion for technology and innovation.",
    "Bob Smith": "Bob Smith is an experienced journalist covering the latest trends in science and health.",
    "Carol Davis": "Carol Davis is a freelance writer who specializes in travel and adventure stories.",
    "David Brown": "David Brown is a tech enthusiast who loves to write about software development.",
    "Eve Wilson": "Eve Wilson is a content creator focused on lifestyle and personal development.",
}


def get_authors() -> list[Author]:
    return [
        Author(
            id=id_,
            name=name,
            bio=AUTHORS[name],
        )
        for id_, name in enumerate(sorted(AUTHORS))
    ]


def extend_article(imported: dict[str, Any], authors: list[Author]) -> Article:
    article_id = imported["id"]
    return Article(
        id=article_id,
        category=imported["category"],
        author=authors[article_id % len(authors)],
        title=imported["title"],
        summary=imported["body"].split(".", 1)[0],
        body=imported["body"],
        date=datetime.strptime(DATES[article_id % len(DATES)], "%Y-%m-%d"),
    )


def import_articles(
    reader: csv.DictReader,
) -> tuple[list[Article], list[Author], list[ArticleCategory]]:
    articles: list[Article] = []
    categories: dict[str, ArticleCategory] = {}
    authors: list[Author] = get_authors()

    category_id = 1
    for article_count, row in enumerate(reader):
        category_name = row["category"].capitalize()
        if category_name not in categories:
            categories[category_name] = ArticleCategory(category_id, category_name, {})
            category_id += 1

        article_dict = {
            "id": article_count,
            "category": categories[category_name],
            "title": row["title"],
            "body": row["content"].strip(),
        }
        article = extend_article(article_dict, authors)
        articles.append(article)
    return articles, authors, list(categories.values())


def main() -> None:
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with Path(input_file).open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        articles, authors, categories = import_articles(reader)

    data = {
        "authors": [author.to_dict() for author in authors],
        "articles": [article.to_dict() for article in articles],
        "categories": [category.to_dict() for category in categories],
    }
    Path(output_file).write_text(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
