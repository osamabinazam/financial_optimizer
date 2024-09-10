import pandas as pd
import requests
from questdb.ingress import Sender, SenderTransaction, TimestampNanos


class QuestDBService():
    """
    Service class to interact with QuestDB.
    """

    def __init__(self):
        pass

    def delete_data(self, base_url, table_name):
        """
        Delete all data from the specified table.
        :param base_url:
        :param table_name:
        :return:
        """

        url = f"{base_url}/exec"
        params = {'query': f'TRUNCATE TABLE {table_name};'}
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an exception for bad status codes
            print("Data deleted successfully")
        except requests.RequestException as e:
            print(f"Error deleting data: {e}")

    def insert_data(self, conf, table_name, data, batch_size=1000):
        """
        Insert data into the specified table.
        :param conf: The QuestDB configuration.
        :param table_name: The name of the table.
        :param data: The data to insert.
        :return:
        """

        with Sender.from_conf(conf) as sender:
            # For single row processing
            for index, row in data.iterrows():
                sender.row(
                    table_name=table_name,
                    symbols={'Symbol': row['Symbol']},
                    columns={
                        'Open': row['Open'],
                        'Low': row['Low'],
                        'High': row['High'],
                        'Close': row['Close'],
                        'Volume': row['Volume']
                    },
                    at=TimestampNanos.from_datetime(row['Date'])
                )
            sender.flush()

    @staticmethod
    def query_data(base_url, query):
        """
        Query data from QuestDB.
        :param base_url:
        :param query:
        :return: A DataFrame containing the query results.
        """
        url = f"{base_url}/exec"
        params = {'query': query}
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            columns_data = data['columns']
            columns_name = [column['name'] for column in columns_data]
            records = data['dataset']
            df = pd.DataFrame(records, columns=columns_name, index=None)
            return df
        except requests.RequestException as e:
            print(f"Error querying data: {e}")
            return None
