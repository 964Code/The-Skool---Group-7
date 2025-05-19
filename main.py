from taipy.gui import Gui

from frontend.pages.home import home_page

pages = {"home": home_page, "dashboard": "", "data": ""}

Gui(pages=pages).run(
    dark_mode=False, use_reloader=True, port=8080
)
