from sqlalchemy.orm import Session
from sqlalchemy import insert, delete, and_, tuple_

from src.api.dates.models import DateSlot, GroupDateSlot, TutorDateSlot


class DateSlotRepository:

    def __init__(self, sess: Session):
        self.Session = sess

    def add_date_slot(self, date_slot: DateSlot):

        with self.Session() as session:
            session.add(date_slot)
            session.commit()
            session.refresh(date_slot)

            session.expunge(date_slot)

        return date_slot

    def add_bulk(
        self, model: DateSlot | GroupDateSlot | TutorDateSlot, data: list[dict]
    ):
        with self.Session() as session:
            result = session.execute(insert(model).returning(model), data)
            session.commit()

            # Extract the inserted rows from the result
            rows = result.fetchall()
            session.expunge_all()
            saved_data = [getattr(row, model.__name__) for row in rows]

        return saved_data

    def get_slots_by_period(self, period: str):
        with self.Session() as session:
            slots = session.query(DateSlot).filter(DateSlot.period_id == period).all()
            for slot in slots:
                session.expunge(slot)

        return slots

    def get_tutor_slots_by_id(self, tutor_id: int, period: str):
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

    def sync_date_slots(self, slots_to_update: list[dict], period: str):
        """
        Deletes existing slots that are not in updated list and add the new ones.
        """
        with self.Session() as session:
            slot_ids = [slot["slot"] for slot in slots_to_update]

            # Delete slots not in the update list
            delete_stmt = delete(DateSlot).where(
                DateSlot.period_id == period, DateSlot.slot.notin_(slot_ids)
            )
            session.execute(delete_stmt)

            existing_slots = session.query(DateSlot).all()
            existing_slot_ids = {(slot.slot, slot.period_id) for slot in existing_slots}

            # Filter slots that already exist
            new_slots = [
                slot
                for slot in slots_to_update
                if (slot["slot"], slot["period_id"]) not in existing_slot_ids
            ]

            # Bulk insert new slots
            if new_slots:
                session.execute(insert(DateSlot).values(new_slots))

            session.commit()

    def sync_group_slots(self, slots_to_update: list[dict], group_id: int):
        """
        Deletes existing slots that are not in updated list and add the new ones.
        """
        with self.Session() as session:
            slot_ids = {(slot["slot"], slot["group_id"]) for slot in slots_to_update}

            existing_slots = session.query(GroupDateSlot).all()
            existing_slot_ids = {(slot.slot, slot.group_id) for slot in existing_slots}

            # Identify slots to delete
            slots_to_delete = existing_slot_ids - slot_ids

            # Delete slots not in the update list
            delete_stmt = delete(GroupDateSlot).where(
                and_(
                    GroupDateSlot.slot.in_(
                        [slot for slot, group_id in slots_to_delete]
                    ),
                    GroupDateSlot.group_id.in_(
                        [group_id for slot, group_id in slots_to_delete]
                    ),
                )
            )
            session.execute(delete_stmt)

            # Filter slots that already exist
            new_slots = [
                slot
                for slot in slots_to_update
                if (slot["slot"], slot["group_id"]) not in existing_slot_ids
            ]

            # Bulk insert new slots
            if new_slots:
                session.execute(insert(GroupDateSlot).values(new_slots))

            session.commit()

    def sync_tutor_slots(self, slots_to_update: list[dict], tutor_id: int, period: str):
        """
        Deletes existing slots that are not in updated list and add the new ones.
        """
        with self.Session() as session:
            slot_ids = {
                (slot["slot"], slot["tutor_id"], slot["period_id"])
                for slot in slots_to_update
            }

            existing_slots = session.query(TutorDateSlot).all()
            existing_slot_ids = {
                (slot.slot, slot.tutor_id, slot.period_id) for slot in existing_slots
            }

            # Identify slots to delete
            slots_to_delete = existing_slot_ids - slot_ids

            # Delete slots not in the update list
            delete_stmt = delete(TutorDateSlot).where(
                and_(
                    TutorDateSlot.slot.in_(
                        [slot for slot, tutor_id, period_id in slots_to_delete]
                    ),
                    TutorDateSlot.tutor_id.in_(
                        [tutor_id for slot, tutor_id, period_id in slots_to_delete]
                    ),
                    TutorDateSlot.period_id.in_(
                        [period_id for slot, tutor_id, period_id in slots_to_delete]
                    ),
                )
            )
            session.execute(delete_stmt)

            # Filter slots that already exist
            new_slots = [
                slot
                for slot in slots_to_update
                if (slot["slot"], slot["tutor_id"], slot["period_id"])
                not in existing_slot_ids
            ]

            # Bulk insert new slots
            if new_slots:
                session.execute(insert(TutorDateSlot).values(new_slots))

            session.commit()
