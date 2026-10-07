import tkinter as tk
from json import JSONDecodeError
from queue import Empty, Queue
from threading import Thread
from tkinter import ttk

from requests.exceptions import RequestException

from browser import Browser
from input import InputData
from parser import Parser
from query import QueryUser
from const import BACKGROUND, FOREGROUND, MUTED, ACCENT

class WikipediaApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Wiki · Поиск статей")
        self.geometry("900x600")
        self.minsize(620, 420)
        self.configure(background=BACKGROUND)
        self.articles: list[dict] = []
        self.results: Queue = Queue()
        self.searching = False
        self.query_text = tk.StringVar()
        self.error_text = tk.StringVar()
        self.status = tk.StringVar(value="Введите запрос, чтобы найти статьи в Википедии.")
        self._configure_styles()
        self._build_widgets()
        self.query_text.trace_add("write", self._clear_error)
        self.after(100, self.poll_results)

    def _configure_styles(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background=BACKGROUND)
        style.configure(
            "TLabel", background=BACKGROUND,
            foreground=FOREGROUND, font=("Times New Roman", 11),
        )
        style.configure("Heading.TLabel", font=("Times New Roman", 24, "bold"))
        style.configure("Muted.TLabel", foreground=MUTED)
        style.configure("Error.TLabel", foreground="#f28b82")
        style.configure(
            "TEntry", fieldbackground="#30302c", foreground=FOREGROUND,
            insertcolor=FOREGROUND, padding=10,
        )
        style.configure("TButton", padding=(16, 10), font=("Timew New Roman", 10))
        style.configure("Search.TButton", background=ACCENT, foreground="#20201e")
        style.map("Search.TButton", background=[("active", "#e1a58e")])
        style.configure(
            "Treeview", background="#292925", fieldbackground="#292925",
            foreground=FOREGROUND, rowheight=38, borderwidth=0,
            font=("Times New Roman", 11),
        )
        style.map("Treeview", background=[("selected", "#604a3e")])
        style.configure(
            "Treeview.Heading", background="#35352f", foreground=MUTED,
            font=("Times New Roman", 10, "bold"), padding=9,
        )

    def _build_widgets(self) -> None:
        content = ttk.Frame(self, padding=28)
        content.pack(fill="both", expand=True)
        content.columnconfigure(0, weight=1)
        content.rowconfigure(4, weight=1)
        ttk.Label(content, text="LAB NO. 2 By Vavilov And Filippenkov", style="Heading.TLabel").grid(
            row=0, column=0, sticky="w",
        )
        ttk.Label(
            content, text="Поиск статьи Википедии", style="Muted.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(6, 22))
        search_bar = ttk.Frame(content)
        search_bar.grid(row=2, column=0, sticky="ew")
        search_bar.columnconfigure(0, weight=1)
        self.entry = ttk.Entry(
            search_bar, textvariable=self.query_text, font=("Timew New Roman", 12),
        )
        self.entry.grid(row=0, column=0, sticky="ew", padx=(0, 12))
        self.entry.bind("<Return>", self._start_search)
        self.search_button = ttk.Button(
            search_bar, text="Найти →", style="Search.TButton", command=self._start_search,
        )
        self.search_button.grid(row=0, column=1)
        self.error_label = ttk.Label(
            search_bar, textvariable=self.error_text, style="Error.TLabel",
            wraplength=500,
        )
        self.error_label.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(6, 0))
        self.error_label.grid_remove()
        search_bar.bind(
            "<Configure>",
            lambda event: self.error_label.configure(wraplength=max(1, event.width)),
        )
        ttk.Label(content, text="Результаты поиска", style="Muted.TLabel").grid(
            row=3, column=0, sticky="w", pady=(24, 10),
        )
        result_frame = ttk.Frame(content)
        result_frame.grid(row=4, column=0, sticky="nsew")
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
        self.article_list = ttk.Treeview(
            result_frame, columns=("title", "pageid"), show="headings", selectmode="browse",
        )
        self.article_list.heading("title", text="Название статьи", anchor="w")
        self.article_list.heading("pageid", text="ID страницы", anchor="w")
        self.article_list.column("title", width=550, minwidth=280)
        self.article_list.column("pageid", width=145, minwidth=145, stretch=False)
        self.article_list.grid(row=0, column=0, sticky="nsew")
        scroll = ttk.Scrollbar(result_frame, orient="vertical", command=self.article_list.yview)
        scroll.grid(row=0, column=1, sticky="ns")
        self.article_list.configure(yscrollcommand=scroll.set)
        self.article_list.bind("<ButtonRelease-1>", self.on_article_click)
        self.article_list.bind("<Return>", self.open_selected)
        footer = ttk.Frame(content)
        footer.grid(row=5, column=0, sticky="ew", pady=(14, 0))
        footer.columnconfigure(0, weight=1)
        ttk.Label(footer, textvariable=self.status, style="Muted.TLabel", wraplength=430).grid(
            row=0, column=0, sticky="w",
        )
        self.entry.focus_set()

    def _show_error(self, message: str) -> None:
        self.error_text.set(message)
        self.error_label.grid()

    def _clear_error(self, *args) -> None:
        self.error_text.set("")
        self.error_label.grid_remove()

    def _start_search(self, event=None) -> None:
        if self.searching:
            return
        try:
            query = InputData(self.query_text.get()).data
        except (ValueError, TypeError) as error:
            self._show_error(str(error))
            self.entry.focus_set()
            return
        self._clear_error()
        self.searching = True
        self.search_button.configure(state="disabled")
        self.entry.configure(state="disabled")
        self.article_list.delete(*self.article_list.get_children())
        self.articles = []
        self.status.set("Ищем статьи…")
        Thread(target=self.fetch_articles, args=(query,), daemon=True).start()

    def fetch_articles(self, query: str) -> None:
        try:
            articles = Parser(QueryUser(query).send_query()).parse()
            if not isinstance(articles, list) or any(
                not isinstance(article, dict)
                or not isinstance(article.get("title"), str)
                or not article["title"].strip()
                or type(article.get("pageid")) is not int
                or article["pageid"] <= 0
                for article in articles
            ):
                raise TypeError("Некорректный список статей")
        except RequestException as error:
            self.results.put((None, f"Ошибка обращения к Википедии: {error}"))
        except (JSONDecodeError, KeyError, TypeError):
            self.results.put((None, "Не удалось разобрать ответ Википедии."))
        except Exception as error:
            self.results.put((None, f"Не удалось выполнить поиск: {error}"))
        else:
            self.results.put((articles, None))

    def poll_results(self) -> None:
        try:
            articles, error = self.results.get_nowait()
        except Empty:
            pass
        else:
            self.searching = False
            self.search_button.configure(state="normal")
            self.entry.configure(state="normal")
            if error:
                self.status.set("Поиск не выполнен. Попробуйте ещё раз.")
                self._show_error(error)
            else:
                self.articles = articles
                for index, article in enumerate(articles):
                    self.article_list.insert(
                        "", "end", iid=str(index), values=(article["title"], article["pageid"]),
                    )
                self.status.set(
                    f"Найдено: {len(articles)}. Нажмите на статью, чтобы открыть её."
                    if articles else "Ничего не найдено. Попробуйте другой запрос."
                )
                if not articles:
                    self._show_error("Ничего не найдено. Попробуйте другой запрос.")
            self.entry.focus_set()
        self.after(100, self.poll_results)

    def on_article_click(self, event) -> None:
        if self.article_list.identify_region(event.x, event.y) != "cell":
            return
        row = self.article_list.identify_row(event.y)
        if row:
            self.article_list.selection_set(row)
            self.open_selected()

    def open_selected(self, event=None) -> None:
        selected = self.article_list.selection()
        if not selected:
            self._show_error("Выберите статью из результатов поиска.")
            return
        try:
            article = self.articles[int(selected[0])]
            Browser().open_article(article["pageid"])
        except Exception as error:
            self._show_error(f"Не удалось открыть статью: {error}")
        else:
            self._clear_error()
            self.status.set(f"Открыта статья: {article['title']}")
