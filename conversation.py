from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode)
from telegram.ext import (CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
import logging
import raid as r
import static_data as s
from keyboard import get_keyboard, get_bosses_keyboard

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

BOSS, GYM, LOCATION, OPENS, SLOT = range(5)
REMOVE_RAID_BOSS = range(1)


def start(bot, update):
    reply_keyboard = get_bosses_keyboard()
    user = update.message.from_user.username
    r.init_raid()

    update.message.reply_text(
        'Hallo %s! Ik zal je helpen om een raid toe te voegen. '
        'Stuur /cancel op elk moment om te stoppen.\n\n'
        'Welke raid gaat starten?' % user,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, selective=True))

    return BOSS


def boss(bot, update):
    user = update.message.from_user
    bossname = update.message.text
    if bossname not in s.pokemon.values():
        return BOSS
    r.set_boss_by_name(r.global_raid_id, bossname)
    logger.info("Boss selected by %s: %s", user.username, bossname)
    update.message.reply_text('Wat is de naam van de gym?',
                              reply_markup=ReplyKeyboardRemove())
    return GYM


def gym(bot, update):
    user = update.message.from_user
    gymname = update.message.text
    r.set_gym(r.global_raid_id, gymname)
    logger.info("Gym selected by user %s: %s", user.username, gymname)
    update.message.reply_text('Episch! Stuur me de locatie van de raid aub.')

    return LOCATION


def location(bot, update):
    user = update.message.from_user
    user_location = update.message.location
    r.set_location_with_object(r.global_raid_id, user_location)
    logger.info("Location of the raid %s: %f / %f", user.username, user_location.latitude,
                user_location.longitude)
    update.message.reply_text('Super, wanneer opent de raid en gebruik het volgende formaat: hh:mm(:ss).')
    return OPENS


def opens(bot, update):
    user = update.message.from_user
    message = update.message
    time_str = message.text
    time_obj = r.parse_time_string(time_str)
    if time_obj is None:
        bot.send_message(chat_id=update.message.chat_id, text="Dat is geen correct formaat, gebruik dit aub: HH:mm(:ss).")
        return OPENS
    r.set_opentime(r.global_raid_id, time_str)
    logger.info("Open time %s: %s", user.username, time_str)
    update.message.reply_text("Geef nu het moment wanneer jullie willen starten met de raid. Gebruik het volgende formaat: hh:mm.")

    return SLOT


def slot(bot, update):
    user = update.message.from_user
    message = update.message
    time_str = message.text
    time_obj = r.parse_time_string(time_str)
    if time_obj is None:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Dat is geen correct formaat, gebruik dit aub: HH:mm.")
        return SLOT
    r.set_timeslots(r.global_raid_id, [time_str, None])
    logger.info("Timeslot %s: %s", user.username, time_str)
    finalize_add(bot, update)
    return ConversationHandler.END


def finalize_add(bot, update):
    update.message.reply_text('Bedankt! Dus om samen te vatten:\n' +
                              r.get_raid_info_as_string(r.global_raid_id), parse_mode=ParseMode.MARKDOWN)
    bot.send_location(chat_id=update.message.chat_id, location=r.get_location_as_object(r.global_raid_id))
    post_in_group(bot)
    r.save_raids_to_file()
    r.increment_global_raid_id()


def post_in_group(bot):
    reply_markup = get_keyboard(r.global_raid_id)
    bot.send_location(chat_id=s.group_chat_id, location=r.get_location_as_object(r.global_raid_id))
    message = bot.send_message(chat_id=s.group_chat_id, text=r.get_raid_info_as_string(r.global_raid_id), reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    r.set_message_id(r.global_raid_id, message.message_id)


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.username)
    update.message.reply_text('Toevoegen van een raid is geannuleerd!',
                              reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def get_add_raid_handler():
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler(command='addRaid', callback=start, filters=Filters.user(s.get_admins()))],

        states={
            BOSS: [MessageHandler(Filters.text, boss)],

            GYM: [MessageHandler(Filters.text, gym)],

            LOCATION: [MessageHandler(Filters.location, location)],

            OPENS: [MessageHandler(Filters.text, opens)],

            SLOT: [MessageHandler(Filters.text, slot)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )
    return conv_handler


def remove_raid_boss_start(bot, update):
    user = update.message.from_user
    bossname = update.message.text
    update.message.reply_text("Welke raid boss wil je verwijderen? Stoppen met /cancel", reply_markup=ReplyKeyboardMarkup(get_bosses_keyboard(), one_time_keyboard=True, selective=True))
    return REMOVE_RAID_BOSS


def remove_raid_boss(bot, update):
    bossname = update.message.text
    if s.remove_raid_boss(bossname):
        update.message.reply_text("Ok, %s is geen raid boss meer" % bossname)
    else:
        update.message.reply_text("Er ging iets mis of %s is al een raid boss" % bossname)
    return ConversationHandler.END


def cancel_remove_boss(bot, update):
    update.message.reply_text("Verwijderen van een raid boss is geannuleerd!", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def get_remove_raid_boss_handler():
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler(command='removeRaidBoss', callback=remove_raid_boss_start, filters=Filters.user(s.get_admins()))],

        states={
            REMOVE_RAID_BOSS: [RegexHandler('^(' + "|".join(s.get_current_raid_bosses()) + ')$', remove_raid_boss)]
        },

        fallbacks=[CommandHandler('cancel', cancel_remove_boss)]
    )
    return conv_handler
