import unittest
import tempfile
from aiosqlite import connect

from api.gspread.gspread import perform_gspread_update
from app.database.exec_methods import user_methods as db_user
from app.database.exec_methods import shop_methods as db_shop
from app.database.exec_methods import shop_settings as db_settings
from app.database.exec_methods import answer_methods as db_ans
from app.database.exec_methods import payments_method as db_pay
from app.database.export.export import get_data_from_db_to_export


# database methods testing
class DBTester(unittest.IsolatedAsyncioTestCase):

    async def test_delete_all_null(self):
        with tempfile.TemporaryDirectory() as tmpdirname:

            db = tmpdirname + "/db_test.db"

            await db_user.add_user(111, "111", db)
            await db_user.add_user(222, "222", db)

            await db_shop.add_shop(111, "test_name1", db)
            await db_shop.add_shop(111, "test_name2", db)
            await db_shop.add_shop(222, "test_name1", db)
            await db_shop.add_shop(222, "test_name2", db)

            await db_settings.set_api_key(111, "test_name1", "api_test1", db)
            await db_settings.set_api_key(222, "test_name1", "api_test2", db)

            await db_shop.delete_shop_if_null(111, db)
            await db_shop.delete_shop_if_null(222, db)

            got_list1 = await db_shop.get_shops_list(111, db)
            got_list2 = await db_shop.get_shops_list(222, db)

            self.assertEqual(len(got_list1), 1)
            self.assertEqual(len(got_list2), 1)

    async def test_delete_all(self):
        with tempfile.TemporaryDirectory() as tmpdirname:

            db = tmpdirname + "/db_test.db"

            await db_user.add_user(111, "111", db)
            await db_user.add_user(222, "222", db)

            await db_shop.add_shop(111, "test_name1", db)
            await db_shop.add_shop(111, "test_name2", db)
            await db_shop.add_shop(111, "test_name3", db)
            await db_shop.add_shop(222, "test_name1", db)

            await db_settings.set_api_key(111, "test_name1", "api1", db)

            await db_shop.delete_all_shops(111, db)

            await db_shop.add_shop(111, "test_name1", db)
            await db_settings.set_api_key(111, "test_name1", "api1", db)

            got_list1 = await db_shop.get_shops_list(111, db)
            got_list2 = await db_shop.get_shops_list(222, db)

            self.assertEqual(len(got_list1), 1)
            self.assertEqual(len(got_list2), 1)

    async def test_delete_null(self):
        with tempfile.TemporaryDirectory() as tmpdirname:

            db = tmpdirname + "/db_test.db"

            await db_user.add_user(111, "111", db)

            await db_shop.add_shop(111, "test_name1", db)
            await db_shop.add_shop(111, "test_name2", db)
            await db_shop.add_shop(111, "test_name3", db)

            await db_settings.set_api_key(111, "test_name1", "api1", db)
            await db_settings.set_api_key(111, "test_name2", "api2", db)

            await db_shop.delete_shop_if_null(111, db)

            got_deleted_id = await db_shop.get_shop_id(111, "test_name3", db)

            self.assertEqual(got_deleted_id, False)

            got_list = await db_shop.get_shops_list(111, db)

            self.assertEqual(len(got_list), 2)

    async def toggle_auto_ans(self):
        with tempfile.TemporaryDirectory() as tmpdirname:

            db = tmpdirname + "/db_test.db"

            await db_user.add_user(111, "111", db)
            await db_user.add_user(222, "222", db)

            await db_shop.add_shop(111, "shop1", db)
            await db_shop.add_shop(111, "shop2", db)
            await db_shop.add_shop(222, "shop21", db)
            await db_shop.add_shop(222, "shop22", db)

            await db_shop.toggle_auto_ans(111, "shop1", db)
            await db_shop.toggle_auto_ans(222, "shop22", db)

            got_status_1 = await db_shop.get_status_auto_ans(111, "shop1", db)
            got_status_2 = await db_shop.get_status_auto_ans(111, "shop2", db)
            got_status_3 = await db_shop.get_status_auto_ans(222, "shop21", db)
            got_status_4 = await db_shop.get_status_auto_ans(222, "shop22", db)
            got_status_5 = await db_shop.get_status_auto_ans(222, "shoppp", db)

            self.assertEqual(got_status_1, True)
            self.assertEqual(got_status_2, False)
            self.assertEqual(got_status_3, False)
            self.assertEqual(got_status_4, True)
            self.assertEqual(got_status_5, None)

    async def test_get_feedback(self):

        with tempfile.TemporaryDirectory() as tmpdirname:

            db = tmpdirname + "/db_test.db"

            await db_ans.fill_unanswered_feedback(
                "fb_id1", 5, "ViPi", "diloda", "very like", "apiapiapi", db
            )

            feedback = await db_ans.get_feedback("fb_id1", db)

            self.assertEqual(feedback, (5, "ViPi", "diloda", "very like"))

    async def test_answers_check(self):

        with tempfile.TemporaryDirectory() as tmpdirname:

            db = tmpdirname + "/db_test.db"

            await db_user.add_user(111, "111", db)

            await db_shop.add_shop(111, "ViPi", db)

            await db_settings.set_api_key(111, "ViPi", "api_key1", db)

            await db_ans.fill_unanswered_feedback(
                "fb_id1", 5, "ViPi", "dildos", "like it", "api_key1", db
            )

            await db_ans.update_answer_text(111, "fb_id1", "ANSWER TEXT TeST", db)

            got_answer = await db_ans.get_answer(111, "ViPi", db)

            self.assertEqual(got_answer, "ANSWER TEXT TeST")

    async def test_get_null_answers_feedbacks_list(self):

        with tempfile.TemporaryDirectory() as tmpdirname:

            db = tmpdirname + "/db_test.db"

            await db_user.add_user(111, "111", db)
            await db_shop.add_shop(111, "ViPi", db)
            await db_settings.set_api_key(111, "ViPi", "api_key1", db)

            await db_ans.fill_unanswered_feedback(
                "fb_id1", 5, "ViPi", "dildos", "like it1", "api_key1", db
            )
            await db_ans.fill_unanswered_feedback(
                "fb_id2", 5, "ViPi", "dildos", "like it2", "api_key1", db
            )
            await db_ans.fill_unanswered_feedback(
                "fb_id3", 5, "ViPi", "dildos", "like it3", "api_key1", db
            )

            await db_ans.update_answer_text(111, "fb_id1", "ANSWER TEXT TeST", db)

            got_null_answer_feedbacks_list = await db_ans.get_unanswered_fb_list(
                111, db
            )

            for i in range(len(got_null_answer_feedbacks_list)):
                self.assertEqual(
                    got_null_answer_feedbacks_list[i],
                    (5, "ViPi", "dildos", f"like it{i+2}", f"fb_id{i+2}"),
                )

    async def test_get_null_answers_feedbacks_list(self):

        with tempfile.TemporaryDirectory() as tmpdirname:

            db = tmpdirname + "/db_test.db"

            await db_user.add_user(12312, "12312", db)
            await db_user.add_user(122, "122", db)
            await db_user.add_user(1212, "1212", db)

            ls = await db_user.get_users(db)

            self.assertEqual(len(ls), 3)

    async def test_getting_payments(self):

        with tempfile.TemporaryDirectory() as tmpdirname:

            db = tmpdirname + "/db_test.db"

            await db_pay.new_payment(111, db)
            await db_pay.new_payment(111, db)
            await db_pay.new_payment(111, db)
            await db_pay.new_payment(111, db)

            await db_pay.new_payment(222, db)
            await db_pay.new_payment(222, db)
            await db_pay.new_payment(222, db)
            await db_pay.new_payment(222, db)

            await db_pay.new_payment(111, db)

            ls1 = await db_pay.get_payment_id(111, db)
            ls2 = await db_pay.get_payment_id(222, db)

            last1 = ls1[-1][0]
            last2 = ls2[-1][0]

            self.assertEqual(len(ls1) + len(ls2), 9)
            self.assertEqual(last1, 9)
            self.assertEqual(last2, 8)

    async def test_getting_payments(self):

        with tempfile.TemporaryDirectory() as tmpdirname:

            db = tmpdirname + "/db_test.db"

            await db_user.add_user(1, "user1", db)
            await db_user.add_user(2, "user2", db)
            await db_user.add_user(3, "user3", db)
            await db_user.add_user(4, "user4", db)

            await db_shop.add_shop(1, "user1_shop1", db)
            await db_shop.add_shop(1, "user1_shop2", db)
            await db_shop.add_shop(1, "user1_shop3", db)
            await db_settings.set_api_key(1, "user1_shop1", "api1", db)
            await db_settings.set_api_key(1, "user1_shop2", "api2", db)
            await db_settings.set_api_key(1, "user1_shop3", "api3", db)

            await db_shop.add_shop(2, "user2_shop1", db)
            await db_shop.add_shop(2, "user2_shop2", db)
            await db_settings.set_api_key(2, "user2_shop1", "api4", db)
            await db_settings.set_api_key(2, "user2_shop2", "api5", db)

            await db_shop.add_shop(4, "user4_shop1", db)
            await db_settings.set_api_key(4, "user4_shop1", "api6", db)

            got_info = await get_data_from_db_to_export(db)

            print(got_info)

            self.assertEqual(True, True)
            
    async def test_getting_payments(self):

        with tempfile.TemporaryDirectory() as tmpdirname:

            db = tmpdirname + "/db_test.db"

            await db_user.add_user(1, "user1", db)
            await db_user.add_user(2, "user2", db)
            await db_user.add_user(3, "user3", db)
            await db_user.add_user(4, "user4", db)

            await db_shop.add_shop(1, "user1_shop1", db)
            await db_shop.add_shop(1, "user1_shop2", db)
            await db_shop.add_shop(1, "user1_shop3", db)
            await db_settings.set_api_key(1, "user1_shop1", "api1", db)
            await db_settings.set_api_key(1, "user1_shop2", "api2", db)
            await db_settings.set_api_key(1, "user1_shop3", "api3", db)

            await db_shop.add_shop(2, "user2_shop1", db)
            await db_shop.add_shop(2, "user2_shop2", db)
            await db_settings.set_api_key(2, "user2_shop1", "api4", db)
            await db_settings.set_api_key(2, "user2_shop2", "api5", db)

            await db_shop.add_shop(4, "user4_shop1", db)
            await db_settings.set_api_key(4, "user4_shop1", "api6", db)

            got_data = await get_data_from_db_to_export(db)
            await perform_gspread_update(got_data)

            self.assertEqual(True, True)
