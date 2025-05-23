import taipy.gui.builder as tgb
from taipy.gui import State
from backend.page_4.data_processing import grupperad_df, skol_resultat_all
from frontend.charts.charts_page_4 import skol_beslut_bar

value = 2024
value_slider = 10
skolor = ["Visa alla"] + grupperad_df["StandardSkola"].unique().tolist()
selected_utbildning = "Visa alla"

total_applys = 0
total_approved = 0
total_procent = 0
total_rejected = 0

# KPI's 
def kpi_exract(df,utbildning ,år):
    filtered_df = df[(df["StandardSkola"] == utbildning) & (df["År"] == år)]
    total_approved = filtered_df["Beviljade"].sum()
    total_rejected = filtered_df["Avslag"].sum()
    total_applys = total_approved + total_rejected
    total_procent = round(total_approved / total_applys * 100) if total_applys > 0 else 0

    return total_applys,total_approved,total_procent,total_rejected

antal_beslut_df = skol_beslut_bar(grupperad_df, år=value)
kpier = kpi_exract(grupperad_df,selected_utbildning, år=value )

def on_value_change(state: State, var_name: str, var_value):
    state.value = int(var_value)
    state.antal_beslut_df = skol_beslut_bar(
    grupperad_df,
    år=state.value,
    antal=state.value_slider,
    highlight=state.selected_utbildning)
    
    state.total_applys, state.total_approved, state.total_procent, state.total_rejected = kpi_exract(grupperad_df,state.selected_utbildning, state.value)


def on_filter_button_click(state: State):
    on_value_change(state, "value", state.value)

with tgb.Page() as page_4:
    with tgb.part(class_name="container card"):
        with tgb.part(class_name="container card"):
            tgb.navbar()
        with tgb.part():
            tgb.text("# Analyser om ansökningsomgång för Anordnare", mode="md")
            with tgb.layout(columns="1 3"):
                with tgb.part(class_name="container card") as column_chart:
                     tgb.text("Välj år som gafen ska visa")
                     tgb.selector("{value}", lov="2024;2023;2022",dropdown=True)
                     tgb.text("Välj skola")
                     tgb.selector("{selected_utbildning}", lov=skolor, dropdown=True, multiple=False, filter=True)
                     tgb.slider(value="{value_slider}", min=1, max=len(grupperad_df.head(50)), continuous=False)
                     tgb.button("FILTRERA DATA", on_action=on_filter_button_click, class_name="plain")
                with tgb.part(class_name="") as column_chart:
                    tgb.chart(figure="{antal_beslut_df}")
            with tgb.layout(class_name="kpi-wrapper"):
                with tgb.part(class_name="kpi-container"):
                    tgb.text("{total_applys}",class_name="kpi-value")
                    tgb.text("Totala ansökningar", class_name="kpi-title")
                with tgb.part(class_name="kpi-container"):
                    tgb.text("{total_approved}",class_name="kpi-value")
                    tgb.text("Antal Beviljade",class_name="kpi-title")
                with tgb.part(class_name="kpi-container"):
                    tgb.text("{total_rejected}",class_name="kpi-value")
                    tgb.text("Antal Avslag",class_name="kpi-title")
                with tgb.part(class_name="kpi-container"):
                    tgb.text("{total_procent}%",class_name="kpi-value")
                    tgb.text("Beviljningsgrad (%)",class_name="kpi-title")