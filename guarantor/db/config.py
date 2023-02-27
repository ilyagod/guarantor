from typing import List

from guarantor.settings import settings

MODELS_MODULES: List[str] = [
    "guarantor.db.models.api_client",
    "guarantor.db.models.deal",
]  # noqa: WPS407

TORTOISE_CONFIG = {  # noqa: WPS407
    "connections": {
        "default": str(settings.db_url),
    },
    "apps": {
        "models": {
            "models": MODELS_MODULES + ["aerich.models"],
            "default_connection": "default",
        },
    },
}
