import static_data as s
import datetime as dt
import users as u
import json
import collections

from telegram import Location

raids = collections.OrderedDict()
global_raid_id = "0"


def increment_global_raid_id():
    global global_raid_id
    global_raid_id = str(int(global_raid_id) + 1)


def reset_raids():
    global global_raid_id
    raids.clear()
    init_raid()
    global_raid_id = "0"


def init_raid():
    raids[global_raid_id] = {
        "boss": "",
        "moveset": ["???", "???"],
        "gym": "",
        "location": {},
        "opens": "",
        "timeslots": [],
        "players": {},
        "message_id": 0
    }


def remove_raid(raid_id):
    print("removed raid:\n" + str(raids.pop(raid_id, None)))


# @s.timing
def save_raids_to_file():
    try:
        with open(s.get_raid_backup_file(), 'w') as file:
            out = {}
            out["global_raid_id"] = global_raid_id
            out["raids"] = raids
            json.dump(out, file, indent=2)
    except:
        return False
    return True


def load_raids_from_file():
    global raids
    global global_raid_id
    try:
        from_file = json.load(open(s.get_raid_backup_file()))
        global_raid_id = from_file["global_raid_id"]
        raids = from_file["raids"]
    except:
        return False
    return True


def add_player_to_raid(username, raid_id, timeslot):
    raids[raid_id]["players"][username] = {
        "persons": 0,
        "coming": True,
        "arrived": False,
        "timeslot": timeslot
    }


def add_person_to_player(username, raid_id):
    raids[raid_id]["players"][username]['persons'] += 1


def remove_person_from_player(username, raid_id):
    if raids[raid_id]["players"][username]["persons"] > 0:
        raids[raid_id]["players"][username]["persons"] -= 1


def remove_player_from_raid(username, raid_id):
    raids[raid_id]["players"][username]['coming'] = False
    raids[raid_id]["players"][username]["arrived"] = False


def player_has_arrived(username, raid_id):
    raids[raid_id]["players"][username]["arrived"] = True


def get_message_id(raid_id):
    return raids[raid_id]["message_id"]


def set_message_id(raid_id, message_id):
    raids[raid_id]["message_id"] = message_id


def set_boss(raid_id, boss_id):
    raids[raid_id]["boss"] = get_boss_name(boss_id)


def set_boss_by_name(raid_id, boss_name):
    raids[raid_id]["boss"] = boss_name


def set_gym(raid_id, gym):
    raids[raid_id]["gym"] = gym


def set_location_with_object(raid_id, location):
    raids[raid_id]["location"]["longitude"] = location["longitude"]
    raids[raid_id]["location"]["latitude"] = location["latitude"]


def set_location_with_dict(raid_id, location):
    raids[raid_id]["location"] = location


def set_opentime(raid_id, time):
    raids[raid_id]["opens"] = time


def set_timeslots(raid_id, timeslots):
    raids[raid_id]["timeslots"] = timeslots


def get_timeslots(raid_id):
    return raids[raid_id]["timeslots"]


def set_moveset(raid_id, moveset):
    raids[raid_id]["moveset"] = get_moveset_names(moveset)


def get_moveset(raid_id):
    return raids[raid_id]["moveset"]


def get_moveset_names(moveset):
    try:
        quick = s.moves[moveset[0]]
    except KeyError:
        quick = "???"
    try:
        charged = s.moves[moveset[1]]
    except KeyError:
        charged = "???"
    return [quick, charged]


def get_boss(raid_id):
    return raids[raid_id]["boss"]


def get_boss_name(boss_id):
    try:
        boss = s.pokemon[boss_id]
    except KeyError:
        boss = "???"
    return boss


def get_boss_id(boss_name):
    return s.current_bosses[boss_name]


def get_gym(raid_id):
    return raids[raid_id]["gym"]


def get_location_as_string(raid_id):
    return raids[raid_id]["location"]["longitude"] + ", " + raids[raid_id]["location"]["latitude"]


def get_location_as_dict(raid_id):
    return raids[raid_id]["location"]


def get_location_as_object(raid_id):
    return Location(raids[raid_id]["location"]["longitude"], raids[raid_id]["location"]["latitude"])


def get_opentime(raid_id):
    return raids[raid_id]["opens"]


def get_opentime_from_end(end):
    end_obj = dt.datetime.fromtimestamp(end)
    return end_obj - dt.timedelta(minutes=45)


def calculate_end_time(start_obj):
    end_obj = start_obj + s.RAID_DURATION
    return end_obj


def is_raid_ongoing(raid_id):
    try:
        start = raids[raid_id]["opens"]
    except KeyError:
        return False
    start_obj = parse_time_string(start)
    end_obj = calculate_end_time(start_obj)
    return end_obj.time() > dt.datetime.now().time()


def parse_time_string(time):
    try:
        result = dt.datetime.strptime(time, '%H:%M')
    except ValueError:
        try:
            result = dt.datetime.strptime(time, '%H:%M:%S')
        except ValueError:
            result = None
    return result


def calculate_timeslots(start_obj):
    slot1 = start_obj + dt.timedelta(minutes=5)
    slot2 = start_obj + dt.timedelta(minutes=33)
    slot1 = roundTime(slot1, 60*5)
    slot2 = roundTime(slot2, 60*5)
    return slot1.strftime('%H:%M'), slot2.strftime('%H:%M')


def roundTime(obj=None, roundTo=60):
    """Round a datetime object to any time laps in seconds
    dt : datetime.datetime object, default now.
    roundTo : Closest number of seconds to round to, default 1 minute.
    Author: Thierry Husson 2012 - Use it as you want but don't blame me.
    """
    if obj is None: obj = dt.datetime.now()
    seconds = (obj.replace(tzinfo=None) - obj.min).seconds
    rounding = (seconds+roundTo/2) // roundTo * roundTo
    return obj + dt.timedelta(0, rounding-seconds, -obj.microsecond)


def to_bold(string):
    return "*" + string + "*"


def check_raids():
    result = []
    for raid_id in raids.keys():
        if not is_raid_ongoing(raid_id):
            result.append(raid_id)
    return result


def get_player_level(player):
    result = ""
    user_id = u.get_user_id(player)
    if user_id is not None:
        result = "(lvl%d) " % u.get_user_level(user_id)
    return result


def get_raid_info_as_string(raid_id):
    return get_boss_line(raid_id) + get_gym_line(raid_id) + get_time_line(raid_id)


def get_time_line(raid_id):
    result = "Opent om %s\n" % raids[raid_id]["opens"]
    return result


def get_gym_line(raid_id):
    gym = get_gym(raid_id)
    result = "Gym naam: %s\n" % (gym)
    return result


def get_boss_line(raid_id):
    moveset = get_moveset(raid_id)
    boss = get_boss(raid_id)
    if moveset[0] == "???" and moveset[1] == "???":
        result = "%s Raid\n" % (to_bold(boss))
    else:
        result = "%s (%s / %s) Raid\n" % (to_bold(boss), moveset[0], moveset[1])
    return result


def get_raid_info_with_loc_as_string(raid_id):
    return get_raid_info_as_string(raid_id) + get_location_as_string(raid_id)


def timeslot_to_icon_string(slot):
    if slot == 0:
        return s.TIMESLOT1_ICON
    else:
        return s.TIMESLOT2_ICON


def slots_to_string(slots, slot1, slot2):
    slot2_string = ""
    if slot2 is not None:
        slot2_string = "\n  Moment %s %s:\n%s" % (s.TIMESLOT2_ICON, slots[1], slot2)
    return "  Moment %s %s:\n%s%s" % (s.TIMESLOT1_ICON, slots[0], slot1, slot2_string)


def get_players_as_string(raid_id):
    result = "\nSpelers die komen:\n"
    players_coming = [0, 0]
    players_arrived = [0, 0]
    slot1 = ""
    slot2 = ""
    for player in raids[raid_id]["players"]:
        coming = raids[raid_id]["players"][player]['coming']
        slot = raids[raid_id]["players"][player]["timeslot"]
        if coming:
            line = "   %s %s%s" % ("└", get_player_level(player), player)
            players_coming[slot] += 1
        else:
            line = "   ❌ %s%s" % (player, get_player_level(player))
        persons = raids[raid_id]["players"][player]['persons']
        if persons > 0:
            line = line + " +" + str(persons)
        arrived = raids[raid_id]["players"][player]['arrived']
        if arrived and coming:
            line = line + "  🆗"
            players_arrived[slot] += 1
        line = line + "\n"
        if slot == 0:
            slot1 = slot1 + line
        else:
            slot2 = slot2 + line
    slots = get_timeslots(raid_id)
    diff2 = players_coming[1] - players_arrived[1]
    if slots[1] is None:
        slot2 = None
        diff2 = None
    result = result + slots_to_string(slots, slot1, slot2)
    return result, players_coming[0] - players_arrived[0], diff2


def get_can_start_message(diff, slot_icon):
    can_start = "\n%s " % slot_icon
    if diff is None:
        return ""
    if diff <= 0:
        can_start = can_start + to_bold("Iedereen is aanwezig!")
    elif diff == 1:
        can_start = can_start + "Er moet nog *één* iemand komen"
    else:
        can_start = can_start + "Er moeten nog " + to_bold(str(diff)) + " spelers komen"
    return can_start


def get_full_raid_message(raid_id):
    players, diff1, diff2 = get_players_as_string(raid_id)
    return get_raid_info_as_string(raid_id) + players + get_can_start_message(diff1, s.TIMESLOT1_ICON) + get_can_start_message(diff2, s.TIMESLOT2_ICON)
