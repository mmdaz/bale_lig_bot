from balebot.updater import Updater
from balebot.models.messages import TemplateMessage, TemplateMessageButton, TextMessage
import asyncio
from Bot.template_messages import Message
from balebot.handlers import MessageHandler
from balebot.filters import TemplateResponseFilter, TextFilter
from Database.operations import *
from Bot.person import Person


updater = Updater(token="4da1a22c3bd8f29afcc59fdcc82721c901134f1a", loop=asyncio.get_event_loop())
dispatcher = updater.dispatcher


def success(result):
    print("success : ", result)


def failure(result):
    print("failure : ", result)

main_menu_button = [
    TemplateMessageButton("بازگشت به منوی اصلی", "/start", 0)
]


@dispatcher.command_handler(["/start"])
def start_bot(bot, update):
    user_peer = update.get_effective_user()
    # TODO check admin and redirect to other function .
    button_list =  [
        TemplateMessageButton("چن تا پین دارم الان ؟؟؟" , "/pin_number", 0),
        TemplateMessageButton("میخوام پین بدم به یکی :)", "/give_pin", 0)
    ] if user_peer.get_json_object()["id"] != "1314892980" else [
        TemplateMessageButton("چن تا پین دارم الان ؟؟؟" , "/pin_number", 0),
        TemplateMessageButton("میخوام پین بدم به یکی :)", "/give_pin", 0),
        TemplateMessageButton("اضافه کردن به لیگ :", "/add_person", 0),
        TemplateMessageButton("حذف از لیگ ", "/delete_person", 0)
    ]

    bot.send_message(TemplateMessage(Message.START_MESSAGE, btn_list=button_list), user_peer, success_callback=success, failure_callback=failure)

    dispatcher.register_conversation_next_step_handler(update, [
        MessageHandler(TemplateResponseFilter(keywords=["/pin_number"]), send_pin_number),
        MessageHandler(TemplateResponseFilter(keywords=["/give_pin"]), give_pin ),
        MessageHandler(TemplateResponseFilter(keywords=["/add_person"]), start_add_conversation),
        MessageHandler(TemplateResponseFilter(keywords=["/delete_person"]), delete_person)
    ])




@dispatcher.command_handler("/pin_number")
@dispatcher.message_handler(TemplateResponseFilter(keywords=["/pin_number"]))
def send_pin_number(bot, update):
    user_peer = update.get_effective_user()
    pin_number = get_pin_numbers(user_peer.get_json_object()["id"])
    bot.send_message(TextMessage("شما {} تا پین دارید ... ".format(pin_number)), user_peer, success_callback=success, failure_callback=failure )
    start_bot(bot, update)
    dispatcher.finish_conversation(update)


def give_pin(bot, update):
    user_peer = update.get_effective_user()
    persons_list = get_all_persons()
    dispatcher.set_conversation_data(update, "persons_list", persons_list)
    message_text = ""
    for person in persons_list:
        message_text += "{} - {}   {}\n".format(person.id, person.first_name, person.last_name)

    bot.send_message(TextMessage(Message.GIVE_PIN_REQ), user_peer, success_callback=success, failure_callback=failure)
    bot.send_message(TextMessage(message_text), user_peer,success_callback=success, failure_callback=failure)
    dispatcher.register_conversation_next_step_handler(update, MessageHandler(TextFilter(), get_pin_numbers))


def get_person_number(bot, update):
    user_peer = update.get_effective_user()
    person_number = update.get_effective_message().text
    # TODO check validation of number : 1)is numeric 2)is not out of bound
    dispatcher.set_conversation_data(update, "person_number", person_number)
    bot.send_message(TextMessage(Message.WHAT_PIN), user_peer, success_callback=success, failure_callback=failure)
    pin_buttons_list = [
        TemplateMessageButton(Message.LEARNING, "/1", 0),
        TemplateMessageButton(Message.HARDWORKING, "/2", 0),
        TemplateMessageButton(Message.RESPONSIBILITI, "/3", 0),
        TemplateMessageButton(Message.TEAMWORKING, "/4", 0),
        TemplateMessageButton(Message.PRODUCT_CONCERN, "/5", 0),
        TemplateMessageButton(Message.OTHER , "/6", 0)
    ]
    bot.send_message(TemplateMessage(TextMessage(Message.WHAT_PIN), pin_buttons_list), user_peer, success_callback=success, failure_callback=failure )
    dispatcher.register_conversation_next_step_handler(update, [
                                                                MessageHandler(TemplateResponseFilter(["/1"]), get_pin_type(bot, update, 1)),
                                                                MessageHandler(TemplateResponseFilter(["/2"]), get_pin_type(bot, update, 2)),
                                                                MessageHandler(TemplateResponseFilter(["/3"]), get_pin_type(bot, update, 3)),
                                                                MessageHandler(TemplateResponseFilter(["/4"]), get_pin_type(bot, update, 4)),
                                                                MessageHandler(TemplateResponseFilter(["/5"]), get_pin_type(bot, update, 5)),
                                                                MessageHandler(TemplateResponseFilter(["/6"]), get_pin_type(bot, update, 6))])


def get_pin_type(bot, update, type_number):
    user_peer = update.get_effective_user()


def get_reason(bot, update):

    pass




@dispatcher.command_handler("/add_person")
def start_add_conversation(bot, update):
    user_peer = update.get_effective_user()
    bot.send_message(Message.GET_FIRST_NAME, user_peer,  success_callback=success, failure_callback=failure)
    bot.send_message(TemplateMessage(Message.BACK_TO_MAIN_MENU, main_menu_button), user_peer, success_callback=success, failure_callback=failure  )
    dispatcher.register_conversation_next_step_handler(update, [MessageHandler(TextFilter(), get_first_name),
                                                                MessageHandler(TemplateResponseFilter(keywords="/start"), start_bot)])


def get_first_name(bot, update):
    user_peer = update.get_effective_user()
    first_name = update.get_effective_message().text
    dispatcher.set_conversation_data(update, "first_name", first_name)
    bot.send_message(Message.GET_LAST_NAME, user_peer,  success_callback=success, failure_callback=failure)
    bot.send_message(TemplateMessage(Message.BACK_TO_MAIN_MENU, main_menu_button), user_peer, success_callback=success, failure_callback=failure)
    dispatcher.register_conversation_next_step_handler(update, [MessageHandler(TextFilter(), get_last_name),
                                                                MessageHandler(TemplateResponseFilter(keywords=["/start"]), start_bot)])


def get_last_name(bot, update):
    user_peer = update.get_effective_user()
    last_name = update.get_effective_message().text
    save_person(Person(dispatcher.get_conversation_data(update, "first_name"), last_name, user_peer.get_json_object()["id"], user_peer.get_json_object()["accessHash"]))
    bot.send_message(Message.PERSON_ADDED, user_peer,  success_callback=success, failure_callback=failure)
    start_bot(bot, update)
    dispatcher.finish_conversation(update)

def delete_person(bot, update):
    pass


updater.run()
