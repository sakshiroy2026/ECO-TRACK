import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Load data
df = pd.read_csv("cleaned_data/cleaned_dataset.csv")

# Initialize app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

companies = df["CompanyName"].unique()
industries = df["Industry"].unique()

# Layout with Tabs
app.layout = html.Div([
    html.H1("🌍 EcoTrack Dashboard", style={"textAlign": "center"}),

    dcc.Tabs(id="tabs", value="overview", children=[
        dcc.Tab(label="🏢 Company Overview", value="overview"),
        dcc.Tab(label="📈 ESG Scores", value="esg"),
        dcc.Tab(label="💧 Resource Utilization", value="resources"),
        dcc.Tab(label="🏭 Industry Comparison", value="industry"),
    ]),

    html.Div(id="tab-content")
])

# ---------------------------
# Tab Content
# ---------------------------
@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "value")
)
def render_tab(tab):
    if tab == "overview":
        return html.Div([
            dcc.Dropdown(id="dropdown-overview", options=[{"label": c, "value": c} for c in companies],
                         value=companies[0], clearable=False),
            dcc.Graph(id="revenue-marketcap"),
            dcc.Graph(id="profit-growth")
        ])

    elif tab == "esg":
        return html.Div([
            dcc.Dropdown(id="dropdown-esg", options=[{"label": c, "value": c} for c in companies],
                         value=companies[0], clearable=False),
            dcc.Graph(id="esg-overall"),
            dcc.Graph(id="esg-breakdown")
        ])

    elif tab == "resources":
        return html.Div([
            dcc.Dropdown(id="dropdown-resources", options=[{"label": c, "value": c} for c in companies],
                         value=companies[0], clearable=False),
            dcc.Graph(id="resource-trends"),
            dcc.Graph(id="industry-treemap")
        ])

    elif tab == "industry":
        return html.Div([
            dcc.Dropdown(id="dropdown-industry", options=[{"label": i, "value": i} for i in industries],
                         value=industries[0], clearable=False),
            dcc.Graph(id="profit-by-industry"),
            dcc.Graph(id="marketcap-esg")
        ])


# ---------------------------
# Callbacks for Each Tab
# ---------------------------

# Company Overview
@app.callback(
    [Output("revenue-marketcap", "figure"),
     Output("profit-growth", "figure")],
    Input("dropdown-overview", "value")
)
def update_overview(company):
    company_df = df[df["CompanyName"] == company]

    fig1 = px.line(company_df, x="Year", y=["Revenue", "MarketCap"],
                   markers=True, title=f"{company} - Revenue & MarketCap")

    fig2 = px.bar(company_df, x="Year", y=["ProfitMargin", "GrowthRate"],
                  barmode="group", title=f"{company} - Profit Margin vs Growth Rate")

    return fig1, fig2

# ESG Tab
@app.callback(
    [Output("esg-overall", "figure"),
     Output("esg-breakdown", "figure")],
    Input("dropdown-esg", "value")
)
def update_esg(company):
    company_df = df[df["CompanyName"] == company]

    fig1 = px.line(company_df, x="Year", y="ESG_Overall",
                   markers=True, title=f"{company} - ESG Overall Trend")

    fig2 = px.bar(company_df, x="Year",
                  y=["ESG_Environmental", "ESG_Social", "ESG_Governance"],
                  barmode="stack", title=f"{company} - ESG Breakdown")

    return fig1, fig2

# Resource Utilization
import pandas as pd

@app.callback(
    [Output("resource-trends", "figure"),
     Output("industry-treemap", "figure")],
    Input("dropdown-resources", "value")
)
def update_resources(company):
    company_df = df[df["CompanyName"] == company]

    # Line chart for company resources
    fig1 = px.line(
        company_df,
        x="Year",
        y=["CarbonEmissions", "WaterUsage", "EnergyConsumption"],
        markers=True,
        title=f"{company} - Resource Utilization Trends"
    )

    # Build summary and FORCE pandas DataFrame
    industry_summary = (
        df.groupby(["Industry", "CompanyName"], as_index=False)["ESG_Overall"]
          .mean()
    )
    industry_summary = pd.DataFrame(industry_summary)   # <-- 🔑 ensures plain pandas

    # Treemap
    fig2 = px.treemap(
        industry_summary,
        path=["Industry", "CompanyName"],
        values="ESG_Overall",
        color="ESG_Overall",
        title="Industry ESG Treemap"
    )

    return fig1, fig2

#industry comparison
@app.callback(
    [Output("profit-by-industry", "figure"),
     Output("marketcap-esg", "figure")],
    Input("dropdown-industry", "value")
)
def update_industry(industry):
    industry_df = df[df["Industry"] == industry]

    fig1 = px.box(
        industry_df,
        x="Industry", y="ProfitMargin",
        title=f"Profit Margin Distribution - {industry}"
    )

    # Fix negative size issue
    size_col = industry_df["GrowthRate"].clip(lower=0)

    fig2 = px.scatter(
        industry_df,
        x="MarketCap", y="ESG_Overall",
        size=size_col,
        color="CompanyName",
        hover_name="CompanyName",
        title=f"{industry} - MarketCap vs ESG Overall (Bubble = Growth Rate)"
    )

    return fig1, fig2


if __name__ == "__main__":
    app.run(debug=True)
