import plotly.express as px


def line_plot_stud(df, areas):
    df_melted = df.melt(id_vars=["År"], var_name="Inriktning", value_name="Studerande")
    resultat = df_melted[df_melted["Inriktning"].isin(areas)]

    # Input list for multiple options
    fig = px.line(
        resultat,
        x="År",
        y="Studerande",
        color="Inriktning",
        title=f"Studerande över tid per utbildningsinriktning ",
        markers=True,
    )
    fig.update_traces(line=dict(width= 4, dash="dot"), marker=dict(symbol="circle", size=8))

    fig.update_layout(
        plot_bgcolor = "white",
        title_font=dict(family="Times New Roman", size=30, weight="bold", color="black",),
        font=dict(family="Times New Roman", size=15, color="black",),
        yaxis_tickfont=dict(family="Times New Roman", size=15, weight="bold", color="black"),
        xaxis_tickfont=dict(family="Times New Roman", size=15, weight="bold", color="black")
        )
    return fig

