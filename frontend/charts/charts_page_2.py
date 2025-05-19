import plotly.express as px

def skola_beviljade_2024_bar(df, **options):
    
    fig = px.bar(df, y="Skola", x="Beviljade", text="Beviljade", hover_name="Skola", title="Antal beviljade utbildningar per skola top 20", color="Beviljade" ,color_continuous_scale=["#9fb28f", "#3f641e"])
    
    fig.update_layout(
        plot_bgcolor="white",
        coloraxis_showscale=False,
        width=1200,
        height=800,
        yaxis=dict(
            autorange="reversed",
            ticklabelposition="outside left",
            showline=True,
            linecolor="lightgray",
            title=dict(text=f"<b>{options.get('ylabel')}</b>")
            ),
        xaxis=dict(
            linecolor="lightgray",
            showticklabels=False,
            title=f"<b>{options.get('xlabel')}</b>"
            ),
        title_font=dict(family="Times New Roman", size=30, weight="bold"),
        font=dict(family="Times New Roman", size=15),
                  yaxis_tickfont=dict(family="Times New Roman", size=15,weight="bold"),
                       annotations=[dict(
                                        x=-0.6,
                                        y=-0.1,
                                        xref="paper",
                                        yref="paper",
                                        text="<b> Data sourse: </b>Myndigheten för yrkeshögskolan (2024)",
                                        showarrow=False,
                                    )]
    )

    fig.update_traces(
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Antal Beviljader: %{x}",
    )

    return fig