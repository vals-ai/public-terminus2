"""
truncation infra for terminus-2 agent
currently consistent with Laude implementation
"""

import logging

from model_library.base import LLM
from pydantic import BaseModel

from terminus2.llms.chat import Chat
from terminus2.llms.utils import get_model_context_limit


# from original tbench
def pretty_print(obj: object, logger: logging.Logger, title: str | None = None):
    """Pretty printer that works with any object.

    Args:
        obj: The object to pretty print.
        logger: Logger to use (required)
        title: The title of the object.
    """

    if isinstance(obj, Exception):
        logger.debug(f"{obj}", exc_info=True)
        return

    if title:
        logger.debug(f"===== {title} =====")

    if hasattr(obj, "__dict__"):
        for key, value in obj.__dict__.items():
            if not key.startswith("_"):
                logger.debug(f"{key}: {value}")
    elif isinstance(obj, dict):
        for key, value in obj.items():
            logger.debug(f"{key}: {value}")
    elif isinstance(obj, BaseModel):
        logger.debug(obj.model_dump_json(indent=2))
    else:
        logger.debug(str(obj))


class Truncator:
    TARGET_FREE_TOKENS: int = 4000

    def __init__(self, chat: Chat, llm: LLM, logger: logging.Logger):
        self.chat = chat
        self.llm = llm
        self._logger = logger
        self.context_limit = get_model_context_limit(llm)

    async def unwind(self) -> None:
        """Remove recent messages until we have enough free tokens."""
        while len(self.chat.messages) > 1:  # Keep at least the first message
            current_tokens = await self.llm.count_tokens(self.chat.messages)
            free_tokens = self.context_limit - current_tokens

            self._logger.debug(f"Free tokens: {free_tokens}, target: {self.TARGET_FREE_TOKENS}")
            if free_tokens >= self.TARGET_FREE_TOKENS:
                break

            # removes until the last user message
            assert self.chat.unwind_last_user_message(), "no user message found to unwind!"

        free_tokens = self.context_limit - await self.llm.count_tokens(self.chat.messages)
        self._logger.debug(
            f"Unwound messages. Remaining messages: {len(self.chat.messages)}, Free tokens: approximately {free_tokens}"
        )
