path = "db/wildberries.db"


creation = """
CREATE TABLE IF NOT EXISTS users (
	id INTEGER PRIMARY KEY,
  	tg_id INTEGER UNIQUE NOT NULL,
    balance INTEGER DEFAULT 9999999,
    count_ans INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS shops (
	id INTEGER PRIMARY KEY,
  	shop_name TEXT NOT NULL,
    api_key TEXT UNIQUE,
  	rating TEXT DEFAULT "0",
  	fk_tg_id INTEGER REFERENCES users(tg_id)
);

CREATE TABLE IF NOT EXISTS feedbacks (
	id INTEGER PRIMARY KEY,
	fb_id TEXT NOT NULL,
	fb_rating INT,
	fb_shop_wb TEXT,
	fb_product_wb TEXT,	
 	fb_text TEXT NOT NULL,
  	fb_answer TEXT,
	show_date TEXT DEFAULT "0",
	fk_api_key INTEGER REFERENCES shops(api_key)
);

CREATE TABLE IF NOT EXISTS payments (
	id INTEGER PRIMARY KEY,
	fb_tg_id INTEGER REFERENCES users(tg_id)
);
"""