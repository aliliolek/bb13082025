"""Utilities to create and run the Telegram bot."""

from __future__ import annotations

import logging
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

from .config import BotSettings
from . import handlers
from ..controller import AppController

logger = logging.getLogger(__name__)


async def _error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.exception("Unhandled exception: %s", context.error)


def create_application(
    controller: AppController, settings: BotSettings | None = None
) -> Application:
    """Create and configure the Telegram application."""
    settings = settings or BotSettings.from_env()
    application = ApplicationBuilder().token(settings.token).build()
    application.bot_data["controller"] = controller
    application.bot_data["admin_id"] = settings.admin_id

    application.add_handler(CommandHandler("start", handlers.start))
    application.add_handler(CommandHandler("stop", handlers.stop))
    application.add_handler(CommandHandler("status", handlers.status))
    application.add_error_handler(_error_handler)
    return application


def run_bot(controller: AppController, settings: BotSettings | None = None) -> None:
    """Run the bot using polling."""
    application = create_application(controller, settings)
    logger.info("Bot starting polling")
    application.run_polling()
