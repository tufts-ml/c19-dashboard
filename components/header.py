import dash_html_components as html


def header_panel() -> html.Div:
    """
    Creates the header panel of dashboard.
    :return: The header panel. Never None.
    """
    return html.Div(className='row', children=[html.Div(className='column', children=[
        html.H2(children='COVID-19 Forecast for TMC (Experimental Draft)')
    ])])
