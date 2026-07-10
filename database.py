import sqlite3
from datetime import datetime


DB_NAME = "signals.db"


def connect():

    return sqlite3.connect(DB_NAME)


def init_db():

    conn = connect()

    cursor = conn.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS signals(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        pair TEXT,

        signal TEXT,

        entry_price REAL,

        exit_price REAL,

        result TEXT,

        timeframe TEXT DEFAULT 'M1',

        expiration INTEGER DEFAULT 60,

        checked INTEGER DEFAULT 0,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)


    conn.commit()
    conn.close()



def save_signal(pair, signal, entry_price):

    conn = connect()

    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT INTO signals(
            pair,
            signal,
            entry_price,
            timeframe,
            expiration
        )

        VALUES(?,?,?,?,?)
        """,
        (
            pair,
            signal,
            entry_price,
            "M1",
            60
        )
    )


    conn.commit()
    conn.close()



def get_unchecked():

    conn = connect()

    cursor = conn.cursor()


    cursor.execute("""
        SELECT

            id,
            pair,
            signal,
            entry_price

        FROM signals

        WHERE checked = 0

        AND created_at <= datetime('now','-60 seconds')

    """)


    rows = cursor.fetchall()


    conn.close()


    return rows




def update_result(signal_id, exit_price, result):

    conn = connect()

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



def get_stats():

    conn = connect()

    cursor = conn.cursor()



    cursor.execute("""
        SELECT

            COUNT(*),

            SUM(
            CASE 
            WHEN result='WIN'
            THEN 1
            ELSE 0
            END
            ),

            SUM(
            CASE 
            WHEN result='LOSS'
            THEN 1
            ELSE 0
            END
            )

        FROM signals

        WHERE checked=1

    """)


    row = cursor.fetchone()


    total = row[0] or 0
    wins = row[1] or 0
    losses = row[2] or 0



    winrate = 0


    if total:

        winrate = round(
            wins / total * 100,
            2
        )



    cursor.execute("""
        SELECT

            pair,

            COUNT(*),

            SUM(
            CASE
            WHEN result='WIN'
            THEN 1
            ELSE 0
            END
            )

        FROM signals

        WHERE checked=1

        GROUP BY pair

        ORDER BY COUNT(*) DESC

    """)


    pairs=[]


    for pair,count,wins_pair in cursor.fetchall():

        pairs.append({

            "pair":pair,

            "signals":count,

            "wins":wins_pair,

            "winrate":round(
                wins_pair/count*100,
                2
            )

        })



    conn.close()



    return {

        "total":total,

        "wins":wins,

        "losses":losses,

        "winrate":winrate,

        "pairs":pairs

    }



def get_last_signals(limit=10):

    conn=connect()

    cursor=conn.cursor()


    cursor.execute("""
        SELECT

        pair,
        signal,
        entry_price,
        exit_price,
        result,
        created_at

        FROM signals

        ORDER BY id DESC

        LIMIT ?

    """,(limit,))


    rows=cursor.fetchall()


    conn.close()


    return rows
