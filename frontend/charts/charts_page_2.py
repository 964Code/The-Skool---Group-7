import plotly.express as px
import plotly.graph_objects as go


def antal_beslut_bar(resultat_df, år, antal=10, highlight=None):
    resultat = resultat_df[resultat_df["År"] == år].sort_values("Beviljade", ascending=False).head(antal)

    fig = go.Figure()

    beviljade_colors = []
    avslag_colors = []

    for område in resultat["Utbildningsområde"]:
        if highlight is None or highlight == "Visa alla" or område == highlight:
            beviljade_colors.append("rgba(74, 140, 232, 1)") 
            avslag_colors.append("rgba(211, 211, 211, 1)")
        else:
            beviljade_colors.append("rgba(74, 140, 232, 0.3)") 
            avslag_colors.append("rgba(211, 211, 211, 0.3)")

    fig.add_trace(go.Bar(
        y=resultat['Utbildningsområde'],
        x=resultat['Beviljade'],
        name='Beviljade',
        orientation='h',
        marker=dict(color=beviljade_colors),
        hovertemplate="<b>%{y}</b><br> Beviljade <br> Antal beslut: %{x} <br><extra></extra>"
    ))

    fig.add_trace(go.Bar(
        y=resultat['Utbildningsområde'],
        x=resultat['Avslag'],
        name='Avslag',
        orientation='h',
        marker=dict(color=avslag_colors),
        hovertemplate="<b>%{y}</b><br> Avslag <br> Antal beslut: %{x} <br><extra></extra>"
    ))

    fig.update_layout(
        barmode='stack',
        title=f'Beviljade och avslagna utbildningar per område ({år})',
        xaxis_title='Antal',
        yaxis_title='Utbildningsområde',
        template='simple_white',
        showlegend=False,
        yaxis=dict(autorange="reversed"),
        title_font=dict(family="Times New Roman", size=30, weight="bold"),
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




def beviljadegrad_bar(beviljandegrad_df, år,antal=10,highlight=None):
    resultat = beviljandegrad_df[beviljandegrad_df["År"] == år].sort_values("beviljandegrad (%)", ascending=False).head(antal)
    
    beviljade_colors = []

    for område in resultat["Utbildningsområde"]:
        if highlight is None or highlight == "Visa alla" or område == highlight:
            beviljade_colors.append("rgba(74, 140, 232, 1)") 
        else:
            beviljade_colors.append("rgba(74, 140, 232, 0.3)") 

    fig = px.bar(
        resultat,
        y=resultat["Utbildningsområde"],
        x=resultat["beviljandegrad (%)"],
        barmode="group",
        title=f"Beviljandegrad per utbildningsområde och år ({år})",
    )
    fig.update_traces(marker=dict(color=beviljade_colors),)
    
    fig.update_layout(
        coloraxis_showscale=False,
        plot_bgcolor = "white",
        yaxis=dict(
                autorange="reversed",
                ticklabelposition="outside left",
                showline=True,
                linecolor="lightgray",
                ),
        xaxis=dict(
                linecolor="lightgray",
                showticklabels=True,
                ),
        title_font=dict(family="Times New Roman", size=30, weight="bold", color="black",),
        font=dict(family="Times New Roman", size=15, color="black",),
        yaxis_tickfont=dict(family="Times New Roman", size=15, weight="bold", color="black"),
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


import plotly.graph_objects as go

def map_beviljade_utbildningar(df_region_total,json_data,region_code_map,log_approved, år):
    resultat = df_region_total[df_region_total["År"] == år].sort_values("Beviljade", ascending=False).head(10)
    fig = go.Figure(
        go.Choroplethmapbox(
            geojson=json_data,
            locations=region_code_map,
            z= log_approved,
            featureidkey="properties.ref:se:länskod",
            colorscale="Blues",
            showscale=False,
            customdata=resultat["Beviljade"],
            text=resultat["Län"],
            hovertemplate="<b>%{text}</b><br>Beviljande utbildningar %{customdata}<extra></extra>,",
            marker_line_width=.3
        )
    )

    fig.update_layout(
        mapbox = dict(style = "white-bg",  zoom=3.3, center=dict(lat=62.6952, lon=13.9149)),
        width=470,
        height= 500,
        margin=dict(r=0, t=50,l=0,b=0),
            title=dict(
            text=f"""
                    <b>Antal beviljade</b>
                    <br>utbildningar per län
                    <br>inom YH i Sverige för 
                    <br>omgång {år}. Ju mörkare 
                    <br>blå färg, desto fler
                    <br>beviljade utbildningar
                    <br>
                    <br><b>I ledningen är</b>
                    <br>1. Stockholm, 
                    <br>2. Västra Götaland
                    <br>3. Skåne""",
            x=0.06,
            y=0.75,
            font=dict(size=14),)
    )


    return fig

import plotly.graph_objects as go

def map_avslag_utbildningar(df_region_total, år,json_data,region_code_map,log_avslag):
    resultat = df_region_total[df_region_total["År"] == år].sort_values("Avslag", ascending=False).head(10)
    fig = go.Figure(
        go.Choroplethmapbox(
            geojson=json_data,
            locations=region_code_map,
            z= log_avslag,
            featureidkey="properties.ref:se:länskod",
            colorscale="reds",
            showscale=False,
            customdata=resultat["Avslag"],
            text=resultat["Län"],
            hovertemplate="<b>%{text}</b><br>Beviljande utbildningar %{customdata}<extra></extra>,",
            marker_line_width=.3
        )
    )

    fig.update_layout(
        mapbox = dict(style = "white-bg",  zoom=3.3, center=dict(lat=62.6952, lon=13.9149)),
        width=470,
        height= 500,
        margin=dict(r=0, t=50,l=0,b=0),
            title=dict(
            text=f"""
                    <b>Antal nekade</b>
                    <br>utbildningar per län
                    <br>inom YH i Sverige för 
                    <br>omgång {år}. Ju mörkare 
                    <br>röd färg, desto fler
                    <br>nekade utbildningar
                    <br>
                    <br><b>I ledningen är</b>
                    <br>1. Stockholm, 
                    <br>2. Västra Götaland
                    <br>3. Skåne""",
            x=0.06,
            y=0.75,
            font=dict(size=14),)
    )


    return fig

