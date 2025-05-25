import taipy.gui.builder as tgb
from utils.constants import IMAGE_DIRECTORY

with tgb.Page() as home_page:
    with tgb.part(class_name="container card"):
        with tgb.part(class_name="container"):
            tgb.navbar(class_name="margin-center")
        with tgb.part(class_name="text-align-center padding-custom"):
            tgb.text("## Välkommen till YH Home 2024", mode="md")
            tgb.text(
                "YH Dash 2024 är ett interaktivt verktyg som visualiserar statistik och insikter kring Yrkeshögskoleutbildningar (YH), med särskilt fokus på ansökningsomgångarna under 2024.",
                mode="md"
            )
            with tgb.part(class_name="text-media"):
                with tgb.part(class_name="text-media-content"):
                    tgb.text("#### Kurser", mode="md")
                    tgb.text(
                        "Här presenteras analyser av ansökningsomgångar för fristående kurser med relevanta nyckeltal (KPI:er) från 2024, såsom antagningsgrad, beviljade platser, mm...",
                        mode="md"
                    )
                with tgb.part():
                     tgb.image(f"{IMAGE_DIRECTORY}/courses_image.png")
                     
            with tgb.part(class_name="text-media reverse"):
                with tgb.part(class_name="text-media-content"):
                    tgb.text("#### Program", mode="md")
                    tgb.text(
                        "Följ utvecklingen för programansökningar under perioden 2022–2024. Filtrera och jämför data utifrån utbildningsområde, år och geografisk region (län).",
                        mode="md"
                    )
                with tgb.part():
                     tgb.image(f"{IMAGE_DIRECTORY}/education_image.png")
                     
            with tgb.part(class_name="text-media"):
                with tgb.part(class_name="text-media-content"):
                    tgb.text("#### Studerande", mode="md")
                    tgb.text(
                        "Visualisera antal studerande inom olika utbildningsområden mellan åren 2005 och 2024. Få en överblick över tillväxt och förändringar inom YH-systemet över tid.",
                        mode="md"
                    )
                    tgb.text(
                        "Ta del av statistik över hur många nyexaminerade inom området Data/IT som får arbete inom sitt utbildningsområde ett år efter examen. Utvecklingen över tid speglar förändringar på arbetsmarknaden.",
                        mode="md"
                    )
                with tgb.part():
                     tgb.image(f"{IMAGE_DIRECTORY}/students_image.png")
                     
            with tgb.part(class_name="text-media reverse"):
                with tgb.part(class_name="text-media-content"):
                    tgb.text("#### Anordnare", mode="md")
                    tgb.text(
                        "Analysera ansökningsstatistik för olika utbildningsanordnare under perioden 2022–2024. Filtrera efter specifik anordnare för att jämföra utveckling och antagningsmönster.",
                        mode="md"
                    )
                with tgb.part():
                     tgb.image(f"{IMAGE_DIRECTORY}/provider_image.png")
