from __future__ import annotations

from zyte_test_websites.articles.views import ARTICLES_PER_FEED, ARTICLES_PER_PAGE


async def test_index(articles_client):
    response = await articles_client.get("/")
    assert response.status == 200
    text = await response.text()
    assert '<h2 class="h3 mb-4">Newest articles</h2>' in text
    assert "Berlin hails European cinema" in text


async def test_category(articles_client):
    response = await articles_client.get("/articles/1")
    assert response.status == 200
    text = await response.text()
    assert '<h1 class="display-4">510 articles in the Business category</h1>' in text
    assert text.count('<h2 class="card-title h4">') == ARTICLES_PER_PAGE
    assert "Cars pull down US retail figures" in text
    assert '<a href="/article/62"' in text
    assert 'href="/articles/1?page=2">Next' in text


async def test_category_page_3(articles_client):
    response = await articles_client.get("/articles/1?page=3")
    assert response.status == 200
    text = await response.text()
    assert '<h1 class="display-4">510 articles in the Business category</h1>' in text
    assert text.count('<h2 class="card-title h4">') == ARTICLES_PER_PAGE
    assert "Ryanair in $4bn Boeing plane deal" in text
    assert '<a href="/article/46"' in text
    assert 'href="/articles/1?page=4">Next' in text


async def test_privacy(articles_client):
    response = await articles_client.get("/privacy")
    assert response.status == 200
    text = await response.text()
    assert "We collect information that" in text


async def test_rss(articles_client):
    response = await articles_client.get("/rss.xml")
    assert response.status == 200
    assert response.headers["Content-Type"] == "application/rss+xml"
    text = await response.text()
    assert "<title>Articles To Scrape - RSS Feed</title>" in text
    assert "<title>Berlin hails European cinema</title>" in text
    assert text.count("<item>") == ARTICLES_PER_FEED


async def test_article_detail(articles_client):
    response = await articles_client.get("/article/119")
    assert response.status == 200
    text = await response.text()
    assert '<h1 class="display-4">Nigeria to boost cocoa production</h1>' in text
    assert "The government of Nigeria is hoping to triple" in text
    assert "June 21, 2024" in text


async def test_search(articles_client):
    response = await articles_client.get("/search?q=sWiSS")
    assert response.status == 200
    text = await response.text()
    assert '<h1 class="display-4">29 articles for search query "swiss"</h1>' in text
    assert text.count('<h2 class="card-title h4">') == ARTICLES_PER_PAGE
    assert '<a href="/article/1806"' in text
    assert 'href="/search?q=sWiSS&amp;page=2">Next' in text


async def test_search_page_2(articles_client):
    response = await articles_client.get("/search?q=sWiSS&page=2")
    assert response.status == 200
    text = await response.text()
    assert '<h1 class="display-4">29 articles for search query "swiss"</h1>' in text
    assert text.count('<h2 class="card-title h4">') == ARTICLES_PER_PAGE
    assert '<a href="/article/352"' in text
    assert 'href="/search?q=sWiSS&amp;page=3">Next' in text


async def test_search_empty(articles_client):
    response = await articles_client.get("/search?q=does-not-exist")
    assert response.status == 200
    text = await response.text()
    assert (
        '<h1 class="display-4">0 articles for search query "does-not-exist"</h1>'
        in text
    )
    assert '<h2 class="card-title h4">' not in text
