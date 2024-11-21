from typing import Dict, Any
from .csv_introspector import CSVIntrospector
# Comment out the following lines if you don't have these introspectors yet
# from .sqlite_introspector import SQLiteIntrospector
# from .postgres_introspector import PostgresIntrospector
from .base import DataIntrospector

def create_introspector(source_type: str, **kwargs) -> DataIntrospector:
    """
    Factory function to create appropriate introspector based on source type.
    
    Args:
        source_type (str): One of 'csv', 'sqlite', or 'postgres'
        **kwargs: Connection parameters specific to each source type
    
    Returns:
        DataIntrospector: Appropriate introspector instance
    """
    if source_type == 'csv':
        if 'directory_path' not in kwargs:
            raise ValueError("directory_path is required for CSV introspector")
        return CSVIntrospector(kwargs['directory_path'])
    
    # Uncomment and implement these sections when you have the respective introspectors
    # elif source_type == 'sqlite':
    #     if 'db_path' not in kwargs:
    #         raise ValueError("db_path is required for SQLite introspector")
    #     return SQLiteIntrospector(kwargs['db_path'])
    
    # elif source_type == 'postgres':
    #     required_params = {'dbname', 'user', 'password', 'host'}
    #     missing_params = required_params - set(kwargs.keys())
    #     if missing_params:
    #         raise ValueError(f"Missing required parameters for PostgreSQL introspector: {missing_params}")
    #     return PostgresIntrospector(
    #         dbname=kwargs['dbname'],
    #         user=kwargs['user'],
    #         password=kwargs['password'],
    #         host=kwargs['host'],
    #         port=kwargs.get('port', '5432')
    #     )
    
    else:
        raise ValueError(f"Unsupported source type: {source_type}")
