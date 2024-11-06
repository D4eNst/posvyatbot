from repository.crud.base import BaseCRUDRepository
from repository.models.message import Message


class MessageRepo(BaseCRUDRepository[Message]):
    model = Message
