import taipy.gui.builder as tgb
from taipy.gui import State
from backend.page_2.data_processing import resultat_all, beviljandegrad_df, df_region_total,json_data,region_code_map,log_approved,log_avslag
from frontend.charts.charts_page_2 import antal_beslut_bar, beviljadegrad_bar, map_beviljade_utbildningar, map_avslag_utbildningar

value = 2024
value_slider = 10
utbildningar = ["Visa alla"] + resultat_all["Utbildningsområde"].unique().tolist()
selected_utbildning = "Visa alla"


map_beviljade = map_beviljade_utbildningar(df_region_total, år=value ,json_data=json_data,region_code_map=region_code_map,log_approved=log_approved)
map_avslag = map_avslag_utbildningar(df_region_total, år=value ,json_data=json_data,region_code_map=region_code_map,log_avslag=log_avslag)

antal_beslut_df = antal_beslut_bar(resultat_all, år=value)

antal_beviljadegrad_df = beviljadegrad_bar(beviljandegrad_df,år=value)

def on_value_change(state: State, var_name: str, var_value):
    state.value = int(var_value)
    state.antal_beslut_df = antal_beslut_bar(
    resultat_all,
    år=state.value,
    antal=state.value_slider,
    highlight=state.selected_utbildning)
    state.antal_beviljadegrad_df = beviljadegrad_bar(
        beviljandegrad_df,
        år=state.value,
        antal=state.value_slider,
        highlight=state.selected_utbildning)
    
    state.map_beviljade = map_beviljade_utbildningar(
        df_region_total, 
        år=state.value,
        json_data=json_data,
        region_code_map=region_code_map,
        log_approved=log_approved
    )

    state.map_avslag = map_avslag_utbildningar(
        df_region_total,
        år=state.value,
        json_data=json_data,
        region_code_map=region_code_map,
        log_avslag=log_avslag
    )
def on_filter_button_click(state: State):
    on_value_change(state, "value", state.value)


with tgb.Page() as page_2:
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
                     tgb.selector("{selected_utbildning}", lov=utbildningar, dropdown=True, multiple=False)
                     tgb.slider(value="{value_slider}", min=1, max=15, continuous=False)
                     tgb.button("FILTRERA DATA", on_action=on_filter_button_click, class_name="plain")
                with tgb.part(class_name="") as column_chart:
                    tgb.chart(figure="{antal_beslut_df}")
            with tgb.layout(columns="1 3"):
                with tgb.part(class_name="") as column_chart:
                     tgb.text("  ")
                with tgb.part(class_name="") as column_chart:
                     tgb.chart(figure="{antal_beviljadegrad_df}")
            with tgb.layout(columns="1 1"):
                with tgb.part(class_name="") as column_chart:
                     tgb.chart(figure="{map_beviljade}")
                with tgb.part(class_name="") as column_chart:
                     tgb.chart(figure="{map_avslag}")
                    
# with tgb.Page() as page_2:
#     with tgb.part(class_name="container card"):
#         with tgb.part(class_name="container card"):
#             tgb.navbar()
#         with tgb.part():
#             tgb.text("# Analyser om ansökningsomgång för Program", mode="md")
#             with tgb.layout(columns="1 3"):
#                 with tgb.part(class_name="") as column_chart:
#                      tgb.text("Välj år som gafen ska visa")
#                      tgb.selector("{value}", lov="2024;2023;2022",dropdown=True ,on_change=on_value_change)
#                 with tgb.part(class_name="") as column_chart:
#                      tgb.text("Välj utbildningsområde")
#                      tgb.selector("{selected_utbildning}", lov=utbildningar, dropdown=True, multiple=True)
#                 with tgb.part(class_name="") as column_chart:
#                     tgb.text("Välj utbildningsområde")
#         with tgb.part(class_name="") as column_chart:
#             tgb.chart(figure="{antal_beslut_df}")
#         with tgb.part(class_name="") as column_chart:
#             tgb.text("## Antal beviljningsgrad", mode="md")
#             tgb.chart(figure="{antal_beviljadegrad_df}")