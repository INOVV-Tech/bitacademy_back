from contextlib import contextmanager
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError

Base = declarative_base()

class PostgreDatasource:
    """
    Don't change this datasource!
    """

    def __init__(self, session: Session):
        self.session = session
        
    @contextmanager
    def session_scope(self, commit: bool = False):
        """
        This method is a context manager that provides a transactional scope
        for a series of operations in the database.
        """
        try:
            yield self.session
            print("Commiting")
            print(commit)   
            if commit:
                self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            logging.error(f"Database transaction failed: {e}", exc_info=True)
            raise
    
    def add_item(self, item):
        """
        This method adds an item to the database.
        This item could be any entity that is mapped to a table in the database, 
        but need to have a DTO to convert it to a model.
        """
        
        with self.session_scope(commit=True) as session:
            print("Adding item")
            session.add(item)
            session.flush()
            session.refresh(item)
            return item
    
    def get_item(self, model_class, item_id):
        """
        This method gets an item from the database.
        The model_class parameter is the class that represents the table in the database.
        """
        with self.session_scope() as session:
            item = session.query(model_class).get(item_id)
            return item
    
    def get_all_items(self, model_class):
        """
        This method gets all items from the database.
        The model_class parameter is required to know which table to query.
        """        
        with self.session_scope() as session:
            items = session.query(model_class).all()
            return items
        
    def delete_item(self, model_class, item_id):
        """
        This method deletes an item from the database.
        The model_class parameter is required to know which table to query.
        The item_id is waiting for the primary key of the item to be deleted.
        It'll return None only if the item doesn't exist, otherwise it'll return the item deleted.
        """
        with self.session_scope(commit=True) as session:
            item = session.query(model_class).get(item_id)
            if item is None:
                return None
            session.delete(item)
            return item

    def update_item(self, item):
        """
        This method updates an item in the database.
        The item parameter is the item to be updated.
        The merge method is used to synchronize the item with the current state of the database.
        On other words, it just updates the item in the database.
        And the refresh method is used to update the item with the new values.
        """
        
        with self.session_scope(commit=True) as session:
            merged_item = session.merge(item)
            session.flush()
            session.refresh(merged_item)
            return merged_item

    def query(self, model_class, **filters):
        """
        This method queries the database.
        The model_class parameter is required to know which table to query.
        The filters parameter is a dictionary with the filters to be applied in the query.

        """
        with self.session_scope() as session:
            query = session.query(model_class)
            for key, value in filters.items():
                query = query.filter(getattr(model_class, key) == value)
            return query.all()