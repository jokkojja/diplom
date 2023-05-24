import dash_bootstrap_components as dbc
from dash import html


def navbar(user=None):
    brand_link = "/"
    if user is None:
        brand_link = ''
        navbar_children = [
            dbc.NavItem([user]),
        ]
    else:
        navbar_children = [
            dbc.NavItem(dbc.NavLink(html.I(className="bi bi-person-circle"), href="", style={'paddingRight': '0px'})),
            dbc.DropdownMenu(nav=True, in_navbar=True, label=user,
                             children=[
                                       dbc.DropdownMenuItem('Log out', href='/login', id="logout_id", external_link=True)]),
        ]   
    navbar_block = dbc.NavbarSimple(
        children=navbar_children,
        brand="Wawe Calculator",
        color="lightgrey",
        brand_href=brand_link,
        brand_external_link=True,
        sticky="top",
        style={'marginBottom': '20px'}
    )
    return navbar_block