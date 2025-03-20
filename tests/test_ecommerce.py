from __future__ import annotations

from zyte_test_websites.ecommerce.views import CATS_PER_PAGE, PRODUCTS_PER_PAGE


async def test_index(ecommerce_client):
    response = await ecommerce_client.get("/")
    assert response.status == 200
    text = await response.text()
    assert "<h1>11 product categories:</h1>" in text
    assert '<ol id="categories" start="1">' in text
    assert text.count('class="category-li"') == CATS_PER_PAGE
    assert '<a href="/category/10">Fiction</a>' in text
    assert 'href="/?page=2">Next' in text


async def test_index_page_2(ecommerce_client):
    response = await ecommerce_client.get("/?page=2")
    assert response.status == 200
    text = await response.text()
    assert "<h1>11 product categories:</h1>" in text
    assert f'<ol id="categories" start="{CATS_PER_PAGE + 1}">' in text
    assert text.count('class="category-li"') <= CATS_PER_PAGE
    assert '<a href="/category/12">Religion</a>' in text


async def test_subcategory_only_products(ecommerce_client):
    response = await ecommerce_client.get("/category/4")
    assert response.status == 200
    text = await response.text()
    assert "<h2>26 products:</h2>" in text
    assert '<ol id="products" start="1">' in text
    assert text.count('class="product-li"') == PRODUCTS_PER_PAGE
    assert ' href="/product/612">A Paris Apartment</a>' in text
    assert 'href="/category/4?page=2">Next' in text


async def test_subcategory_only_products_page_2(ecommerce_client):
    response = await ecommerce_client.get("/category/4?page=2")
    assert response.status == 200
    text = await response.text()
    assert "<h2>26 products:</h2>" in text
    assert f'<ol id="products" start="{PRODUCTS_PER_PAGE + 1}">' in text
    assert text.count('class="product-li"') == PRODUCTS_PER_PAGE
    assert ' href="/product/846">The House by the Lake</a>' in text
    assert 'href="/category/4?page=3">Next' in text


async def test_subcategory_only_subcategories(ecommerce_client):
    response = await ecommerce_client.get("/category/1000")
    assert response.status == 200
    text = await response.text()
    assert "<h2>4 subcategories:</h2>" in text
    assert '<ol id="products"' not in text
    assert ' href="/category/14">Music</a>' in text


async def test_subcategory_both(ecommerce_client):
    response = await ecommerce_client.get("/category/11")
    assert response.status == 200
    text = await response.text()
    assert "<h2>2 subcategories:</h2>" in text
    assert ' href="/category/20">New Adult</a>' in text
    assert "<h2>29 products:</h2>" in text
    assert '<ol id="products" start="1">' in text
    assert text.count('class="product-li"') == PRODUCTS_PER_PAGE
    assert ' href="/product/142">Counting Thyme</a>' in text
    assert 'href="/category/11?page=2">Next' in text


async def test_subcategory_both_page_2(ecommerce_client):
    response = await ecommerce_client.get("/category/11?page=2")
    assert response.status == 200
    text = await response.text()
    assert "<h2>2 subcategories:</h2>" in text
    assert ' href="/category/20">New Adult</a>' in text
    assert "<h2>29 products:</h2>" in text
    assert f'<ol id="products" start="{PRODUCTS_PER_PAGE + 1}">' in text
    assert text.count('class="product-li"') == PRODUCTS_PER_PAGE
    assert ' href="/product/567">Nap-a-Roo</a>' in text
    assert 'href="/category/11?page=3">Next' in text


async def test_product_detail(ecommerce_client):
    response = await ecommerce_client.get("/product/300")
    assert response.status == 200
    text = await response.text()
    assert "<h1>Walk the Edge (Thunder Road #2)</h1>" in text
    assert "Price: £32.36" in text
    assert "0e4e2d31c2fb3aad" in text
    assert text.count("★") == 3
    assert text.count("☆") == 2


async def test_search(ecommerce_client):
    response = await ecommerce_client.get("/search?q=niGhT")
    assert response.status == 200
    text = await response.text()
    assert '<h1>138 products for search query "night":</h1>' in text
    assert '<ol id="products" start="1">' in text
    assert text.count('class="product-li"') == PRODUCTS_PER_PAGE
    assert ' href="/product/684">Dear Mr. Knightley</a>' in text
    assert 'href="/search?q=niGhT&amp;page=2">Next' in text


async def test_search_page_3(ecommerce_client):
    response = await ecommerce_client.get("/search?q=niGhT&page=3")
    assert response.status == 200
    text = await response.text()
    assert '<h1>138 products for search query "night":</h1>' in text
    assert f'<ol id="products" start="{2 * PRODUCTS_PER_PAGE + 1}">' in text
    assert text.count('class="product-li"') == PRODUCTS_PER_PAGE
    assert ' href="/product/2">1st to Die (Women&#39;s Murder Club #1)</a>' in text
    assert 'href="/search?q=niGhT&amp;page=4">Next' in text


async def test_search_empty(ecommerce_client):
    response = await ecommerce_client.get("/search?q=does-not-exist")
    assert response.status == 200
    text = await response.text()
    assert '<h1>0 products for search query "does-not-exist":</h1>' in text
    assert '<ol id="products" start="1">' in text
    assert 'class="product-li"' not in text
