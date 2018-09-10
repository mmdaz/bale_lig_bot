from balebot.models.messages import TextMessage

class Message:

    START_MESSAGE = TextMessage("سلام من بازوی لیگ برتر دمت گرمم :) حالا بگو میخوای چیکار کنی ؟؟")
    GET_FIRST_NAME = TextMessage("لطفا نام شخص مورد نظر را وارد نمایید :")
    GET_LAST_NAME = TextMessage("نام خانوادگی را وارد کنید : ")
    PERSON_ADDED = TextMessage("شخص مورد نظر اضافه شد . ")
    BACK_TO_MAIN_MENU = TextMessage("بازگشت به منوی اصلی")