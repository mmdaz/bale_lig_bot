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
    button_list = [
        TemplateMessageButton("چن تا پین دارم الان ؟؟؟" , "/pin_number", 0),
        TemplateMessageButton("میخوام پین بدم به یکی :)", "/give_pin", 0)
    ]

    bot.send_message(TemplateMessage(Message.START_MESSAGE, btn_list=button_list), user_peer, success_callback=success, failure_callback=failure)

    dispatcher.register_conversation_next_step_handler(update, [
        MessageHandler(TemplateResponseFilter(keywords=["pin_number"]), send_pin_number),
        MessageHandler(TemplateResponseFilter(keywords=["give_pin"]), give_pin )
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
    # save_person(Person(dispatcher.get_conversation_data(update, "first_name"), last_name, user_peer.get_json_object()["id"], user_peer.get_json_object()["accessHash"]))
    bot.send_message(Message.PERSON_ADDED, user_peer,  success_callback=success, failure_callback=failure)
    start_bot(bot, update)
    dispatcher.finish_conversation(update)


updater.run()
