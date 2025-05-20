import taipy.gui.builder as tgb
from backend.page_1.data_processing import df_kurser
from backend.page_1.data_processing import approved_courses_filter
from frontend.charts.charts_page_1 import plot_bar, bar_approval, bar_filter_approved_areas


#! When importing information, it wont be read unless I run main.py - Cannot troubleshoot variables direcrly in here. 

#filter
filtered_test = approved_courses_filter(df_kurser)

list_val = []

slider_val_one = 5
slider_val_two = 5
slider_val_three = 5

#chrats/plot functions
bar = plot_bar(filtered_test)
approval_bar = bar_approval(df_kurser)
top_approved_area = bar_filter_approved_areas(df_kurser, 5)



with tgb.Page() as page_1:
    with tgb.part(class_name="container card"):
        with tgb.part(class_name="container card"):
            tgb.navbar()
        with tgb.part():
            tgb.text("# Page 1 - Kurser info", mode="md")
            tgb.text(
                """
                Descriptive text 
            """
            )
            
            #tgb.table("{df_kurser}")
            #tgb.text("# Filtered test")
            #tgb.table("{filtered_test}")
            tgb.chart(figure="{bar}")
            tgb.chart(figure="{approval_bar}")
        with tgb.layout(columns="2 1"):
        
            with tgb.part(class_name="card") as column_filters:
                tgb.text("{slider_val_one}")
                tgb.slider("{slider_val_one}", min=1, max=10)
                tgb.button(label="filter", on_action=bar_approval(df_kurser))
                tgb.chart(figure="{top_approved_area}")
            with tgb.part() as column_chart:
                tgb.button(
                    "Page_1 Kurser",
                )
