import dividends_agenda
import generic_data
import infomoney_news
import recommended_portfolio
import stock_data
import stock_fundamentus_data
import stock_returns_data
import utils
from dash import Dash, html, dash_table, dcc, callback, Output, Input, State
import pandas as pd
import plotly.express as px

dividends_agenda.get_dividens_agenda()
div_agenda = pd.read_csv('financial-dashboard\dividends_agenda.csv')

recommended_portfolios = recommended_portfolio.load_recommended_portfolios()

followed_stocks = {}

generic_data.get_generic_data()
main_graph = pd.read_csv('financial-dashboard\generic_data.csv')
main_graph = utils.df_treatment(main_graph)

# Initialize the app
app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.Div([ # Dividends Agenda
        html.Div('Dividends Agenda', className='purpose'),
        html.Div(dash_table.DataTable(
            data=div_agenda.to_dict('records'),
            columns=[{'name': col, 'id': col} for col in div_agenda.columns],
            style_header={
                'backgroundColor': 'var(--secondary-color)', 
                'color': 'white',
                'fontFamily': 'Bahnschrift',
                'fontWeight': 'bold'
            },
            style_cell={
                'backgroundColor': 'var(--primary-color)', 
                'color': 'white',
                'fontFamily': 'Bahnschrift'
            }
        ), className='content data-table')
    ], className='div-section dividends-agenda'),

    html.Div([ # News Dashboard
        html.Div('News Dashboard', className='purpose'),
        html.Div([
            dcc.RadioItems(
                options=[
                    {'label': 'Mercados', 'value': 'mercados'},
                    {'label': 'Global', 'value': 'global'},
                    {'label': 'Investimentos', 'value': 'investimentos'},
                    {'label': 'Política', 'value': 'politica'},
                    {'label': 'Economia', 'value': 'economia'}
                ],
                value='mercados',
                id='news-section',
                inline=True,
                className='radio-items'
            ),
            html.Div(id='news-content')
        ], className='content')
    ], className='div-section news-dashboard'),

    html.Div([ # Recommended Portfolios
        html.Div('Recommended Portfolios', className='purpose'),
        html.Div([
            dcc.Dropdown(
                options=list(recommended_portfolios.keys()),
                value=list(recommended_portfolios.keys())[0],
                id='recommendation-owner',
                className='dropdown'
            ),
            dcc.Graph(id='recommendation-graph')
        ], className='content')
    ], className='div-section recommended-portfolios'),

    html.Div([ # Fundamentus data
        html.Div('Fundamentus Data', className='purpose'),
        html.Div([
            dcc.Input(id='stock-ticker', type='text', placeholder='Enter a stock ticker...', className='input'),
            html.Div(id='stock-fundamentus-data')
        ], className='content')
    ], className='div-section fundamentus-data'),

    html.Div([ # Followed Stocks
        html.Div('Followed Stocks', className='purpose'),
        html.Div([
            dcc.Input(id='followed-stock', type='text', placeholder='Enter a stock ticker...', className='input'),
            html.Button('Follow', id='follow-button', className='button'),
            html.Div(id='followed-stocks-list', className='content')
        ], className='content')
    ], className='div-section followed-stocks'),

    html.Div([ # Main Graph
        html.Div('Main Graph', className='purpose'),
        html.Div([
            dcc.Checklist(
                options=[{'label': col, 'value': col} for col in main_graph.columns],
                value=main_graph.columns.tolist(),
                id='main-graph-checklist',
                inline=True,
                className='checklist'
            ),
            dcc.Input(id='add-ticker', type='text', placeholder='Enter a stock ticker...', className='input'),
            html.Button('+', id='add-button', className='button'),
            dcc.Graph(id='main-graph')
        ], className='content')
    ], className='div-section main-graph')
], className='container')

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

app.css.append_css({
    'external_url': '/assets/style.css'
})

@callback(
    Output('news-content', 'children'),
    Input('news-section', 'value')
)
def update_news(news_section):
    news_list = infomoney_news.infomoney_news_api(news_section)
    return [
        html.Div([ 
            html.Div([
                html.A(news['title'], href=news['link'], target='_blank'),
                html.Br(),
                html.Small(news['time'])
            ]) for news in news_list
        ])
    ]

@callback(
    Output('recommendation-graph', 'figure'),
    Input('recommendation-owner', 'value')
)
def update_recommended_portfolios(selected_owner):
    df = recommended_portfolios[selected_owner]
    fig = px.pie(df, names='Stock', values='Weight', hole=.7)
    fig.update_traces(textposition='outside', textinfo='label+percent')
    fig.update_layout(
        showlegend=False,
        autosize=True,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', family='Bahnschrift'),
        )
    return fig

@callback(
    Output('stock-fundamentus-data', 'children'),
    Input('stock-ticker', 'value')
)
def update_stock_fundamentus_data(stock_ticker):
    if stock_ticker and len(stock_ticker) >= 5:
        stock_ticker = stock_ticker.upper()
        fundamentus_data = stock_fundamentus_data.get_fundamentus_data(stock_ticker)
        return html.Div([
            html.H3(f'Fundamentus data for {stock_ticker}:'),
            html.P(f'P/L: {fundamentus_data["P/L"]}'),
            html.P(f'P/VP: {fundamentus_data["P/VP"]}'),
            html.P(f'DY: {fundamentus_data["DY"]}'),
            html.P(f'ROE: {fundamentus_data["ROE"]}'),
            html.P(f'ROIC: {fundamentus_data["ROIC"]}')
        ])
    else:
        return html.Div([])

@callback(
    Output('followed-stocks-list', 'children'),
    Input('follow-button', 'n_clicks'),
    State('followed-stock', 'value')
)
def follow_stock(n_clicks, stock_ticker):
    if n_clicks and stock_ticker and len(stock_ticker) >= 5:
        stock_ticker = stock_ticker.upper()
        followed_stocks[stock_ticker] = stock_returns_data.get_stock_returns_data(stock_ticker)
    return [
        html.Div([
            html.Div([
                html.Div([
                    html.H3(f'{stock_ticker}', style={'margin': '0', 'font-size': '1rem'}),
                    html.Button('X', style={'margin-left': '10px', 'font-size': '0.8rem', 'padding': '0 5px'})
                ], className='followed-stock-header'),
                html.Div([
                    html.P(f'1d: {followed_stocks[stock_ticker]["1d"]}', style={'margin': '2'}),
                    html.P(f'7d: {followed_stocks[stock_ticker]["7d"]}', style={'margin': '2'}),
                    html.P(f'1m: {followed_stocks[stock_ticker]["1m"]}', style={'margin': '2'}),
                    html.P(f'3m: {followed_stocks[stock_ticker]["3m"]}', style={'margin': '2'}),
                    html.P(f'1y: {followed_stocks[stock_ticker]["1y"]}', style={'margin': '2'}),
                    html.P(f'YTD: {followed_stocks[stock_ticker]["ytd"]}', style={'margin': '2'})
                ], className='followed-stock-returns')
            ], className='followed-stock-item') for stock_ticker in followed_stocks
        ])
    ]

@callback(
    Output('main-graph', 'figure'),
    Output('main-graph-checklist', 'options'), # Update checklist
    Output('main-graph-checklist', 'value'), # Update checklist
    Input('main-graph-checklist', 'value'),
    Input('add-button', 'n_clicks'),
    State('add-ticker', 'value')
)
def update_main_graph(selected_columns, n_clicks, add_ticker):
    global main_graph
    if add_ticker and n_clicks and len(add_ticker) >= 5 and add_ticker.upper() not in main_graph.columns:
        add_ticker = add_ticker.upper()
        stock_data_df, main_graph = stock_data.add_stock_data(add_ticker, main_graph)
    options = [{'label': col, 'value': col} for col in main_graph.columns]
    fig = px.line(main_graph, y=selected_columns, title='Percentage Change Over Time')
    fig.update_layout(
        showlegend=False,
        autosize=True,
        margin=dict(l=20, r=20, t=30, b=20),  # Reduce margins to use more space
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', family='Bahnschrift')
    )
    return fig, options, selected_columns

if __name__ == '__main__':
    app.run(debug=True)