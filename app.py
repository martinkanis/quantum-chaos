from __future__ import annotations

import logging

from dash import Dash

from auth.login import HEALTH_PATH, install_login
from auth.settings import settings_from_environment
from edits.store import TextEdits, text_edit_store_from_environment
from ui.advantage_callbacks import register_advantage_callbacks
from ui.assistant_callbacks import register_assistant_callbacks
from ui.breadcrumbs import register_breadcrumb_callbacks
from ui.callbacks import register_callbacks
from ui.editable_text import EditablePages
from ui.gbs_callbacks import register_gbs_callbacks
from ui.knowledge_map_callbacks import register_knowledge_map_callbacks
from ui.layout import build_layout
from ui.lazy_pages import LAZY_PAGE_IDS, built_page, register_lazy_page_callbacks
from ui.navigation import register_navigation_callbacks
from ui.random_matrix_callbacks import register_random_matrix_callbacks
from ui.study_progress import register_study_progress_callbacks
from ui.text_edit_callbacks import register_text_edit_callbacks
from web.compression import install_compression
from web.lecture_slides import install_lecture_slides

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

app = Dash(__name__, title="Quantum Knowledge Base")
pages = EditablePages(TextEdits(text_edit_store_from_environment()), build_layout, built_page, LAZY_PAGE_IDS)
# A function, so that each page load gets the paragraphs with the current hand edits.
app.layout = pages.layout
register_navigation_callbacks(app)
register_lazy_page_callbacks(app, pages.page_children)
register_breadcrumb_callbacks(app)
register_callbacks(app)
register_gbs_callbacks(app)
register_advantage_callbacks(app)
register_random_matrix_callbacks(app)
register_study_progress_callbacks(app)
register_knowledge_map_callbacks(app)
register_assistant_callbacks(app)
register_text_edit_callbacks(app, pages)

server = app.server
install_login(server, settings_from_environment())
install_compression(server)
install_lecture_slides(server)


@server.route(HEALTH_PATH)
def health() -> str:
    return "ok"


if __name__ == "__main__":
    # The local debug server runs on plain HTTP, where browsers would drop a Secure cookie.
    server.config["SESSION_COOKIE_SECURE"] = False
    app.run(debug=True)
