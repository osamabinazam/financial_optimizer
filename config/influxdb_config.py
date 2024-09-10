# import os
# from dotenv import load_dotenv
# from influxdb_client import InfluxDBClient
#
# # Load environment variables from .env file
# load_dotenv()
#
#
# class InfluxDBConfig:
#     """
#     Configuration class for handling the InfluxDB connection, fetching credentials from environment variables.
#     Provides methods to create and manage the connection lifecycle.
#     """
#
#     def __init__(self):
#         # Fetching InfluxDB configuration from environment variables
#         self.url = os.getenv("INFLUXDB_URL", "http://localhost:8086")
#         self.token = os.getenv("INFLUXDB_TOKEN")
#         self.org = os.getenv("INFLUXDB_ORG")
#         self.bucket = os.getenv("INFLUXDB_BUCKET")
#         self.timeout = os.getenv("INFLUXDB_TIMEOUT", "10000")  # Default timeout set to 10000 ms
#
#         # Create the InfluxDB client
#         self.client = None
#         self._initialize_client()
#
#     def _initialize_client(self):
#         """
#         Initializes the InfluxDB client using the loaded configuration.
#         """
#         if not all([self.url, self.token, self.org, self.bucket]):
#             raise ValueError("InfluxDB configuration is incomplete. Please check the environment variables.")
#         try:
#             self.client = InfluxDBClient(url=self.url, token=self.token, org=self.org, timeout=self.timeout)
#             print("InfluxDB client initialized successfully.")
#         except Exception as e:
#             raise ConnectionError(f"Failed to initialize InfluxDB client: {e}")
#
#     def check_connection(self):
#         """
#         Verifies the connection to InfluxDB by pinging the database.
#         """
#         try:
#             health = self.client.ping()
#             if health:
#                 print("Connected to InfluxDB successfully!")
#                 return True
#             else:
#                 print("Failed to connect to InfluxDB.")
#                 return False
#         except Exception as e:
#             print(f"An error occurred while checking the InfluxDB connection: {e}")
#             return False
#
#     def get_client(self):
#         """
#         Returns the initialized InfluxDB client after verifying the connection.
#         """
#         if not self.client:
#             raise Exception("InfluxDB client not initialized.")
#         if not self.check_connection():
#             raise Exception("Failed to connect to InfluxDB.")
#         return self.client
#
#     def close_connection(self):
#         """
#         Closes the InfluxDB client connection.
#         """
#         if self.client:
#             self.client.close()
#             print("Connection to InfluxDB closed successfully.")
