import requests
import sqlite3
import json
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import time


# L'URL de base de l'API
BASE_URL = "http://127.0.0.1:8000"

# Requête GET pour récupérer la liste des morceaux (tracks)
def get_tracks():
    tracks_data = None
    response_tracks = requests.get(f"{BASE_URL}/tracks")
    if response_tracks.status_code == 200:
        tracks_data = response_tracks.json()['items']
    else:
        print(f"Erreur lors de la récupération des morceaux: {response_tracks.status_code}")
    return tracks_data

# Requête GET pour récupérer la liste des utilisateurs (users)
def get_users():
    users_data = None
    response_users = requests.get(f"{BASE_URL}/users")
    if response_users.status_code == 200:
        users_data = response_users.json()['items']
    else:
        print(f"Erreur lors de la récupération des utilisateurs: {response_users.status_code}")
    return users_data

# Requête GET pour récupérer l'historique des écoutes (listen_history)
def get_listen_history():
    listen_history_data = None
    response_listen_history = requests.get(f"{BASE_URL}/listen_history")
    if response_listen_history.status_code == 200:
        listen_history_data = response_listen_history.json()['items']
    else:
        print(f"Erreur lors de la récupération de l'historique des écoutes: {response_listen_history.status_code}")
    return listen_history_data



### BDD ###
def create_tables(conn):
    conn.execute('''
    CREATE TABLE IF NOT EXISTS musiques (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        artist TEXT NOT NULL,
        songwriters TEXT NOT NULL,
        duration TEXT NOT NULL,
        genres TEXT NOT NULL,
        album TEXT NOT NULL,
        created_at DATETIME NOT NULL,
        updated_at DATETIME NOT NULL
    )
    ''')

    conn.execute('''
    CREATE TABLE IF NOT EXISTS utilisateurs (
        id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL,
        gender TEXT NOT NULL,
        favorite_genres TEXT NOT NULL,
        created_at DATETIME NOT NULL,
        updated_at DATETIME NOT NULL
    )
    ''')

    conn.execute('''
    CREATE TABLE IF NOT EXISTS historiques (
        user_id INTEGER NOT NULL,
        musique_id INTEGER NOT NULL,
        created_at DATETIME NOT NULL,
        updated_at DATETIME NOT NULL,
        PRIMARY KEY (user_id, musique_id),
        FOREIGN KEY (user_id) REFERENCES utilisateurs(id),
        FOREIGN KEY (musique_id) REFERENCES musiques(id)
    )
    ''')
    conn.commit()

def post_users(conn, users):
    query = '''
    INSERT INTO utilisateurs (id, first_name, last_name, email, gender, favorite_genres, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(id) DO UPDATE SET
        first_name = excluded.first_name,
        last_name = excluded.last_name,
        email = excluded.email,
        gender = excluded.gender,
        favorite_genres = excluded.favorite_genres,
        created_at = excluded.created_at,
        updated_at = excluded.updated_at
    '''
    try:
        with conn: 
            conn.executemany(query, [
                (
                    user['id'],
                    user['first_name'],
                    user['last_name'],
                    user['email'],
                    user['gender'],
                    user['favorite_genres'],
                    user['created_at'],
                    user['updated_at']
                )
                for user in users
            ])
    except sqlite3.Error as e:
        print(f"Erreur lors de l'insertion en batch : {e}")
    
def read_users(conn):
    cur = conn.cursor()

    cur.execute("SELECT * FROM utilisateurs")
    for row in cur.fetchall():
        print(row)

    
def post_tracks(conn, tracks):
    query = '''
    INSERT INTO musiques (id, name, artist, songwriters, duration, genres, album, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(id) DO UPDATE SET
        name = excluded.name,
        artist = excluded.artist,
        songwriters = excluded.songwriters,
        duration = excluded.duration,
        genres = excluded.genres,
        album = excluded.album,
        created_at = excluded.created_at,
        updated_at = excluded.updated_at
    '''
    try:
        with conn: 
            conn.executemany(query, [
                (
                    track['id'],
                    track['name'],
                    track['artist'],
                    track['songwriters'],
                    track['duration'],
                    track['genres'],
                    track['album'],
                    track['created_at'],
                    track['updated_at']
                )
                for track in tracks
            ])
    except sqlite3.Error as e:
        print(f"Erreur lors de l'insertion en batch : {e}")
        
def read_tracks(conn):
    cur = conn.cursor()

    cur.execute("SELECT * FROM musiques")
    for row in cur.fetchall():
        print(row)

def post_listen_histories(conn, formatted_history):
    query = '''
    INSERT INTO historiques (user_id, musique_id, created_at, updated_at)
    VALUES (?, ?, ?, ?)
    ON CONFLICT(user_id,musique_id) DO UPDATE SET
        updated_at = excluded.updated_at
    '''
    try:
        with conn:
            conn.executemany(query, [
                (entry["user_id"], entry["musique_id"], entry["created_at"],entry["updated_at"])
                for entry in formatted_history
            ])
    except sqlite3.Error as e:
        print(f"Erreur lors de l'insertion en batch : {e}")
    
def read_history(conn):
    cur = conn.cursor()

    cur.execute("SELECT * FROM historiques")
    for row in cur.fetchall():
        print(row)


### MAIN ###

def format_history(histories, tracks):
    formatted_history = []

    for history in histories:
        user_id = history["user_id"] 
        for track_id in history["items"]:
            formatted_history.append({
                "user_id": user_id,
                "musique_id": track_id,
                "created_at": history["created_at"], 
                "updated_at": history["updated_at"] 
            })

    return formatted_history
            

def run_main_logic():
    conn = sqlite3.connect('ma_base_de_donnees.db')
    create_tables(conn)
    
    
    ### Get DATA
    tracks = get_tracks()
    users = get_users()
    history = get_listen_history()
    
    ### Build DATA
    post_users(conn, users)
    post_tracks(conn, tracks)
    
    formatted_history = format_history(history, tracks)
    post_listen_histories(conn, formatted_history)
    
    # Debug
    read_tracks(conn)
    read_users(conn)
    read_history(conn)

    conn.close()
    
if __name__ == "__main__":
    scheduler = BackgroundScheduler()

    scheduler.add_job(run_main_logic, 'interval', days=1, id='daily_job')   
    # scheduler.add_job(run_main_logic, 'interval', minutes=1, id='daily_job')


    print("Le planificateur est lancé. Le script s'exécutera une fois par jour.")
    run_main_logic() # Premier lancement
    try:
        while True:
            time.sleep(1)  # Le programme continue de tourner en attendant des interruptions
    except (KeyboardInterrupt, SystemExit):
        print("Arrêt du planificateur.")
#        scheduler.shutdown()  # Arrêt propre du planificateur

