from db.connection import get_connection

def test_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (user_name) VALUES (%s) RETURNING user_id;", ("123",))
    user_id = cur.fetchone()["user_id"]
    conn.commit()
    cur.close()
    conn.close()
    print("插入成功，user_id=", user_id)

if __name__ == "__main__":
    test_db()
