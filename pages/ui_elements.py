import marimo as mo

def nav_menu():
    return mo.nav_menu( { "/": "Home",
                   "/viewer": "Viewer",
                   "/settings": "Settings",
                   "/about": "About",
                    "Links": { "https://twitter.com/marimo_io": "Twitter", 
                               "https://github.com/marimo-team/marimo": "GitHub", }, },
                               orientation="horizontal", )