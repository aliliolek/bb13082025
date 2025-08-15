"""Command handlers for the Telegram bot."""

from __future__ import annotations

import logging
from telegram import Update
from telegram.ext import ContextTypes

from ..controller import AppController

logger = logging.getLogger(__name__)


def _controller(context: ContextTypes.DEFAULT_TYPE) -> AppController:
    controller = context.application.bot_data.get("controller")
    if not isinstance(controller, AppController):
        raise RuntimeError("Controller is not configured")
    return controller


def _is_authorized(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    admin_id = context.application.bot_data.get("admin_id")
    user = update.effective_user
    return user is not None and admin_id == user.id


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command."""
    if not _is_authorized(update, context):
        await update.effective_message.reply_text("Unauthorized")
        logger.warning("Unauthorized /start attempt by user %s", update.effective_user)
        return
    controller = _controller(context)
    try:
        status = controller.start()
        await update.effective_message.reply_text(f"Application is {status.state.value}.")
    except Exception:
        logger.exception("Error handling /start")
        await update.effective_message.reply_text("Failed to start the application.")


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /stop command."""
    if not _is_authorized(update, context):
        await update.effective_message.reply_text("Unauthorized")
        logger.warning("Unauthorized /stop attempt by user %s", update.effective_user)
        return
    controller = _controller(context)
    try:
        status = controller.stop()
        await update.effective_message.reply_text(f"Application is {status.state.value}.")
    except Exception:
        logger.exception("Error handling /stop")
        await update.effective_message.reply_text("Failed to stop the application.")


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /status command."""
    if not _is_authorized(update, context):
        await update.effective_message.reply_text("Unauthorized")
        logger.warning("Unauthorized /status attempt by user %s", update.effective_user)
        return
    controller = _controller(context)
    try:
        status = controller.status()
        await update.effective_message.reply_text(f"Application is {status.state.value}.")
    except Exception:
        logger.exception("Error handling /status")
        await update.effective_message.reply_text("Failed to retrieve status.")
