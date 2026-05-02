import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Ammu8610@",
        database="fake_job_detection"
    )

    if conn.is_connected():
        print("Connected to MySQL Successfully!")

        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")

        for table in cursor:
            print(table)

except Exception as e:
    print("Error:", e)
