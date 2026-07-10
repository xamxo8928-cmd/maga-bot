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

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        UPDATE signals

        SET
            exit_price = ?,
            result = ?,
            checked = 1

        WHERE id = ?
    """,
    (
        exit_price,
        result,
        signal_id
    ))

    conn.commit()
    conn.close()


def get_stats():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()


    cursor.execute("""
        SELECT
            COUNT(*),
            SUM(CASE WHEN result = 'WIN' THEN 1 ELSE 0 END),
            SUM(CASE WHEN result = 'LOSS' THEN 1 ELSE 0 END)

        FROM signals

        WHERE checked = 1
    """)


    row = cursor.fetchone()

    total = row[0] or 0
    wins = row[1] or 0
    losses = row[2] or 0


    winrate = 0

    if total > 0:
        winrate = round(
            (wins / total) * 100,
            2
        )


    cursor.execute("""
        SELECT
            pair,
            COUNT(*) as total,
            SUM(CASE WHEN result = 'WIN' THEN 1 ELSE 0 END) as wins

        FROM signals

        WHERE checked = 1

        GROUP BY pair

        ORDER BY total DESC
    """)


    pairs = []

    for pair, count, pair_wins in cursor.fetchall():

        pair_rate = round(
            (pair_wins / count) * 100,
            2
        )

        pairs.append({
            "pair": pair,
            "signals": count,
            "wins": pair_wins,
            "winrate": pair_rate
        })


    conn.close()


    return {
        "total": total,
        "wins": wins,
        "losses": losses,
        "winrate": winrate,
        "pairs": pairs
    }
