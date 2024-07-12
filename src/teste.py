import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the data
file_path = 'Moly.csv'
data = pd.read_csv(file_path)

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout of the app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Label('Cliente'),
            dcc.Dropdown(
                id='cliente-dropdown',
                options=[{'label': cliente, 'value': cliente} for cliente in data['Cliente'].unique()],
                multi=True
            )
        ], width=4),
        dbc.Col([
            html.Label('Tipo'),
            dcc.Dropdown(
                id='tipo-dropdown',
                options=[{'label': tipo, 'value': tipo} for tipo in data['Tipo'].unique()],
                multi=True
            )
        ], width=4),
        dbc.Col([
            html.Label('Ano'),
            dcc.Dropdown(
                id='ano-dropdown',
                options=[{'label': ano, 'value': ano} for ano in data['Ano'].unique()],
                multi=True
            )
        ], width=4)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='sales-graph')
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.Div(id='totals-legend')
        ], width=12)
    ])
], fluid=True)

# Callback to update the graph and totals legend
@app.callback(
    [Output('sales-graph', 'figure'),
     Output('totals-legend', 'children')],
    [Input('cliente-dropdown', 'value'),
     Input('tipo-dropdown', 'value'),
     Input('ano-dropdown', 'value')]
)
def update_graph(selected_clientes, selected_tipos, selected_anos):
    filtered_data = data

    if selected_clientes:
        filtered_data = filtered_data[filtered_data['Cliente'].isin(selected_clientes)]
    if selected_tipos:
        filtered_data = filtered_data[filtered_data['Tipo'].isin(selected_tipos)]
    if selected_anos:
        filtered_data = filtered_data[filtered_data['Ano'].isin(selected_anos)]

    # Convert monthly columns to long format
    filtered_data_long = filtered_data.melt(id_vars=['Cliente', 'Tipo', 'Ano'], 
                                            value_vars=['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez'], 
                                            var_name='Mês', value_name='Vendas')

    fig = px.bar(filtered_data_long, x='Mês', y='Vendas', color='Cliente', barmode='group', facet_row='Ano', height=600 * len(filtered_data['Ano'].unique()))
    
    # Calculate totals
    total_spot = filtered_data[filtered_data['Tipo'] == 'Spot']['TOTAL'].sum()
    total_ltc = filtered_data[filtered_data['Tipo'] == 'LTC']['TOTAL'].sum()
    total_sum = filtered_data['TOTAL'].sum()

    totals_text = f"Total Spot: {total_spot:.2f} | Total LTC: {total_ltc:.2f} | Soma Total: {total_sum:.2f}"

    return fig, totals_text

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
