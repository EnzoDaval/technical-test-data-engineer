import datetime
import pytest
from script import format_history, create_tables, post_listen_histories
import sqlite3


@pytest.fixture
def sample_histories():
    return [
        {"user_id": 1, "items": [101, 102, 103], "created_at": "2024-11-12T02:32:18.150597", "updated_at": "2025-01-12T16:33:42.125577"},
        {"user_id": 2, "items": [104, 105, 101], "created_at": "2024-11-12T02:32:18.150597", "updated_at": "2025-01-12T16:33:42.125577"}
    ]

@pytest.fixture
def sample_tracks():
    return [
        {"id": 101, "name": "Song A", "artist": "Artist A"},
        {"id": 102, "name": "Song B", "artist": "Artist B"},
        {"id": 103, "name": "Song C", "artist": "Artist C"},
        {"id": 104, "name": "Song D", "artist": "Artist D"},
        {"id": 105, "name": "Song E", "artist": "Artist E"}
    ]

@pytest.fixture
def sample_formatted_histories():
    return [
        {"user_id": 1, "musique_id": 101, "created_at": "2024-11-12T02:32:18.150597", "updated_at": "2025-01-12T16:33:42.125577"},
        {"user_id": 1, "musique_id": 102, "created_at": "2024-11-12T02:32:18.150597", "updated_at": "2025-01-12T16:33:42.125577"},
        {"user_id": 1, "musique_id": 103, "created_at": "2024-11-12T02:32:18.150597", "updated_at": "2025-01-12T16:33:42.125577"},
        {"user_id": 2, "musique_id": 104, "created_at": "2024-11-12T02:32:18.150597", "updated_at": "2025-01-12T16:33:42.125577"},
        {"user_id": 2, "musique_id": 105, "created_at": "2024-11-12T02:32:18.150597", "updated_at": "2025-01-12T16:33:42.125577"},
        {"user_id": 2, "musique_id": 101, "created_at": "2024-11-12T02:32:18.150597", "updated_at": "2025-01-12T16:33:42.125577"}
    ]

## Testing format_history
def test_format_history(sample_histories, sample_tracks):
    formatted_history = format_history(sample_histories, sample_tracks)

    assert len(formatted_history) == 6  # 6 éléments dans l'historique attendu

    assert formatted_history[0]["user_id"] == 1
    assert formatted_history[0]["musique_id"] == 101

    assert formatted_history[1]["user_id"] == 1
    assert formatted_history[1]["musique_id"] == 102

    assert formatted_history[4]["user_id"] == 2
    assert formatted_history[4]["musique_id"] == 105

#utils
def reset_table(table_name):
    conn = sqlite3.connect(table_name)

    conn.execute("DROP TABLE IF EXISTS musiques;")
    conn.execute("DROP TABLE IF EXISTS utilisateurs;")
    conn.execute("DROP TABLE IF EXISTS historiques;")

    conn.commit()
    conn.close()
    
def test_post_listen_histories(sample_formatted_histories):
    reset_table('ma_base_de_donnees_de_test.db')
    
    conn = sqlite3.connect('ma_base_de_donnees_de_test.db')
    create_tables(conn)
    
    post_listen_histories(conn, sample_formatted_histories)
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM historiques;")
    entries = cursor.fetchall()
    
    assert len(entries) == 6
    assert entries[0][0] == sample_formatted_histories[0]["user_id"]
    assert entries[2][1] == sample_formatted_histories[2]["musique_id"]
    assert entries[3][0] == sample_formatted_histories[3]["user_id"]
    assert entries[5][1] == sample_formatted_histories[5]["musique_id"]
    
def test_run_main_logic():
    

    
