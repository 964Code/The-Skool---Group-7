import plotly.express as px
import plotly.graph_objects as go

def plot_bar(df, antal=10, highlight=None):
    result = df.sort_values("antal beviljade", ascending=False).head(antal)

    fig = go.Figure()

    approved_colors = []
    denied_colors = []

    for area in result["anordnare"]:
        if highlight is None or highlight == "Visa alla" or area == highlight:
            approved_colors.append("rgba(74, 140, 232, 1)") 
            denied_colors.append("rgba(211, 211, 211, 1)")
        else:
            approved_colors.append("rgba(74, 140, 232, 0.3)") 
            denied_colors.append("rgba(211, 211, 211, 0.3)")

    fig.add_trace(go.Bar(
        y=result['anordnare'],
        x=result['antal beviljade'],
        name='antal beviljade',
        orientation='h',
        marker=dict(color=approved_colors),
        hovertemplate="<b>%{y}</b><br> Beviljade <br> Antal beslut: %{x} <br><extra></extra>"
    ))

    fig.add_trace(go.Bar(
        y=result['anordnare'],
        x=result['antal avslag'],
        name='antal avslag',
        orientation='h',
        marker=dict(color=denied_colors),
        hovertemplate="<b>%{y}</b><br> Avslag <br> Antal beslut: %{x} <br><extra></extra>"
    ))

    fig.update_layout(
        barmode='stack',
        title='Beviljade och avslagna kurser per område (2024)',
        xaxis_title='Antal',
        yaxis_title='Skola',
        template='simple_white',
        showlegend=False,
        yaxis=dict(autorange="reversed"),
        title_font=dict(family="Sans-serif", size=23, weight="bold"),
        font=dict(family="Sans-serif", size=12),
        yaxis_tickfont=dict(family="Sans-serif", size=12, weight="normal"),
        annotations=[dict(
            x=-0.9,
            y=-0.2,
            xref="paper",
            yref="paper",
            text="<b>Data source:</b> Myndigheten för yrkeshögskolan",
            showarrow=False,
        )]
    )

    return fig

def bar_approval(df):
    beslut_counts = df["Beslut"].value_counts().reset_index()
    beslut_counts.columns = ["Beslut", "Antal"]

    beslut_counts["Percent"] = (
        100 * beslut_counts["Antal"] / beslut_counts["Antal"].sum()
    )

    fig = px.bar(
        beslut_counts,
        x="Beslut",
        y="Antal",
        title="Separate Courses - Approved / Denied for 2024",
        labels={
            "Beslut": "Decision",
            "Antal": "Count",
        },
        color="Beslut",
        color_discrete_map={
            "Beviljad": "#636EFA",
            "Avslag": "salmon",
        },
        category_orders={"Beslut": beslut_counts["Beslut"].tolist()},
        custom_data=["Percent"], 
    )

    fig.update_layout(bargap=0.5, width=500)

    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>Count: %{y}<br>Percent: %{customdata[0]:.2f}%<extra></extra>"
        
    )

    return fig

## Regular df from kurser
## re-use for school?
def bar_filter_approved_areas(df, number=0):
    # Filter for approved courses
    approved_df = df[df["Beslut"] == "Beviljad"]

    # Group by utbildningsområde and count
    area_counts = approved_df["Utbildningsområde"].value_counts().reset_index()
    area_counts.columns = ["Utbildningsområde", "Antal"]

    # Add percentage
    area_counts["Percent"] = 100 * area_counts["Antal"] / area_counts["Antal"].sum()

    # Keep only top 10
    if number < 1:
        filter = area_counts.head(len(area_counts))
    else:
        filter = area_counts.head(number)

    # Plot (horizontal bar chart)
    fig = px.bar(
        filter,
        x="Antal",
        y="Utbildningsområde",
        orientation="h",
        title=f"Top {len(filter)} Utbildningsområde by Approved Courses",
        labels={"Antal": "Approved Count", "Utbildningsområde": "Area of Education"},
        color="Utbildningsområde",
        custom_data=["Percent"],
    )

    fig.update_traces(
        hovertemplate="<b>%{y}</b><br>Count: %{x}<br>Percent: %{customdata:.2f}%<extra></extra>",
        showlegend=False,
        marker=dict(color="rgba(74, 140, 232, 1)")
    )

    fig.update_layout(
        yaxis={"categoryorder": "total ascending"},
        plot_bgcolor = "white",
        title_font=dict(family="Sans-serif", size=23, weight="bold", color="black",),
        font=dict(family="Sans-serif", size=15, color="black",),
        yaxis_tickfont=dict(family="Sans-serif", size=15, weight="normal", color="black"),
        )

    return fig



