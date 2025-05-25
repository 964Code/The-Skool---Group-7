import plotly.express as px
import plotly.graph_objects as go


def school_decision_bar(df, year, count=10, highlight=None):
    resultat = df[df["År"] == year].sort_values("Beviljade", ascending=False).head(count)

    fig = go.Figure()

    approved_colors = []
    rejected_colors = []

    for area in resultat["StandardSkola"]:
        if highlight is None or highlight == "Visa alla" or area == highlight:
            approved_colors.append("rgba(74, 140, 232, 1)") 
            rejected_colors.append("rgba(211, 211, 211, 1)")
        else:
            approved_colors.append("rgba(74, 140, 232, 0.3)") 
            rejected_colors.append("rgba(211, 211, 211, 0.3)")

    fig.add_trace(go.Bar(
        y=resultat['StandardSkola'],
        x=resultat['Beviljade'],
        name='Beviljade',
        orientation='h',
        marker=dict(color=approved_colors),
        hovertemplate="<b>%{y}</b><br> Beviljade <br> Antal beslut: %{x} <br><extra></extra>"
    ))

    fig.add_trace(go.Bar(
        y=resultat['StandardSkola'],
        x=resultat['Avslag'],
        name='Avslag',
        orientation='h',
        marker=dict(color=rejected_colors),
        hovertemplate="<b>%{y}</b><br> Avslag <br> Antal beslut: %{x} <br><extra></extra>"
    ))

    fig.update_layout(
        barmode='stack',
        title=f'Beviljade och avslagna utbildningar per utbildningsanordnare ({year})',
        xaxis_title='Antal',
        yaxis_title='Skola',
        template='simple_white',
        showlegend=False,
        yaxis=dict(autorange="reversed"),
        title_font=dict(family="Times New Roman", size=25, weight="bold"),
        font=dict(family="Times New Roman", size=15),
        yaxis_tickfont=dict(family="Times New Roman", size=15, weight="bold"),
        annotations=[dict(
            x=-0.7,
            y=-0.2,
            xref="paper",
            yref="paper",
            text="<b>Data source:</b> Myndigheten för yrkeshögskolan",
            showarrow=False,
        )]
    )

    return fig