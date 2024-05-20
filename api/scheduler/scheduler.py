from app.database.user_methods import get_users_with_balance
from app.database.shop_methods import get_apis_list
from app.database.answer_methods import fill_unanswered_feedbacks
from api.wb.wb_feedbacks_ans import get_feedback


async def test_sched() -> None:
    print("Scheduler работает каждые 10 секунд")


async def scheduled_db_fill_job() -> bool:
    
    users_with_balance = await get_users_with_balance()
    
    if users_with_balance is None:
        print("все пользователи без баланса")
        return None
    
    for user_id in users_with_balance:
        got_apis_for_user_id = await get_apis_list(user_id)
    
        if got_apis_for_user_id is None:
            print("по какой-то причине у пользователя нет магазинов")
            continue
        
        for api_key in got_apis_for_user_id:
            got_feedback = await get_feedback(api_key)
            
            if got_feedback is None:
                continue
            
            for i in range(got_feedback['data']['countUnanswered']):
                fb_id = got_feedback['data']['feedbacks'][i]['id']
                fb_rating = got_feedback['data']['feedbacks'][i]['productValuation']
                fb_shop_wb = got_feedback['data']['feedbacks'][i]['productDetails']['brandName']
                fb_product_wb = got_feedback['data']['feedbacks'][i]['productDetails']['productName']
                fb_text = got_feedback['data']['feedbacks'][i]['text']
            
                if not await fill_unanswered_feedbacks(fb_id, fb_rating, fb_shop_wb, fb_product_wb, fb_text, api_key):
                    print("ошибка при заполнении новых отзывов в БД")
                    return False
                
    return True
            
            
            
                
            
        
        
        