from typing import Sequence

from sqlalchemy import func, desc

from repository.crud.base import BaseCRUDRepository
from repository.models.message import Message


class MessageRepo(BaseCRUDRepository[Message]):
    model = Message

    async def get_page(self, cnt_in_page: int, page_num: int) -> tuple[int, Sequence[Message]]:
        count_query = await self.async_session.execute(func.count(self.model.id))
        total_count = count_query.scalar()

        if total_count == 0:
            return 0, []

        if total_count <= (page_num - 1) * cnt_in_page:
            return total_count, []

        stmt = self._stmt_filter().order_by(desc('id')).offset(cnt_in_page * (page_num - 1)).limit(cnt_in_page)

        query = await self.async_session.execute(statement=stmt)
        result = query.scalars().all()
        return total_count, result
