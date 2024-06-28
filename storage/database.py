from sqlalchemy import create_engine, Column, String, DateTime, Index
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager
import sqlalchemy.exc

Base = declarative_base()


class TopicPreferences(Base):
    __tablename__ = "topic_preferences"

    email = Column(String, primary_key=True, index=True)
    group_id = Column(DateTime)
    topic1 = Column(String)
    topic2 = Column(String)
    topic3 = Column(String)


class Database:
    """
    Database class that manages the database setup and sessions.
    """

    def __init__(self, url: str):
        self.engine = create_engine(url)
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )
        self.drop_tables()
        self.create_tables()

    @contextmanager
    def get_session(self):
        """
        Context manager to handle SQLAlchemy sessions.
        """
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error during session: {e}")
            raise
        finally:
            session.close()

    def create_tables(self):
        """
        Creates all tables in the database.
        """
        try:
            Base.metadata.create_all(bind=self.engine)
            self.create_index_if_not_exists(
                "ix_topic_preferences_email", "topic_preferences", ["email"]
            )
        except sqlalchemy.exc.ProgrammingError as e:
            if "relation already exists" in str(e):
                print("Table or index already exists, skipping creation.")
            else:
                raise e

    def create_index_if_not_exists(self, index_name, table_name, columns):
        """
        Create an index on a table if it does not already exist.
        """
        with self.engine.connect() as connection:
            inspector = sqlalchemy.inspect(connection)
            indexes = inspector.get_indexes(table_name)
            if index_name not in [index["name"] for index in indexes]:
                table = Base.metadata.tables.get(table_name)
                if table is not None:
                    index = Index(index_name, *columns)
                    index.create(connection, checkfirst=True)

    def drop_tables(self):
        """
        Drop all tables in the database.
        """
        try:
            Base.metadata.drop_all(bind=self.engine)
        except Exception as e:
            print(f"Error dropping tables: {e}")
            raise

    def get_db(self):
        with self.get_session() as session:
            return session

    def delete_all_records_from_table(self, model):
        """
        Delete all records from the specified table.
        """
        with self.get_session() as session:
            try:
                session.query(model).delete()
                print(f"All records deleted from {model.__tablename__}.")
            except Exception as e:
                print(f"Error deleting records: {e}")
                raise
