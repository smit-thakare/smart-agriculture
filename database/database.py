import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "agriculture.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS disease_predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        image TEXT,
        disease TEXT,
        confidence REAL,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS yield_predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        crop TEXT,
        area REAL,
        rainfall REAL,
        temperature REAL,
        humidity REAL,
        soil_ph REAL,
        fertilizer REAL,
        predicted_yield REAL,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def save_disease_prediction(
    disease,
    confidence,
    image=None,
    user_id=None
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO disease_predictions
    (user_id, image, disease, confidence)
    VALUES (?, ?, ?, ?)
    """, (
        user_id,
        image,
        disease,
        confidence
    ))

    conn.commit()
    conn.close()


def save_yield_prediction(
    crop,
    area,
    rainfall,
    temperature,
    humidity,
    soil_ph,
    fertilizer,
    predicted_yield,
    user_id=None
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO yield_predictions
    (
        user_id,
        crop,
        area,
        rainfall,
        temperature,
        humidity,
        soil_ph,
        fertilizer,
        predicted_yield
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        crop,
        area,
        rainfall,
        temperature,
        humidity,
        soil_ph,
        fertilizer,
        predicted_yield
    ))

    conn.commit()
    conn.close()


def get_disease_history():

    conn = get_connection()
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM disease_predictions
    ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data


def get_yield_history():

    conn = get_connection()
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM yield_predictions
    ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data


if __name__ == "__main__":

    create_tables()

    print("Database tables created successfully.")