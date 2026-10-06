BASE_URL = "https://ru.wikipedia.org/w/api.php"

SEARCH_PARAMS = {
    "action": "query",
    "list": "search",
    "utf8": "",
    "format": "json",
}

ARTICLE_URL = "https://ru.wikipedia.org/w/index.php?curid="

HEADERS = {
    "User-Agent": "LETIWikiSearch/1.0 (https://github.com/ECS1PLE/lab-No.-2)",
}