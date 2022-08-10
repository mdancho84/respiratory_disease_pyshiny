from pathlib import Path
from shiny import App, ui, reactive, Session

from modules import map, plot
from utils.helper_text import info_modal

app_ui = ui.page_bootstrap(
    ui.tags.head(
        ui.tags.link(rel="stylesheet", type="text/css", href="style.css"),
        ui.tags.script(src="index.js"),

        # PWA Support
        ui.tags.script("""
            $('head').append('<link rel="manifest" href="pwa/manifest.json"/>');

            if('serviceWorker' in navigator) {
              navigator.serviceWorker
                .register('/respiratory_disease_pyshiny/pwa-service-worker.js', { scope: '/respiratory_disease_pyshiny/' })
                .then(function() { console.log('Service Worker Registered'); });
            }
        """),
        ui.tags.link(rel="apple-touch-icon", href="pwa/icon.png"),

        ui.tags.meta(name="description", content="Respiratory Disease PyShiny"),
        ui.tags.meta(name="theme-color", content="#000000"),
        ui.tags.meta(name="apple-mobile-web-app-status-bar-style", content="#000000"),
        ui.tags.meta(name="apple-mobile-web-app-capable", content="yes"),
    ),
    # top navbar
    ui.tags.div(
        ui.row(
            ui.column(
                2,
                ui.tags.div(
                    ui.tags.a(
                        ui.tags.img(
                            src="static/img/appsilon-logo.png", height="50px"
                        ),
                        href="https://demo.appsilon.com/",
                    ),
                    id="logo-top",
                ),
            ),
            ui.column(2),
            ui.column(
                2,
                ui.tags.div(
                    ui.tags.div(
                        ui.input_action_button(
                            id="tab_map",
                            label="Map",
                            class_="navbar-button",
                        ),
                        id="div-navbar-map",
                    ),
                    ui.tags.div(
                        ui.input_action_button(
                            id="tab_plot",
                            label="Graphs",
                            class_="navbar-button",
                        ),
                        id="div-navbar-plot",
                    ),
                    id="div-navbar-tabs",
                ),
            ),
            ui.column(3),
            ui.column(
                2,
                ui.tags.div(
                    ui.input_switch(
                        id="dataset", label="Dataset Select", value=True
                    ),
                    id="div-navbar-selector",
                ),
            ),
            ui.column(
                1,
                ui.tags.div(
                    ui.input_action_button(
                        id="info_icon",
                        label=None,
                        icon=ui.tags.i(class_="glyphicon glyphicon-info-sign"),
                        class_="navbar-info",
                    )
                ),
            ),
        ),
        id="div-navbar",
        class_="navbar-top",
    ),
    # main area
    ui.tags.div(map.map_ui("map"), id="map-container"),
    ui.tags.div(plot.plot_ui("plot"), id="plot-container"),
    title="Respiratory Disease App",
)


def server(input, output, session: Session):

    info_modal()

    @reactive.Effect
    @reactive.event(input.info_icon)
    def _():
        info_modal()

    @reactive.Calc
    def is_wb_data():
        return input.dataset()

    map.map_server("map", is_wb_data)
    plot.plot_server("plot", is_wb_data)

    @reactive.Effect
    @reactive.event(input.tab_map)
    async def _():
        await session.send_custom_message(
            "toggleActiveTab", {"activeTab": "map"}
        )

    @reactive.Effect
    @reactive.event(input.tab_plot)
    async def _():
        await session.send_custom_message(
            "toggleActiveTab", {"activeTab": "plot"}
        )


www_dir = Path(__file__).parent / "www"
app = App(app_ui, server, static_assets=www_dir)
