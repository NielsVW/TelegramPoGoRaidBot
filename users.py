import static_data as s
import json

users = {}


def add_user(user_id, username):
    users[str(user_id)] = username


def add_user_id(user_id):
    users[user_id] = None


def get_username(user_id):
    try:
        result = int(users[user_id])
    except KeyError:
        result = None
    return result


def get_user_id(username):
    try:
        result = int(list(users.keys())[list(users.values()).index(username)])
    except ValueError:
        result = None
    return result


def save_users_to_file():
    try:
        with open(s.get_user_backup_file(), 'w') as file:
            json.dump(users, file, indent=2)
    except:
        return False
    return True


def load_users_from_file():
    global users
    try:
        users = json.load(open(s.get_user_backup_file()))
    except:
        return False
    return True


def make_admin(user_id):
    admins = s.get_admins()
    if user_id not in admins:
        admins.append(user_id)
        s.dump_and_reload_config("TelegramSettings", "admins", ", ".join(map(str, admins)))
        return True
    else:
        return False


def remove_admin(user_id):
    admins = s.get_admins()
    try:
        admins.remove(user_id)
    except ValueError:
        return False
    s.dump_and_reload_config("TelegramSettings", "admins", ", ".join(map(str, admins)))
    return True


def clear_users():
    global users
    users = {}


def print_users():
    print(users)
