import taipy.gui.builder as tgb

with tgb.Page() as page_2:
    with tgb.part(class_name="container card"):
        with tgb.part(class_name="container card"):
            tgb.navbar()
        with tgb.part():
            tgb.text("# Page 2", mode="md")
            tgb.text(
                """
            Page_2 text
            """
            )
            tgb.button(
                "Page_2",
            )
