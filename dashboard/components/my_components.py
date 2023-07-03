import dash_bootstrap_components as dbc
from dash import html, dash_table, dcc
text_font_size = '18px'
def input_top_label(id, label, value, type="number"):
    """
    Create a container with a labeled input field on top.

    Args:
        id (str): The ID of the input field.
        label (str): The label for the input field.
        value: The initial value of the input field.

    Returns:
        dbc.Container: A container with the labeled input field.
    """
    input_label = dbc.Container(
            [
            dbc.Row(dbc.Label(label, 
                              size="md",
                              style={'font-size': text_font_size}),),
            dbc.Row(dbc.Input(
                    id=id,
                    value=value,
                    type=type,
                    #min=0,
                    #max=300,
                    # className="form-control",
                    style={'width': '150px',
                           'font-size': text_font_size}))
            ]
            )
    return input_label

def centered_table(id, width, table_title=None):
    """
    Create a centered table.

    Args:
        id (str): The ID of the table.
        width (int): The width of the table.
        table_title (str, optional): The title of the table. Defaults to None.

    Returns:
        dbc.Row: A row containing the centered table.
    """
    if table_title:
        table = dbc.Row(
                dbc.Col([
                html.H2(table_title, style={'justify': 'center', 'alight': 'center'}),
                dash_table.DataTable(
                        id=id,
                        data=[],
                        columns=[],
                        editable=True,
                        sort_action="native",
                        page_action="native",
                        page_current= 0,
                        page_size= 10,
                        style_table={'height': '350px', 'overflowY': 'auto'},
                        style_data={
                                'font-family': 'Arial, sans-serif',
                                'font-size': '17px',
                                'text-align': 'left',
                                },
                        style_header={
                                'font-family': 'Arial, sans-serif',
                                'font-weight': 'bold',
                                'background-color': 'lightgray',
                                'border': '1px solid black',
                                'text-align': 'left',
                                'font-size': text_font_size
                                },
                        style_cell={
                                'border': '1px solid grey',
                                'padding': '5px',
                                },
                        
                        )],
                        width=width,
                ),
                justify='center',
                )
    else:
        table = dbc.Row(
                dbc.Col([
                dash_table.DataTable(
                        id=id,
                        data=[],
                        columns=[],
                        editable=True,
                        sort_action="native",
                        page_action="native",
                        page_current= 0,
                        page_size= 10,
                        style_table={'height': '350px', 'overflowY': 'auto'},
                        style_data={
                                'font-family': 'Arial, sans-serif',
                                'font-size': '17px',
                                'text-align': 'left',
                                },
                        style_header={
                                'font-weight': 'bold',
                                'background-color': 'lightgray',
                                'border': '1px solid black',
                                'text-align': 'left',
                                'font-size': text_font_size
                                },
                        style_cell={
                                'border': '1px solid grey',
                                'padding': '5px',
                                },
                        
                        )],
                        width=width,
                ),
                justify='center',
                )
    return table

def indicator_card(id, width):
    """
    Create an indicator card with a graph.

    Args:
        id (str): The ID of the graph.
        width (int): The width of the card.

    Returns:
        dbc.Col: A column containing the indicator card.
    """
    indicator= dbc.Col(
                dbc.Card(
                        dbc.CardBody(
                        dcc.Graph(figure={}, id=id),
                        className='text-center',
                        style={'padding':0},
                        ),
                        color='#ff4e1a',
                        inverse=True,
                        className='mb-4',
                        style={'padding':0}
                ),
                width=width,
                className="d-flex align-items-center justify-content-center"
                )
    return indicator

def create_slider(id, width, label, value):
    slider = dbc.Row(dbc.Label(label, 
                               size='md',
                               style={'font-size': text_font_size}),
        dcc.Slider(min=1, max=99, step=5, value=value, id=id)
    )


def create_indicator(value, title):
    color = '#e6e1df'
    indicator = go.Figure(go.Indicator(
        mode="number",
        value=value,
        title={
            'text': title,
            'font': {'color': color}
        },
        number={
            'font': {'color': color}
        }
    ))
    indicator.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",  # Set the plot background color to transparent
        paper_bgcolor="rgba(0,0,0,0)"  # Set the paper (plot area) background color to transparent
        )
    return indicator