'''
                dmc.AppShellHeader(
                    style={
                        'display':'flex',
                        'alignItems': 'center',
                        'justifyContent': 'space-between',
                        'padding': '0 1.5rem',
                        'backgroundColor': 'var(--mantine-color-blue-6)'
                    },
                    children=[
                        dmc.Tooltip(
                            label='This is you and only you.',
                            color='#fafafa',
                            withArrow=True,
                            arrowPosition='center',
                            arrowSize=8,
                            multiline=True,
                            transitionProps={'transition':'pop-bottom-left', 'duration':100},
                            styles={'tooltip': {'color': '#000000', 'fontSize': '0.7rem'}},
                            openDelay=1000,
                            children=[
                                DashIconify(
                                    icon='carbon:user-avatar-filled', style={'width':'3rem', 'height':'3rem', 'color':'white', 'marginTop': '0.5rem'}
                                )
                            ]
                        ),
                        dmc.Box(
                            style={'flexGrow': 1, 'textAlign': 'center'},
                            children=[
                                dmc.Text(
                                    'Portfolio ToGo',
                                    variant='gradient',
                                    gradient={'from': 'gray.5', 'to': 'white', 'deg': '180'},
                                    style={
                                        'fontFamily': 'Roboto', 
                                        'fontSize': '3.5rem', 
                                        'fontWeight': '700'
                                    }
                                )                                
                            ]
                        ),
                        dmc.Tooltip(
                            label='This burger unfortunately does not do anything.',
                            color='#fafafa',
                            withArrow=True,
                            arrowPosition='center',
                            arrowSize=8,
                            multiline=True,
                            transitionProps={'transition':'pop-bottom-left', 'duration':100},
                            styles={'tooltip': {'color': '#000000', 'fontSize': '0.7rem'}},
                            openDelay=1000,
                            children=[
                                dmc.Burger(
                                    style={'width': '3rem', 'height': '3rem', 'color': 'white'}
                                )
                            ]
                        )
                    ]
                )
'''
'''
                                                dmc.Group(
                                                    justify='center',
                                                    align='baseline',
                                                    bg='var(--mantine-color-blue-6)',
                                                    h={'base': '2rem', 'md': '2rem', 'lg': '2rem'},
                                                    px='1rem',
                                                    style={"marginTop": "auto"},
                                                    children=[
                                                        dmc.Title(
                                                            'Disclaimer: This tool is for educational purposes only and does not constitute investment advice.',
                                                            order=5,
                                                            textWrap='wrap',
                                                            style={'fontFamily': 'Roboto', 'fontWeight': '700', 'color':'white'}
                                                        )
                                                    ]
                                                )
'''