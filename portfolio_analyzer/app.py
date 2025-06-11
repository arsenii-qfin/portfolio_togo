import dash_mantine_components as dmc
import pandas as pd
import numpy as np
import plotly.express as px
from dash import Dash, dash_table, Input, Output, State, Patch, callback, dcc, no_update
import yfinance as yf
from dash_iconify import DashIconify
from datetime import datetime, timedelta
from base64 import b64decode
from io import StringIO, BytesIO
from random import sample
from data.quiz import quiz
from data.scroll_text import left_scroll_text, right_scroll_text 
from data.plot_scroll_text import plot_1, plot_2, plot_3, plot_4, plot_5, plot_6, plot_7
from utils.make_quiz_card import make_quiz_card

dummy_df = pd.DataFrame({
    "Date": pd.date_range(start="2023-01-01", periods=10, freq="ME"),
    "Portfolio": [0.01, 0.03, 0.025, 0.05, 0.06, 0.07, 0.1, 0.09, 0.12, 0.14],
    "S&P500": [0.02, 0.025, 0.03, 0.045, 0.05, 0.06, 0.08, 0.085, 0.09, 0.1]
})

app = Dash(
    __name__,
    title='Portfolio ToGo',
    update_title='Wait for it!',
    external_stylesheets=dmc.styles.ALL,
    on_error=None
    )

app.layout=dmc.MantineProvider(
    children=[
        dmc.NotificationProvider(position='top-right'),
        dmc.Group(id='notification-container'),
        dcc.Store(id='fetched_data_store', storage_type='session'), # ---> dict(portfolio_data)
        dcc.Store(id='S&P_data_store', storage_type='session'), # ---> dict(spy_store_df)
        dcc.Store(id='quiz_data', storage_type='memory'), # ---> dict(quiz_batch)
        dmc.AppShell(
            children=[
                dmc.AppShellMain(
                    children=[
                        dmc.Group(
                            justify='center',
                            bg='var(--mantine-color-blue-6)',
                            h={'base': '3rem', 'md': '4rem', 'lg': '4rem'},
                            children=[
                                dmc.Title(
                                    'Portfolio ToGo',
                                    order=1,
                                    style={'fontFamily': 'Roboto', 'fontWeight': '1000', 'background': 'linear-gradient(180deg, #adb5bd, white)', 'WebkitBackgroundClip': 'text', 'WebkitTextFillColor': 'transparent'}
                                )
                            ]
                        ),
                        dmc.Tabs(
                            color='blue',
                            activateTabWithKeyboard=True,
                            value='tab-0',
                            orientation='horizontal',
                            inverted=True,
                            variant='pills',
                            autoContrast=True,
                            children=[
                                dmc.TabsList(
                                    grow=True, #NOTE
                                    display='-ms-inline-flexbox',
                                    style={'borderTop': '2px solid black'},
                                    h={'base': '3rem', 'md': '4rem', 'lg': '4rem'},
                                    children=[ 
                                        dmc.TabsTab(value='tab-0', children=[dmc.Title('Main', order=3, style={'fontFamily': 'Roboto', "fontSize": "clamp(0.8rem, 4vw, 1.5rem)"})], leftSection=DashIconify(icon='rivet-icons:home-solid', style={"width": "clamp(0.9rem, 4vw, 1.5rem)", "height": "clamp(0.9rem, 4vw, 1.5rem)"})),
                                        dmc.TabsTab(value='tab-1', children=[dmc.Title('Analysis', order=3, style={'fontFamily': 'Roboto', "fontSize": "clamp(0.8rem, 4vw, 1.5rem)"})], leftSection=DashIconify(icon='mdi:performance', style={"width": "clamp(0.9rem, 4vw, 1.5rem)", "height": "clamp(0.9rem, 4vw, 1.5rem)"})),
                                        dmc.TabsTab(value='tab-2', children=[dmc.Title('Monte Carlo', order=3, style={'fontFamily': 'Roboto', "fontSize": "clamp(0.8rem, 4vw, 1.5rem)"})], leftSection=DashIconify(icon='mdi:graph', rotate=3, style={"width": "clamp(0.9rem, 4vw, 1.5rem)", "height": "clamp(0.9rem, 4vw, 1.5rem)"}))
                                    ]
                                ),
                                dmc.TabsPanel(
                                    value='tab-0',
                                    children=[
                                        dmc.Box(
                                            pt='2rem',
                                            children=[
                                                dmc.Stack(
                                                    py='1rem',
                                                    justify='center',
                                                    style={'height': '100%'},
                                                    gap='lg',
                                                    children=[
                                                        dmc.Grid(
                                                            justify='center',
                                                            align='center',
                                                            gutter=0,
                                                            children=[
                                                                dmc.GridCol(
                                                                    span=4,
                                                                    px='md',
                                                                    children=[
                                                                        dmc.Paper(
                                                                            style={'width':'100%'},
                                                                            withBorder=True,
                                                                            shadow='sm',
                                                                            p='md',
                                                                            children=[
                                                                                dmc.Text('What is It?', c='dimmed', style={'textAlign': 'center', 'fontSize': '2rem', 'fontWeight': '500', 'color': 'grey'}),
                                                                                dmc.Divider(variant='solid', size='sm', color='blue', w='100%'),
                                                                                dmc.Text(left_scroll_text, c='dimmed', style={'fontSize': '1.25rem', 'fontFamily': 'Roboto'})
                                                                            ]
                                                                        )
                                                                    ]
                                                                ),
                                                                dmc.GridCol(
                                                                    span=4,
                                                                    children=[
                                                                        dmc.Carousel(
                                                                            id='quiz_carousel',
                                                                            withIndicators=True,
                                                                            loop=True,
                                                                            slideSize='100%',
                                                                            style={'width':'100%', 'boxShadow': '3px 3px 8px rgba(0, 0, 0, 0.5)'}
                                                                        )
                                                                    ]
                                                                ),
                                                                dmc.GridCol(
                                                                    span=4,
                                                                    px='md',
                                                                    children=[
                                                                        dmc.Paper(
                                                                            style={'width':'100%'},
                                                                            withBorder=True,
                                                                            shadow='sm',
                                                                            p='md',
                                                                            children=[
                                                                                dmc.Text('How to Use?', c='dimmed', style={'textAlign': 'center', 'fontSize': '2rem', 'fontWeight': '500', 'color': 'grey'}),
                                                                                dmc.Divider(variant='solid', size='sm', color='blue', w='100%'),
                                                                                dmc.Text(right_scroll_text, c='dimmed', style={'fontSize': '1.25rem', 'fontFamily': 'Roboto'})
                                                                            ]
                                                                        )
                                                                    ]
                                                                )
                                                            ]
                                                        ),
                                                        dmc.Divider(label='Input Tickers Below', labelPosition='center', variant='solid', size='sm', color='blue', w='100%'),
                                                        dmc.Grid(
                                                            justify='center',
                                                            gutter='md',
                                                            overflow='hidden',
                                                            children=[
                                                                dmc.GridCol(
                                                                    span='content',
                                                                    children=[
                                                                        dmc.DatePickerInput(
                                                                            id='date_picker_range',
                                                                            size='xl',
                                                                            type='range',
                                                                            valueFormat='YYYY-MM-DD',
                                                                            value=[datetime.now().date() - timedelta(days=30), datetime.now().date()],
                                                                            clearable=True,
                                                                            style={'boxShadow': '2px 2px 8px rgba(0, 0, 0, 0.2)'},
                                                                            radius='0rem',
                                                                            leftSection=dmc.Tooltip(
                                                                                DashIconify(icon='uil:calender', style={'width': '1.5rem', 'height': '1.5rem', 'color': '#000'}), 
                                                                                label='Note: The market is closed on weekends and holidays.',
                                                                                color='#fafafa',
                                                                                withArrow=True,
                                                                                arrowPosition='center',
                                                                                arrowSize=8,
                                                                                multiline=True,
                                                                                transitionProps={'transition':'pop-bottom-left', 'duration':100},
                                                                                styles={'tooltip': {'color': '#000000', 'fontSize': '1rem'}}
                                                                            )
                                                                        )
                                                                    ]
                                                                ),
                                                                dmc.GridCol(
                                                                    span='content',
                                                                    children=[
                                                                        dmc.Stack(
                                                                            justify='center',
                                                                            gap='0',
                                                                            children=[
                                                                                dmc.Tooltip(
                                                                                    color='#fafafa',
                                                                                    withArrow=True,
                                                                                    arrowPosition='center',
                                                                                    arrowSize=8,
                                                                                    multiline=True,
                                                                                    label='Click to add another row.',
                                                                                    transitionProps={'transition':'pop-bottom-left', 'duration':200},
                                                                                    styles={'tooltip': {'color': '#000000', 'fontSize': '1rem'}},
                                                                                    children=[
                                                                                        dmc.ActionIcon(
                                                                                            id='add_row_button',
                                                                                            n_clicks=0,
                                                                                            variant='light',
                                                                                            style={'boxShadow': '1px 1px 4px rgba(0, 0, 0, 0.3)'},
                                                                                            children=[
                                                                                                DashIconify(icon='mi:add', style={'height':'2rem', 'width': '2rem'})
                                                                                            ]
                                                                                        )                                                                                        
                                                                                    ]                                                                                    
                                                                                ),
                                                                                dmc.Tooltip(
                                                                                    color='#fafafa',
                                                                                    withArrow=True,
                                                                                    arrowPosition='center',
                                                                                    arrowSize=8,
                                                                                    multiline=True,
                                                                                    label='Click to clear the entire table.',
                                                                                    transitionProps={'transition':'pop-bottom-left', 'duration':200},
                                                                                    styles={'tooltip': {'color': '#000000', 'fontSize': '1rem'}},
                                                                                    children=[
                                                                                        dmc.ActionIcon(
                                                                                            id='clear_table_button',
                                                                                            n_clicks=0,
                                                                                            variant='light',
                                                                                            style={'boxShadow': '1px 1px 4px rgba(0, 0, 0, 0.3)'},
                                                                                            children=[
                                                                                                DashIconify(icon='ix:clear', style={'height':'2rem', 'width': '2rem'})
                                                                                            ]
                                                                                        )                                                                                        
                                                                                    ]
                                                                                )
                                                                            ]    
                                                                        )
                                                                    ]
                                                                ),        
                                                                dmc.GridCol(
                                                                    span=5,
                                                                    children=[
                                                                        dash_table.DataTable(
                                                                            id='ticker_unit_picker_table',
                                                                            columns=[
                                                                                {'name': 'Ticker', 'id': 'Ticker', 'type': 'text'},
                                                                                {'name': 'Units', 'id': 'Units', 'type': 'numeric'}
                                                                            ],
                                                                            data=[{'Ticker': 'AAPL', 'Units': 4}, {'Ticker': 'GOOG', 'Units': 6}, {'Ticker': 'AMZN', 'Units': 3}, {'Ticker': 'NVDA', 'Units': 9}],
                                                                            editable=True,
                                                                            row_deletable=True,
                                                                            page_size=5,
                                                                            page_action='native',
                                                                            style_data={'padding': '6px', 'textAlign': 'center'},
                                                                            style_data_conditional=[
                                                                                {
                                                                                    'if': {
                                                                                        'column_id': 'Ticker',
                                                                                        'filter_query': '{Ticker} is blank'
                                                                                    },
                                                                                    'backgroundColor': '#ffdbd8'
                                                                                },
                                                                                {
                                                                                    'if': {
                                                                                        'column_id': 'Units',
                                                                                        'filter_query': '{Units} is blank'
                                                                                    },
                                                                                    'backgroundColor': '#ffdbd8'
                                                                                },
                                                                            ],
                                                                            style_table={
                                                                                'overflowX': 'auto',
                                                                                'boxShadow': '2px 2px 8px rgba(0, 0, 0, 0.2)'
                                                                            },
                                                                            style_header={'padding': '6px', 'fontWeight': '700', 'textAlign': 'center', 'textDecoration': 'underline'},
                                                                            tooltip_header={'Ticker': 'Enter valid tickers of desired stocks', 'Units': 'Enter number of respective units as a whole number ≥1'},
                                                                            tooltip_duration=None,
                                                                            tooltip_delay=None,
                                                                            style_as_list_view=True
                                                                        )
                                                                    ]
                                                                ),
                                                                dmc.GridCol(
                                                                    span='content',
                                                                    children=[
                                                                        dmc.Stack(
                                                                            justify='center',
                                                                            gap='0',
                                                                            children=[
                                                                                dmc.Tooltip(
                                                                                    color='#fafafa',
                                                                                    withArrow=True,
                                                                                    arrowPosition='center',
                                                                                    arrowSize=8,
                                                                                    multiline=True,
                                                                                    label='Click to export the table.',
                                                                                    transitionProps={'transition':'pop-bottom-left', 'duration':200},
                                                                                    styles={'tooltip': {'color': '#000000', 'fontSize': '1rem'}},
                                                                                    children=[
                                                                                        dmc.ActionIcon(
                                                                                            id='export_table_button',
                                                                                            n_clicks=0,
                                                                                            variant='light',
                                                                                            style={'boxShadow': '1px 1px 4px rgba(0, 0, 0, 0.3)'},
                                                                                            children=[
                                                                                                DashIconify(icon='pajamas:export', style={'height':'2rem', 'width': '2rem'}),
                                                                                                dcc.Download(id='download_table_button')
                                                                                            ]
                                                                                        )                                                                                       
                                                                                    ]                                                                                    
                                                                                ),
                                                                                dcc.Upload(
                                                                                    id='import_table_button',
                                                                                    accept='.csv, .xlsx',
                                                                                    multiple=False,
                                                                                    max_size=1000000, #1MB
                                                                                    children=[
                                                                                        dmc.Tooltip(
                                                                                            color='#fafafa',
                                                                                            withArrow=True,
                                                                                            arrowPosition='center',
                                                                                            arrowSize=8,
                                                                                            multiline=True,
                                                                                            label='Click to select a file to import a table (csv, xlsl, xlx).',
                                                                                            transitionProps={'transition':'pop-bottom-left', 'duration':200},
                                                                                            styles={'tooltip': {'color': '#000000', 'fontSize': '1rem'}},
                                                                                            children=[
                                                                                                dmc.ActionIcon(
                                                                                                    n_clicks=0,
                                                                                                    variant='light',
                                                                                                    style={'boxShadow': '1px 1px 4px rgba(0, 0, 0, 0.3)'},
                                                                                                    children=[
                                                                                                        DashIconify(icon='pajamas:import', style={'height':'2rem', 'width': '2rem'})
                                                                                                    ]
                                                                                                )                                                                                        
                                                                                            ]                                                                                    
                                                                                        )
                                                                                    ]
                                                                                )
                                                                            ]
                                                                        )
                                                                    ]
                                                                ),
                                                                dmc.GridCol(
                                                                    span=2,
                                                                    children=[
                                                                        dmc.Button(
                                                                            id='run_analysis_button',
                                                                            children=['Run Analysis'],
                                                                            size='xl',
                                                                            style={'boxShadow': '2px 2px 8px rgba(0, 0, 0, 0.3)'},
                                                                            leftSection=DashIconify(icon='material-symbols-light:rocket-launch', style={'height':'2rem', 'width': '2rem'})
                                                                        )
                                                                    ]
                                                                )
                                                            ]
                                                        )
                                                    ]
                                                )
                                            ]
                                        )
                                    ]
                                ),
                                dmc.TabsPanel(
                                    value='tab-1',
                                    children=[
                                        dmc.Box(
                                            children=[
                                                dmc.Stack(
                                                    p='1rem',
                                                    gap='sm',
                                                    children=[
                                                        dmc.Grid(
                                                            style={'height':'100%'},
                                                            children=[
                                                                dmc.GridCol(
                                                                    span=6,
                                                                    style={'borderRight': '2px solid var(--mantine-color-blue-6)'},
                                                                    children=[
                                                                        dmc.Stack(
                                                                            style={'height':'100%'},
                                                                            children=[
                                                                                dmc.Box(
                                                                                    id='plot_1',
                                                                                    children=[
                                                                                        dmc.Skeleton(style={'height':'34rem'})
                                                                                    ]
                                                                                ),
                                                                                dmc.Divider(variant='solid', size='sm', color='blue', w='100%'),
                                                                                dmc.Group(
                                                                                    justify='center',
                                                                                    children=[
                                                                                        dmc.Badge('Portfolio vs S&P500', variant='dot', size='xl', style={'boxShadow': '2px 2px 8px rgba(0, 0, 0, 0.2)'}),
                                                                                        dmc.Button('Render Figure', id='btn_1', w='15rem', size='compact-xl', style={'boxShadow': '2px 2px 8px rgba(0, 0, 0, 0.3)'}, leftSection=DashIconify(icon='svg-spinners:gooey-balls-2', style={'height':'2rem', 'width': '2rem'})),
                                                                                        dmc.ScrollArea(dmc.Text(plot_1, c='black', style={'fontSize': '1rem', 'fontFamily': 'Roboto'}), h='3rem', w='15rem', type='hover', offsetScrollbars='y')
                                                                                    ]
                                                                                ),
                                                                                dmc.Divider(variant='solid', size='sm', color='blue', w='100%')
                                                                            ]
                                                                        )
                                                                    ]
                                                                ),
                                                                dmc.GridCol(
                                                                    span=6,
                                                                    children=[
                                                                        dmc.Stack(
                                                                            style={'height':'100%'},
                                                                            children=[
                                                                                dmc.Box(
                                                                                    id='plot_2',
                                                                                    children=[
                                                                                        dmc.Skeleton(style={'height':'34rem'}),
                                                                                    ]
                                                                                ),
                                                                                dmc.Divider(variant='solid', size='sm', color='blue', w='100%'),
                                                                                dmc.Group(
                                                                                    justify='center',
                                                                                    children=[
                                                                                        dmc.Badge('Returns Heatmap', variant='dot', size='xl', style={'boxShadow': '2px 2px 8px rgba(0, 0, 0, 0.2)'}),
                                                                                        dmc.Button('Render Figure', id='btn_2', w='15rem', size='compact-xl', style={'boxShadow': '2px 2px 8px rgba(0, 0, 0, 0.3)'}, leftSection=DashIconify(icon='svg-spinners:gooey-balls-2', style={'height':'2rem', 'width': '2rem'})),
                                                                                        dmc.ScrollArea(dmc.Text(plot_2, c='black', style={'fontSize': '1rem', 'fontFamily': 'Roboto'}), h='3rem', w='15rem', type='hover', offsetScrollbars='y')
                                                                                    ]
                                                                                ),
                                                                                dmc.Divider(variant='solid', size='sm', color='blue', w='100%')
                                                                            ]
                                                                        )
                                                                    ]
                                                                )
                                                            ]
                                                        ),
                                                        dmc.Grid(
                                                            style={'height':'100%'},
                                                            children=[
                                                                dmc.GridCol(
                                                                    span=6,
                                                                    style={'borderRight': '2px solid var(--mantine-color-blue-6)'},
                                                                    children=[
                                                                        dmc.Stack(
                                                                            style={'height':'100%'},
                                                                            children=[
                                                                                dmc.Box(
                                                                                    id='plot_3',
                                                                                    children=[
                                                                                        dmc.Skeleton(style={'height':'34rem'})
                                                                                    ]
                                                                                ),
                                                                                dmc.Divider(variant='solid', size='sm', color='blue', w='100%'),
                                                                                dmc.Group(
                                                                                    justify='center',
                                                                                    children=[
                                                                                        dmc.Badge('Bollinger Bands', variant='dot', size='xl', style={'boxShadow': '2px 2px 8px rgba(0, 0, 0, 0.2)'}),
                                                                                        dmc.Button('Render Figure', id='btn_3', w='15rem', size='compact-xl', style={'boxShadow': '2px 2px 8px rgba(0, 0, 0, 0.3)'}, leftSection=DashIconify(icon='svg-spinners:gooey-balls-2', style={'height':'2rem', 'width': '2rem'})),
                                                                                        dmc.ScrollArea(dmc.Text(plot_3, c='black', style={'fontSize': '1rem', 'fontFamily': 'Roboto'}), h='3rem', w='15rem', type='hover', offsetScrollbars='y')
                                                                                    ]
                                                                                ),
                                                                                dmc.Divider(variant='solid', size='sm', color='blue', w='100%')
                                                                            ]
                                                                        )
                                                                    ]
                                                                ),
                                                                dmc.GridCol(
                                                                    span=6,
                                                                    children=[
                                                                        dmc.Stack(
                                                                            style={'height':'100%'},
                                                                            children=[
                                                                                dmc.Box(
                                                                                    id='plot_4',
                                                                                    children=[
                                                                                        dmc.Skeleton(style={'height':'34rem'})
                                                                                    ]
                                                                                ),
                                                                                dmc.Divider(variant='solid', size='sm', color='blue', w='100%'),
                                                                                dmc.Group(
                                                                                    justify='center',
                                                                                    children=[
                                                                                        dmc.Badge('Spider Chart', variant='dot', size='xl', style={'boxShadow': '2px 2px 8px rgba(0, 0, 0, 0.2)'}),
                                                                                        dmc.Button('Render Figure', id='btn_4', w='15rem', size='compact-xl', style={'boxShadow': '2px 2px 8px rgba(0, 0, 0, 0.3)'}, leftSection=DashIconify(icon='svg-spinners:gooey-balls-2', style={'height':'2rem', 'width': '2rem'})),
                                                                                        dmc.ScrollArea(dmc.Text(plot_4, c='black', style={'fontSize': '1rem', 'fontFamily': 'Roboto'}), h='3rem', w='15rem', type='hover', offsetScrollbars='y')
                                                                                    ]
                                                                                ),
                                                                                dmc.Divider(variant='solid', size='sm', color='blue', w='100%')
                                                                            ]
                                                                        )
                                                                    ]
                                                                )
                                                            ]
                                                        ),
                                                        dmc.Grid(
                                                            style={'height':'100%'},
                                                            children=[
                                                                dmc.GridCol(
                                                                    span=6,
                                                                    style={'borderRight': '2px solid var(--mantine-color-blue-6)'},
                                                                    children=[
                                                                        dmc.Stack(
                                                                            style={'height':'100%'},
                                                                            children=[
                                                                                dmc.Box(
                                                                                    id='plot_5',
                                                                                    children=[
                                                                                        dmc.Skeleton(style={'height':'34rem'})
                                                                                    ]
                                                                                ),
                                                                                dmc.Divider(variant='solid', size='sm', color='blue', w='100%'),
                                                                                dmc.Group(
                                                                                    justify='center',
                                                                                    children=[
                                                                                        dmc.Badge('Value at Risk', variant='dot', size='xl', style={'boxShadow': '2px 2px 8px rgba(0, 0, 0, 0.2)'}),
                                                                                        dmc.Button('Render Figure', id='btn_5', w='15rem', size='compact-xl', style={'boxShadow': '2px 2px 8px rgba(0, 0, 0, 0.3)'}, leftSection=DashIconify(icon='svg-spinners:gooey-balls-2', style={'height':'2rem', 'width': '2rem'})),
                                                                                        dmc.ScrollArea(dmc.Text(plot_5, c='black', style={'fontSize': '1rem', 'fontFamily': 'Roboto'}), h='3rem', w='15rem', type='hover', offsetScrollbars='y')
                                                                                    ]
                                                                                ),
                                                                                dmc.Divider(variant='solid', size='sm', color='blue', w='100%')
                                                                            ]
                                                                        )
                                                                    ]
                                                                ),
                                                                dmc.GridCol(
                                                                    span=6,
                                                                    children=[
                                                                        dmc.Stack(
                                                                            style={'height':'100%'},
                                                                            children=[
                                                                                dmc.Box(
                                                                                    id='plot_6',
                                                                                    children=[
                                                                                        dmc.Skeleton(style={'height':'34rem'})
                                                                                    ]
                                                                                ),
                                                                                dmc.Divider(variant='solid', size='sm', color='blue', w='100%'),
                                                                                dmc.Group(
                                                                                    justify='center',
                                                                                    children=[
                                                                                        dmc.Badge('Correlation Heatmap', variant='dot', size='xl', style={'boxShadow': '2px 2px 8px rgba(0, 0, 0, 0.2)'}),
                                                                                        dmc.Button('Render Figure', id='btn_6', w='15rem', size='compact-xl', style={'boxShadow': '2px 2px 8px rgba(0, 0, 0, 0.3)'}, leftSection=DashIconify(icon='svg-spinners:gooey-balls-2', style={'height':'2rem', 'width': '2rem'})),
                                                                                        dmc.ScrollArea(dmc.Text(plot_6, c='black', style={'fontSize': '1rem', 'fontFamily': 'Roboto'}), h='3rem', w='15rem', type='hover', offsetScrollbars='y')
                                                                                    ]
                                                                                ),
                                                                                dmc.Divider(variant='solid', size='sm', color='blue', w='100%')
                                                                            ]
                                                                        )
                                                                    ]
                                                                )
                                                            ]
                                                        )
                                                    ]
                                                )
                                            ]
                                        )
                                    ]
                                ),   
                                dmc.TabsPanel(
                                    value='tab-2',
                                    children=[
                                        dmc.Box(
                                            children=[
                                                dmc.Stack(
                                                    style={'height':'100%'},
                                                    children=[
                                                        dmc.Box(
                                                            id='plot_7',
                                                            p={'base': '0.5rem', 'md': '1rem', 'lg': '1.5rem'},
                                                            children=[
                                                                dmc.Skeleton(
                                                                    style={'height':'55rem'}
                                                                )
                                                            ]
                                                        ),
                                                        dmc.Divider(variant='solid', size='sm', color='blue', w='100%'),
                                                        dmc.Group(
                                                            justify='center',
                                                            gap='xl',
                                                            my={'base': '0.5rem', 'md': '1rem', 'lg': '1.5rem'},
                                                            children=[
                                                                dmc.Group(
                                                                    children=[
                                                                        dmc.Text('# of days', c='grey'),
                                                                        dmc.Slider(id='n_days', color='blue', radius='lg', showLabelOnHover=True, min=10, max=200, step=1, size='lg', w='15rem', value=50, marks=[{'value': 40, 'label': '20%'}, {'value': 100, "label": '50%'},{'value': 160, 'label': '80%'}])
                                                                    ]
                                                                ),
                                                                dmc.Group(
                                                                    children=[
                                                                        dmc.Text('# of simulations', c='grey'),
                                                                        dmc.Slider(id='n_simulations', color='blue', radius='lg', showLabelOnHover=True, min=10, max=200, step=1, size='lg', w='15rem', value=50, marks=[{'value': 40, 'label': '20%'}, {'value': 100, "label": '50%'},{'value': 160, 'label': '80%'}])
                                                                    ]
                                                                ),
                                                                dmc.Badge('Monte Carlo Simulation', variant='dot', size='xl', style={'boxShadow': '2px 2px 8px rgba(0, 0, 0, 0.2)'}),
                                                                dmc.Button('Render Figure', id='btn_7', w='15rem', size='compact-xl', style={'boxShadow': '2px 2px 8px rgba(0, 0, 0, 0.3)'}, leftSection=DashIconify(icon='svg-spinners:gooey-balls-2', style={'height':'2rem', 'width': '2rem'})),
                                                                dmc.ScrollArea(dmc.Text(plot_7, c='black', style={'fontSize': '1rem', 'fontFamily': 'Roboto'}), h='4rem', w='15rem', type='hover', offsetScrollbars='y')
                                                            ]
                                                        )
                                                    ]
                                                )
                                            ]
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)			

#populate questions
@callback(
    Output('quiz_data', 'data'),
    Input('quiz_carousel', 'id')
)

def generate_slides(_):
    quiz_batch = sample(quiz, 3)
    return quiz_batch

@callback(
    Output('quiz_carousel', 'children'),
    Input('quiz_data', 'data')
)

def render_slides(quiz_batch):
    return [dmc.CarouselSlide(children=make_quiz_card(q), bg='blue') for q in quiz_batch]

#add row 
@callback(
    Output(component_id='ticker_unit_picker_table', component_property='data', allow_duplicate=True),
    Input(component_id='add_row_button', component_property='n_clicks'),
    State(component_id='ticker_unit_picker_table', component_property='data'),
    prevent_initial_call=True
)

def add_row(n_clicks, data):
    patched_rows = Patch()
    patched_rows.append({'Ticker': '', 'Units': None})
    return patched_rows

#clear table
@callback(
    Output(component_id='ticker_unit_picker_table', component_property='data', allow_duplicate=True),
    Input(component_id='clear_table_button', component_property='n_clicks'),
    prevent_initial_call=True
)

def clear_table(_):
    return []

#import table
@callback(
        Output(component_id='ticker_unit_picker_table', component_property='data'),
        Input(component_id='import_table_button', component_property='contents'),
        State(component_id='import_table_button', component_property='filename'),
        prevent_initial_call=True
)

def import_table(contents, filename):
    if contents is None:
        return []
    
    _, content_string = contents.split(',')
    decoded = b64decode(content_string)

    try:
        if filename.endswith('.csv'):
            df = pd.read_csv(StringIO(decoded.decode('utf-8')))
        elif filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(BytesIO(decoded))
        else:
            return []

        df = df[['Ticker', 'Units']]
        df['Ticker'] = df['Ticker'].astype(str)
        df['Units'] = pd.to_numeric(df['Units'], errors='coerce').fillna(0).astype('int')
        return df.to_dict(orient='records')

    except Exception as e:
        print(f"Error processing uploaded file: {e}")
        return []

#export table
@callback(
    Output(component_id='download_table_button', component_property='data'),
    Input(component_id='export_table_button', component_property='n_clicks'),
    State(component_id='ticker_unit_picker_table', component_property='data'),
    prevent_initial_call=True
)

def export_table(_, data_table):
    df=pd.DataFrame(data_table)
    return dcc.send_data_frame(df.to_excel, f'portfolio_togo_{datetime.now().date()}.xlsx', index=False, sheet_name='my_portfolio_togo')

#fetch data
@callback(
    Output(component_id='fetched_data_store', component_property='data'),
    Output(component_id='notification-container', component_property='children'),
    Input(component_id='run_analysis_button', component_property='n_clicks'),
    State(component_id='ticker_unit_picker_table', component_property='data'),
    State(component_id='date_picker_range', component_property='value'),
    prevent_initial_call=True,
)

def fetch_portfolio_data(_, data_table, date_range):
    if not data_table or not date_range:
        return None, dmc.Notification(
            radius='md',
            icon=DashIconify(icon='material-symbols:error-outline', style={'width':'3rem', 'height':'3rem', 'color': '#FF0000'}),
            title='Error!',
            withBorder=True,
            withCloseButton=True,
            message=f'Provide valid tickers and date range.',
            autoClose=5000,
            action='show',
            bg='white',
            styles={'icon': {'backgroundColor': 'white'}}
        )

    portfolio_data = {}
    errors=[]
    start_date, end_date = [str(i) for i in date_range]

    for row in data_table:
        ticker = str(row.get('Ticker')).strip().upper()
        units = row.get('Units')

        if not (ticker and units and units>0):
            errors.append(f'Invalid entry for {ticker if ticker else 'empty ticker'}')
            continue

        try:
            df = yf.Ticker(ticker).history(start=start_date, end=end_date)

            if df.empty:
                errors.append(f'No data found for {str(ticker)}')
                continue

            df = df[['Close']].reset_index()
            df['Date'] = df['Date'].dt.date.astype(str, errors='raise')
            units = int(units)

            portfolio_data[ticker] = {
                'units': units,
                'data': df.to_dict(orient='records')
            }
        except Exception as e:
            errors.append(f'Error fetching data for {str(ticker)}: {str(e)}')
    
    if errors:
        return None, dmc.Notification(
            radius='md',
            icon=DashIconify(icon='material-symbols:error-outline', style={'width':'3rem', 'height':'3rem', 'color': '#FF0000'}),
            title='Error!',
            withBorder=True,
            withCloseButton=True,
            message=f'Provide valid tickers and date range.',
            autoClose=5000,
            action='show',
            bg='white',
            styles={'icon': {'backgroundColor': 'white'}}
        )
    else: 
        return portfolio_data, dmc.Notification(
            radius='md',
            icon=DashIconify(icon='mdi:success-bold', style={'width':'3rem', 'height':'3rem', 'color': '#008000'}),
            title='Success!',
            withBorder=True,
            withCloseButton=True,
            message=f'Data has been fetched successfully.',
            autoClose=5000,
            action='show',
            bg='white',
            styles={'icon': {'backgroundColor': 'white'}}
        )

#graph 1
@callback(
    Output('S&P_data_store', 'data'),
    Output('plot_1', 'children'),
    Input('btn_1', 'n_clicks'),
    State('fetched_data_store', 'data'),
    State('date_picker_range', 'value'),
    prevent_initial_call=True
)

def returns_vs_spy(_, portfolio_data, date_range):
    
    start_date, end_date = [str(i) for i in date_range]
    df_list=[]
   
    for ticker, info in portfolio_data.items():
        units = info['units']
        data = pd.DataFrame(info['data'])
        data['Date']=pd.to_datetime(data['Date'])
        data.set_index('Date', inplace=True)
        data[ticker] = data['Close']*units
        df_list.append(data[[ticker]])

    portfolio_df = pd.concat(df_list, axis=1)
    portfolio_df['Portfolio'] = portfolio_df.sum(axis=1)

    spy_df = yf.download('SPY', start=start_date, end=end_date, progress=False)
    spy_df = spy_df[['Close']]
    spy_df.columns = ['S&P500']

    spy_store_df = spy_df.copy()
    spy_store_df = spy_df.reset_index()
    spy_store_df['Date'] = pd.to_datetime(spy_store_df['Date']).dt.strftime('%Y-%m-%d')
    spy_store_df = spy_store_df.to_dict('records')

    combined_df = portfolio_df[['Portfolio']].join(spy_df[['S&P500']], how='left')
    combined_df = combined_df.dropna()
    combined_df /= combined_df.iloc[0]
    combined_df = combined_df.reset_index()
    
    fig = px.line(combined_df, x='Date', y=['Portfolio', 'S&P500'],template='plotly_white', line_shape='spline')
    fig.update_layout(xaxis_title=None, yaxis_title=None, showlegend=False, margin=dict(t=10, l=10, r=10, b=10), height=544)
    fig.update_traces(line={'dash':'dot'}, selector={'name':'S&P500'})
    return spy_store_df, dcc.Graph(figure=fig)

#graph 2
@callback(
    Output('plot_2', 'children'),
    Input('btn_2', 'n_clicks'),
    State('fetched_data_store', 'data'),
    prevent_initial_call=True
)

def returns_heatmap(_, portfolio_data):

    unpack=[]
    weekdays=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

    for i, j in portfolio_data.items():
        for k in j['data']:
            unpack.append({
                'Ticker': i,
                'Date': pd.to_datetime(k['Date']),
                'Close': k['Close']
            }
        )

    df=pd.DataFrame(unpack)
    df.sort_values(by=['Ticker', 'Date'], inplace=True)
    df['Return']=df.groupby('Ticker')['Close'].pct_change()*100
    df.dropna(inplace=True)
    df['Weekday']=df['Date'].dt.day_name()

    heatmap_df=df.groupby(['Ticker', 'Weekday'])['Return'].mean() 
    heatmap_df = heatmap_df.reset_index()
    heatmap_df['Weekday']=pd.Categorical(heatmap_df['Weekday'], weekdays, ordered=True)
    heatmap_df = heatmap_df.pivot(index='Ticker', columns='Weekday', values='Return').copy()
    
    fig = px.imshow(heatmap_df, x=weekdays, y=heatmap_df.index, color_continuous_scale='RdYlGn', text_auto='.2f')
    fig.update_layout(xaxis_title=None, yaxis_title=None, margin=dict(t=10, l=10, r=10, b=10), height=544)
    fig.update_xaxes(side='top')
    return dcc.Graph(figure=fig)

#graph 3
@callback(
    Output('plot_3', 'children'),
    Input('btn_3', 'n_clicks'),
    State('fetched_data_store', 'data'),
    prevent_initial_call=True
)

def bollinger_bands(_, portfolio_data, window=10, _std=1):
    df_list=[]
    for i, j in portfolio_data.items():
        units = j['units']
        data = pd.DataFrame(j['data'])
        data['Date']=pd.to_datetime(data['Date'])
        data.set_index('Date', inplace=True)
        data[i]=data['Close']*units
        df_list.append(data[[i]])

    portfolio_df=pd.concat(df_list, axis=1)
    portfolio_df['Portfolio']=portfolio_df.sum(axis=1)
    portfolio_df=portfolio_df[['Portfolio']]
    portfolio_df = portfolio_df.ffill()
    portfolio_df['SMA']=portfolio_df['Portfolio'].rolling(window=window).mean()
    portfolio_df['STD']=portfolio_df['Portfolio'].rolling(window=window).std()
    portfolio_df['Upper']=portfolio_df['SMA'] + _std*portfolio_df['STD']
    portfolio_df['Lower']=portfolio_df['SMA'] - _std*portfolio_df['STD']
    portfolio_df = portfolio_df.reset_index()[['Date', 'Portfolio', 'SMA', 'Upper', 'Lower']]

    fig = px.line(portfolio_df, x='Date', y=['Portfolio', 'SMA', 'Upper', 'Lower'], template='plotly_white', line_shape='spline')
    fig.update_layout(xaxis_title=None, yaxis_title=None, showlegend=False, margin=dict(t=10, l=10, r=10, b=10), height=544)
    fig.update_traces(line={'dash':'dot'}, selector={'name':'SMA'})
    fig.update_traces(line={'color': 'green'}, selector={'name': 'Upper'})  
    fig.update_traces(line={'color': 'red'}, selector={'name': 'Lower'})
    fig.update_traces(line={'color': 'black'}, selector={'name': 'SMA'})
    return dcc.Graph(figure=fig)

#graph 4
@callback(
    Output('plot_4', 'children'),
    Input('btn_4', 'n_clicks'),
    State('fetched_data_store', 'data'),
    State('S&P_data_store', 'data'),
    prevent_initial_call=True
)

def spider_chart(_, portfolio_data, spy_store_df):
    df_list = []
    spy_store_df = pd.DataFrame(spy_store_df)
    spy_store_df = spy_store_df[['S&P500']]
    spy_store_df = spy_store_df[1:].ffill()
    for i, j in portfolio_data.items():
        units = j['units']
        data = pd.DataFrame(j['data'])
        data['Date']=pd.to_datetime(data['Date'])
        data.set_index('Date', inplace=True)
        data[i]=data['Close']*units
        df_list.append(data[[i]])

    portfolio_df=pd.concat(df_list, axis=1)
    portfolio_df['Portfolio']=portfolio_df.sum(axis=1)
    portfolio_df=portfolio_df[['Portfolio']]
    portfolio_df = portfolio_df.ffill()
    portfolio_df['Return'] = portfolio_df['Portfolio'].pct_change()
    portfolio_df = portfolio_df[1:]
    portfolio_df.reset_index(inplace=True)
    portfolio_df['Cummax'] = portfolio_df['Portfolio'].cummax()
    portfolio_df['Drawdown'] = (portfolio_df['Portfolio']-portfolio_df['Cummax']) / portfolio_df['Cummax']
    portfolio_df = portfolio_df[['Portfolio', 'Return', 'Drawdown']]

    _return = (portfolio_df['Portfolio'].iloc[-1] / portfolio_df['Portfolio'].iloc[0]) -1
    _std = portfolio_df['Return'].std()
    _downstd = portfolio_df[portfolio_df['Return'] < 0]['Return'].std()
    _maxdrawdown = portfolio_df['Drawdown'].min()
    _spy = (spy_store_df['S&P500'].iloc[-1] / spy_store_df['S&P500'].iloc[0]) - 1
    _alpha = _return - _spy
    stats = {'Return': _return, 'Volatility': _std, 'Downward STD': _downstd, 'Max Drawdown': _maxdrawdown, 'S&P500': _spy, 'Alpha': _alpha}
    line_polar = pd.DataFrame({'Stat' : list(stats.keys()), 'Value': list(stats.values())})
    fig = px.line_polar(line_polar, r='Value', theta='Stat', markers=True, line_close=True, template='ggplot2')
    fig.update_layout(margin=dict(t=20, l=20, r=20, b=20), height=544)
    fig.update_traces(fill='toself')
    fig.update_traces(line=dict(color='red', width=3), marker=dict(size=8, color='black'))
    return dcc.Graph(figure=fig)

#graph 5
@callback(
    Output('plot_5', 'children'),
    Input('btn_5', 'n_clicks'),
    State('fetched_data_store', 'data'),
    prevent_initial_call=True
)

def value_at_risk(_, portfolio_data):
    df_list = []
    for i, j in portfolio_data.items():
        units = j['units']
        data = pd.DataFrame(j['data'])
        data['Date']=pd.to_datetime(data['Date'])
        data.set_index('Date', inplace=True)
        data[i]=data['Close']*units
        df_list.append(data[[i]])

    portfolio_df=pd.concat(df_list, axis=1)
    portfolio_df['Value'] = portfolio_df.sum(axis=1)
    portfolio_df = portfolio_df[['Value']].pct_change().dropna()
    
    mu = portfolio_df['Value'].mean()
    sigma = portfolio_df['Value'].std()
    z_95 = 1.645
    z_99 = 2.326

    parametric_var_95 = (mu+z_95*sigma)*100
    parametric_var_99 = (mu+z_99*sigma)*100
    historic_var_95 = -np.percentile(portfolio_df['Value'], 5)*100
    historic_var_99 = -np.percentile(portfolio_df['Value'], 1)*100
    columns = {'Parametric (95%)': parametric_var_95, 'Parametric (99%)': parametric_var_99, 'Historic (95%)': historic_var_95, 'Historic (99%)': historic_var_99}
    df = pd.DataFrame([columns])
    long_df = df.melt(var_name='VaR Type', value_name='VaR (%)')
    
    fig = px.bar(long_df, x='VaR Type', y='VaR (%)', template='plotly_white', barmode='group')
    fig.update_layout(xaxis_title=None, yaxis_title=None, margin=dict(t=20, l=20, r=20, b=20), height=544)
    fig.update_traces(marker_color=['#A7C7E7', '#F2D8A7', '#F2DFEB', '#B0E0A8'], marker_line_color='rgb(8,48,107)', marker_line_width=1.5, opacity=0.6)
    return dcc.Graph(figure=fig)

#graph 6
@callback(
    Output('plot_6', 'children'),
    Input('btn_6', 'n_clicks'),
    State('fetched_data_store', 'data'),
    prevent_initial_call=True
)

def correlation_mtx(_, portfolio_data):
    df_list = []
    for i, j in portfolio_data.items():
        data = pd.DataFrame(j['data'])
        data[i]=data['Close'].pct_change()
        data = data[1:].reset_index()
        df_list.append(data[[i]])

    portfolio_ret = pd.concat(df_list, axis=1)
    correlation_mtx = portfolio_ret.corr()

    fig = px.imshow(correlation_mtx, color_continuous_scale='RdBu', range_color=[-1,1], text_auto='.2f')
    fig.update_layout(xaxis_title=None, yaxis_title=None, margin=dict(t=10, l=10, r=10, b=10), height=544)
    fig.update_xaxes(side='top')
    return dcc.Graph(figure=fig)

#plot 7
@callback(
    Output('plot_7', 'children'),
    Input('btn_7', 'n_clicks'),
    State('n_simulations', 'value'),
    State('n_days', 'value'),
    State('fetched_data_store', 'data'),
    prevent_initial_call=True
)

def monte_carlo(_, n_simulations, n_days, portfolio_data):
    df_list = []
    simulated_paths = pd.DataFrame()

    for i, j in portfolio_data.items():
        data = pd.DataFrame(j['data'])
        data[i]=data['Close']
        df_list.append(data[[i]])

    portfolio = pd.concat(df_list, axis=1)
    portfolio['Value'] = portfolio.sum(axis=1)
    portfolio['Ret'] = portfolio['Value'].pct_change()
    portfolio = portfolio[['Value', 'Ret']][1:]
    _mu = portfolio['Ret'].mean()
    _std = portfolio['Ret'].std()

    for i in range(n_simulations):
        simulated_path = np.random.normal(_mu, _std, n_days)
        simulated_path = (1+simulated_path).cumprod()
        simulated_path = pd.concat([pd.Series([1.0]), pd.Series(simulated_path)], ignore_index=True)
        simulated_paths[f'Sim_Path_{i+1}'] = simulated_path

    fig = px.line(simulated_paths, template='plotly_white')
    fig.update_layout(xaxis_title='Simulation Day', yaxis_title='Normalized Portfolio Value', margin=dict(t=10, l=10, r=10, b=10), showlegend=False, height=880)
    return dcc.Graph(figure=fig, style={'height': '100%', 'minHeight':'50vh'})


if __name__ == '__main__':
    app.run(debug=True)
