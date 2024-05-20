from app.database.user_methods import get_users_with_balance
from app.database.shop_methods import get_apis_list


async def test_sched() -> None:
    print("Scheduler работает каждые 10 секунд")


# async def scheduled_db_scan_job() -> bool:
    
#     users_with_balance = await get_users_with_balance()
    
#     if users_with_balance is None:
#         print("все пользователи без баланса")
#         return None
    
#     for user_id in users_with_balance:
#         got_apis_for_user_id = await get_apis_list(user_id)
        
#         if got_apis_for_user_id is None:
#             print("по какой-то причине у пользователя нет магазинов")
#             continue
        
#         for api_key in got_apis_for_user_id:
#             got_feedback = await get_feedback(api_key)
            
#             if got_feedback is None:
#                 print(f"у пользователя {user_id} нет новых отзывов")
                
            
        
        
        