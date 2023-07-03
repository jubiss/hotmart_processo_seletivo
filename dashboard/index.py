from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from apps import page1
# Connect to main app.py file
from app import app
# from app import server
# from apps import page1, page2

def navbar_():
    """
    Creates a navigation bar component with logo and navigation links.

    Returns:
        dbc.Navbar: Navigation bar component.
    """
    logo_square = 'https://yt3.googleusercontent.com/KhdnfdgHlj2lUDKnWGMiKSTy8irLNg3FQALtiQKy6DJLJ2vEBujm6Tw8JItOOta2OCP3xi7QFQ=s176-c-k-c0x00ffffff-no-rj'

    navbar = dbc.Navbar(
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=logo_square, width='80'), width=1), #Logo Column
                        dbc.Col(
                            dbc.Nav(
                                [
                                    dbc.NavItem(dbc.NavLink("Visão Geral", href="/")), # Navigation Link page 1
                                    dbc.NavItem(dbc.NavLink("Estoque", href="/Estoque")), # Navigation Link page 2
                                    dbc.NavItem(dbc.NavLink("Profiling_report", href="Profiling_report"))
                                ],
                                navbar=True,
                                className="justify-content-end",
                            ),
                            style={'align': 'right'},
                            width=9,
                        ),
                    ],
                    #align="center",
                    #className="justify-content-between",  # Added justify-content-between class
                    style={'width': '100%'}
                ),
            ],
        fluid=True),
        color="#ff4e1a",
        dark=True,
        className='mb-5',
    )
    return navbar

def pandas_profiling_layout():
    """
    Creates a layout component for displaying the PandasProfiling report.

    Returns:
        html.Div: Layout component for the PandasProfiling report page.
    """
    return html.Div(
        [
            dcc.Markdown(
                '''
                # PandasProfiling Report
                
                The following is the PandasProfiling report for your data:
                '''
            ),
            html.Iframe(
                src='/assets/viva_report.html',
                style={'width': '100%', 'height': '800px'}
            )
        ]
    )

app.layout = html.Div([
    navbar_(), # Navbar component
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content') # Placeholder div for page content
])

@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    """
    Determines the content to display based on the current URL pathname.

    Args:
        pathname (str): Current URL pathname.

    Returns:
        str or dash.Dash: Layout of the selected page or "404 Page not found" message.
    """
    if pathname == '/':
        return page1.layout
    elif pathname == '/Estoque':
        return # page2.layout
    elif pathname == '/Profiling_report':
        return #pandas_profiling_layout()
    else:
        return #'404 Page not found'

if __name__ == '__main__':
    app.run_server(debug=True)