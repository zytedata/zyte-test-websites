from __future__ import annotations

from itemadapter import ItemAdapter

from tests.utils_extraction import get_web_poet_response
from zyte_test_websites.ecommerce.extraction import (
    TestProductListPage,
    TestProductNavigationPage,
    TestProductPage,
)


async def test_product_extraction(ecommerce_client):
    response = await get_web_poet_response(ecommerce_client, "/product/1000")
    page = TestProductPage(response)
    descr = (
        "It's hard to imagine a world without A Light in the Attic. This"
        " now-classic collection of poetry and drawings from Shel Silverstein"
        " celebrates its 20th anniversary with this special edition."
        " Silverstein's humorous and creative verse can amuse the dowdiest of"
        " readers. Lemon-faced adults and fidgety kids sit still and read"
        " these rhythmic words and laugh and smile and love th It's hard to"
        " imagine a world without A Light in the Attic. This now-classic"
        " collection of poetry and drawings from Shel Silverstein celebrates"
        " its 20th anniversary with this special edition. Silverstein's"
        " humorous and creative verse can amuse the dowdiest of readers."
        " Lemon-faced adults and fidgety kids sit still and read these"
        " rhythmic words and laugh and smile and love that Silverstein. Need"
        " proof of his genius? RockabyeRockabye baby, in the treetopDon't you"
        " know a treetopIs no safe place to rock?And who put you up there,And"
        " your cradle, too?Baby, I think someone down here'sGot it in for you."
        " Shel, you never sounded so good. ...more"
    )
    item = await page.to_item()
    assert ItemAdapter(item).asdict() == {
        "url": str(response.url),
        "additionalProperties": [
            {"name": "UPC", "value": "a897fe39b1053632"},
            {"name": "Product Type", "value": "Books"},
            {"name": "Price (excl. tax)", "value": "£51.77"},
            {"name": "Price (incl. tax)", "value": "£51.77"},
            {"name": "Tax", "value": "£0.00"},
            {"name": "Availability", "value": "In stock (22 available)"},
            {"name": "Number of reviews", "value": "0"},
        ],
        "aggregateRating": {"bestRating": 5.0, "ratingValue": 3},
        "availability": "InStock",
        "breadcrumbs": [
            {"name": "Home", "url": str(response.urljoin("/"))},
            {
                "name": "Arts & Creativity",
                "url": str(response.urljoin("/category/1000")),
            },
            {"name": "Poetry", "url": str(response.urljoin("/category/23"))},
            {"name": "A Light in the Attic"},
        ],
        "currencyRaw": "£",
        "description": descr,
        "descriptionHtml": f"<article>\n\n<p>{descr}</p>\n\n</article>",
        "metadata": {
            "dateDownloaded": item.metadata.dateDownloaded,
            "probability": 1.0,
        },
        "name": "A Light in the Attic",
        "price": "51.77",
        "productId": "1000",
        "sku": "a897fe39b1053632",
    }


async def test_nav_extraction_only_products(ecommerce_client):
    response = await get_web_poet_response(ecommerce_client, "/category/4")
    page = TestProductNavigationPage(response)
    item = await page.to_item()
    products = [
        ("876", "A Flight of Arrows (The Pathfinders #2)"),
        ("612", "A Paris Apartment"),
        ("3", "A Spy's Devotion (The Regency Spies of London #1)"),
        ("128", "Between Shades of Gray"),
        (
            "894",
            "Forever and Forever: The Courtship of Henry Longfellow and Fanny Appleton",
        ),
        ("322", "Girl With a Pearl Earring"),
        ("160", "Girl in the Blue Coat"),
        ("696", "Glory over Everything: Beyond The Kitchen House"),
        ("597", "Lilac Girls"),
        ("31", "Lost Among the Living"),
    ]
    assert ItemAdapter(item).asdict() == {
        "url": str(response.url),
        "categoryName": "Historical Fiction",
        "items": [
            {
                "url": str(response.urljoin(f"/product/{product[0]}")),
                "method": "GET",
                "name": product[1],
            }
            for product in products
        ],
        "nextPage": {
            "url": str(response.urljoin("/category/4?page=2")),
            "method": "GET",
        },
        "pageNumber": 1,
        "metadata": {"dateDownloaded": item.metadata.dateDownloaded},
    }


async def test_nav_extraction_only_subcategories(ecommerce_client):
    response = await get_web_poet_response(ecommerce_client, "/category/1000")
    page = TestProductNavigationPage(response)
    item = await page.to_item()
    subcats = [
        ("25", "Art"),
        ("14", "Music"),
        ("23", "Poetry"),
        ("5", "Sequential Art"),
    ]
    assert ItemAdapter(item).asdict() == {
        "url": str(response.url),
        "categoryName": "Arts & Creativity",
        "subCategories": [
            {
                "url": str(response.urljoin(f"/category/{subcat[0]}")),
                "method": "GET",
                "name": subcat[1],
            }
            for subcat in subcats
        ],
        "metadata": {"dateDownloaded": item.metadata.dateDownloaded},
    }


async def test_nav_extraction_both(ecommerce_client):
    response = await get_web_poet_response(ecommerce_client, "/category/11")
    page = TestProductNavigationPage(response)
    item = await page.to_item()
    subcats = [
        ("20", "New Adult"),
        ("21", "Young Adult"),
    ]
    products = [
        ("122", "Are We There Yet?"),
        ("975", "Birdsong: A Story in Pictures"),
        ("13", "Charlie and the Chocolate Factory (Charlie Bucket #1)"),
        ("142", "Counting Thyme"),
        (
            "99",
            "Diary of a Minecraft Zombie Book 1: A Scare of a Dare (An Unofficial Minecraft Book)",
        ),
        ("165", "Green Eggs and Ham (Beginner Books B-16)"),
        ("168", "Horrible Bear!"),
        ("817", "Little Red"),
        ("714", "Luis Paints the World"),
        ("32", "Matilda"),
    ]
    assert ItemAdapter(item).asdict() == {
        "url": str(response.url),
        "categoryName": "Children's",
        "items": [
            {
                "url": str(response.urljoin(f"/product/{product[0]}")),
                "method": "GET",
                "name": product[1],
            }
            for product in products
        ],
        "nextPage": {
            "url": str(response.urljoin("/category/11?page=2")),
            "method": "GET",
        },
        "subCategories": [
            {
                "url": str(response.urljoin(f"/category/{subcat[0]}")),
                "method": "GET",
                "name": subcat[1],
            }
            for subcat in subcats
        ],
        "pageNumber": 1,
        "metadata": {"dateDownloaded": item.metadata.dateDownloaded},
    }


async def test_product_list_extraction(ecommerce_client):
    response = await get_web_poet_response(ecommerce_client, "/category/11")
    page = TestProductListPage(response)
    item = await page.to_item()
    products = [
        ("122", "Are We There Yet?", "10.66"),
        ("975", "Birdsong: A Story in Pictures", "54.64"),
        ("13", "Charlie and the Chocolate Factory (Charlie Bucket #1)", "22.85"),
        ("142", "Counting Thyme", "10.62"),
        (
            "99",
            "Diary of a Minecraft Zombie Book 1: A Scare of a Dare (An Unofficial Minecraft Book)",
            "52.88",
        ),
        ("165", "Green Eggs and Ham (Beginner Books B-16)", "10.79"),
        ("168", "Horrible Bear!", "37.52"),
        ("817", "Little Red", "13.47"),
        ("714", "Luis Paints the World", "53.95"),
        ("32", "Matilda", "28.34"),
    ]
    assert ItemAdapter(item).asdict() == {
        "url": str(response.url),
        "breadcrumbs": [
            {"name": "Home", "url": str(response.urljoin("/"))},
            {
                "name": "Children's",
            },
        ],
        "categoryName": "Children's",
        "products": [
            {
                "currencyRaw": "£",
                "name": product[1],
                "price": product[2],
                "productId": product[0],
                "url": str(response.urljoin(f"/product/{product[0]}")),
            }
            for product in products
        ],
        "paginationNext": {
            "text": "Next →",
            "url": str(response.urljoin("/category/11?page=2")),
        },
        "pageNumber": 1,
        "metadata": {"dateDownloaded": item.metadata.dateDownloaded},
    }
