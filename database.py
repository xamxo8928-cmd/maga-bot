import sqlite3

DB_NAME = "signals.db"

def init_db():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS signals(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        pair TEXT,

        signal TEXT,

        entry_price REAL,

        exit_price REAL,

        result TEXT,

        checked INTEGER DEFAULT 0,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    conn.commit()
    conn.close()

def save_signal(pair, signal, entry_price):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO signals(pair, signal, entry_price)
        VALUES(?,?,?)
        """,
        (
            pair,
            signal,
            entry_price
        )
    )

    conn.commit()
    conn.close()

def get_unchecked():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id,pair,signal,entry_price
        FROM signals
        WHERE checked=0
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows

def update_result(signal_id, exit_price, result):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        UPDATE signals

        SET
            exit_price=?,
            result=?,
            checked=1

        WHERE id=?
    """,
    (
        exit_price,
        result,
        signal_id
    ))

    conn.commit()

    conn.close()
