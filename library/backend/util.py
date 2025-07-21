from enum import Enum
from models import Book, Borrow, Comment, ULibrary, User, Announcement, Consult, UBorrow


class APIResponse:
    def __init__(self, code, data=None, msg=None):
        self.code = code
        self.data = data
        self.msg = msg


class ResposeCode(Enum):

    ADD_BOOK_SUCCESS = 20011
    DELETE_BOOK_SUCCESS = 20012
    UPDATE_BOOK_SUCCESS = 20013
    GET_BOOK_SUCCESS = 20014

    ADD_BOOK_ERR = 40011
    DELETE_BOOK_ERR = 40012
    UPDATE_BOOK_ERR = 40013
    GET_BOOK_ERR = 40014

    ADD_USER_SUCCESS = 20021
    DELETE_USER_SUCCESS = 20022
    UPDATE_USER_SUCCESS = 20023
    GET_USER_SUCCESS = 20024

    ADD_USER_ERR = 40021
    DELETE_USER_ERR = 40022
    UPDATE_USER_ERR = 40023
    GET_USER_ERR = 40024

    ADD_ANNOUNCEMENT_SUCCESS = 20031
    DELETE_ANNOUNCEMENT_SUCCESS = 20032
    UPDATE_ANNOUNCEMENT_SUCCESS = 20033
    GET_ANNOUNCEMENT_SUCCESS = 20034

    ADD_ANNOUNCEMENT_ERR = 40031
    DELETE_ANNOUNCEMENT_ERR = 40032
    UPDATE_ANNOUNCEMENT_ERR = 40033
    GET_ANNOUNCEMENT_ERR = 40034

    ADD_ULibrary_SUCCESS = 20041
    DELETE_ULibrary_SUCCESS = 20042
    UPDATE_ULibrary_SUCCESS = 20043
    GET_ULibrary_SUCCESS = 20044

    ADD_ULibrary_ERR = 40041
    DELETE_ULibrary_ERR = 40042
    UPDATE_ULibrary_ERR = 40043
    GET_ULibrary_ERR = 40044

    ADD_UBorrow_SUCCESS = 20051
    DELETE_UBorrow_SUCCESS = 20052
    UPDATE_UBorrow_SUCCESS = 20053
    GET_UBorrow_SUCCESS = 20054

    ADD_UBorrow_ERR = 40051
    DELETE_UBorrow_ERR = 40052
    UPDATE_UBorrow_ERR = 40053
    GET_UBorrow_ERR = 40054

    ADD_BORROW_SUCCESS = 20061
    DELETE_BORROW_SUCCESS = 20062
    UPDATE_BORROW_SUCCESS = 20063
    GET_BORROW_SUCCESS = 20064

    ADD_BORROW_ERR = 40061
    DELETE_BORROW_ERR = 40062
    UPDATE_BORROW_ERR = 40063
    GET_BORROW_ERR = 40064

    ADD_CONSULT_SUCCESS = 20071
    DELETE_CONSULT_SUCCESS = 20072
    UPDATE_CONSULT_SUCCESS = 20073
    GET_CONSULT_SUCCESS = 20074

    ADD_CONSULT_ERR = 40071
    DELETE_CONSULT_ERR = 40072
    UPDATE_CONSULT_ERR = 40073
    GET_CONSULT_ERR = 40074

    ADD_COMMENT_SUCCESS = 20081
    DELETE_COMMENT_SUCCESS = 20082
    UPDATE_COMMENT_SUCCESS = 20083
    GET_COMMENT_SUCCESS = 20084

    ADD_COMMENT_ERR = 40081
    DELETE_COMMENT_ERR = 40082
    UPDATE_COMMENT_ERR = 40083
    GET_COMMENT_ERR = 40084

    GET_CHAT_RESPONSE_SUCCESS = 20094
    GET_CHAT_RESPONSE_ERR = 40094

    ADD_TTS_SUCCESS = 200101
    GET_TTS_SUCCESS = 200104

    ADD_TTS_ERR = 400101
    GET_TTS_ERR = 400104

    ADD_ADMINISTRATOR_SUCCESS = 200101
    DELETE_ADMINISTRATOR_SUCCESS = 200102
    UPDATE_ADMINISTRATOR_SUCCESS = 200103
    GET_ADMINISTRATOR_SUCCESS = 200104

    ADD_ADMINISTRATOR_ERR = 400101
    DELETE_ADMINISTRATOR_ERR = 400102
    UPDATE_ADMINISTRATOR_ERR = 400103
    GET_ADMINISTRATOR_ERR = 400104


class AccessKey(Enum):
    API_KEY = "MD8Yqq2yYA0ox52Hu8WvpWPY"
    SECRET_KEY = "12QK4F9C6TKtwT0diqKQkylcBnypNcsZ"


def book_to_dict(book: Book):
    return {
        "book_id": book.book_id,
        "book_name": book.book_name,
        "author": book.author,
        "category": book.category,
        "press": book.press,
        "introduction": book.introduction,
        "stars": book.stars,
        "number": book.number,
        "cover": book.cover,
    }


def user_to_dict(user: User):
    return {
        "user_id": user.user_id,
        "user_account": user.user_account,
        "user_name": user.user_name,
        "user_password": user.user_password,
        "gender": user.gender,
        "phone": user.phone,
        "email": user.email,
        "profile": user.profile,
        "cover": user.cover,
    }


def comment_to_dict(comment: Comment):
    return {
        "comment_id": comment.id,
        "user_id": comment.user_id,
        "user_name": comment.user_name,
        "book_id": comment.book_id,
        "content": comment.content,
        "comment_date": comment.comment_date,
    }


def borrow_to_dict(borrow: Borrow):
    return {
        "id": borrow.id,
        "user_id": borrow.user_id,
        "user_name": borrow.user_name,
        "book_id": borrow.book_id,
        "book_name": borrow.book_name,
        "borrow_date": (
            borrow.borrow_date.strftime("%Y-%m-%d") if borrow.borrow_date else None
        ),
        "expired_date": (
            borrow.expired_date.strftime("%Y-%m-%d") if borrow.expired_date else None
        ),
        "is_return": borrow.is_return,
        "is_agree": borrow.is_agree,
    }


def comment_to_dict(comment: Comment):
    return {
        "id": comment.id,
        "user_id": comment.user_id,
        "user_name": comment.user_name,
        "book_id": comment.book_id,
        "content": comment.content,
        "comment_date": (
            comment.comment_date.strftime("%Y-%m-%d") if comment.comment_date else None
        ),
    }


def u_library_to_dict(u_library: ULibrary):
    return {
        "id": u_library.id,
        "user_id": u_library.user_id,
        "book_name": u_library.book_name,
        "author": u_library.author,
        "category": u_library.category,
        "press": u_library.press,
        "introduction": u_library.introduction,
    }


def u_borrow_to_dict(u_borrow: UBorrow):
    return {
        "id": u_borrow.id,
        "borrow_id": u_borrow.borrower_id,
        "lender_id": u_borrow.lender_id,
        "book_id": u_borrow.book_id,
        "book_name": u_borrow.book_name,
        "borrow_date": u_borrow.borrow_date,
        "is_agree": u_borrow.is_agree,
        "is_return": u_borrow.is_return,
    }


def announcement_to_dict(announcement: Announcement):
    return {
        "id": announcement.id,
        "title": announcement.title,
        "content": announcement.content,
        "publish_time": (
            announcement.publish_time.strftime("%Y-%m-%d %H:%M:%S")
            if announcement.publish_time
            else None
        ),
    }


def consult_to_dict(consult: Consult):
    return {
        "id": consult.id,
        "user_id": consult.user_id,
        "user_name": consult.user_name,
        "title": consult.title,
        "content": consult.content,
        "consult_time": (
            consult.consult_time.strftime("%Y-%m-%d %H:%M:%S")
            if consult.consult_time
            else None
        ),
    }
