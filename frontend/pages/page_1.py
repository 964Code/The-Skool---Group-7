import taipy.gui.builder as tgb
from taipy.gui import State
from backend.page_1.data_processing import df_kurser
from backend.page_1.data_processing import approved_courses_filter, generate_kpi_df, filter_kpi_data, extract_kpis_kurser
from frontend.charts.charts_page_1 import plot_bar, bar_approval, bar_filter_approved_areas


# DF
filtered_df = approved_courses_filter(df_kurser)
kpi_df = generate_kpi_df(df_kurser)

# Variables & Setters
slider_val_one = 5

anordnare_list = []
anordnare_value = ""

utbildning_list = ["Välj områrde"] + df_kurser["Utbildningsområde"].unique().tolist()
utbildning_value = "Välj område"

skolor = ["Visa alla"] + filtered_df["anordnare"].unique().tolist()
selected_utbildning = "Visa alla"

anordnare_namn = ""
total_kurser = 0
antal_beviljade_kurser = 0
beviljade_platser = 0
procent_beviljade = 0

# Bar
bar = plot_bar(filtered_df)
approval_bar = bar_approval(df_kurser)
top_approved_area = bar_filter_approved_areas(df_kurser, slider_val_one)

# Functions
def slider_on_change(state: State):
    state.top_approved_area = bar_filter_approved_areas(df_kurser, state.slider_val_one)
    state.bar = plot_bar(
    filtered_df,
    antal=state.slider_val_one,
    highlight=state.selected_utbildning)

def on_filter_button_click(state):
    state.anordnare_namn = state.anordnare_value

    filtered_kpi = filter_kpi_data(kpi_df, utbildningsområde=state.utbildning_value, skola=state.anordnare_value)

    if filtered_kpi.empty:
        print("No data found for this filter")
    else:
        kpis = extract_kpis_kurser(filtered_kpi)
        print("Extracted KPIs:", kpis)
        
        state.total_kurser = kpis["antal_kurser"]
        state.antal_beviljade_kurser = kpis["antal_beviljade_kurser"]
        state.beviljade_platser = kpis["antal_beviljade_platser"]
        state.procent_beviljade = kpis["godkännandeprocent"]


def on_utbildning_change(state):
    if state.utbildning_value == "Visa alla" or state.utbildning_value == "Välj område":
        state.anordnare_list = []
        state.anordnare_value = ""
    else:
        filtered = df_kurser[df_kurser["Utbildningsområde"] == state.utbildning_value]
        state.anordnare_list = ["Visa alla"] + filtered["Anordnare namn"].unique().tolist()
        state.anordnare_value = "Visa alla"  # Optionally reset selection

def on_button_click(state: State):
    slider_on_change(state)

with tgb.Page() as page_1:
    with tgb.part(class_name="container card"):
        with tgb.part(class_name="container card"):
            tgb.navbar()
        with tgb.part():
            tgb.text("# Analyser om ansökningsomgång för Kurser", mode="md")
        with tgb.layout(columns="1 3"):
            with tgb.part(class_name="card") as column_filters:
                tgb.text("Increase/decrease results")
                tgb.slider("{slider_val_one}", min=1, max=10, continuous=False)
                tgb.text("Välj skola")
                tgb.selector("{selected_utbildning}", lov=skolor, dropdown=True, multiple=False, filter=True)
                tgb.button("FILTRERA DATA", on_action=on_button_click, class_name="plain")
            with tgb.part() as column_chart:
                tgb.chart(figure="{bar}")
        with tgb.part():
                tgb.text("## KPI efter anordnare 2024", mode="md")
                tgb.chart(figure="{top_approved_area}")
        with tgb.part():
                tgb.text("## KPI efter anordnare 2024", mode="md")
        with tgb.layout(columns="1 3", class_name="container card"):
                with tgb.part() as column_chart:
                    tgb.text("Utbildningsområde")
                    tgb.selector("{utbildning_value}", lov=utbildning_list, dropdown=True, multiple=False, on_change=on_utbildning_change,filter=True)
                with tgb.part() as column_chart:
                    tgb.text("Skola / Anordnare")
                    tgb.selector("{anordnare_value}",lov="{anordnare_list}",dropdown=True,multiple=False,filter=True)
                    tgb.button("FILTRERA DATA", on_action=on_filter_button_click, class_name="plain")
        with tgb.layout(class_name="kpi-wrapper",):            
            with tgb.part(class_name="kpi-container"):
                 tgb.text("{total_kurser}",class_name="kpi-value")
                 tgb.text("Totalt antal kurser",class_name="kpi-title")
            with tgb.part(class_name="kpi-container "):
                 tgb.text("{antal_beviljade_kurser}",class_name="kpi-value")
                 tgb.text("Beviljade kurser",class_name="kpi-title")
            with tgb.part(class_name="kpi-container "):
                 tgb.text("{beviljade_platser}", class_name="kpi-value")
                 tgb.text("Beviljade platser",class_name="kpi-title")
            with tgb.part(class_name="kpi-container"):
                 tgb.text(" {procent_beviljade}%", class_name="kpi-value")
                 tgb.text("Beviljandegrad",class_name="kpi-title")



