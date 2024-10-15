from sqlalchemy.orm import Session
from sqlalchemy import insert, delete

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

    def bulk_update_slots(self, slots_to_update: list[dict], period: str):
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
            # Add new slots
            for slot in slots_to_update:
                if (slot["slot"], slot["period_id"]) not in existing_slot_ids:
                    new_slot = DateSlot(**slot)
                    session.add(new_slot)

            session.commit()

    def bulk_update_group_slots(self, slots_to_update: list[dict], group_id: int):
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
            for slot, group_id in slots_to_delete:
                delete_stmt = delete(GroupDateSlot).where(
                    GroupDateSlot.slot == slot, GroupDateSlot.group_id == group_id
                )
                session.execute(delete_stmt)

            # Add new slots
            for slot in slots_to_update:
                if (slot["slot"], slot["group_id"]) not in existing_slot_ids:
                    new_slot = GroupDateSlot(**slot)
                    session.add(new_slot)

            session.commit()
