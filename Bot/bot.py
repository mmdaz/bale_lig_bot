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

Config.use_graylog = "2"

loop = asyncio.get_event_loop()
updater = Updater(token="4da1a22c3bd8f29afcc59fdcc82721c901134f1a", loop=loop)
dispatcher = updater.dispatcher

logger = Logger()
logger = logger.get_logger()


def success(bot, result):
    print("success : ", result)



def failure(bot, result):
    print("failure : ", result)


main_menu_button = [
    TemplateMessageButton("بازگشت به منوی اصلی", "/start", 0)
]


def get_pin_type_from_number(pin_number):
    return (pin_number == 1 and Message.LEARNING) or (pin_number == 2 and Message.HARDWORKING) or (
            pin_number == 3 and Message.RESPONSIBILITI) or (pin_number == 4 and Message.TEAMWORKING) or (
                   pin_number == 5 and Message.PRODUCT_CONCERN) or (pin_number == 6 and Message.OTHER)


@dispatcher.command_handler(["/start"])
def start_bot(bot, update):
    logger.info("receiving :  " + TextMessage("/start").get_json_str())
    logger.info("Bot started")
    user_peer = update.get_effective_user()
    logger.info("user :   " + user_peer.get_json_str())
    button_list = [
        TemplateMessageButton("چن تا پین دارم الان ؟؟؟", "/pin_number", 0),
        TemplateMessageButton("میخوام پین بدم به یکی :)", "/give_pin", 0),
        TemplateMessageButton("ثبت نام ", "/add_person", 0)
    ] if user_peer.get_json_object()["id"] != "1314892980" else [
        TemplateMessageButton("چن تا پین دارم الان ؟؟؟", "/pin_number", 0),
        TemplateMessageButton("میخوام پین بدم به یکی :)", "/give_pin", 0),
        TemplateMessageButton("حذف از لیگ ", "/delete_person", 0),
        TemplateMessageButton("ثبت نام ", "/add_person", 0)
    ]

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
    bot.send_message(TextMessage("شما {} تا پین دارید که میتوانید به دیگران بدهید  ... ".format(pin_number)), user_peer,
                     success_callback=success,
                     failure_callback=failure)

    pin_detail_message = "تعداد پین های شما در هر قسمت که دریافت کردید :‌" + "\n" + Message.LEARNING + " : {}".format(
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
    message_text = ""
    for person in persons_list:
        message_text += "{} - {}   {}\n".format(person.id, person.first_name, person.last_name)

    bot.send_message(TextMessage(Message.GIVE_PIN_REQ), user_peer, success_callback=success, failure_callback=failure)
    bot.send_message(TextMessage(message_text), user_peer, success_callback=success, failure_callback=failure)
    dispatcher.register_conversation_next_step_handler(update, MessageHandler(TextFilter(), get_person_number))


def get_person_number(bot, update):
    person_number = 0
    user_peer = update.get_effective_user()
    input = update.get_effective_message().text
    if input.isnumeric():
        person_number = update.get_effective_message().text
    else:
        bot.send_message(Message.WRONG_ANSWER, user_peer, success_callback=success, failure_callback=failure)
        dispatcher.register_conversation_next_step_handler(update, MessageHandler(TextFilter(), get_person_number))
    if check_person_validation(user_peer.get_json_object()["id"], person_number):
        dispatcher.set_conversation_data(update, "person_number", person_number)
        pin_buttons_list = [
            TemplateMessageButton(Message.LEARNING, "/1", 0),
            TemplateMessageButton(Message.HARDWORKING, "/2", 0),
            TemplateMessageButton(Message.RESPONSIBILITI, "/3", 0),
            TemplateMessageButton(Message.TEAMWORKING, "/4", 0),
            TemplateMessageButton(Message.PRODUCT_CONCERN, "/5", 0),
            TemplateMessageButton(Message.OTHER, "/6", 0)
        ]
        bot.send_message(TemplateMessage(Message.WHAT_PIN, pin_buttons_list), user_peer, success_callback=success,
                         failure_callback=failure)
        dispatcher.register_conversation_next_step_handler(update, [
            MessageHandler(TemplateResponseFilter(["/1"]), get_pin_type),
            MessageHandler(TemplateResponseFilter(["/2"]), get_pin_type),
            MessageHandler(TemplateResponseFilter(["/3"]), get_pin_type),
            MessageHandler(TemplateResponseFilter(["/4"]), get_pin_type),
            MessageHandler(TemplateResponseFilter(["/5"]), get_pin_type),
            MessageHandler(TemplateResponseFilter(["/6"]), get_pin_type)
        ]
                                                           )
    else:
        bot.send_message(Message.WRONG_ANSWER, user_peer, success_callback=success, failure_callback=failure)
        logger.info("")
        dispatcher.register_conversation_next_step_handler(update, MessageHandler(TextFilter(), get_person_number))


def get_pin_type(bot, update):
    user_peer = update.get_effective_user()
    pin_type_number = int(update.get_effective_message().text_message[1])
    dispatcher.set_conversation_data(update, "pin_type_number", pin_type_number)
    bot.send_message(Message.HOW_MANY_PINS, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.register_conversation_next_step_handler(update, MessageHandler(TextFilter(), get_numbers_of_pins))


def get_numbers_of_pins(bot, update):
    number = 0
    user_peer = update.get_effective_user()
    input = update.get_effective_message().text
    if input.isnumeric():
        number = int(input)
    else:
        bot.send_message(Message.WRONG_ANSWER, user_peer, success_callback=success, failure_callback=failure)
        dispatcher.register_conversation_next_step_handler(update, MessageHandler(TextFilter(), get_numbers_of_pins))
    if check_pins_limitation(user_peer.get_json_object()["id"], number):
        dispatcher.set_conversation_data(update, "numbers", number)
        bot.send_message(Message.GET_REASON, user_peer, success_callback=success, failure_callback=failure)
        dispatcher.register_conversation_next_step_handler(update, MessageHandler(TextFilter(), get_reason))
    else:
        bot.send_message(Message.END_PINS, user_peer, success_callback=success, failure_callback=failure)
        start_bot(bot, update)


def get_reason(bot, update):
    user_peer = update.get_effective_user()
    reason = update.get_effective_message().text
    dispatcher.set_conversation_data(update, "reason", reason)
    id = dispatcher.get_conversation_data(update, "person_number")
    pin_type = dispatcher.get_conversation_data(update, "pin_type_number")
    pin_numbers = dispatcher.get_conversation_data(update, "numbers")
    update_pins(id, pin_type, pin_numbers)
    update_pin_numbers(user_peer.get_json_object()["id"], pin_numbers)
    save_reason(Reason(reason, pin_type, id))
    bot.send_message(Message.GIVE_PIN_SUCCESS, user_peer, success_callback=success, failure_callback=failure)
    send_report(bot, update)
    dispatcher.finish_conversation(update)


def send_report(bot, update):
    user_peer = update.get_effective_user()
    person = get_person_name_from_user_id(user_peer.get_json_object()["id"])
    persons_list = dispatcher.get_conversation_data(update, "persons_list")
    receiver_id = dispatcher.get_conversation_data(update, "person_number")

    for p in persons_list:
        if p.id == int(receiver_id):
            receiver_person = p
    message = "پین دهنده :{} {}".format(person.first_name, person.last_name) + "\n" + "گیرنده :‌ {}  {}".format(
        receiver_person.first_name, receiver_person.last_name) + "\n" + \
              "نوع پین :‌{}".format(get_pin_type_from_number(
                  dispatcher.get_conversation_data(update, "pin_type_number"))) + "\n" + "تعداد پین :{}".format(
        dispatcher.get_conversation_data(update, "numbers")) + "\n" + "دلیل و توضیحات : {}".format(
        dispatcher.get_conversation_data(update, "reason"))
    bot.send_message(TextMessage(message), user_peer, success_callback=success, failure_callback=failure)
    logger.info("Every thing completed successfully ")


@dispatcher.command_handler("/add_person")
@dispatcher.message_handler(TemplateResponseFilter(keywords=["/add_person"]))
def start_register_conversation(bot, update):
    user_peer = update.get_effective_user()
    if check_register_validation(user_peer.get_json_object()["id"]):
        bot.send_message(Message.GET_FIRST_NAME, user_peer, success_callback=success, failure_callback=failure)
        bot.send_message(TemplateMessage(Message.BACK_TO_MAIN_MENU, main_menu_button), user_peer,
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
    bot.send_message(Message.GET_LAST_NAME, user_peer, success_callback=success, failure_callback=failure)
    bot.send_message(TemplateMessage(Message.BACK_TO_MAIN_MENU, main_menu_button), user_peer, success_callback=success,
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
    logger.info("Person registered successfully .")
    start_bot(bot, update)
    dispatcher.finish_conversation(update)


@dispatcher.command_handler("/report_winner")
def send_winner_report(bot):
    winners = sort_by_all_elements()
    message = "رتبه بندی کلی لیگ برتر دمت گرم ..." + "\n\n\n*****************************\n\n"
    for p, i in zip(winners, range(1, len(winners) + 2)):
        print(p)
        message += "{})  {} {}  **********   ".format(i, p.first_name, p.last_name) + "تعداد پین : {}".format(
            p.total_pins) + "\n"

    g_peer = Peer(peer_type="Group", peer_id="568560388", access_hash="-993816927678809060")
    bot.send_message(TextMessage(message), g_peer, success_callback=success, failure_callback=failure)
    logger.info("Report of winners ranking sent ")


def send_each_field_winners():
    bot = dispatcher.bot
    g_peer = Peer(peer_type="Group", peer_id="568560388", access_hash="-993816927678809060")
    current_time = jdatetime.datetime.now()
    field = sort_by_special_field()
    # for f in field:
    #     print(f)
    if current_time.day == 2:
        send_winner_report(bot)
        winners = sort_by_special_field()[0]
        message = Message.LEARNING + "\n\n\n"
        for p, i in zip(winners[:5], range(1, 6)):
            message += "{}) {}   {}   **********   ".format(i, p.first_name,
                                                            p.last_name) + "تعداد پین در این قسمت : {}".format(
                p.learning) + "\n"

        bot.send_message(TextMessage(message), g_peer, success_callback=success, failure_callback=failure)

        winners = sort_by_special_field()[1]
        message = Message.HARDWORKING + "\n\n\n"
        for p, i in zip(winners[:5], range(1, 6)):
            message += "{}) {}   {}   **********   ".format(i, p.first_name,
                                                            p.last_name) + "تعداد پین در این قسمت : {}".format(
                p.hardworking) + "\n"

        bot.send_message(TextMessage(message), g_peer, success_callback=success, failure_callback=failure)

        winners = sort_by_special_field()[2]
        message = Message.RESPONSIBILITI + "\n\n\n"
        for p, i in zip(winners[:5], range(1, 6)):
            message += "{}) {}   {}   **********   ".format(i, p.first_name,
                                                            p.last_name) + "تعداد پین در این قسمت : {}".format(
                p.resposibility) + "\n"

        bot.send_message(TextMessage(message), g_peer, success_callback=success, failure_callback=failure)

        winners = sort_by_special_field()[3]
        message = Message.TEAMWORKING + "\n\n\n"
        for p, i in zip(winners, range(1, 6)):
            print(p)
            message += "{}) {}   {}   **********   ".format(i, p.first_name,
                                                            p.last_name) + "تعداد پین در این قسمت : {}".format(
                p.teamworking) + "\n"

        bot.send_message(TextMessage(message), g_peer, success_callback=success, failure_callback=failure)

        winners = sort_by_special_field()[4]
        message = Message.PRODUCT_CONCERN + "\n\n\n"
        for p, i in zip(winners[:5], range(1, 6)):
            message += "{}) {}   {}   **********   ".format(i, p.first_name,
                                                            p.last_name) + "تعداد پین در این قسمت : {}".format(
                p.product_concern) + "\n"

        bot.send_message(TextMessage(message), g_peer, success_callback=success, failure_callback=failure)

        winners = sort_by_special_field()[5]
        message = Message.OTHER + "\n\n\n"
        for p, i in zip(winners[:5], range(1, 6)):
            message += "{}) {}   {}   **********   ".format(i, p.first_name,
                                                            p.last_name) + "تعداد پین در این قسمت : {}".format(
                p.other) + "\n"

        bot.send_message(TextMessage(message), g_peer, success_callback=success, failure_callback=failure)

        reset_date()
        logger.info("Ranking of each field sent. ")
        loop.call_later(86300, send_each_field_winners)
    elif current_time.day != 2:
        loop.call_later(86300, send_each_field_winners)


def delete_person(bot, update):
    user_peer = update.get_effective_user()
    bot.send_message(TextMessage("این قسمت در ورژن بعدی اضافه خواهد شد ... :)"), user_peer, success_callback=success,
                     failure_callback=failure)
    start_bot(bot, update)


loop.call_soon(send_each_field_winners)
updater.run()
