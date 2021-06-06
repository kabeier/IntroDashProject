import dash
from dash.exceptions import PreventUpdate
import dash_core_components as dcc
from dash_core_components.Dropdown import Dropdown
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
import plotly.express as px



app=dash.Dash(__name__,external_stylesheets=[dbc.themes.DARKLY])
app.title="My First Dash App"
app.config['suppress_callback_exceptions'] = True

gapminder = px.data.gapminder()
iris = px.data.iris()

indicators = {"gdpPercap":"GDP Per Capita",
            "lifeExp":"Life Expectancy",
            "pop":"Population"}
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Gap Minder Data", href="/gapminder")),
        dbc.NavItem(dbc.NavLink("Iris Data", href="/iris")),


    ],
    brand="Learning Dash",
    brand_href="/",
    color="primary",
    dark=True,
)
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='content')
])

index_page=html.Div([
    navbar,
    html.H1("Hello Dash!", className="mt-5 ml-4"),
    html.P("This is our First Dash App!", className="m-5")
])

gapminder_page=html.Div([
    navbar,
    dcc.Dropdown(id="mapchoice",
        options=[{'label': name,'value': indicator} for indicator, name in indicators.items()],
        className="m-5"),
    dcc.Graph(id="gapminder_chart")
])

iris_choices={'sepal_width':'Sepal Width','sepal_length':'Sepal Length', 'petal_width':'Petal Width', 'petal_length':'Petal Length'}
iris_page=html.Div([
    navbar,
    dcc.Dropdown(id="xchoice",
        options=[{'label': name,'value': indicator} for indicator, name in iris_choices.items()],
        className="m-5"),
    dcc.Dropdown(id="ychoice",
        options=[{'label': name,'value': indicator} for indicator, name in iris_choices.items()],
        className="m-5"),
    dcc.Graph(id="iris_chart"),

    
])

#Iris callback
@app.callback(Output('iris_chart','figure'),Input('xchoice','value'),Input('ychoice','value'))
def iris_chart(xchoice,ychoice):
    if xchoice is None or ychoice is None:
        raise PreventUpdate
    chart=px.scatter(data_frame= iris, x=xchoice,  y=ychoice, color = 'species', title = "Iris Dataset", labels={**iris_choices,'species':'Species'}, template="plotly_dark", height=1000)
    return chart

#heatmap for gapminder
@app.callback(Output('gapminder_chart','figure'),Input('mapchoice','value'))
def heatmap(mapchoice):
    if mapchoice is None:
        mapchoice="gdpPercap"
    map = px.choropleth(gapminder,labels={**indicators},locations='iso_alpha',color=mapchoice ,animation_frame='year',hover_name='country',template="plotly_dark", height=1000, title=f'{indicators[mapchoice]} 1952-2007 by Country', range_color=[min(gapminder[mapchoice]),max(gapminder[mapchoice])])
    return map

#nav callback
@app.callback(Output('content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/gapminder':
        return gapminder_page
    elif pathname == '/iris':
        return iris_page
    else:
        return index_page

pages = ["/", "/gapminder", "iris"]

#Callback to set active page
@app.callback(
    [Output(f"{page}-link", "active") for page in pages],
    [Input("url", "pathname")],
)
def toggle_active(pathname):
    active = [False] * len(pages)
    active[pages.index(pathname)] = True
    return active

if __name__ == "__main__":
    app.run_server(debug=True)