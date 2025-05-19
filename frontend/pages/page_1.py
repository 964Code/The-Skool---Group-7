import taipy.gui.builder as tgb

with tgb.Page() as page_1:
    with tgb.part(class_name="container card"):
        with tgb.part(class_name="container card"):
            tgb.navbar()
        with tgb.part():
            tgb.text("# Page 1", mode="md")
            tgb.text(
                """
                Page_1 text. 
            """
            )
            tgb.button(
                "Page_1",
            )
