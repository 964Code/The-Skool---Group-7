import plotly.express as px

def plot_bar(df):
    df_long = df.head(5).melt(
    id_vars="anordnare",
    value_vars=["antal beviljade", "antal avslag"],
    var_name="Beslut",
    value_name="Antal",
)

    # Create the bar chart
    fig = px.bar(
        df_long,
        x="Antal",
        y="anordnare",
        color="Beslut",
        orientation="h",
        title="Antal beviljade/avslag ",
    )

    fig.update_layout(
        yaxis={"categoryorder": "total ascending"},
        xaxis_title="Antal",
        yaxis_title="Anordnare",
        legend_title="Beslut",
        bargap=0.2,
    )

    return fig

# reg df, not filtered. 
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
    if number <= 1:
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
    )

    fig.update_layout(yaxis={"categoryorder": "total ascending"})

    return fig



