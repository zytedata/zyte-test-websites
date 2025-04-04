from __future__ import annotations

from itemadapter import ItemAdapter

from tests.utils_extraction import get_web_poet_response
from zyte_test_websites.articles.extraction import (
    TestArticleNavigationPage,
    TestArticlePage,
)


async def test_article_extraction(articles_client):
    response = await get_web_poet_response(articles_client, "/article/119")
    page = TestArticlePage(response)
    body = (
        "The government of Nigeria is hoping to triple cocoa production over"
        " the next three years with the launch of an ambitious development"
        " programme.  Agriculture Minister Adamu Bello said the scheme aimed"
        " to boost production from an expected 180,000 tonnes this year to"
        " 600,000 tonnes by 2008. The government will pump 154m naira ($1.1m;"
        " £591,000) into subsidies for farming chemicals and seedlings."
        " Nigeria is currently the world's fourth-largest cocoa producer."
        "  Cocoa was the main export product in Nigeria during the 1960s. But"
        " with the coming of oil, the government began to pay less attention"
        " to the cocoa sector and production began to fall from a peak of"
        " about 400,000 tonnes a year in 1970. At the launch of the programme"
        " in the south-western city of Ibadan, Mr Bello explained that an"
        " additional aim of the project is to encourage the processing of"
        " cocoa in the country and lift local consumption. He also announced"
        " that 91m naira of the funding available had been earmarked for"
        " establishing cocoa plant nurseries. The country could be looking to"
        " emulate rival Ghana, which produced a bumper crop last year."
        ' However, some farmers are sceptical about the proposals. "People'
        ' who are not farming will hijack the subsidy," said Joshua Osagie,'
        ' a cocoa farmer from Edo state told Reuters. "The farmers in the'
        ' village never see any assistance," he added.  At the same time as'
        " Nigeria announced its new initiative, Ghana - the world's second"
        " largest cocoa exporter - announced revenues from the industry had"
        " broken new records. The country saw more than $1.2bn-worth of the"
        " beans exported during 2003-04. Analysts said high tech-production"
        " techniques and crop spraying introduced by the government led to"
        " the huge crop, pushing production closer to levels seen in the 1960s"
        " when the country was the world's leading cocoa grower."
    )
    item = await page.to_item()
    assert ItemAdapter(item).asdict() == {
        "articleBody": body,
        "articleBodyHtml": f"<article>\n\n<p>{body}</p>\n\n</article>",
        "authors": [{"name": "Eve Wilson", "url": str(response.urljoin("/author/4"))}],
        "datePublished": "2024-06-21T00:00:00",
        "datePublishedRaw": "June 21, 2024",
        "description": (
            "The government of Nigeria is hoping to triple cocoa"
            " production over the next three years with the launch"
            " of an ambitious development programme"
        ),
        "headline": "Nigeria to boost cocoa production",
        "metadata": {
            "dateDownloaded": item.metadata.dateDownloaded,
            "probability": 1.0,
        },
        "url": str(response.url),
    }


async def test_article_extraction_wrong(articles_client):
    response = await get_web_poet_response(articles_client, "/articles/2")
    page = TestArticlePage(response)
    item = await page.to_item()
    assert item.url == str(response.url)
    assert item.metadata.probability == 0.0


async def test_nav_extraction(articles_client):
    response = await get_web_poet_response(articles_client, "/articles/2")
    page = TestArticleNavigationPage(response)
    item = await page.to_item()
    articles = [
        ("567", "Berlin hails European cinema"),
        ("746", "Singer Knight backs anti-gun song"),
        ("599", "Berlin cheers for anti-Nazi film"),
        ("778", "Michael film signals 'retirement'"),
        ("606", "Surprise win for anti-Bush film"),
        ("785", "Rocker Doherty in on-stage fight"),
        ("546", "Film row over Pirates 'cannibals'"),
        ("725", "Housewives lift Channel 4 ratings"),
        ("635", "Doves soar to UK album summit"),
        ("814", "The comic book genius of Stan Lee"),
    ]
    assert ItemAdapter(item).asdict() == {
        "url": str(response.url),
        "categoryName": "Entertainment",
        "items": [
            {
                "url": str(response.urljoin(f"/article/{article[0]}")),
                "method": "GET",
                "name": article[1],
            }
            for article in articles
        ],
        "nextPage": {
            "url": str(response.urljoin("/articles/2?page=2")),
            "method": "GET",
        },
        "pageNumber": 1,
        "metadata": {"dateDownloaded": item.metadata.dateDownloaded},
    }


async def test_nav_extraction_last_page(articles_client):
    response = await get_web_poet_response(articles_client, "/articles/2?page=39")
    page = TestArticleNavigationPage(response)
    item = await page.to_item()
    articles = [
        ("548", "Aviator 'creator' in Oscars snub"),
        ("727", "Stern dropped from radio stations"),
        ("542", "DVD review: Harry Potter and the Prisoner of Azkaban"),
        ("721", "Little Britain two top comic list"),
        ("538", "Baghdad Blogger on big screen"),
        ("717", "Duran Duran show set for US TV"),
    ]
    assert ItemAdapter(item).asdict() == {
        "url": str(response.url),
        "categoryName": "Entertainment",
        "items": [
            {
                "url": str(response.urljoin(f"/article/{article[0]}")),
                "method": "GET",
                "name": article[1],
            }
            for article in articles
        ],
        "pageNumber": 39,
        "metadata": {"dateDownloaded": item.metadata.dateDownloaded},
    }
