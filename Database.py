import mysql.connector as connector

class Connection:
    def __init__(self, connection_params):
        self.conn = None
        self._modifyColumn = {
            "addColumn": 1,
            "dropColumn": 2,
        }  
        try:
            # Attempt connection using default settings
            connection = connector.connect(**connection_params)

            if connection.is_connected():
                self.conn = connection
                print("Connection successful!")
        except connector.Error as err:
            print(f"Error: {err}")

    @property
    def modifyColumn(self):
        return self._modifyColumn        
    
    def __del__(self):
        if self.conn is not None and self.conn.is_connected():
            self.conn.close()
            print("Connection closed.")        

    def connectDatabase(self, database: str):
        if self.conn is not None and self.conn.is_connected():
            cursor = self.conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
            cursor.execute(f"USE {database}")
            print(f"Database {database} connected.")
            cursor.close()

    def executeQuery(self, query: str):
        try:
            if self.conn is not None and self.conn.is_connected():
                cursor = self.conn.cursor()
                cursor.execute(query)
                self.conn.commit()
                print("Query executed.")
        except connector.Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()        

    def checkTable(self, table: str) -> bool:
        try:
            if self.conn is not None and self.conn.is_connected():
                cursor = self.conn.cursor()
                cursor.execute("SHOW TABLES LIKE %s", (table,))
                result = cursor.fetchone()
                if result:
                    return True
                else:
                    return False
        except connector.Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()        

    def createTable(self, table: str, query: str):
        try:
            if self.conn is not None and self.conn.is_connected():
                cursor = self.conn.cursor()
                create_table_query = f"CREATE TABLE IF NOT EXISTS {table} ({query})"
                cursor.execute(create_table_query)
                print(f"Table {table} created.")
                cursor.commit()          #optional      
        except connector.Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()

    def modifyTable(self, action: int, table: str, column: str, datatype: str):
        try:
            if self.conn is not None and self.conn.is_connected():
                cursor = self.conn.cursor()
                #Check if column exists
                cursor.execute(f"SHOW COLUMNS FROM {table} LIKE %s", (column,))
                result = cursor.fetchone()                
                if action == self._modifyColumn['addColumn'] and not result:
                    cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {datatype}")
                elif action == self._modifyColumn['dropColumn'] and result:
                    cursor.execute(f"ALTER TABLE {table} DROP COLUMN {column}")
                print(f"Table {table} modified.")
                self.conn.commit()
        except connector.Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()

    def insertRow(self, table: str, data: dict):
        try:
            if self.conn is not None and self.conn.is_connected():
                cursor = self.conn.cursor()
                columns = ', '.join(data.keys())
                values = ', '.join(data.values())
                insert_query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
                cursor.execute(insert_query)
                self.conn.commit()
                print(f"Row inserted into {table}")
        except connector.Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()

    def insertMany(self, table: str, cols: list, values: list):
        try:
            if self.conn is not None and self.conn.is_connected():
                cursor = self.conn.cursor()
                columns = ', '.join(cols)
                valPlace = ', '.join(['%s' for _ in range(len(cols))])
                insert_query = f"INSERT IGNORE INTO {table} ({columns}) VALUES ({valPlace})"
                print(insert_query)
                cursor.executemany(insert_query, values)
                self.conn.commit()
                print(f"Data inserted into {table}")
        except connector.Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()

    def readTable(self, table: str, cols: list = None, where: list[tuple] = None, sortBy: str = None, order='DESC') -> list:
        try:
            if self.conn is not None and self.conn.is_connected():
                cursor = self.conn.cursor()
                columns = ', '.join(cols) if cols else '*'
                query = f"SELECT {columns} FROM {table}"
                
                if where:
                    conditions = ' AND '.join([f"{w[0]} = %s" for w in where])
                    query += f" WHERE {conditions}"
                
                if sortBy:
                    query += f" ORDER BY {sortBy} {order}"
                
                cursor.execute(query, tuple(w[1] for w in where) if where else None)
                rows = cursor.fetchall()
                print(f"Data read from {table}")
                return rows
        except connector.Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()

            
if __name__ == "__main__":
    conn = Connection()
    del conn            
