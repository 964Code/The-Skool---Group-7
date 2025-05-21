import taipy.gui.builder as tgb
from backend.page_3.data_processing import df_stud
from frontend.charts.charts_page_3 import line_plot_stud


area_list = df_stud.columns.to_list()[1:]

selected_area = ["Totalt", "Data/It"]
line_graph_stud = line_plot_stud(df_stud, selected_area)

def on_area_change(state):
    state.line_graph_stud = line_plot_stud(df_stud, state.selected_area)

with tgb.Page() as page_3:
    with tgb.part(class_name="container card"):
        with tgb.part(class_name="container card"):
            tgb.navbar()
        with tgb.part():
            tgb.text("# Analyser om ansökningsomgång för studerande", mode="md")
            tgb.selector(
                lov=area_list,
                dropdown=True,
                multiple=True,
                value="{selected_area}",
                on_change=on_area_change,
            )
            tgb.chart(figure="{line_graph_stud}")
