import configparser, json, datetime, time


config = configparser.ConfigParser()
config.read("properties.ini")


# button numbers
ADD_PLAYER_BUTTON_SLOT1 = "1"
ADD_PLAYER_BUTTON_SLOT2 = "2"
ADD_PERSON_BUTTON = "3"
REMOVE_PERSON_BUTTON = "4"
PLAYER_ARRIVED_BUTTON = "5"
REMOVE_PLAYER_BUTTON = "6"

# boss keyboard
MAX_COLUMN_WIDTH = 4

# chat ids
group_chat_id = config["TelegramSettings"]["group_chat_id"]

# icons
TIMESLOT1_ICON = "1️⃣"
TIMESLOT2_ICON = "2️⃣"

# teams
INSTINCT = "Instinct"
MYSTIC = "Mystic"
VALOR = "Valor"
INSTINCT_ICON = ""
MYSTIC_ICON = ""
VALOR_ICON = ""
INSTINCT_ACCEPTED = [INSTINCT, "Geel", "Yellow"]
MYSTIC_ACCEPTED = [MYSTIC, "Blauw", "Blue"]
VALOR_ACCEPTED = [VALOR, "Rood", "Red"]

# times
START_TIME = datetime.time(hour=8)
END_TIME = datetime.time(hour=21)
BUFFER_TIME = datetime.timedelta(hours=1, minutes=45)
RAID_DURATION = datetime.timedelta(minutes=int(config["GameData"]["raid_duration"]))


def reload_config():
    global config
    config.read("properties.ini")


def dump_and_reload_config(section, field, value):
    global config
    config.set(section, field, value)
    with open("properties.ini", "w+") as configfile:
        config.write(configfile)
    reload_config()


def get_token():
    return config["TelegramSettings"]["token"]


def get_moves_file():
    try:
        return config["GameData"]["moves_file"]
    except KeyError:
        return "parsed_moves.json"


def get_pokemon_file():
    try:
        return config["GameData"]["pokemon_file"]
    except KeyError:
        return "parsed_pokemon.json"


moves = json.load(open(get_moves_file()))
pokemon = json.load(open(get_pokemon_file()))
region = config["PokeHuntAPI"]["region"]


def get_admins():
    admins = config["TelegramSettings"]["admins"].split(",")
    admins = [int(x) for x in admins]
    return admins


def get_current_raid_bosses():
    bosses = config["GameData"]["current_raid_bosses"].split(",")
    bosses = [x.strip().capitalize() for x in bosses]
    return bosses


def make_current_bosses_dict():
    bosses = get_current_raid_bosses()
    result = {}
    for boss_id, name in pokemon.items():
        if name in bosses:
            result[name] = boss_id
    return result


current_bosses = make_current_bosses_dict()


def remove_raid_boss(bossname):
    bosses = get_current_raid_bosses()
    try:
        bosses.remove(bossname)
    except KeyError:
        return False
    dump_and_reload_config("GameData", "current_raid_bosses", ", ".join(map(str, bosses)))
    return True


def add_raid_boss(bossname):
    bosses = get_current_raid_bosses()
    if bossname not in bosses:
        bosses.append(bossname)
        dump_and_reload_config("GameData", "current_raid_bosses", ", ".join(map(str, bosses)))
        return True
    else:
        return False


def get_raid_backup_file():
    try:
        return config["GameData"]["raid_backup_file"]
    except KeyError:
        return "raids.json"


def get_user_backup_file():
    try:
        return config["TelegramSettings"]["user_backup_file"]
    except KeyError:
        return "users.json"


def get_request_method():
    try:
        return config["TelegramSettings"]["request_method"].lower()
    except KeyError:
        return "polling"


def get_webhook_parameters():
    result = {}
    try:
        result["listen"] = config["TelegramSettings"]["listen"]
    except KeyError:
        result["listen"] = '127.0.0.1'
    try:
        result["port"] = int(config["TelegramSettings"]["port"])
    except KeyError:
        result["port"] = 80
    try:
        result["url_path"] = config["TelegramSettings"]["url_path"]
    except KeyError:
        result["url_path"] = ''
    try:
        result["cert"] = config["TelegramSettings"]["cert"]
    except KeyError:
        result["cert"] = None
    try:
        result["key"] = config["TelegramSettings"]["key"]
    except KeyError:
        result["key"] = None
    try:
        result["webhook_url"] = config["TelegramSettings"]["webhook_url"]
    except KeyError:
        result["webhook_url"] = None
    print(str(result))
    return result


def verify_colour_input(colour):
    colour = colour.capitalize()
    if colour in INSTINCT_ACCEPTED:
        return INSTINCT
    elif colour in MYSTIC_ACCEPTED:
        return MYSTIC
    elif colour in VALOR_ACCEPTED:
        return VALOR
    else:
        return None


def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print('%s function took %0.3f ms' % (f.__name__, (time2-time1)*1000.0))
        return ret
    return wrap
