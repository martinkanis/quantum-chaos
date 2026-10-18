from __future__ import annotations

import logging

from dash import Dash

from ui.advantage_callbacks import register_advantage_callbacks
from ui.breadcrumbs import register_breadcrumb_callbacks
from ui.callbacks import register_callbacks
from ui.gbs_callbacks import register_gbs_callbacks
from ui.layout import build_layout
from ui.navigation import register_navigation_callbacks
from ui.random_matrix_callbacks import register_random_matrix_callbacks
from ui.study_progress import register_study_progress_callbacks

HEALTH_ENDPOINT = "/healthz"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

app = Dash(__name__, title="Monte Carlo portfolio")
app.layout = build_layout()
register_navigation_callbacks(app)
register_breadcrumb_callbacks(app)
register_callbacks(app)
register_gbs_callbacks(app)
register_advantage_callbacks(app)
register_random_matrix_callbacks(app)
register_study_progress_callbacks(app)

server = app.server


@server.route(HEALTH_ENDPOINT)
def health() -> str:
    return "ok"


if __name__ == "__main__":
    app.run(debug=True)
