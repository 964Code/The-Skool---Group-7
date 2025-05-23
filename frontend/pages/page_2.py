import taipy.gui.builder as tgb
from taipy.gui import State
from backend.page_2.data_processing import result_all, approval_rate_df, df_region_total,json_data,region_code_map,log_approved,log_rejected
from frontend.charts.charts_page_2 import decision_count_bar, approval_rate_bar, map_approved_programs, map_rejected_programs

year_selected = 2024
value_slider = 10
educational_fields = ["Visa alla"] + result_all["Utbildningsområde"].unique().tolist()
selected_field = "Visa alla"


map_approved = map_approved_programs(df_region_total, year=year_selected ,json_data=json_data,region_code_map=region_code_map,log_approved=log_approved)
map_rejected = map_rejected_programs(df_region_total, year=year_selected ,json_data=json_data,region_code_map=region_code_map,log_rejected=log_rejected)

decision_count_chart = decision_count_bar(result_all, year=year_selected)

approval_rate_chart = approval_rate_bar(approval_rate_df,year=year_selected)

def on_value_change(state: State, var_name: str, var_value):
    state.year_selected = int(var_value)
    state.decision_count_chart = decision_count_bar(
    result_all,
    year=state.year_selected,
    count=state.value_slider,
    highlight=state.selected_field)

    state.approval_rate_chart = approval_rate_bar(
        approval_rate_df,
        year=state.year_selected,
        count=state.value_slider,
        highlight=state.selected_field)
    
    state.map_approved = map_approved_programs(
        df_region_total, 
        year=state.year_selected,
        json_data=json_data,
        region_code_map=region_code_map,
        log_approved=log_approved
    )

    state.map_rejected = map_rejected_programs(
        df_region_total,
        year=state.year_selected,
        json_data=json_data,
        region_code_map=region_code_map,
        log_rejected=log_rejected
    )
def on_filter_button_click(state: State):
    on_value_change(state, "value", state.year_selected)


with tgb.Page() as page_2:
    with tgb.part(class_name="container card"):
        with tgb.part(class_name="container card"):
            tgb.navbar()
        with tgb.part():
            tgb.text("# Analyser om ansökningsomgång för Program", mode="md")
            with tgb.layout(columns="1 3"):
                with tgb.part(class_name="container card") as column_chart:
                     tgb.text("Välj år som gafen ska visa")
                     tgb.selector("{year_selected}", lov="2024;2023;2022",dropdown=True)
                     tgb.text("Välj utbildningsområde")
                     tgb.selector("{selected_field}", lov=educational_fields, dropdown=True, multiple=False, filter=True)
                     tgb.slider(value="{value_slider}", min=1, max=len(educational_fields), continuous=False)
                     tgb.button("FILTRERA DATA", on_action=on_filter_button_click, class_name="plain")
                with tgb.part(class_name="") as column_chart:
                    tgb.chart(figure="{decision_count_chart}")
            with tgb.layout(columns="1 3"):
                with tgb.part(class_name="") as column_chart:
                     tgb.text("  ")
                with tgb.part(class_name="") as column_chart:
                     tgb.chart(figure="{approval_rate_chart}")
            with tgb.layout(columns="1 1"):
                with tgb.part(class_name="") as column_chart:
                     tgb.chart(figure="{map_approved}")
                with tgb.part(class_name="") as column_chart:
                     tgb.chart(figure="{map_rejected}")
                    
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