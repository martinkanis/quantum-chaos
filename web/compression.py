"""Gzip for text responses: the hosting proxy passes them on uncompressed, and Plotly alone is 4.7 MB of JavaScript."""

from __future__ import annotations

import gzip
from http import HTTPStatus

from flask import Flask, Response, request

COMPRESSIBLE_MIMETYPES = frozenset({
    "application/javascript",
    "application/json",
    "image/svg+xml",
    "text/css",
    "text/html",
    "text/javascript",
    "text/plain",
})
MIN_COMPRESSED_SIZE = 1024
"""Bytes; below this the gzip overhead and the CPU time outweigh the saving."""
COMPRESSION_LEVEL = 6
"""Zlib's default trade-off between size and speed."""
GZIP = "gzip"


def install_compression(server: Flask) -> None:
    server.after_request(compress_response)


def compress_response(response: Response) -> Response:
    if not _should_compress(response):
        return response
    # Static files are sent straight from disk; reading them here lets their content be compressed too.
    response.direct_passthrough = False
    response.set_data(gzip.compress(response.get_data(), compresslevel=COMPRESSION_LEVEL))
    response.headers["Content-Encoding"] = GZIP
    response.vary.add("Accept-Encoding")
    _weaken_etag(response)
    return response


def _should_compress(response: Response) -> bool:
    accepts_gzip = request.accept_encodings[GZIP] > 0
    is_large_text = (
        response.mimetype in COMPRESSIBLE_MIMETYPES
        and response.content_length is not None
        and response.content_length >= MIN_COMPRESSED_SIZE
    )
    is_plain_success = response.status_code == HTTPStatus.OK and "Content-Encoding" not in response.headers
    return accepts_gzip and is_large_text and is_plain_success


def _weaken_etag(response: Response) -> None:
    """The compressed bytes differ from the original, so a strong validator would no longer be true."""
    etag, is_weak = response.get_etag()
    if etag and not is_weak:
        response.set_etag(etag, weak=True)
