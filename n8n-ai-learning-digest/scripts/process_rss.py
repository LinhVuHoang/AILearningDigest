def process_articles(items):
    articles = []

    for item in items:
        data = item.get("json",item)

        iso_date = data.get("isoDate", "")

        if not iso_date:
            continue

        articles.append({
            "title": data.get("title", ""),
            "link": data.get("link", ""),
            "pubDate": data.get("pubDate", ""),
            "isoDate": iso_date
        })

    if not articles:
        return [{"json": {"articles": []}}]

    # Lấy thời gian mới nhất
    latest_date = max(article["isoDate"][:10] for article in articles)

    # Lấy tất cả bài có cùng thời gian mới nhất
    latest_articles = []

    for article in articles:
        if article["isoDate"][:10] == latest_date:
            latest_articles.append({
                "title": article["title"],
                "link": article["link"],
                "pubDate": article["pubDate"]
            })

    return [
        {
            "json": {
                "articles": latest_articles
            }
        }
    ]
    

items = [
    {
        "title": "This is AI news A",
        "link": "example_url a",
        "pubDate": "Mon, 09 Nov 2026 12:00:00 GMT",
        "isoDate": "2026-11-09T12:00:00.000Z"
    },
    {
        "title": "This is AI news B",
        "link": "example_url b",
        "pubDate": "Mon, 09 Nov 2026 10:00:00 GMT",
        "isoDate": "2026-11-09T10:00:00.000Z"
    }
]

result = process_articles(items)

print(result)