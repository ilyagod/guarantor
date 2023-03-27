from guarantor.db.dao.base import BaseDAO
from guarantor.db.models.chat_message import ChatMessage


class ChatMessageDAO(BaseDAO[ChatMessage]):
    _model = ChatMessage
