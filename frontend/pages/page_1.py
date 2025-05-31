import taipy.gui.builder as tgb
from taipy.gui import State
from backend.page_1.data_processing import df_courses
from backend.page_1.data_processing import approved_courses_filter, generate_kpi_df, filter_kpi_data, extract_kpis_kurser
from frontend.charts.charts_page_1 import plot_bar, bar_approval, bar_filter_approved_areas


# DF
filtered_df = approved_courses_filter(df_courses)
kpi_df = generate_kpi_df(df_courses)

# Variables & Setters
slider_val_one = 5

approved_class = "kpi-value"

school_list = []
school_value = ""

education_area = ["Välj områrde"] + df_courses["Utbildningsområde"].unique().tolist()
education_value = "Välj område"

schools = ["Visa alla"] + filtered_df["anordnare"].unique().tolist()
selected_utbildning = "Visa alla"

school_name = ""
total_courses = 0
amount_total_approved = 0
approved_seats = 0
percentage_approved = 0

# Bar
bar = plot_bar(filtered_df)
approval_bar = bar_approval(df_courses)
top_approved_area = bar_filter_approved_areas(df_courses, slider_val_one)

# Functions
def slider_on_change(state: State):
    state.top_approved_area = bar_filter_approved_areas(df_courses, state.slider_val_one)
    state.bar = plot_bar(
    filtered_df,
    antal=state.slider_val_one,
    highlight=state.selected_utbildning)

def on_filter_button_click(state):
    state.school_name = state.school_value
    
    filtered_kpi = filter_kpi_data(kpi_df, education_area=state.education_value, school=state.school_value)


    if filtered_kpi.empty:
        print("No data found for this filter")
    else:
        kpis = extract_kpis_kurser(filtered_kpi)
        print("Extracted KPIs:", kpis)
        
        state.total_courses = kpis["antal_kurser"]
        state.amount_total_approved = kpis["antal_beviljade_kurser"]
        state.approved_seats = kpis["antal_beviljade_platser"]
        state.percentage_approved = kpis["godkännandeprocent"]

    state.approved_class = "kpi-trend_positve" if state.amount_total_approved > 0 else "kpi-trend_negative"


def on_utbildning_change(state):
    if state.education_value == "Visa alla" or state.education_value == "Välj område":
        state.school_list = []
        state.school_value = ""
    else:
        filtered = df_courses[df_courses["Utbildningsområde"] == state.education_value]
        state.school_list = ["Visa alla"] + filtered["Anordnare namn"].unique().tolist()
        state.school_value = "Visa alla" 

    
def on_button_click(state: State):
    slider_on_change(state)

with tgb.Page() as page_1:
    with tgb.part(class_name="container card"):
        with tgb.part(class_name="container"):
            tgb.navbar(class_name="margin-center")

        with tgb.part(class_name="text-align-center"):
                tgb.text("### KPI efter anordnare 2024", mode="md")
        with tgb.layout(columns="1 3", gap="32px"):
                with tgb.part(class_name="aside-controls") as column_chart:
                    tgb.text("Utbildningsområde")
                    tgb.selector("{education_value}", lov=education_area, dropdown=True, multiple=False, on_change=on_utbildning_change,filter=True)
                    tgb.text("Skola / Anordnare")
                    tgb.selector("{school_value}",lov="{school_list}",dropdown=True,multiple=False,filter=True)
                    tgb.button("FILTRERA DATA", on_action=on_filter_button_click, class_name="plain", width="100%")
                with tgb.part(class_name="kpi-part") as column_chart:
                    with tgb.layout(class_name="kpi-wrapper",):            
                        with tgb.part(class_name="kpi-container"):
                            tgb.text("{total_courses}",class_name="kpi-trend_natural")
                            tgb.text("Totalt ansökta kurser",class_name="kpi-title")
                        with tgb.part(class_name="kpi-container "):
                            tgb.text("{amount_total_approved}",class_name="{approved_class}")
                            tgb.text("Beviljade kurser",class_name="kpi-title")
                        with tgb.part(class_name="kpi-container "):
                            tgb.text("{approved_seats}", class_name="{approved_class}")
                            tgb.text("Beviljade platser",class_name="kpi-title")
                        with tgb.part(class_name="kpi-container"):
                            tgb.text(" {percentage_approved}%", class_name="kpi-value")
                            tgb.text("Beviljandegrad",class_name="kpi-title")


        with tgb.part(class_name="text-align-center"):
            tgb.text("### Analyser om ansökningsomgång för Kurser", mode="md")
        with tgb.layout(columns="1 3", gap="32px"):
            with tgb.part(class_name="aside-controls") as column_filters:
                tgb.text("Öka/Minska resultat")
                tgb.slider("{slider_val_one}", min=1, max=10, continuous=False, class_name="test")
                tgb.text("Välj skola")
                tgb.selector("{selected_utbildning}", lov=schools, dropdown=True, multiple=False, filter=True)
                tgb.button("FILTRERA DATA", on_action=on_button_click, class_name="plain", width="100%")
            with tgb.part() as column_chart:
                tgb.chart(figure="{bar}")
        with tgb.part(class_name="text-align-center"):
                tgb.text("### KPI efter anordnare 2024", mode="md")
                tgb.chart(figure="{top_approved_area}")


