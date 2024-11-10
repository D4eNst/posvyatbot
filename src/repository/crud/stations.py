from select import select
from typing import Sequence

from sqlalchemy import func

from repository.crud.base import BaseCRUDRepository
from repository.models.station import Station


class StationRepo(BaseCRUDRepository[Station]):
    model = Station

    async def get_page(self, cnt_in_page: int, page_num: int) -> tuple[int, Sequence[Station]]:
        count_query = await self.async_session.execute(func.count(self.model.id))
        total_count = count_query.scalar()

        if total_count == 0:
            return 0, []

        if total_count <= (page_num - 1) * cnt_in_page:
            return total_count, []

        stmt = self._stmt_filter().order_by('id').offset(cnt_in_page * (page_num-1)).limit(cnt_in_page)

        query = await self.async_session.execute(statement=stmt)
        result = query.scalars().all()
        return total_count, result
