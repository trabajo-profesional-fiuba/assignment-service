import re

from src.api.exceptions import Duplicated
from src.api.periods.schemas import (
    PeriodRequest,
    PeriodList,
    UpdatePeriodRequest,
    PeriodResponse,
)
from src.api.tutors.exceptions import (
    InvalidPeriod,
    PeriodDuplicated,
)
from src.api.periods.models import Period


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
                period_db = Period(id=period.id)
                return self._repository.add_period(period_db)
            else:
                raise InvalidPeriod(
                    message="Period id should follow patter nC20year, ie. 1C2024"
                )
        except PeriodDuplicated as e:
            raise Duplicated(str(e))

    def get_all_periods(self, order) -> PeriodList:
        """
        Returns the list of periods
        """
        return PeriodList.model_validate(self._repository.get_all_periods(order))

    def get_period_by_id(self, period_id: str) -> Period:
        return self._repository.get_period_by_id(period_id)

    def update(self, period: UpdatePeriodRequest):
        try:
            attributes = period.dict(exclude_unset=True)
            attributes.pop("id", None)
            self._repository.update(period.id, attributes)
            return PeriodResponse.model_validate(period)
        except Exception as e:
            logger.error(f"Could not update period because of: {str(e)}")
            raise EntityNotInserted(
                message="Period could't be updated due a database problem. Check if the\
                id provided are correct."
            )
