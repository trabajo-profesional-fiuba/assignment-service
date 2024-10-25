from sqlalchemy import asc, desc, exc, update
from sqlalchemy.orm import Session

from src.api.periods.models import Period
from src.api.periods.exceptions import (
    PeriodDuplicated,
    PeriodNotFound,
)


class PeriodRepository:

    def __init__(self, sess: Session):
        self.Session = sess

    def _order_clause(self, order):
        """Define el orden de busqueda ascendente o descendente"""
        if order == "ASC":
            return asc(Period.created_at)
        elif order == "DESC":
            return desc(Period.created_at)
        else:
            raise ValueError("Invalid order direction. Use 'ASC' or 'DESC'.")

    def add_period(self, period: Period) -> Period:
        """Agrega un cuatrimestre a la tabla"""
        try:
            with self.Session() as session:
                session.add(period)
                session.commit()
                session.refresh(period)
                session.expunge(period)

            return period
        except exc.IntegrityError:
            raise PeriodDuplicated(message="Period already exist")

    def get_all_periods(self, order: str) -> list[Period]:
        """Devuelve todos los cuatrimestres ordenados segun la condicion"""
        with self.Session() as session:
            order_clause = self._order_clause(order)
            results = session.query(Period).order_by(order_clause).all()
            session.expunge_all()
        return results

    def get_period_by_id(self, period_id: str) -> Period:
        """Devuelve un cuatrimestre puntual"""
        with self.Session() as session:
            period = session.query(Period).filter(Period.id == period_id).first()
            if period is None:
                raise PeriodNotFound("The period does not exist")
        return period

    def update(self, period_id: str, attributes: dict):
        """Actualiza los atributos de un cuatrimestre particular"""
        stmt = (
            update(Period)
            .where(Period.id == period_id)
            .values(**attributes)
            .returning(Period.id)
        )

        with self.Session() as session:
            result = session.execute(stmt).fetchone()
            if result is None:
                raise PeriodNotFound("The period does not exist")
            session.commit()
