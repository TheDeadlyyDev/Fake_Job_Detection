import mysql.connector

try:
    conn = mysql.connector.connect(
        host="nozomi.proxy.rlwy.net",
        user="root",
        password="SGsrgeCOmdHqQgDPNAcdXZLiNCYtMOuD",
        port=23220
        database="railway"
    )

    if conn.is_connected():
        print("Connected to MySQL Successfully!")

        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")

        for table in cursor:
            print(table)

except Exception as e:
    print("Error:", e)
