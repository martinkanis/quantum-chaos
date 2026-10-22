from __future__ import annotations

import logging

from dash import Dash

from auth.login import HEALTH_PATH, install_login
from auth.settings import settings_from_environment
from ui.advantage_callbacks import register_advantage_callbacks
from ui.breadcrumbs import register_breadcrumb_callbacks
from ui.callbacks import register_callbacks
from ui.gbs_callbacks import register_gbs_callbacks
from ui.knowledge_map_callbacks import register_knowledge_map_callbacks
from ui.layout import build_layout
from ui.navigation import register_navigation_callbacks
from ui.random_matrix_callbacks import register_random_matrix_callbacks
from ui.study_progress import register_study_progress_callbacks

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
register_knowledge_map_callbacks(app)

server = app.server
install_login(server, settings_from_environment())


@server.route(HEALTH_PATH)
def health() -> str:
    return "ok"


if __name__ == "__main__":
    # The local debug server runs on plain HTTP, where browsers would drop a Secure cookie.
    server.config["SESSION_COOKIE_SECURE"] = False
    app.run(debug=True)
