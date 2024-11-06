from repository.crud.base import BaseCRUDRepository
from repository.models.station import Station


class StationRepo(BaseCRUDRepository[Station]):
    model = Station
