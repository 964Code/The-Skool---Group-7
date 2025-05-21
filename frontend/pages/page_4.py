import taipy.gui.builder as tgb
from taipy.gui import State
from backend.page_4.data_processing import grupperad_df
from frontend.charts.charts_page_4 import skol_beslut_bar

value = 2024
value_slider = 10
skolor = ["Visa alla"] + grupperad_df["StandardSkola"].unique().tolist()
selected_utbildning = "Visa alla"

antal_beslut_df = skol_beslut_bar(grupperad_df, år=value)

def on_value_change(state: State, var_name: str, var_value):
    state.value = int(var_value)
    state.antal_beslut_df = skol_beslut_bar(
    grupperad_df,
    år=state.value,
    antal=state.value_slider,
    highlight=state.selected_utbildning)

def on_filter_button_click(state: State):
    on_value_change(state, "value", state.value)

with tgb.Page() as page_4:
    with tgb.part(class_name="container card"):
        with tgb.part(class_name="container card"):
            tgb.navbar()
        with tgb.part():
            tgb.text("# Analyser om ansökningsomgång för Program", mode="md")
            with tgb.layout(columns="1 3"):
                with tgb.part(class_name="container card") as column_chart:
                     tgb.text("Välj år som gafen ska visa")
                     tgb.selector("{value}", lov="2024;2023;2022",dropdown=True)
                     tgb.text("Välj utbildningsområde")
                     tgb.selector("{selected_utbildning}", lov=skolor, dropdown=True, multiple=False, filter=True)
                     tgb.slider(value="{value_slider}", min=1, max=len(grupperad_df.head(50)), continuous=False)
                     tgb.button("FILTRERA DATA", on_action=on_filter_button_click, class_name="plain")
                with tgb.part(class_name="") as column_chart:
                    tgb.chart(figure="{antal_beslut_df}")