"""Which build this process is compiling.

GitHub Pages sets ``REFLEX_FRONTEND_PATH=/Plato5`` and gets a static frontend.
Local ``reflex run`` and the Azure export leave that variable unset and keep
the Python backend on ``/``.
"""

import os

STATIC = bool(os.environ.get("REFLEX_FRONTEND_PATH", "").strip("/"))
