import dash
from dash.exceptions import PreventUpdate
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
import plotly.express as px

#init dash app and use bootstrap theme
app=dash.Dash(__name__,external_stylesheets=[dbc.themes.DARKLY])
app.title="My First Dash App"
#Suppress warning for callback if they are not rendered on screen
app.config['suppress_callback_exceptions'] = True
server = app.server
#Data Collection
gapminder = px.data.gapminder()
iris = px.data.iris()
tips = px.data.tips()

#Data manipulation
tips['percentage']=tips["tip"]/tips["total_bill"]*100

#Labels
labels={
    "total_bill":"Total bill",
    "tip":"Tip",
    "smoker":"Smoker",
    "sex":"Sex",
    "day":"Day",
    "size":"Size",
    "percentage":"Tip Percentage"
}
#Indicators
indicators = {"gdpPercap":"GDP Per Capita",
            "lifeExp":"Life Expectancy",
            "pop":"Population"}

iris_choices={'sepal_width':'Sepal Width','sepal_length':'Sepal Length', 'petal_width':'Petal Width', 'petal_length':'Petal Length'}

#Bootstrap Simple Navbar
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Tip Data", href="/tips")),
        dbc.NavItem(dbc.NavLink("Gap Minder Data", href="/gapminder")),
        dbc.NavItem(dbc.NavLink("Iris Data", href="/iris")),
    ],
    brand="Learning Dash",
    brand_href="/",
    color="primary",
    dark=True,
)

#Similar to my App.js in React this will be the starting location where we swap out the pages.
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='content')
])

#Index
index_page=html.Div([
    navbar,
    html.H1("Hello Dash!", className="mt-5 ml-4"),
    html.P("This is our First Dash App!", className="m-5"),
    html.Br(),
    "This was fun"
])

#Gapminder Data
gapminder_page=html.Div([
    navbar,
    html.H1("GDP, Life Expectancy, and Population Map", className="mt-5 ml-4"),

    dcc.Dropdown(id="mapchoice",
        options=[{'label': name,'value': indicator} for indicator, name in indicators.items()],
        className="m-5"),
    dcc.Graph(id="gapminder_chart")
])

##Iris Tabs
#Tab for 2-D graph
tab1= dbc.Card(dbc.CardBody([
    html.H3("Choose your Values to compare", className="mt-5 ml-4"),
    dcc.Dropdown(id="xchoice",
        options=[{'label': name,'value': indicator} for indicator, name in iris_choices.items()],
        className="m-5"),
    dcc.Dropdown(id="ychoice",
        options=[{'label': name,'value': indicator} for indicator, name in iris_choices.items()],
        className="m-5"),
    dcc.Graph(id="iris_chart",figure=px.scatter(iris,x="sepal_length",y="sepal_width", color = 'species', title = "Iris Dataset", labels={**iris_choices,'species':'Species'}, template="plotly_dark", height=1000)),
    html.Br()
    ]),className='mt-5 mb-10')

#Tab for 3-D graph
tab2=dbc.Card(
dbc.CardBody([
    html.H3("Try Moving the slider"),
    dcc.Graph(id="iris_chart2"),
    html.H3("Petal Width:"),
    dcc.RangeSlider(
        id='slider',
        min=0, max=2.5, step=0.25,
        marks={0: '0',1.25:'1,25', 2.5: '2.5'},
        value=[0, 2.5]
    ),
    html.Br(className="mb-10")
]),className='mt-5 mb-10')

#Iris Data
iris_page=html.Div([
    navbar,
    html.H1("Explore the Iris Data Set", className="mt-5 ml-4"),
    dbc.Tabs([
        dbc.Tab(tab1,label="2-D Chart"),
        dbc.Tab(tab2,label="3-D Chart"),
    ])
])


#Tips Data
tips_page=html.Div([
    navbar,
    html.H1("Explore Tip data", className="mt-5 ml-4"),

    dbc.Row([
        dbc.Col(dcc.Graph(id="t1",figure=px.histogram(tips,width=300, y='percentage', x='total_bill', color='sex',histfunc='avg', labels=labels, template="plotly_dark", title="Average Tip vs Total Bill by sex"))),
        dbc.Col(dcc.Graph(id="t2",figure=px.scatter(tips, width=300, x='percentage',y='total_bill',size='size',color='day',animation_frame='sex', labels=labels,template="plotly_dark", title="Bill Size vs Tip Percentage by Day on Gender"))),
    ]),
    html.Br(),

    dbc.Row([dbc.Col(dcc.Graph(id='t3',figure=px.scatter(tips,x="tip",y="total_bill",size="percentage", color = 'sex', facet_col="time", labels=labels,template="plotly_dark", title="Total Bill by Tip With Gender")))])
])

##CALLBACKS
#Iris callback build chart based on two user choices of Sepal/Petal Length/Width
@app.callback(Output('iris_chart','figure'),Input('xchoice','value'),Input('ychoice','value'))
def iris_chart(xchoice,ychoice):
    if xchoice is None or ychoice is None:
        raise PreventUpdate
    chart=px.scatter(data_frame= iris, x=xchoice,  y=ychoice, color = 'species', title = "Iris Dataset", labels={**iris_choices,'species':'Species'}, template="plotly_dark", height=1000)
    return chart

#Iris call back to control chart based on Slider input of petal_width
@app.callback(
    Output("iris_chart2", "figure"), 
    [Input("slider", "value")])
def update_bar_chart(slider):
    low, high = slider
    filter = (iris.petal_width > low) & (iris.petal_width < high)
    fig = px.scatter_3d(iris[filter], 
        x='sepal_length', y='sepal_width', z='petal_length',
        height=1000,  title="Sepal length x Sepal width x Petal Length and Scrollbar for Petal Width",
        color="species",  labels={**iris_choices,'species':'Species'}, template="plotly_dark", hover_data=['petal_width'])
    return fig

#heatmap for gapminder build chart based on users choice of GDP, Population, or Life expectancy
@app.callback(Output('gapminder_chart','figure'),Input('mapchoice','value'))
def heatmap(mapchoice):
    if mapchoice is None:
        mapchoice="gdpPercap"
    map = px.choropleth(gapminder,labels={**indicators},locations='iso_alpha',color=mapchoice ,animation_frame='year',hover_name='country',template="plotly_dark", height=1000, title=f'{indicators[mapchoice]} 1952-2007 by Country', range_color=[min(gapminder[mapchoice]),max(gapminder[mapchoice])])
    return map

#nav callback to swap pages
@app.callback(Output('content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/gapminder':
        return gapminder_page
    elif pathname == '/iris':
        return iris_page
    elif pathname == '/tips':
        return tips_page
    else:
        return index_page

# Best Practices is to run modules as a script
if __name__ == "__main__":
    app.run_server(debug=True)