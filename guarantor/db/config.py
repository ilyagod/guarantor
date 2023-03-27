from typing import List

from guarantor.settings import settings

MODELS_MODULES: List[str] = [
    "guarantor.db.models.user",
    "guarantor.db.models.deal",
    "guarantor.db.models.dispute",
    "guarantor.db.models.payment_gateway",
    "guarantor.db.models.payment",
    "guarantor.db.models.user_correct",
    "guarantor.db.models.tron_wallet",
    "guarantor.db.models.chat_message",
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
