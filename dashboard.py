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
div_agenda = pd.read_csv('dividends_agenda.csv')

#news_list = ...

recommended_portfolios = recommended_portfolio.load_recommended_portfolios()

followed_stocks = {}

generic_data.get_generic_data()
main_graph = pd.read_csv('generic_data.csv')
main_graph = utils.df_treatment(main_graph)
# main_graph['Date'] = pd.to_datetime(main_graph['Date'])
# main_graph.set_index('Date', inplace=True)

# # Normalize the data for comparison
# main_graph = main_graph.div(main_graph.iloc[0]).multiply(100).reset_index()
# main_graph.set_index('Date', inplace=True)


# Initialize the app
app = Dash()

app.layout = [
    html.Div([ # Dividends Agenda
    html.H2('Dividends Agenda'),
    dash_table.DataTable(
        data=div_agenda.to_dict('records'),
        columns=[{'name': col, 'id': col} for col in div_agenda.columns]
        )
    ]),

    html.Div([ #News Dashboard
        html.H2('News Dashboard'),
        dcc.RadioItems(
            options=[
                {'label': 'Mercados', 'value': 'mercados'},
                #{'label': 'Recentes', 'value': 'recentes'},
                {'label': 'Global', 'value': 'global'},
                {'label': 'Investimentos', 'value': 'investimentos'},
                {'label': 'Política', 'value': 'politica'},
                {'label': 'Economia', 'value': 'economia'}
            ],
            value='mercados',
            id='news-section',
            inline=True),
        html.Div(id='news-content'),
    ]),

    html.Div([ # Recommended Portfolios
        dcc.Dropdown(
                options=list(recommended_portfolios.keys()),
                value = list(recommended_portfolios.keys())[0],
                id='recommendation-owner'),
        dcc.Graph(id='recommendation-graph')
    ]),

    html.Div([ # Fundamentus data
        dcc.Input(id='stock-ticker', type='text', placeholder='Enter a stock ticker...'),
        html.Div(id='stock-fundamentus-data')
    ]),

    html.Div([ # Followed Stocks
        dcc.Input(id='followed-stock', type='text', placeholder='Enter a stock ticker...'),
        html.Button('Follow', id='follow-button'),
        html.Div(id='followed-stocks-list')
    ]),

    html.Div([ # Main Graph
        html.H2('Main Graph'),
        dcc.Checklist(
            options=[{'label': col, 'value': col} for col in main_graph.columns],
            value=main_graph.columns.tolist(),
            id='main-graph-checklist',
            inline=True
        ),
        dcc.Input(id='add-ticker', type='text', placeholder='Enter a stock ticker...'),
        html.Button('+', id='add-button'),
        dcc.Graph(id='main-graph')
    ])
]



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
    fig = px.pie(df, names='Stock', values='Weight', hole = .5)
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
                html.H3(f'{stock_ticker}'),
                html.Button('X'),
                html.P(f'1d: {followed_stocks[stock_ticker]["1d"]}'),
                html.P(f'7d: {followed_stocks[stock_ticker]["7d"]}'),
                html.P(f'1m: {followed_stocks[stock_ticker]["1m"]}'),
                html.P(f'3m: {followed_stocks[stock_ticker]["3m"]}'),
                html.P(f'1y: {followed_stocks[stock_ticker]["1y"]}'),
                html.P(f'YTD: {followed_stocks[stock_ticker]["ytd"]}')
            ]) for stock_ticker in followed_stocks
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
    #TODO: Check callback trigger
    if add_ticker and n_clicks and len(add_ticker) >= 5 and add_ticker.upper() not in main_graph.columns:
        add_ticker = add_ticker.upper()
        stock_data_df, main_graph = stock_data.add_stock_data(add_ticker, main_graph)
        # stock_data_df = stock_data.get_stock_data(add_ticker)
        # stock_data_df = trata_main_graph(stock_data_df)
        #     #main_graph = main_graph.join(stock_data_df, how='left', rsuffix=f'_{add_ticker}')
        # main_graph = pd.merge(main_graph, stock_data_df, left_index=True, right_index=True)
        # main_graph = main_graph.ffill().bfill()
        # main_graph.rename(columns={'Close': add_ticker}, inplace=True)
        # print(main_graph)
        
    options = [{'label': col, 'value': col} for col in main_graph.columns]
    fig = px.line(main_graph, y=selected_columns, title='Percentage Change Over Time')
    return fig, options, selected_columns

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
