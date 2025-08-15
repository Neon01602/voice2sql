import sqlite3
import mysql.connector
import psycopg2
import requests
import getpass
import threading
import speech_recognition as sr
import time

# === Console Logger ===
def log(message):
    print(message)

# Gemini API config
GEMINI_API_KEY = "AIzaSyDHYLmJVPAPV9hj722jgSWgsEMg3EqU1R0"
api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

SUPPORTED_ENGINES = ['sqlite', 'mysql', 'postgresql']

# === Voice Input ===
def get_voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        log("Speak your query:")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        log(f"Recognized text: {text}")
        return text
    except sr.UnknownValueError:
        log("Stop singing and say something interpretable!")
    except sr.RequestError as e:
        log(f"Sorry, could'nt fetch your vocals (Too sweet): {e}")
    return None

# === Gemini Conversion ===
def convert_to_sql_gemini(nl_query, db_type):
    prompt = f"""
Convert the following natural language command into a valid SQL query for a {db_type} database.
Return only the SQL query as raw text — no markdown, comments, or extra formatting.

Command: {nl_query}
"""
    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    response = requests.post(api_url, json=payload)
    if response.status_code == 200:
        try:
            text = response.json()['candidates'][0]['content']['parts'][0]['text']
            cleaned = text.strip().replace("```sql", "").replace("```", "").strip()
            return cleaned
        except Exception as e:
            log("Sorry, i have Dyslexia. Please try again." + str(e))
    else:
        log(f"Bot crashed! {response.status_code}: {response.text}")
    return None

# === Execute SQL ===
def connect_and_execute_sql(db_type, db_config, sql_query):
    conn = None
    cursor = None
    try:
        if db_type == "sqlite":
            conn = sqlite3.connect(db_config['database'])
        elif db_type == "mysql":
            conn = mysql.connector.connect(
                host=db_config['host'],
                port=db_config['port'],
                user=db_config['user'],
                password=db_config['password'],
                database=db_config['database']
            )
        elif db_type == "postgresql":
            conn = psycopg2.connect(
                host=db_config['host'],
                port=db_config['port'],
                user=db_config['user'],
                password=db_config['password'],
                dbname=db_config['database']
            )
        else:
            log("You sure this is a kind of DB?")
            return

        cursor = conn.cursor()
        cursor.execute(sql_query)

        if cursor.description:  # SELECT-like query
            rows = cursor.fetchall()
            log("Results:")
            for row in rows:
                log(str(row))
        else:
            conn.commit()
            log("Query executed successfully.")

    except Exception as e:
        log(f"Error executing SQL: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# === DB Config ===
def get_db_config(db_type):
    if db_type == "sqlite":
        filename = input("Enter SQLite database filename (e.g., data.db): ")
        return {'database': filename}
    else:
        host = input("DB Host (e.g., localhost): ")
        port = input("DB Port (default: 5432 for PostgreSQL, 3306 for MySQL): ")
        user = input("DB Username: ")
        password = getpass.getpass("DB Password: ")
        database = input("DB Name: ")

        return {
            'host': host,
            'port': int(port) if port else (5432 if db_type == "postgresql" else 3306),
            'user': user,
            'password': password,
            'database': database
        }

# === Main Loop ===
def run_main():
    db_type = input("Enter DB type (sqlite/mysql/postgresql): ").strip().lower()
    if db_type not in SUPPORTED_ENGINES:
        log("Unsupported DB type.")
        return

    db_config = get_db_config(db_type)
    log("Database configuration saved. Ready for voice commands.")

    while True:
        log("\nDo mind not to sing and only put query (Say 'exit' or 'quit' to stop)")
        voice_input = get_voice_input()

        if not voice_input:
            continue

        if voice_input.lower().strip() in ['exit', 'quit', 'stop']:
            log("Have a grat day mate!")
            break

        sql = convert_to_sql_gemini(voice_input, db_type)
        if not sql:
            log("Try again, I could'nt generate the query.")
            continue

        log(f"\nGenerated SQL (Is it Okay?):\n{sql}\n")
        confirm = input("Execute this query? (y/n or q to quit): ").strip().lower()
        if confirm == 'y':
            connect_and_execute_sql(db_type, db_config, sql)
        elif confirm == 'q':
            log("Goodbye Mate!")
            break
