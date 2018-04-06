import static_data as s
import json
import collections

users = collections.OrderedDict()


def add_user(user_id, username):
    user_id = str(user_id)
    if user_id not in users:
        add_user_id(user_id)
    users[user_id]["username"] = username


def add_user_and_save_on_changes(user_id, username):
    user_id = str(user_id)
    if user_id in users:
        if users[user_id]["username"] != username:
            users[user_id]["username"] = username
            save_users_to_file()
            return
    else:
        add_user(user_id, username)
        save_users_to_file()


def add_user_id(user_id):
    users[str(user_id)] = {
        "username": "",
        "level": 0,
        "colour": ""
    }


def set_user_level(user_id, level):
    users[str(user_id)]["level"] = int(level)
    save_users_to_file()


def set_user_colour(user_id, colour):
    users[str(user_id)]["colour"] = colour
    save_users_to_file()


def get_user_level(user_id):
    return int(users[str(user_id)]["level"])


def get_user_colour(user_id):
    return users[str(user_id)]["colour"]


def get_username(user_id):
    try:
        username = str(users[str(user_id)]["username"])
    except KeyError:
        username = None
    return username


def get_user_id(username):
    for user_id in users.keys():
        if users[user_id]["username"] == username:
            return user_id
    return None


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
    user_id = int(user_id)
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
        admins.remove(int(user_id))
    except ValueError:
        return False
    s.dump_and_reload_config("TelegramSettings", "admins", ", ".join(map(str, admins)))
    return True


def clear_users():
    global users
    users = {}


def print_users():
    print(users)
