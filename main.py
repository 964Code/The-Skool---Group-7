from taipy.gui import Gui

from frontend.pages.home import home_page
from frontend.pages.page_1 import page_1
from frontend.pages.page_2 import page_2
from frontend.pages.page_3 import page_3
from frontend.pages.page_4 import page_4

pages = {"home": home_page, "page_1": page_1, "page_2": page_2, "page_3": page_3, "page_4": page_4,}

Gui(pages=pages).run(
    dark_mode=False, use_reloader=True, port="auto"
)
