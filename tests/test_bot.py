import unittest
import tempfile
from aiosqlite import connect

from app.database import user_methods as db_user
from app.database import shop_methods as db_shop
from app.database import shop_settings as db_settings
from app.database import connection as db_conn
from app.database import vars

# database methods testing
class DBTester(unittest.IsolatedAsyncioTestCase):
      
    
    async def test_delete_all_null(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            
            db = tmpdirname+'/db_test.db'
            
            await db_user.add_user(111, db)
            await db_user.add_user(222, db)
            
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
            
            db = tmpdirname+'/db_test.db'
            
            await db_user.add_user(111, db)
            await db_user.add_user(222, db)
            
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
            
            db = tmpdirname+'/db_test.db'
            
            await db_user.add_user(111, db)
            
            await db_shop.add_shop(111, "test_name1", db)
            await db_shop.add_shop(111, "test_name2", db)
            await db_shop.add_shop(111, "test_name3", db)
            
            await db_settings.set_api_key(111, "test_name1", "api1", db)
            await db_settings.set_api_key(111, "test_name2", "api2", db)
            
            got_api1 = await db_settings.get_api_key(111, "test_name1", db)
            got_api2 = await db_settings.get_api_key(111, "test_name2", db)
            got_api3 = await db_settings.get_api_key(111, "test_name3", db)
            
            print(got_api1, got_api2, got_api3)
            
            await db_shop.delete_shop_if_null(111, db)
            
            got_deleted_id = await db_shop.get_shop_id(111, "test_name3", db)
            
            self.assertEqual(got_deleted_id, None)
            
            got_list = await db_shop.get_shops_list(111, db)
            
            self.assertEqual(len(got_list), 2)     
    
            
    async def test_get_null_rating_name(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            
            db = tmpdirname+'/db_test.db'
            
            await db_user.add_user(111, db)
            await db_shop.add_shop(111, "test_name1", db)
            await db_shop.add_shop(111, "test_name2", db)
            await db_settings.set_api_key(111, "test_name1", "api1", db)
            await db_settings.set_api_key(111, "test_name2", "api2", db)
            await db_settings.set_rating(111, "test_name2", "gt2", db)
            
            got_name1 = await db_shop.get_shop_name_rating(111, db)
            
            self.assertEqual(got_name1, "test_name1")
            
            await db_settings.set_rating(111, got_name1, "gt3", db)
            
            got_name = await db_shop.get_shop_name_rating(111, db)
            
            self.assertEqual(got_name, None)
            
            await db_shop.add_shop(111, "last", db)
            
            got_last_name = await db_shop.get_shop_name_rating(111, db)
            
            self.assertEqual(got_last_name, "last")
            
            
            
            
    # async def test_add_user(self):
        
    #     with tempfile.TemporaryDirectory() as tmpdirname:
        
    #         await init_connection(tmpdirname+'/db_test.db')
    #         await db_user.add_user(111)
            
    #         got_id_from_user1 = await db_user.get_user(111)
    #         got_id_from_user2 = await db_user.get_user(222)
    #         got_id_from_user3 = await db_user.get_user(333)
            
    #         self.assertEqual(got_id_from_user1, 111)
    #         self.assertEqual(got_id_from_user2, -1)
    #         self.assertEqual(got_id_from_user3, -1)
            
    #         await close_connection()
            
            
    # async def test_add_shop(self):
        
    #     with tempfile.TemporaryDirectory() as tmpdirname:
        
    #         await init_connection(tmpdirname+'/db_test.db')
    #         await db_user.add_user(111)
            
    #         added1 = await db_shop.add_shop(111, "test_name1")
    #         added2 = await db_shop.add_shop(111, "test_name2")
    #         added3 = await db_shop.add_shop(111, "test_name3")
            
            
    #         self.assertEqual(added1, True)
    #         self.assertEqual(added2, True)
    #         self.assertEqual(added3, True)
            
    #         await close_connection()
            
            
    # async def test_get_shop_by_id(self):
        
    #     with tempfile.TemporaryDirectory() as tmpdirname:
        
    #         await init_connection(tmpdirname+'/db_test.db')
    #         await db_user.add_user(111)
            
    #         await db_shop.add_shop(111, "test_name1")
    #         await db_shop.add_shop(111, "test_name2")
    #         await db_shop.add_shop(111, "test_name3")
            
    #         got_test_shop_id1 = await db_shop.get_shop_id(111, "test_name1")
    #         got_test_shop_id2 = await db_shop.get_shop_id(111, "test_name2")
    #         got_test_shop_id3 = await db_shop.get_shop_id(111, "test_name3")            
            
    #         self.assertEqual(got_test_shop_id1[0], 1)
    #         self.assertEqual(got_test_shop_id2[0], 2)
    #         self.assertEqual(got_test_shop_id3[0], 3)
            
    #         await close_connection()
            
            
    # async def test_get_shop_by_name(self):
        
    #     with tempfile.TemporaryDirectory() as tmpdirname:
        
    #         await init_connection(tmpdirname+'/db_test.db')
    #         await db_user.add_user(111)
            
    #         await db_shop.add_shop(111, "test_name1")
    #         await db_shop.add_shop(111, "test_name2")
    #         await db_shop.add_shop(111, "test_name3")
            
    #         got_test_shop_name1 = await db_shop.get_shop_name(111, "test_name1")
    #         got_test_shop_name2 = await db_shop.get_shop_name(111, "test_name2")
    #         got_test_shop_name3 = await db_shop.get_shop_name(111, "test_name3")            
            
    #         self.assertEqual(got_test_shop_name1[0], "test_name1")
    #         self.assertEqual(got_test_shop_name2[0], "test_name2")
    #         self.assertEqual(got_test_shop_name3[0], "test_name3")
            
    #         await close_connection() 
            
            
    # async def test_update_shop_name(self):
        
    #     with tempfile.TemporaryDirectory() as tmpdirname:
        
    #         await init_connection(tmpdirname+'/db_test.db')
    #         await db_user.add_user(111)
            
    #         await db_shop.add_shop(111, "test_name1")
    #         await db_shop.add_shop(111, "test_name2")
    #         await db_shop.add_shop(111, "test_name3")
            
    #         await db_shop.new_name_shop(111, "test_name1", "new_test_name1")
    #         await db_shop.new_name_shop(111, "test_name2", "new_test_name2")
    #         await db_shop.new_name_shop(111, "test_name3", "new_test_name3")
            
    #         got_test_shop_name1 = await db_shop.get_shop_name(111, "new_test_name1")
    #         got_test_shop_name2 = await db_shop.get_shop_name(111, "new_test_name2")
    #         got_test_shop_name3 = await db_shop.get_shop_name(111, "new_test_name3")             
            
    #         self.assertEqual(got_test_shop_name1[0], "new_test_name1")
    #         self.assertEqual(got_test_shop_name2[0], "new_test_name2")
    #         self.assertEqual(got_test_shop_name3[0], "new_test_name3")
            
    #         await close_connection()
            
            
    # async def test_delete_shop(self):
        
    #     with tempfile.TemporaryDirectory() as tmpdirname:
        
    #         await init_connection(tmpdirname+'/db_test.db')
    #         await db_user.add_user(111)
            
    #         await db_shop.add_shop(111, "test_name1")
    #         await db_shop.add_shop(111, "test_name2")
            
    #         is_deleted_shop1 = await db_shop.delete_shop(111, "test_name1")
    #         is_deleted_shop2 = await db_shop.delete_shop(111, "test_name2")
    #         is_deleted_shop3 = await db_shop.delete_shop(111, "test_name3")
            
    #         self.assertEqual(is_deleted_shop1, True)
    #         self.assertEqual(is_deleted_shop2, True)
    #         self.assertEqual(is_deleted_shop3, False)
            
    #         await close_connection()
            
        
    # async def test_get_shops_list(self):
        
    #     with tempfile.TemporaryDirectory() as tmpdirname:
        
    #         await init_connection(tmpdirname+'/db_test.db')
    #         await db_user.add_user(111)
    #         await db_user.add_user(222)
    #         await db_user.add_user(333)
            
    #         await db_shop.add_shop(111, "test_name1")
    #         await db_shop.add_shop(111, "test_name2")
    #         await db_shop.add_shop(111, "test_name3")
            
    #         await db_shop.add_shop(222, "test_name4")
    #         await db_shop.add_shop(222, "test_name5")
            
    #         got_list1 = await db_shop.get_shops_list(111)
    #         got_list2 = await db_shop.get_shops_list(222)
    #         got_list3 = await db_shop.get_shops_list(333)
        
    #         self.assertEqual(got_list1[0], "test_name1")
    #         self.assertEqual(got_list1[1], "test_name2")
    #         self.assertEqual(got_list1[2], "test_name3")
            
    #         self.assertEqual(got_list2[0], "test_name4")
    #         self.assertEqual(got_list2[1], "test_name5")
            
    #         self.assertEqual(got_list3, None)
            
    #         await close_connection()
            
            
    # async def test_set_api_key(self):
        
    #     with tempfile.TemporaryDirectory() as tmpdirname:
        
    #         await init_connection(tmpdirname+'/db_test.db')
    #         await db_user.add_user(111)
            
    #         await db_shop.add_shop(111, "test_name1")
    #         await db_shop.add_shop(111, "test_name2")
            
    #         await db_settings.set_api_key(111, "test_name1", "api111")
    #         await db_settings.set_api_key(111, "test_name2", "api222")
            
    #         got_api_key1 = await db_settings.get_api_key(111, "test_name1")
    #         got_api_key2 = await db_settings.get_api_key(111, "test_name2")
    #         got_api_key3 = await db_settings.get_api_key(111, "dont exist")
            
    #         self.assertEqual(got_api_key1, "api111")
    #         self.assertEqual(got_api_key2, "api222")
    #         self.assertEqual(got_api_key3, None)
            
    #         await close_connection()
            
    
    # async def test_set_rating(self):
        
    #     with tempfile.TemporaryDirectory() as tmpdirname:
        
    #         await init_connection(tmpdirname+'/db_test.db')
    #         await db_user.add_user(111)
            
    #         await db_shop.add_shop(111, "test_name1")
    #         await db_shop.add_shop(111, "test_name2")
            
    #         await db_settings.set_rating(111, "test_name1", "gt0")
    #         await db_settings.set_rating(111, "test_name2", "gt3")
            
    #         got_rating1 = await db_settings.get_rating(111, "test_name1")
    #         got_rating2 = await db_settings.get_rating(111, "test_name2")
    #         got_rating3 = await db_settings.get_rating(111, "dont exist")
            
    #         self.assertEqual(got_rating1, "gt0")
    #         self.assertEqual(got_rating2, "gt3")
    #         self.assertEqual(got_rating3, None)
            
    #         await db_settings.set_rating(111, "test_name1", "gt5")
            
    #         got_rating1 = await db_settings.get_rating(111, "test_name1")
            
    #         self.assertEqual(got_rating1, "gt5")
            
    #         await close_connection()