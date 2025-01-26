import mysql.connector
import time

def initialize_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="comfrog",
    )
    cursor = conn.cursor()
    cursor.execute("USE pycard")

    return conn, cursor


def register(conn, cursor, data):
    try:
        cursor.execute(f"INSERT INTO users (username, password) values('{data['username']}','{data['password']}')")
        conn.commit()
        return login(cursor, data)
    except:
        return False


def is_already_exist(cursor, username):
    try:
        cursor.execute(f"SELECT username FROM users WHERE username = '{username}'")
        user = cursor.fetchone()
        return True if user is not None else False
    except:
        return False


def login(cursor, data):
    try:
        cursor.execute(
            f"SELECT id,username FROM users WHERE username = '{data['username']}' AND password = '{data['password']}'")
        result = cursor.fetchone()
        user = {}
        user["id"] = result[0]
        user["username"] = result[1]
        return user if result is not None else None
    except:
        return None


def create_flashcard(conn, cursor, user_id, name, cards, time_limit):
    try:
        id = round(time.time() * 1000)
        cursor.execute(f"INSERT INTO flashcards (flashcard_id, flashcard_name, user_id, completed_decks, score, heart_count, remaining_time, total_decks) values('{id}','{name}','{user_id}', 0, 0, {len(cards) * 2}, {time_limit}, {len(cards)})")
        # conn.commit()
        sql = "INSERT INTO cards (flashcard_id, card_description, card_answer) VALUES (%s, %s, %s)"
        val = []
        for i in range(len(cards)):
            val.append((f'{id}',f'{cards[i]["desc"]}', f'{cards[i]["ans"]}'))
        cursor.executemany(sql, val)
        conn.commit()
        return True
    except:
        return False

def get_flashcards(cursor, user_id):
    try:
        cursor.execute(
            f"SELECT * FROM flashcards WHERE user_id = '{user_id}'")
        result = cursor.fetchall()
        flashcard = []
        for i in range(len(result)):
            temp = {}
            temp["id"] = result[i][0]
            temp["name"] = result[i][1]
            temp["completed"] = result[i][2]
            temp["score"] = result[i][3]
            temp["heart"] = result[i][4]
            temp["start"] = result[i][5]
            temp["remaining"] = result[i][6]
            temp["total"] = result[i][7]
            flashcard.append(temp)
        print(flashcard)
        return flashcard if result is not None else None
    except:
        return None
def get_flashcard_by_id(cursor,id):
    try:
        cursor.execute(
            f"SELECT * FROM flashcards WHERE flashcard_id = '{id}'")
        result = cursor.fetchone()
        temp = {}
        temp["id"] = result[0]
        temp["name"] = result[1]
        temp["completed"] = result[2]
        temp["score"] = result[3]
        temp["hearts"] = result[4]
        return temp if result is not None else None
    except:
        return None

    pass
def get_cards_by_id(cursor,id):
    try:
        cursor.execute(
            f"SELECT * FROM cards WHERE flashcard_id = '{id}'")
        result = cursor.fetchall()
        cards = []
        for i in range(len(result)):
            temp = {}
            temp["id"] = result[i][0]
            temp["name"] = result[i][1]
            temp["description"] = result[i][2]
            temp["answer"] = result[i][3]
            cards.append(temp)
        print(cards)
        return cards if result is not None else None
    except:
        return None

def timeLimitMinusOne(conn, cursor, flashcard_id):
    try:
        cursor.execute(
            f"SELECT remaining_time FROM flashcards WHERE flashcard_id = '{flashcard_id}'")
        result = cursor.fetchone()
        remaining = int(result[0]) - 1
        cursor.execute(f"UPDATE flashcards SET remaining_time = '{int(result[0]) - 1}' WHERE flashcard_id = '{flashcard_id}'")
        conn.commit()
        return remaining
    except:
        return -1

def heartMinusOne(conn, cursor, flashcard_id):
    try:
        cursor.execute(
            f"SELECT heart_count FROM flashcards WHERE flashcard_id = '{flashcard_id}'")
        result = cursor.fetchone()
        remaining = int(result[0]) - 1
        cursor.execute(f"UPDATE flashcards SET heart_count = '{int(result[0]) - 1}' WHERE flashcard_id = '{flashcard_id}'")
        conn.commit()
        return remaining
    except:
        return -1

def completedDeckPlusOne(conn, cursor, flashcard_id):
    try:
        cursor.execute(
            f"SELECT completed_decks FROM flashcards WHERE flashcard_id = '{flashcard_id}'")
        result = cursor.fetchone()
        updatedValue = int(result[0]) + 1
        cursor.execute(f"UPDATE flashcards SET completed_decks = '{updatedValue}' WHERE flashcard_id = '{flashcard_id}'")
        conn.commit()
        return updatedValue
    except:
        return -1


def check_flashcard_by_id(cursor, flashcard_id):
    try:
        cursor.execute(
            f"SELECT completed_decks, total_decks, heart_count, remaining_time, flashcard_name FROM flashcards WHERE flashcard_id = '{flashcard_id}'")
        result = cursor.fetchone()
        response = []
        if result is None:
            return response
        if result[0] == result[1]:
            response.append(f"{result[4]} already completed")
        if result[2] == 0:
            response.append(f"No remaining heart")
        if int(result[3]) <= 0:
            response.append(f"No remaining time")
        return response
    except:
        return []
