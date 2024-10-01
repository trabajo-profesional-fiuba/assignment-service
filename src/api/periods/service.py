import re

from src.api.exceptions import Duplicated
from src.api.periods.schemas import (
    PeriodRequest,
    PeriodList,
    UpdatePeriodRequest,
    PeriodResponse,
)
from src.api.periods.exceptions import InvalidPeriod, PeriodDuplicated, PeriodNotFound
from src.api.periods.models import Period
from src.api.exceptions import EntityNotFound
from src.config.logging import logger


class PeriodService:

    def __init__(self, repository) -> None:
        self._repository = repository

    def _validate_period(self, period_id):
        """Validates that the period id
        follows the expected pattern
        ^[1|2]C20[0-9]{2}$

        Matches cases where 1|2C20xx where xx are numbers from 0-9
        """
        regex = re.compile("^[1|2]C20[0-9]{2}$")
        if regex.search(period_id) is not None:
            return True
        else:
            return False

    def add_period(self, period: PeriodRequest) -> Period:
        """
        Creates a nw global period
        """
        try:
            valid = self._validate_period(period.id)
            if valid:
                logger.info(f"Attempting to create new period with id: {period.id}")
                period_db = Period(id=period.id)
                return self._repository.add_period(period_db)
            else:
                raise InvalidPeriod(
                    message="Period id should follow patter nC20year, ie. 1C2024"
                )
        except PeriodDuplicated as e:
            logger.error(f"Could not add period because of: {str(e)}")
            raise Duplicated(str(e))

    def get_all_periods(self, order) -> PeriodList:
        """
        Returns the list of periods
        """
        logger.info(f"Attempts to get all the periods ordered by: {order}")
        return PeriodList.model_validate(self._repository.get_all_periods(order))

    def get_period_by_id(self, period_id: str) -> Period:
        logger.info(f"Attempts to get one period by id: {period_id}")
        return self._repository.get_period_by_id(period_id)

    def update(self, period: UpdatePeriodRequest):
        try:
            logger.info(f"Updatin period with id: {period.id}")
            attributes = period.model_dump(exclude_unset=True)
            attributes.pop("id", None)
            self._repository.update(period.id, attributes)
            return PeriodResponse.model_validate(period)
        except PeriodNotFound as e:
            logger.error(f"Could not update period because of: {str(e)}")
            raise EntityNotFound(str(e))
