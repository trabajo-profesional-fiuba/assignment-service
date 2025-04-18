from datetime import datetime
from sqlalchemy.orm import Session, aliased
from sqlalchemy import insert, delete, and_, tuple_, update, select

from src.api.dates.models import DateSlot, GroupDateSlot, TutorDateSlot
from src.api.groups.models import Group
from src.api.topics.models import Topic


class DateSlotRepository:

    def __init__(self, sess: Session):
        self.Session = sess

    def add_date_slot(self, date_slot: DateSlot):
        """Agrega una nueva fecha a la tabla"""
        with self.Session() as session:
            session.add(date_slot)
            session.commit()
            session.refresh(date_slot)

            session.expunge(date_slot)

        return date_slot

    def add_bulk(
        self, model: DateSlot | GroupDateSlot | TutorDateSlot, data: list[dict]
    ) -> list[dict]:
        """Dependiendo el modelo, agrega una lista de filas a la correspondiente tabla"""
        with self.Session() as session:
            result = session.execute(insert(model).returning(model), data)
            session.commit()

            # Extract the inserted rows from the result
            rows = result.fetchall()
            session.expunge_all()
            saved_data = [getattr(row, model.__name__) for row in rows]

        return saved_data

    def get_slots_by_period(self, period: str, only_available: bool):
        """Obtiene todos los slots por cuatrimestre"""
        query = select(DateSlot).filter(DateSlot.period_id == period)
        with self.Session() as session:
            if only_available:
                query = query.filter(DateSlot.assigned == False)

            result = session.execute(query)
            slots = result.scalars().all()

            for slot in slots:
                session.expunge(slot)

        return slots

    def get_tutor_slots_by_id(self, tutor_id: int, period: str) -> list[TutorDateSlot]:
        """Obtiene todos los slots de un tutor por cuatrimestre"""
        with self.Session() as session:
            slots = (
                session.query(TutorDateSlot)
                .filter(
                    TutorDateSlot.tutor_id == tutor_id,
                    TutorDateSlot.period_id == period,
                )
                .all()
            )
            for slot in slots:
                session.expunge(slot)

        return slots

    def get_groups_slots_by_id(self, group_id: int):
        """Obtiene todos los slots de un grupo"""
        with self.Session() as session:
            slots = (
                session.query(GroupDateSlot)
                .filter(
                    GroupDateSlot.group_id == group_id,
                )
                .all()
            )
            for slot in slots:
                session.expunge(slot)

        return slots

    def delete_date_slots(self, slots_to_delete: list[dict], period: str):
        """Borra los slots de un cuatrimestre"""
        with self.Session() as session:
            delete_stmt = delete(DateSlot).where(
                DateSlot.period_id == period,
                DateSlot.slot.in_([slot[0] for slot in slots_to_delete]),
            )
            session.execute(delete_stmt)
            session.commit()

    def sync_date_slots(self, slots_to_update: list[dict], period: str):
        """Borra aquellos slots que no estan en la lista y agrega los que faltan en un cuatrimestre"""
        with self.Session() as session:
            # Retrieve existing slots
            existing_slots = session.query(DateSlot).all()
            existing_slots_set = {(slot.slot, period) for slot in existing_slots}

            # Delete existing slots
            slots_to_update_set = set(
                (slot["slot"], period) for slot in slots_to_update
            )
            slots_to_delete = existing_slots_set - slots_to_update_set
            self.delete_date_slots(slots_to_delete, period)

            # Bulk insert new slots
            new_slots = [
                slot
                for slot in slots_to_update
                if (slot["slot"], slot["period_id"]) not in existing_slots_set
            ]
            if new_slots:
                self.add_bulk(DateSlot, new_slots)

    def delete_group_slots(self, slots_to_delete: list[dict], group_id: int):
        """Borra los slots de un grupo"""
        with self.Session() as session:
            delete_stmt = delete(GroupDateSlot).where(
                and_(
                    GroupDateSlot.group_id == group_id,
                    GroupDateSlot.slot.in_(
                        [slot for slot, group_id in slots_to_delete]
                    ),
                )
            )
            session.execute(delete_stmt)
            session.commit()

    def sync_group_slots(self, slots_to_update: list[dict], group_id: int):
        """Borra aquellos slots de un grupo que no estan en la lista y agrega los que faltan"""
        with self.Session() as session:
            # Retrieve existing slots
            existing_slots = session.query(GroupDateSlot).all()
            existing_slots_set = {(slot.slot, group_id) for slot in existing_slots}

            # Delete existing slots
            slots_to_update_set = set(
                (slot["slot"], group_id) for slot in slots_to_update
            )
            slots_to_delete = existing_slots_set - slots_to_update_set
            self.delete_group_slots(slots_to_delete, group_id)

            # Bulk insert new slots
            new_slots = [
                slot
                for slot in slots_to_update
                if (slot["slot"], slot["group_id"]) not in existing_slots_set
            ]
            if new_slots:
                self.add_bulk(GroupDateSlot, new_slots)

    def delete_tutor_slots(
        self, slots_to_delete: list[dict], tutor_id: int, period: str
    ):
        """Borra todos los slots de un tutor en un cuatrimestre especifico"""
        with self.Session() as session:
            delete_stmt = delete(TutorDateSlot).where(
                and_(
                    TutorDateSlot.period_id == period,
                    TutorDateSlot.tutor_id == tutor_id,
                    TutorDateSlot.slot.in_([slot for slot, _, _ in slots_to_delete]),
                )
            )
            session.execute(delete_stmt)
            session.commit()

    def sync_tutor_slots(self, slots_to_update: list[dict], tutor_id: int, period: str):
        """Borra aquellos slots de un tutor que no estan en la lista y agrega los que faltan en un cuatrimestre"""
        with self.Session() as session:
            # Retrieve existing slots
            existing_slots = session.query(TutorDateSlot).all()
            existing_slots_set = {
                (slot.slot, tutor_id, period) for slot in existing_slots
            }

            # Delete existing slots
            slots_to_update_set = set(
                (slot["slot"], tutor_id, period) for slot in slots_to_update
            )
            slots_to_delete = existing_slots_set - slots_to_update_set
            self.delete_tutor_slots(slots_to_delete, tutor_id, period)

            # Bulk insert new slots
            new_slots = [
                slot
                for slot in slots_to_update
                if (slot["slot"], slot["tutor_id"], slot["period_id"])
                not in existing_slots_set
            ]
            if new_slots:
                self.add_bulk(TutorDateSlot, new_slots)

    def update_tutor_dates(self, tutor_id: int, date: datetime, attributes: dict):
        """Updatea la fila basado en la fecha y tutor_id"""
        stmt = (
            update(TutorDateSlot)
            .filter(TutorDateSlot.tutor_id == tutor_id, TutorDateSlot.slot == date)
            .values(**attributes)
        )
        with self.Session() as session:
            session.execute(stmt)
            session.commit()

    def _upsert_tutor(
        self, session, date: datetime, tutor_id: int, period_id: str, type
    ):
        tutor_insert = insert(TutorDateSlot).values(
            slot=date,
            assigned=True,
            period_id=period_id,
            tutor_id=tutor_id,
            tutor_or_evaluator=type,
        )
        db_tutor = (
            session.query(TutorDateSlot)
            .filter(TutorDateSlot.tutor_id == tutor_id, TutorDateSlot.slot == date)
            .first()
        )
        if db_tutor:
            tutor_update = (
                update(TutorDateSlot)
                .filter(TutorDateSlot.tutor_id == tutor_id, TutorDateSlot.slot == date)
                .values(assigned=True, tutor_or_evaluator=type)
            )
            session.execute(tutor_update)
        else:
            tutor_insert
            session.execute(tutor_insert)

    def _upsert_group(self, session, date: datetime, group_id: int):
        db_group = (
            session.query(GroupDateSlot)
            .filter(GroupDateSlot.group_id == group_id, GroupDateSlot.slot == date)
            .first()
        )
        group_insert = insert(GroupDateSlot).values(slot=date, group_id=group_id)
        if not db_group:
            session.execute(group_insert)

    def _upsert_date(self, session, date: datetime, period_id: str):
        db_date = session.query(DateSlot).filter(DateSlot.slot == date).first()
        if db_date:
            date_update = (
                update(DateSlot).filter(DateSlot.slot == date).values(assigned=True)
            )
            session.execute(date_update)
        else:
            date_insert = insert(DateSlot).values(
                slot=date, assigned=True, period_id=period_id
            )
            session.execute(date_insert)

    def update_date(
        self,
        date: datetime,
        tutor_id: int,
        evaluator_id: int,
        group_id: int,
        period_id: str,
    ):
        """Updatea basado en la fecha"""
        with self.Session() as session:
            self._upsert_date(session, date, period_id)
            self._upsert_tutor(session, date, tutor_id, period_id, "tutor")
            self._upsert_tutor(session, date, evaluator_id, period_id, "evaluator")
            self._upsert_group(session, date, group_id)
            session.commit()

    def get_assigned_dates(self, period_id):
        """Las asignaciones dadas entre tutor,"""
        TutorDateSlotAlias = aliased(TutorDateSlot)
        EvaluatorDateSlotAlias = aliased(TutorDateSlot)
        query = (
            select(
                DateSlot.slot.label("date"),
                EvaluatorDateSlotAlias.tutor_id.label("evaluator_id"),
                TutorDateSlotAlias.tutor_id.label("tutor_id"),
                Group.id.label("group_id"),
                Group.group_number.label("group_number"),
            )
            .join(TutorDateSlotAlias, DateSlot.slot == TutorDateSlotAlias.slot)
            .join(EvaluatorDateSlotAlias, DateSlot.slot == EvaluatorDateSlotAlias.slot)
            .join(Group, DateSlot.slot == Group.exhibition_date)
            .where(DateSlot.assigned == True)
            .where(EvaluatorDateSlotAlias.tutor_or_evaluator == "evaluator")
            .where(TutorDateSlotAlias.tutor_or_evaluator == "tutor")
            .where(Group.period_id == period_id)
        )
        with self.Session() as session:
            result = session.execute(query)
            assignments = result.fetchall()

        return assignments

    def get_tutors_assigned_dates(self, tutor_id, period_id):
        """Obtiene todos los slots asiganados de un tutor  por cuatrimestre"""
        with self.Session() as session:
            slots = (
                session.query(TutorDateSlot, Group.group_number, Topic.name)
                .join(Group, Group.exhibition_date == TutorDateSlot.slot)
                .join(Topic, Topic.id == Group.assigned_topic_id)
                .filter(
                    TutorDateSlot.tutor_id == tutor_id,
                    TutorDateSlot.period_id == period_id,
                    TutorDateSlot.assigned == True,
                )
                .all()
            )
            session.expunge_all()

        return slots
