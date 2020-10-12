# importing all the required library
import pandas as pd
import dash
import dash_html_components as html
import webbrowser
import dash_core_components as dcc
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate


# Place to call global variable
app = dash.Dash()

global colors
colors = {'background':'#C0C0C0','text':'#111111'}

print("program stating")

# Function To load data
def load_data():
    dataset_name = "global_terror.csv"
    # df is a global variable
    global df
    df=pd.read_csv(dataset_name)

    month={
        'January': 1,
        'February': 2,
        'March': 3,
        'April': 4,
        'May': 5,
        'June': 6,
        'July': 7,
        'August': 8,
        'September': 9,
        'October': 10,
        'November': 11,
        'December': 12
        }

    global date_list
    date_list=[x for x in range(1, 32)]

    global month_list
    month_list=[{'label': key, 'value': values} for key, values in month.items()]

    global region_list
    region_list=[{'label': str(i), 'value': str(i)} for i in sorted(df['region_txt'].unique().tolist())]

    global country_list
    country_list=df.groupby('region_txt')['country_txt'].unique().apply(list).to_dict()

    global state_list
    state_list=df.groupby('country_txt')['provstate'].unique().apply(list).to_dict()

    global city_list
    city_list=df.groupby('provstate')['city'].unique().apply(list).to_dict()

    global attack_type_list
    attack_type_list=[{'label': str(i), 'value': str(i)} for i in df['attacktype1_txt'].unique().tolist()]

    global year_list
    year_list=sorted(df['iyear'].unique().tolist())

    global year_dict
    year_dict={str(year): str(year) for year in year_list}
    
    # Chart dropdown values
    global chart_dropdown_values
    chart_dropdown_values = {"Terrorist Organisation": 'gname',
                             "Target Nationality": 'natlty1_txt',
                             "Target Type": 'targtype1_txt',
                             "Type of Attack": 'attacktype1_txt',
                             "Weapon Type": 'weaptype1_txt',
                             "Region": 'region_txt',
                             "Country Attacked": 'country_txt'
                             }
    chart_dropdown_values=[{'label': keys, 'value': value} for keys, value in chart_dropdown_values.items()]

# Fuction to open browser automatically by running
def open_browser():
    webbrowser.open_new('http://127.0.0.1:8050/')

# Function to create app UI
def create_app_ui():
    main_layout=html.Div(style={'backgroundColor':colors['background']}, children=[
        html.H1(children='Terrorism Analysis with Insights', id='Main_title', style={'textAlign': "center"}),
        dcc.Tabs(id='Tabs', value='Map', children=[
            dcc.Tab(label="Map Tool", id='Map Tool', value='Map', children=[
                dcc.Tabs(id='subtabs', value='WorldMap', children=[
                    dcc.Tab(label='World Map Tool', id='World', value='WorldMap'),
                    dcc.Tab(label="India Map tool", id="India", value="IndiaMap")
                    ]),
                

                html.Hr(),
                dcc.Dropdown(id='month',
                             options=month_list,
                             placeholder='Select Month',
                             multi=True),
                html.Br(),
                dcc.Dropdown(id='date',
                             # options=date_list,
                             placeholder='Select Day',
                             multi=True),
                html.Br(),
                dcc.Dropdown(id='region-dropdown',
                             options=region_list,
                             placeholder='Select Region',
                             multi=True),
                html.Br(),
                dcc.Dropdown(id='country-dropdown',
                             options=[{'label': 'All', 'value': 'All'}],
                             placeholder='Select Country',
                             multi=True),
                html.Br(),
                dcc.Dropdown(id='state-dropdown',
                             options=[{'label': 'All', 'value': 'All'}],
                             placeholder='Select State or Province',
                             multi=True),
                html.Br(),
                dcc.Dropdown(id='city-dropdown',
                             options=[{'label': 'All', 'value': 'All'}],
                             placeholder='Select City',
                             multi=True),
                html.Br(),
                dcc.Dropdown(id='attack-type-dropdown',
                             options=attack_type_list,
                             placeholder='Select Attack Type',
                             multi=True),
                html.Br(),
                html.H5('Select The Year', id='year-title'),
                html.Br(),
                dcc.RangeSlider(id='year-slider',
                                min=min(year_list),
                                max=max(year_list),
                                value=[min(year_list), max(year_list)],
                                marks=year_dict),
                html.Br(),
                ]),
            
            dcc.Tab(label="Chart Tool", id="chart tool", value="Chart", children=[
                dcc.Tabs(id="subtabs2", value="WorldChart", children=[
                    
                    dcc.Tab(label="World Chart tool", id="WorldC", value="WorldChart"),
                    dcc.Tab(label="India Chart tool", id="IndiaC", value="IndiaChart")]),
                    dcc.Dropdown(id='Chart_Dropdown', options=chart_dropdown_values, placeholder="Select Option", value= "region_txt"),
                    html.Br(),
                    html.Hr(),
                    dcc.Input(id="search", placeholder="Search Filter", style={'textAlign':'center','width':'60%','display':'inline-block','verticalAlign':'middle'}),
                    html.Hr(),
                    html.Br(),
                    html.Hr(),
                    dcc.RangeSlider(
                        id='cyear_slider',
                        min=min(year_list),
                        max=max(year_list),
                        value=[min(year_list), max(year_list)],
                        marks=year_dict,
                        step=None
                        ),
                    html.Br()
                    ]),          
        
            ]),
    html.Div(id='graph-object', children= 'Graph will be shown Here') 
    ])    
    
    return main_layout

# cllbacks of Tabs and Dropdowns
@app.callback(
     dash.dependencies.Output('graph-object', 'children'),
     [dash.dependencies.Input('Tabs', 'value'),
      dash.dependencies.Input('month', 'value'),
      dash.dependencies.Input('date', 'value'),
      dash.dependencies.Input('region-dropdown', 'value'),
      dash.dependencies.Input('country-dropdown', 'value'),
      dash.dependencies.Input('state-dropdown', 'value'),
      dash.dependencies.Input('city-dropdown', 'value'),
      dash.dependencies.Input('attack-type-dropdown', 'value'),
      dash.dependencies.Input('year-slider', 'value'),
      dash.dependencies.Input('cyear_slider', 'value'),
      dash.dependencies.Input("Chart_Dropdown", "value"),
      dash.dependencies.Input("search", "value"),
      dash.dependencies.Input("subtabs2", "value")]
     )
def update_app_ui(Tabs, month_value, date_value, region_value, country_value, state_value, city_value, attacktype_value, year_value, chart_year_selector, chart_dp_value, search, subtabs2):
    fig = None
    if Tabs =='Map':
        print("datatype of month_value is=", str(type(month_value)))
        print('value of month_value is=', month_value)

        print("datatype of date_value is=", str(type(date_value)))
        print('value of date_value is=', date_value)

        print("datatype of region_value is=", str(type(region_value)))
        print('value of region_value is=', region_value)

        print("datatype of country_value is=", str(type(country_value)))
        print('value of country_value is=', country_value)
        
        print("datatype of state_value is=", str(type(state_value)))
        print('value of state_value is=', state_value)
        
        print("datatype of country_value is=", str(type(city_value)))
        print('value of country_value is=', city_value)
        
        print("datatype of attacktype_value is=", str(type(attacktype_value)))
        print('value of attacktype_value is=', attacktype_value)
        
        print("datatype of year_value is=", str(type(year_value)))
        print('value of year_value is=', year_value)
        
        # Year filter
        year_range=range(year_value[0],year_value[1]+1)
        new_df=df[df['iyear'].isin(year_range)]
        
        
        #month and date filter
        if month_value== [] or month_value is None:
            pass
        else:
            if date_value== [] or date_value is None:
                new_df = new_df[new_df["imonth"].isin(month_value)]
             
                
            else:
                
                new_df = new_df[(new_df["imonth"].isin(month_value))
                                & (new_df["iday"].isin(date_value))]
        
        # region, country, state, city filter
        if region_value == [] or region_value is None:
            pass
        else:
              if country_value == [] or country_value is None:
                 new_df = new_df[(new_df["region_txt"].isin(region_value))]
              else:
                   if state_value == [] or state_value is None:
                        new_df = new_df[(new_df["region_txt"].isin(region_value)) &
                                        (new_df["country_txt"].isin(country_value))]
                   else:
                        
                       if city_value == [] or city_value is None:
                            new_df = new_df[(new_df["region_txt"].isin(region_value)) &
                                            (new_df["country_txt"].isin(country_value)) &
                                            (new_df["provstate"].isin(state_value))]
                       else:
                            
                            new_df = new_df[(new_df["region_txt"].isin(region_value)) &
                                            (new_df["country_txt"].isin(country_value)) &
                                            (new_df["provstate"].isin(state_value)) &
                                            (new_df["city"].isin(city_value))]
                        
        #Attack Type
        if attacktype_value == [] or attacktype_value is None:
            pass
        else:
            new_df = new_df[new_df["attacktype1_txt"].isin(attacktype_value)]
         # You should always set the figure for blank, since this callback 
         # is called once when it is drawing for first time  
        mapFigure = go.Figure()
        if new_df.shape[0]:
            pass
        else:
            
            new_df = pd.DataFrame(columns=['iyear', 'imonth', 'iday', 'country_txt', 'region_txt', 'provstate',
                                       'city', 'latitude', 'longitude', 'attacktype1_txt', 'nkill'])

            new_df.loc[0] = [0, 0, 0, None, None, None, None, None, None, None, None]
    
        mapFigure = px.scatter_mapbox(new_df,
                            lat='latitude',
                            lon='longitude',
                            color=('attacktype1_txt'),
                            hover_data=('region_txt', 'country_txt', 'provstate', 'city', 'nkill', 'iyear'),
                            zoom=1
                            )
        mapFigure.update_layout(mapbox_style="stamen-watercolor",
                    autosize=True,
                    margin=dict(l=0, r=0, t=25, b=20)
                    )
        
        fig = mapFigure
        
    elif Tabs=='Chart':
        fig = None
        year_range_c=range(chart_year_selector[0], chart_year_selector[1]+1)
        
        chart_df = df[df["iyear"].isin(year_range_c)]
        
        
        if subtabs2=='WorldChart':
            
            pass
        elif subtabs2=='IndiaChart':
            
            chart_df = chart_df[(chart_df["region_txt"]=='South Asia') & (chart_df['country_txt']=="India")]
        if chart_dp_value is not None and chart_df.shape[0]:
            if search is not None:
                chart_df = chart_df.groupby("iyear")[chart_dp_value].value_counts().reset_index(name ='count')
                chart_df = chart_df[chart_df[chart_dp_value].str.contains(search, case=False)]
            else:
                chart_df = chart_df.groupby("iyear")[chart_dp_value].value_counts().reset_index(name= "count")
                
        if chart_df.shape[0]:
            
            pass
        else:
            chart_df = pd.DataFrame(columns = ['iyear', 'count', chart_dp_value])
            
            chart_df.loc[0] = [0, 0, "No Data"]
        fig = px.area(chart_df, x='iyear', y = 'count', color = chart_dp_value)
        
    return dcc.Graph(figure=fig)


@app.callback(
    Output('date', 'options'),
    [Input('month','value')]
    )
def update_date_options(month_value):
    date_list=[x for x in range(1, 32)]
    option=[]
    if month_value:
        option=[{"label": m, "value": m} for m in date_list]
    return option

@app.callback(
        [Output('region-dropdown', 'value'),
         Output('region-dropdown', 'disabled'),
         Output('country-dropdown', 'value'),
         Output('country-dropdown', 'disabled')],
         [Input("subtabs", 'value')])
def update_r(tab):
    region = None
    disabled_r = False
    country = None
    disabled_c = False
    if tab=='WorldMap':
        pass
    elif tab=="IndiaMap":
        region = ["South Asia"]
        disabled_r = True
        country = ["India"]
        disabled_c = True
    return region, disabled_r, country, disabled_c

@app.callback(
    Output('country-dropdown', 'options'),
    [Input('region-dropdown','value')]
    )
def set_country_options(region_value):
    option=[]
    # Making the country dropdown data
    if region_value is None:
        raise PreventUpdate
    else:
        for var in region_value:
            if var in country_list.keys():
                option.extend(country_list[var])
    return[{'label':m,'value': m} for m in option]


@app.callback(
    Output('state-dropdown', 'options'),
    [Input('country-dropdown','value')]
    )
def set_state_options(country_value):
    option=[]
    # Making the state dropdown data
    if country_value is None:
        raise PreventUpdate
    else:
        for var in country_value:
            if var in state_list.keys():
                option.extend(state_list[var])
    return[{'label':m,'value': m} for m in option]


@app.callback(
    Output('city-dropdown', 'options'),
    [Input('state-dropdown','value')]
    )
def set_city_options(state_value):
    option=[]
    # Making the city dropdown data
    if state_value is None:
        raise PreventUpdate
    else:
        for var in state_value:
            if var in city_list.keys():
                option.extend(city_list[var])
    return[{'label':m,'value': m} for m in option]

# Flow of the project
def main():
    print("Starting the Main function...")
    load_data()
    open_browser()

    global app

    app.layout = create_app_ui()
    app.title = "Terrorism Analysis With Insights"
    app.run_server()
    
# Deallocating memory    
    df=None
    app=None

    print("Ending the Main function....")
    
if __name__== "__main__":
    print('Starting the project....')
    main()
    print('ending the project......')
    