from aiogram.fsm.state import StatesGroup, State

class UserStates(StatesGroup):
    awaiting_api_key = State()
    awaiting_rating = State()
    awaiting_request = State()
    awaiting_shop_name = State()
    started = State()
    menu = State()
    shop_list = State()
    chosen_to_delete = State()
    balance_menu = State()
    balance_replenishment = State()
    support_menu = State()
    answer_menu = State()
    show_last_answers = State()
    example_answer = State()
    show_more_answers = State()
    awaiting_auto_choose = State()
    toggle_auto = State()