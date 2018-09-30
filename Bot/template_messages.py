from balebot.models.messages import TextMessage


class Message:
    START_MESSAGE = TextMessage("سلام من بازوی لیگ برتر دمت گرمم :) حالا بگو میخوای چیکار کنی ؟؟")
    GET_FIRST_NAME = TextMessage("لطفا *نام* خود را وارد نمایید :")
    GET_LAST_NAME = TextMessage("*نام خانوادگی* خود را وارد کنید : ")
    PERSON_ADDED = TextMessage("ثبت نام با موفقیت انجام شد :) ")
    BACK_TO_MAIN_MENU = TextMessage("بازگشت به منوی اصلی")
    GIVE_PIN_REQ = TextMessage("لطفا شماره فرد مورد نظر (انگلیسی ) را از لیست  انتخاب و ارسال نمایید :) ")
    WHAT_PIN = TextMessage("چه پینی میخوای بهش بدی ؟؟؟")
    LEARNING = "یادگیرندگی و یاد دهندگی"
    HARDWORKING = "روحیه جهادی"
    RESPONSIBILITI = "تعهد و مسئولیت پذیری"
    TEAMWORKING = "همکاری تیمی"
    OTHER = "سایر"
    PRODUCT_CONCERN = "دغدغه محصول و مشتری"
    GET_REASON = TextMessage("لطفا دلیل خود را برای این عمل بفرستید ...")
    HOW_MANY_PINS = TextMessage("چند تا پین میخوای بهش بدی ؟؟ ")
    GIVE_PIN_SUCCESS = TextMessage("پین  مورد نظر داده شد ... ")
    END_PINS = TextMessage("پین های شما به اتمام رسیده است ...")
    WRONG_ANSWER = TextMessage("ورودی اشتباه است لطفا دوباره وارد نمایید ...")
    WRONG_ANSWER_FOR_REGISTER = TextMessage("شما قبلا ثبت نام کرده اید ... ")
    VERIFICATION = TextMessage("آیا اطمینان دارید ؟؟؟")
    HOW_MANY_PINS_I_HAVE = "چن تا پین دارم الان ؟؟؟"
    I_WANT_TO_GIVE_PIN = "میخوام پین بدم به یکی ..."
    REGISTER = "ثبت نام"
    DELETE_FROM_LIG = "حذف از لیگ"
    YOU_ARE_N_PINS = "شما {} تا پین دارید که میتوانید به دیگران بدهید  ... "
    NUMBER_OF_YOUR_PINS = "تعداد پین های شما در هر قسمت که دریافت کردید :‌"
    PIN_NUMBER = "تعداد پین : {}"
    REASON = "دلیل و توضیحات : {}"
    Receiver = "گیرنده :‌ {}  {}"
    PIN_GIVER = "پین دهنده :{} {}"
    PIN_KIND = "نوع پین :‌{}"
    TOTAL_RANCKING = "رتبه بندی کلی لیگ برتر دمت گرم ..."
    SPECIAL_PIN_NUMBER = "تعداد پین در این قسمت : {}"
    NEXT_VERSION = "این قسمت در ورژن بعدی اضافه خواهد شد ... :)"
    YES = "آرههههه :)"
    NO = "نه نه اشتباه شد برگرد عقب برگرد عقب :)))"
