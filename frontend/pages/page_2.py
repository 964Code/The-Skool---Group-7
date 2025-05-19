import taipy.gui.builder as tgb
from backend.page_2.data_processing import skola_beviljade
from frontend.charts.charts_page_2 import skola_beviljade_2024_bar

skola_beviljade_df = skola_beviljade_2024_bar(skola_beviljade.head(20), ylabel= "SKOLA", xlabel="# ANTAL BEVILJADE UTBILDNINGAR")

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
            tgb.chart(figure="{skola_beviljade_df}")
