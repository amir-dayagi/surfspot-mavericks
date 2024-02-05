from flask import jsonify

# {'id': int, 'name': str, 'email': str, 'sessions': [session_user]}
users = [{'id': 0, 'name': 'Amir Dayagi', 'email': 'amir.dayagi@gmail.com', 'sessions': []}]

next_user_id = 1

def get_users():
    return jsonify(users)

def get_user(id: int):
    # simple search
    for user in users:
        if user['id'] == id:
            return jsonify(user)
    return False # handle errors later

def create_user(user_json: 'user_schema'):
    global next_user_id
    user_json['id'] = next_user_id
    user_json['sessions'] = []
    next_user_id += 1
    users.append(user_json)

def delete_user(id: int):
    for i, user in enumerate(users):
        if user['id'] == id:
            break
    del users[i]

