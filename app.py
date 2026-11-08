from __future__ import annotations

import logging

from dash import Dash

from assistant.lecture_requests import lecture_request_store_from_environment
from auth.login import HEALTH_PATH, install_login
from auth.settings import settings_from_environment
from edits.store import TextEdits, text_edit_store_from_environment
from ui.advantage_callbacks import register_advantage_callbacks
from ui.assistant_callbacks import register_assistant_callbacks
from ui.breadcrumbs import register_breadcrumb_callbacks
from ui.callbacks import register_callbacks
from ui.chip_bench_callbacks import register_chip_bench_callbacks
from ui.chip_interaction_callbacks import register_chip_interaction_callbacks
from ui.chip_sampling_callbacks import register_chip_sampling_callbacks
from ui.chip_simulator_callbacks import register_chip_simulator_callbacks
from ui.editable_text import EditablePages
from ui.gbs_callbacks import register_gbs_callbacks
from ui.knowledge_map_callbacks import register_knowledge_map_callbacks
from ui.layout import build_layout
from ui.lazy_pages import LAZY_PAGE_IDS, built_page, register_lazy_page_callbacks
from ui.lecture_requests_callbacks import register_lecture_request_callbacks
from ui.navigation import register_navigation_callbacks
from ui.photon_loss_callbacks import register_photon_loss_callbacks
from ui.random_matrix_callbacks import register_random_matrix_callbacks
from ui.study_progress import register_study_progress_callbacks
from ui.text_edit_callbacks import register_text_edit_callbacks
from web.compression import install_compression
from web.lecture_queue_api import API_PREFIX as LECTURE_API_PREFIX, install_lecture_queue_api
from web.lecture_slides import install_lecture_slides
from web.offline import install_offline

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

app = Dash(__name__, title="Quantum Knowledge Base")
lecture_requests = lecture_request_store_from_environment()
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
register_photon_loss_callbacks(app)
register_chip_simulator_callbacks(app)
register_chip_interaction_callbacks(app)
register_chip_bench_callbacks(app)
register_chip_sampling_callbacks(app)
register_study_progress_callbacks(app)
register_knowledge_map_callbacks(app)
register_assistant_callbacks(app)
register_lecture_request_callbacks(app, lecture_requests)
register_text_edit_callbacks(app, pages)

server = app.server
install_login(server, settings_from_environment(), token_protected_prefixes=(LECTURE_API_PREFIX,))
install_compression(server)
install_lecture_slides(server)
install_lecture_queue_api(server, lecture_requests)
install_offline(app)


@server.route(HEALTH_PATH)
def health() -> str:
    return "ok"


if __name__ == "__main__":
    # The local debug server runs on plain HTTP, where browsers would drop a Secure cookie.
    server.config["SESSION_COOKIE_SECURE"] = False
    app.run(debug=True)
