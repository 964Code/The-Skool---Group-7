import taipy.gui.builder as tgb
from taipy.gui import State
from backend.page_4.data_processing import grouped_df 
from frontend.charts.charts_page_4 import school_decision_bar

year_selected = 2024
value_slider = 10
schools = ["Visa alla"] + grouped_df["StandardSkola"].unique().tolist()
selected_school = "Visa alla"

approved_class = "kpi-value"
rejected_class = "kpi-value"

total_applys = 0
total_approved = 0
total_procent = 0
total_rejected = 0

# KPI's 
def kpi_exract(df,utbildning, year):
    filtered_df = df[(df["StandardSkola"] == utbildning) & (df["År"] == year)]
    total_approved = filtered_df["Beviljade"].sum()
    total_rejected = filtered_df["Avslag"].sum()
    total_applys = total_approved + total_rejected
    total_procent = round(total_approved / total_applys * 100) if total_applys > 0 else 0

    return total_applys,total_approved,total_procent,total_rejected

decision_count_df = school_decision_bar(grouped_df, year=year_selected)
kpis = kpi_exract(grouped_df,selected_school, year=year_selected )

def on_value_change(state: State, var_name: str, var_value):
    state.year_selected = int(var_value)
    state.decision_count_df = school_decision_bar(
    grouped_df,
    year=state.year_selected,
    count=state.value_slider,
    highlight=state.selected_school)
    
    state.total_applys, state.total_approved, state.total_procent, state.total_rejected = kpi_exract(grouped_df,state.selected_school, state.year_selected)

    state.approved_class = "kpi-trend_positve" if state.total_approved > 0 else "kpi-trend_negative"
    state.rejected_class = "kpi-trend_negative" if state.total_rejected > 0 else "kpi-trend_positve"

def on_filter_button_click(state: State):
    on_value_change(state, "value", state.year_selected)

with tgb.Page() as page_4:
    with tgb.part(class_name="container card"):
        with tgb.part(class_name="container"):
            tgb.navbar(class_name="margin-center")
        with tgb.part(class_name="text-align-center"):
            tgb.text("# Analyser om ansökningsomgång för Anordnare", mode="md")
            with tgb.layout(columns="1 3", gap="32px"):
                with tgb.part(class_name="aside-controls") as column_chart:
                     tgb.text("Välj år som gafen ska visa")
                     tgb.selector("{year_selected}", lov="2024;2023;2022",dropdown=True)
                     tgb.text("Välj skola")
                     tgb.selector("{selected_school}", lov=schools, dropdown=True, multiple=False, filter=True)
                     tgb.slider(value="{value_slider}", min=1, max=len(grouped_df.head(100)), continuous=False)
                     tgb.button("FILTRERA DATA", on_action=on_filter_button_click, class_name="plain", width="100%")
                with tgb.part(class_name="") as column_chart:
                    tgb.chart(figure="{decision_count_df}")
            with tgb.layout(class_name="kpi-wrapper space-top"):
                with tgb.part(class_name="kpi-container"):
                    tgb.text("{total_applys}",class_name="kpi-trend_natural")
                    tgb.text("Totala ansökningar", class_name="kpi-title")
                with tgb.part(class_name="kpi-container"):
                    tgb.text("{total_approved}",class_name="{approved_class}")
                    tgb.text("Antal Beviljade",class_name="kpi-title")
                with tgb.part(class_name="kpi-container"):
                    tgb.text("{total_rejected}",class_name="{rejected_class}")
                    tgb.text("Antal Avslag",class_name="kpi-title")
                with tgb.part(class_name="kpi-container"):
                    tgb.text("{total_procent}%",class_name="kpi-value")
                    tgb.text("Beviljningsgrad (%)",class_name="kpi-title")