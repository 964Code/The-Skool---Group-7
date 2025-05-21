from taipy.gui import Gui, State

from frontend.pages.home import home_page
from frontend.pages.page_1 import page_1
from frontend.pages.page_2 import page_2
from frontend.pages.page_3 import page_3
from frontend.pages.page_4 import page_4

pages = {"home": home_page, "Kurser": page_1, "Program": page_2, "Studerande": page_3, "Anordnare": page_4,}

Gui(pages=pages,css_file="style.css").run(
    dark_mode=False, use_reloader=True, port="auto"
)
