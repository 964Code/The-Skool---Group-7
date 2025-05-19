import taipy.gui.builder as tgb

with tgb.Page() as page_4:
    with tgb.part(class_name="container card"):
        with tgb.part(class_name="container card"):
            tgb.navbar()
        with tgb.part():
            tgb.text("# Page 4", mode="md")
            tgb.text(
                """
                Page_4 text. 
            """
            )
            tgb.button(
                "Page_4",
            )
