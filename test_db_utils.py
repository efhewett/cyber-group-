import unittest
from db_utils import create_connection, insert_data, fetch_data, execute_query, close_connection

class TestDbUtils(unittest.TestCase):

    def test_create_connection(self):
        connection = create_connection()
        self.assertIsNotNone(connection)
        close_connection(connection)

    def test_insert_data(self):
        table = "TestTable"
        data = {"column1": "value1", "column2": "value2"}
        result = insert_data(table, data)
        self.assertTrue(result)

    def test_fetch_data(self):
        query = "SELECT * FROM TestTable WHERE column1 = %s"
        params = ("value1",)
        data = fetch_data(query, params)
        self.assertIsInstance(data, list)

    def test_execute_query(self):
        query = "UPDATE TestTable SET column2 = %s WHERE column1 = %s"
        params = ("new_value", "value1")
        result = execute_query(query, params)
        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()
