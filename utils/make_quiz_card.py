import dash_mantine_components as dmc
from dash import Input, Output, State, callback, ctx, ALL, no_update
from uuid import uuid4
from dash_iconify import DashIconify

def make_quiz_card(q):
    question = q['question']
    choices = q['choices']
    answer = q['answer']
    explanation = q['explanation']
    answer_buttons = []
    unique_id = str(uuid4())

    for i, j in enumerate(choices):
        if j == answer:
            button = dmc.Box(
                children=[
                    dmc.Modal(
                        id={'type': 'modal', 'id': f'modal-correct-{unique_id}-{i}'},
                        centered=True,
                        children=[
                            dmc.Stack(
                                children=[
                                    dmc.Divider(variant='solid', size='sm', color='var(--mantine-color-blue-6)', w='100%'),
                                    dmc.Alert(
                                        w='100%',
                                        h='100%',
                                        color='var(--mantine-color-blue-6)',
                                        radius='sm',
                                        hide=False,
                                        children=[
                                            dmc.Group(
                                                justify='center',
                                                children=[
                                                    DashIconify(icon='material-symbols:check', style={'height':'4rem', 'width': '4rem', 'color': 'var(--mantine-color-blue-6)'}),
                                                    dmc.Text('Right!', c='var(--mantine-color-blue-6)', style={'fontSize':'1.5rem', 'fontWeight':'500'})
                                                ]
                                            )
                                        ]
                                    ),
                                    dmc.Divider(variant='solid', size='sm', color='var(--mantine-color-blue-6)', w='100%'),
                                    dmc.Alert(
                                        w='100%',
                                        h='100%',
                                        color='var(--mantine-color-blue-6)',
                                        radius='sm',
                                        hide=False,
                                        children=[
                                            dmc.Group(
                                                justify='center',
                                                children=[
                                                    dmc.Text(explanation, c='var(--mantine-color-blue-6)', ta='center', style={'fontSize':'1rem'})
                                                ]
                                            )
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),
                    dmc.Button(
                        j, 
                        id={'type': 'button', 'id': f'btn-correct-{unique_id}-{i}'},
                        style={'fontSize': '1rem', 'fontFamily': 'Roboto', 'borderColor': 'var(--mantine-color-blue-5)', 'boxShadow': '2px 2px 8px rgba(0, 0, 0, 0.2)'}
                    )
                ]
            )
        else:
            button = dmc.Box(
                children=[
                    dmc.Modal(
                        id={'type': 'modal', 'id': f'modal-wrong-{unique_id}-{i}'},
                        styles={'header': {'paddingTop': '0rem', 'paddingBottom': '0rem'}},
                        centered=True,
                        children=[
                            dmc.Stack(
                                children=[
                                    dmc.Divider(variant='solid', size='sm', color='#FF0000', w='100%'),
                                    dmc.Alert(
                                        w='100%',
                                        h='100%',
                                        color='#FF0000',
                                        radius='sm',
                                        hide=False,
                                        children=[
                                            dmc.Group(
                                                justify='center',
                                                children=[
                                                    DashIconify(icon='mdi:stop-remove-outline', style={'height':'4rem', 'width': '4rem', 'color': '#FF0000'}),
                                                    dmc.Text('Wrong!', c='#FF0000', style={'fontSize':'1.5rem', 'fontWeight':'500'})
                                                ]
                                            )
                                        ]
                                    ),
                                    dmc.Divider(variant='solid', size='sm', color='#FF0000', w='100%')
                                ]
                            )
                        ]
                    ),
                    dmc.Button(
                        j, 
                        id={'type': 'button', 'id': f'btn-wrong-{unique_id}-{i}'}, 
                        style={'fontSize': '1rem', 'fontFamily': 'Roboto', 'borderColor': 'var(--mantine-color-blue-5)', 'boxShadow': '2px 2px 8px rgba(0, 0, 0, 0.2)'}
                    )
                ]
            )
        answer_buttons.append(button)

    slide = dmc.Box(
        mx='3rem',
        my='2rem',
        children=[
            dmc.Stack(
                justify='center',
                align='center',
                gap='0',
                children=[
                    dmc.Text(question, ta='center', my='0rem', c='white', style={'fontSize': '1.25rem', 'fontFamily': 'Roboto'}),
                    dmc.Divider(label='Answer Choices', labelPosition='center', variant='solid', size='sm', color='white', w='100%', my='0rem', mt='0rem', mb='0.4rem', styles={'label': {'color':'white'}}),
                    dmc.Group(gap='xs', justify='center', children=[dmc.Box(i) for i in answer_buttons])
                ]
            )
        ]
    )
    return slide

@callback(
    Output({'type': 'modal', 'id': ALL}, 'opened'),
    Input({'type': 'button', 'id': ALL}, 'n_clicks'),
    State({'type': 'modal', 'id': ALL}, 'id'),
    prevent_initial_call=True
)
def toggle_modal(_, modal_ids):
    if not ctx.triggered_id:
        return [no_update] * len(modal_ids)

    triggered_id = ctx.triggered_id 
    triggered_btn_id = triggered_id['id'].replace('btn-', 'modal-')

    opened = []
    opened = [modal['id'] == triggered_btn_id for modal in modal_ids]
    return opened