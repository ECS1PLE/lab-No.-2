import webbrowser

from const import ARTICLE_URL


class Browser:
    def open_article(self, pageid: int) -> None:
        url = f"{ARTICLE_URL}{pageid}"

        if not webbrowser.open(url):
            raise RuntimeError(f"Не удалось открыть браузер. Откройте ссылку: {url}")
