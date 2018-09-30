from balebot.models.base_models import Peer
from balebot.updater import Updater
from balebot.models.messages import TemplateMessage, TemplateMessageButton, TextMessage
import asyncio
from balebot.utils.logger import Logger
from Bot.template_messages import Message
from balebot.handlers import MessageHandler
from balebot.filters import TemplateResponseFilter, TextFilter
from Database.operations import *
from Bot.models import Person, Reason
from balebot.config import Config
import jdatetime
from Bot.utils import arabic_to_eng_number

Config.use_graylog = "2"

loop = asyncio.get_event_loop()
updater = Updater(token=LigBotConfig.bot_token, loop=loop)
dispatcher = updater.dispatcher
g_peer = Peer(peer_type="Group", peer_id=LigBotConfig.group_id, access_hash=LigBotConfig.group_access_hash)
start_menu_template_message = TemplateMessage(Message.BACK_TO_MAIN_MENU,
                                              [TemplateMessageButton(Message.BACK_TO_MAIN_MENU.text, "/start", 0)])
start_menu_button = [TemplateMessageButton(Message.BACK_TO_MAIN_MENU.text, "/start", 0)]

logger = Logger()
logger = logger.get_logger()


def success(bot, result):
    print("success sent message : ", result)


def failure(bot, result):
    print("failure sent message : ", result)


main_menu_button = [
    TemplateMessageButton(Message.BACK_TO_MAIN_MENU.text, "/start", 0)
]


def get_pin_type_from_number(pin_number):
    return (pin_number == 1 and Message.LEARNING) or (pin_number == 2 and Message.HARDWORKING) or (
            pin_number == 3 and Message.RESPONSIBILITI) or (pin_number == 4 and Message.TEAMWORKING) or (
                   pin_number == 5 and Message.PRODUCT_CONCERN) or (pin_number == 6 and Message.OTHER)


@dispatcher.command_handler(["/start"])
@dispatcher.message_handler([TemplateResponseFilter(keywords=["/start"]), TextFilter(keywords=["/start"])])
def start_bot(bot, update):
    user_peer = update.get_effective_user()
    logger.info("receiving :  " + TextMessage("/start").get_json_str())
    logger.info("Bot started")
    logger.info("user :   " + user_peer.get_json_str())
    button_list = ((user_peer.get_json_object()["id"] != LigBotConfig.admin_user_id and is_registered(
        user_peer.get_json_object()["id"])) and [
                       TemplateMessageButton(Message.HOW_MANY_PINS_I_HAVE, "/pin_number", 0),
                       TemplateMessageButton(Message.I_WANT_TO_GIVE_PIN, "/give_pin", 0),
                       TemplateMessageButton(Message.REGISTER, "/add_person", 0)
                   ]) or ((user_peer.get_json_object()["id"] == LigBotConfig.admin_user_id and is_registered(
        user_peer.get_json_object()["id"])) and [
                              TemplateMessageButton(Message.HOW_MANY_PINS_I_HAVE, "/pin_number", 0),
                              TemplateMessageButton(Message.I_WANT_TO_GIVE_PIN, "/give_pin", 0),
                              TemplateMessageButton(Message.DELETE_FROM_LIG, "/delete_person", 0),
                              TemplateMessageButton(Message.REGISTER, "/add_person", 0)
                          ]) or (not is_registered(user_peer.get_json_object()["id"]) and [
        TemplateMessageButton(Message.REGISTER, "/add_person", 0)]) or (
                          is_registered(user_peer.get_json_object()["id"]) and [
                      TemplateMessageButton(Message.HOW_MANY_PINS_I_HAVE, "/pin_number", 0),
                      TemplateMessageButton(Message.I_WANT_TO_GIVE_PIN, "/give_pin", 0)])

    bot.send_message(TemplateMessage(Message.START_MESSAGE, btn_list=button_list), user_peer, success_callback=success,
                     failure_callback=failure)

    dispatcher.register_conversation_next_step_handler(update, [
        MessageHandler(TemplateResponseFilter(keywords=["/pin_number"]), send_pin_number),
        MessageHandler(TemplateResponseFilter(keywords=["/give_pin"]), give_pin),
        MessageHandler(TemplateResponseFilter(keywords=["/add_person"]), start_register_conversation),
        MessageHandler(TemplateResponseFilter(keywords=["/delete_person"]), delete_person)
    ])


@dispatcher.command_handler("/pin_number")
@dispatcher.message_handler(TemplateResponseFilter(keywords=["/pin_number"]))
def send_pin_number(bot, update):
    user_peer = update.get_effective_user()
    target_person = get_pin_numbers(user_peer.get_json_object()["id"])
    pin_number = target_person.pins
    bot.send_message(TextMessage(Message.YOU_ARE_N_PINS.format(pin_number)), user_peer,
                     success_callback=success,
                     failure_callback=failure)

    pin_detail_message = Message.NUMBER_OF_YOUR_PINS + "\n" + Message.LEARNING + " : {}".format(
        target_person.learning) + "\n" + Message.HARDWORKING + " :  {}".format(
        target_person.hardworking) + "\n" + Message.RESPONSIBILITI + " :  {}".format(
        target_person.resposibility) + "\n" + \
                         Message.TEAMWORKING + " : {}".format(
        target_person.teamworking) + "\n" + Message.PRODUCT_CONCERN + " : {}".format(
        target_person.product_concern) + "\n" + Message.OTHER + " :  {}".format(target_person.other)
    bot.send_message(TextMessage(pin_detail_message), user_peer, success_callback=success,
                     failure_callback=failure)
    logger.info("Pins report sent." + user_peer.get_json_str())
    start_bot(bot, update)
    dispatcher.finish_conversation(update)


@dispatcher.message_handler(TemplateResponseFilter(keywords=["/give_pin"]))
def give_pin(bot, update):
    user_peer = update.get_effective_user()
    persons_list = get_all_persons()
    dispatcher.set_conversation_data(update, "persons_list", persons_list)
    message_text = Message.GIVE_PIN_REQ.text + "\n\n"
    for person in persons_list:
        message_text += "{} - {}   {}\n".format(persons_list.index(person) + 1, person.first_name, person.last_name)


    bot.send_message(TemplateMessage(TextMessage(message_text), start_menu_button), user_peer, success_callback=success,
                     failure_callback=failure)
    # bot.send_message(TextMessage(message_text), user_peer, success_callback=success, failure_callback=failure)
    dispatcher.register_conversation_next_step_handler(update, [MessageHandler(TextFilter(), get_person_number),
                                                                MessageHandler(
                                                                    TemplateResponseFilter(keywords="/start"),
                                                                    start_bot)])


def get_person_number(bot, update):
    person_number = 0
    user_peer = update.get_effective_user()
    input = update.get_effective_message().text
    persons_list = dispatcher.get_conversation_data(update, "persons_list")
    if input.isnumeric():
        person_number = arabic_to_eng_number(input)
    else:
        bot.send_message(TemplateMessage(Message.WRONG_ANSWER, start_menu_button), user_peer, success_callback=success,
                         failure_callback=failure)
        dispatcher.register_conversation_next_step_handler(update, [MessageHandler(TextFilter(), get_person_number),
                                                                    MessageHandler(
                                                                        TemplateResponseFilter(keywords=["/start"]),
                                                                        start_bot)])
    if check_person_validation(user_peer.get_json_object()["id"], persons_list[int(person_number) - 1].id):
        dispatcher.set_conversation_data(update, "person_number", int(person_number) - 1)
        pin_buttons_list = [
            TemplateMessageButton(Message.LEARNING, "/1", 0),
            TemplateMessageButton(Message.HARDWORKING, "/2", 0),
            TemplateMessageButton(Message.RESPONSIBILITI, "/3", 0),
            TemplateMessageButton(Message.TEAMWORKING, "/4", 0),
            TemplateMessageButton(Message.PRODUCT_CONCERN, "/5", 0),
            TemplateMessageButton(Message.OTHER, "/6", 0),
            start_menu_button[0]
        ]
        bot.send_message(TemplateMessage(Message.WHAT_PIN, pin_buttons_list), user_peer, success_callback=success,
                         failure_callback=failure)
        dispatcher.register_conversation_next_step_handler(update, [
            MessageHandler(TemplateResponseFilter(["/1"]), get_pin_type),
            MessageHandler(TemplateResponseFilter(["/2"]), get_pin_type),
            MessageHandler(TemplateResponseFilter(["/3"]), get_pin_type),
            MessageHandler(TemplateResponseFilter(["/4"]), get_pin_type),
            MessageHandler(TemplateResponseFilter(["/5"]), get_pin_type),
            MessageHandler(TemplateResponseFilter(["/6"]), get_pin_type),
            MessageHandler(TemplateResponseFilter("/start"), start_bot)
        ]
                                                           )
    else:
        bot.send_message(TemplateMessage(Message.WRONG_ANSWER, start_menu_button), user_peer, success_callback=success,
                         failure_callback=failure)
        logger.info("")
        dispatcher.register_conversation_next_step_handler(update, [MessageHandler(TextFilter(), get_person_number),
                                                                    MessageHandler(
                                                                        TemplateResponseFilter(keywords="/start"),
                                                                        start_bot)])


def get_pin_type(bot, update):
    user_peer = update.get_effective_user()
    pin_type_number = int(update.get_effective_message().text_message[1])
    dispatcher.set_conversation_data(update, "pin_type_number", pin_type_number)
    bot.send_message(TemplateMessage(Message.HOW_MANY_PINS, start_menu_button), user_peer, success_callback=success, failure_callback=failure)
    # bot.send_message(start_menu_template_message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.register_conversation_next_step_handler(update, [MessageHandler(TextFilter(), get_numbers_of_pins),
                                                                MessageHandler(
                                                                    TemplateResponseFilter(keywords="/start"),
                                                                    start_bot)])


def get_numbers_of_pins(bot, update):
    number = 0
    user_peer = update.get_effective_user()
    input = update.get_effective_message().text
    if input.isnumeric():
        input = arabic_to_eng_number(input)
        number = int(input)
    else:
        bot.send_message(TemplateMessage(Message.WRONG_ANSWER, start_menu_button), user_peer, success_callback=success,
                         failure_callback=failure)
        dispatcher.register_conversation_next_step_handler(update, [MessageHandler(TextFilter(), get_numbers_of_pins),
                                                                    MessageHandler(
                                                                        TemplateResponseFilter(keywords=["/start"]),
                                                                        start_bot)])
    if check_pins_limitation(user_peer.get_json_object()["id"], number):
        dispatcher.set_conversation_data(update, "numbers", number)
        bot.send_message(TemplateMessage(Message.GET_REASON, start_menu_button), user_peer, success_callback=success,
                         failure_callback=failure)
        dispatcher.register_conversation_next_step_handler(update, [MessageHandler(TextFilter(), get_reason),
                                                                    MessageHandler(
                                                                        TemplateResponseFilter(keywords=["/start"]),
                                                                        start_bot)])
    else:
        bot.send_message(Message.END_PINS, user_peer, success_callback=success, failure_callback=failure)
        start_bot(bot, update)


def get_reason(bot, update):
    reason = update.get_effective_message().text
    dispatcher.set_conversation_data(update, "reason", reason)
    verification(bot, update)


def verification(bot, update):
    logger.info("verification start")
    user_peer = update.get_effective_user()
    person = get_person_name_from_user_id(user_peer.get_json_object()["id"])
    persons_list = dispatcher.get_conversation_data(update, "persons_list")
    receiver_id = dispatcher.get_conversation_data(update, "person_number")
    print(persons_list)
    print(receiver_id)
    for p in persons_list:
        if persons_list.index(p) == int(receiver_id):
            receiver_person = p
    message = Message.PIN_GIVER.format(person.first_name, person.last_name) + "\n" + Message.Receiver.format(
        receiver_person.first_name, receiver_person.last_name) + "\n" + \
              Message.PIN_KIND.format(get_pin_type_from_number(
                  dispatcher.get_conversation_data(update, "pin_type_number"))) + "\n" + Message.PIN_NUMBER.format(
        dispatcher.get_conversation_data(update, "numbers")) + "\n" + Message.REASON.format(
        dispatcher.get_conversation_data(update, "reason"))
    bot.send_message(TextMessage(message), user_peer, success_callback=success, failure_callback=failure)
    verification_btn_list = [
        TemplateMessageButton(Message.YES, "yes", 0),
        TemplateMessageButton(Message.NO, "no", 0)
    ]
    bot.send_message(TemplateMessage(Message.VERIFICATION, verification_btn_list), user_peer, success_callback=success,
                     failure_callback=failure)
    dispatcher.register_conversation_next_step_handler(update, [
        MessageHandler(TemplateResponseFilter(keywords=["yes"]), save_pin),
        MessageHandler(TemplateResponseFilter(keywords=["no"]), start_bot)
    ])


def save_pin(bot, update):
    user_peer = update.get_effective_user()
    id = dispatcher.get_conversation_data(update, "person_number")
    persons_list = dispatcher.get_conversation_data(update, "persons_list")
    for p in persons_list:
        if persons_list.index(p) == int(id):
            receiver_person = p
    reason = dispatcher.get_conversation_data(update, "reason")
    pin_type = dispatcher.get_conversation_data(update, "pin_type_number")
    pin_numbers = dispatcher.get_conversation_data(update, "numbers")
    update_pins(receiver_person.id, pin_type, pin_numbers)
    update_pin_numbers(user_peer.get_json_object()["id"], pin_numbers)
    save_reason(Reason(reason, pin_type, receiver_person.id))
    send_report(bot, update)
    logger.info("every thing saved successfully .")
    bot.send_message(Message.GIVE_PIN_SUCCESS, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.finish_conversation(update)
    start_bot(bot, update)


def send_report(bot, update):
    user_peer = update.get_effective_user()
    person = get_person_name_from_user_id(user_peer.get_json_object()["id"])
    persons_list = dispatcher.get_conversation_data(update, "persons_list")
    receiver_id = dispatcher.get_conversation_data(update, "person_number")
    print(persons_list)
    print(receiver_id)
    for p in persons_list:
        if persons_list.index(p) == int(receiver_id):
            receiver_person = p
    message = Message.PIN_GIVER.format(person.first_name, person.last_name) + "\n" + Message.Receiver.format(
        receiver_person.first_name, receiver_person.last_name) + "\n" + \
              Message.PIN_KIND.format(get_pin_type_from_number(
                  dispatcher.get_conversation_data(update, "pin_type_number"))) + "\n" + Message.PIN_NUMBER.format(
        dispatcher.get_conversation_data(update, "numbers")) + "\n" + Message.REASON.format(
        dispatcher.get_conversation_data(update, "reason"))
    bot.send_message(TextMessage(message), g_peer, success_callback=success, failure_callback=failure)


@dispatcher.command_handler("/add_person")
@dispatcher.message_handler(TemplateResponseFilter(keywords=["/add_person"]))
def start_register_conversation(bot, update):
    user_peer = update.get_effective_user()
    if check_register_validation(user_peer.get_json_object()["id"]):
        bot.send_message(TemplateMessage(Message.GET_FIRST_NAME, main_menu_button), user_peer,
                         success_callback=success,
                         failure_callback=failure)
        dispatcher.register_conversation_next_step_handler(update, [MessageHandler(TextFilter(), get_first_name),
                                                                    MessageHandler(
                                                                        TemplateResponseFilter(keywords="/start"),
                                                                        start_bot)])
    else:
        bot.send_message(Message.WRONG_ANSWER_FOR_REGISTER, user_peer, success_callback=success,
                         failure_callback=failure)
        start_bot(bot, update)
        dispatcher.finish_conversation(update)


def get_first_name(bot, update):
    user_peer = update.get_effective_user()
    first_name = update.get_effective_message().text
    logger.info("First name of user received. ")
    dispatcher.set_conversation_data(update, "first_name", first_name)
    bot.send_message(TemplateMessage(Message.GET_LAST_NAME, main_menu_button), user_peer, success_callback=success,
                     failure_callback=failure)
    dispatcher.register_conversation_next_step_handler(update, [MessageHandler(TextFilter(), get_last_name),
                                                                MessageHandler(
                                                                    TemplateResponseFilter(keywords=["/start"]),
                                                                    start_bot)])


def get_last_name(bot, update):
    user_peer = update.get_effective_user()
    last_name = update.get_effective_message().text
    logger.info("Last name of user received. ")
    save_person(
        Person(dispatcher.get_conversation_data(update, "first_name"), last_name, user_peer.get_json_object()["id"],
               user_peer.get_json_object()["accessHash"]))
    bot.send_message(Message.PERSON_ADDED, user_peer, success_callback=success, failure_callback=failure)
    logger.info("A new user registered successfully .")
    start_bot(bot, update)
    dispatcher.finish_conversation(update)


@dispatcher.command_handler("/report_winner")
def send_winner_report(bot):
    winners = sort_by_all_elements()
    message = Message.TOTAL_RANCKING + "\n\n\n*****************************\n\n"
    for p, i in zip(winners, range(1, len(winners) + 2)):
        print(p)
        message += "{})  {} {}  **********   ".format(i, p.first_name, p.last_name) + Message.PIN_NUMBER.format(
            p.total_pins) + "\n"

    bot.send_message(TextMessage(message), g_peer, success_callback=success, failure_callback=failure)
    logger.info("Report of winners ranking sent ")


def send_each_field_winners():
    bot = dispatcher.bot
    current_time = jdatetime.datetime.now()
    field = sort_by_special_field()
    # for f in field:
    #     print(f)
    if current_time.day == LigBotConfig.report_delay1 or current_time.day == LigBotConfig.report_delay2:
        send_winner_report(bot)
        winners = sort_by_special_field()[0]
        message = Message.LEARNING + "\n\n\n"
        for p, i in zip(winners[:5], range(1, 6)):
            message += "{}) {}   {}   **********   ".format(i, p.first_name,
                                                            p.last_name) + Message.SPECIAL_PIN_NUMBER.format(
                p.learning) + "\n"

        bot.send_message(TextMessage(message), g_peer, success_callback=success, failure_callback=failure)

        winners = sort_by_special_field()[1]
        message = Message.HARDWORKING + "\n\n\n"
        for p, i in zip(winners[:5], range(1, 6)):
            message += "{}) {}   {}   **********   ".format(i, p.first_name,
                                                            p.last_name) + Message.SPECIAL_PIN_NUMBER.format(
                p.hardworking) + "\n"

        bot.send_message(TextMessage(message), g_peer, success_callback=success, failure_callback=failure)

        winners = sort_by_special_field()[2]
        message = Message.RESPONSIBILITI + "\n\n\n"
        for p, i in zip(winners[:5], range(1, 6)):
            message += "{}) {}   {}   **********   ".format(i, p.first_name,
                                                            p.last_name) + Message.SPECIAL_PIN_NUMBER.format(
                p.resposibility) + "\n"

        bot.send_message(TextMessage(message), g_peer, success_callback=success, failure_callback=failure)

        winners = sort_by_special_field()[3]
        message = Message.TEAMWORKING + "\n\n\n"
        for p, i in zip(winners, range(1, 6)):
            print(p)
            message += "{}) {}   {}   **********   ".format(i, p.first_name,
                                                            p.last_name) + Message.SPECIAL_PIN_NUMBER.format(
                p.teamworking) + "\n"

        bot.send_message(TextMessage(message), g_peer, success_callback=success, failure_callback=failure)

        winners = sort_by_special_field()[4]
        message = Message.PRODUCT_CONCERN + "\n\n\n"
        for p, i in zip(winners[:5], range(1, 6)):
            message += "{}) {}   {}   **********   ".format(i, p.first_name,
                                                            p.last_name) + Message.SPECIAL_PIN_NUMBER.format(
                p.product_concern) + "\n"

        bot.send_message(TextMessage(message), g_peer, success_callback=success, failure_callback=failure)

        winners = sort_by_special_field()[5]
        message = Message.OTHER + "\n\n\n"
        for p, i in zip(winners[:5], range(1, 6)):
            message += "{}) {}   {}   **********   ".format(i, p.first_name,
                                                            p.last_name) + Message.SPECIAL_PIN_NUMBER.format(
                p.other) + "\n"

        bot.send_message(TextMessage(message), g_peer, success_callback=success, failure_callback=failure)

        reset_date()
        logger.info("Ranking of each field sent. ")
        loop.call_later(86300, send_each_field_winners)
    elif current_time.day != LigBotConfig.report_delay1 and current_time.day != LigBotConfig.report_delay2:
        loop.call_later(86300, send_each_field_winners)


def delete_person(bot, update):
    user_peer = update.get_effective_user()
    bot.send_message(TextMessage(Message.NEXT_VERSION), user_peer, success_callback=success,
                     failure_callback=failure)
    start_bot(bot, update)


loop.call_soon(send_each_field_winners)
updater.run()
