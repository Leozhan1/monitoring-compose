import json
import pyodbc

connection_string = (
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=tcp:sqlserver2-0.database.windows.net,1433;"
    "Database=database3.0;"
    "Uid=sqladmin;"
    "Pwd={sql123123!};"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

print("Connected!")

with open("data.json", "r") as f:
    metrics = json.load(f)

for entry in metrics:
    cursor.execute(
        "INSERT INTO metrics (cpu, memory, gpu) VALUES (?, ?, ?)",
        (entry["cpu"], entry["memory"], entry["gpu"])
    )

conn.commit()
print("All data inserted!")
