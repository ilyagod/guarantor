from typing import Any, Dict, Optional

from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError

from guarantor.common.socketio import sio
from guarantor.db.dao.chat_message_dao import ChatMessageDAO
from guarantor.db.dao.deal_dao import DealDAO
from guarantor.socketio.chat.schema import ChatMessageSchema, RequestChatMessageSchema


async def sio_connect_handler(
    sid: str,
    environ: Dict[str, Any],
    auth: Optional[Dict[str, Any]],
) -> None:
    if not auth:
        raise ConnectionRefusedError("authentication failed")
    chat_id = auth.get("token")
    deal = await DealDAO.get_or_none({"chat_id": chat_id})
    if not deal:
        raise ConnectionRefusedError("authentication failed")

    await sio.save_session(sid, {"deal": deal})
    sio.enter_room(sid, chat_id)

    messages = await ChatMessageDAO.filter({"deal": deal})

    for message in messages:
        await sio.emit(
            "message",
            jsonable_encoder(ChatMessageSchema.from_orm(message).dict()),
        )


async def sio_message_handler(sid: str, message_data: Dict[str, Any], _: Any) -> None:
    try:
        data: RequestChatMessageSchema = RequestChatMessageSchema.parse_obj(
            message_data,
        )
    except ValidationError:
        return

    session = await sio.get_session(sid)
    deal = session["deal"]
    if data.user_id not in {deal.customer_id, deal.performer_id}:
        return
    message = await ChatMessageDAO.create(
        {
            "user_id": data.user_id,
            "message": data.message,
            "deal_id": deal.id,
        },
    )

    await sio.emit(
        "message",
        jsonable_encoder(ChatMessageSchema.from_orm(message).dict()),
        room=session["deal"].chat_id,
    )
