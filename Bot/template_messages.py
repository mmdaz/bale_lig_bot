from balebot.models.messages import TextMessage

class Message:

    START_MESSAGE = TextMessage("سلام من بازوی لیگ برتر دمت گرمم :) حالا بگو میخوای چیکار کنی ؟؟")
    GET_FIRST_NAME = TextMessage("لطفا نام شخص مورد نظر را وارد نمایید :")
    GET_LAST_NAME = TextMessage("نام خانوادگی را وارد کنید : ")
    PERSON_ADDED = TextMessage("شخص مورد نظر اضافه شد . ")
    BACK_TO_MAIN_MENU = TextMessage("بازگشت به منوی اصلی")
    GIVE_PIN_REQ = TextMessage("لطفا شماره فرد مورد نظر را از لیست بالا انتخاب و ارسال نمایید :) ")
    WHAT_PIN = TextMessage("چه پینی میخوای بهش بدی ؟؟؟")
    LEARNING = "یادگیرندگی و یاد دهندگی"
    HARDWORKING = "روحیه جهادی"
    RESPONSIBILITI = "تعهد و مسئولیت پذیری"
    TEAMWORKING = "همکاری تیمی"
    OTHER = "سایر"
    PRODUCT_CONCERN = "دغدغه محصول و مشتری"

