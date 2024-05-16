path = "db/wildberries.db"


creation = """
CREATE TABLE IF NOT EXISTS users (
	id INTEGER PRIMARY KEY,
  	tg_id INTEGER UNIQUE NOT NULL,
    balance INTEGER DEFAULT 10
);

CREATE TABLE IF NOT EXISTS shops (
	id INTEGER PRIMARY KEY,
  	shop_name TEXT NOT NULL,
    api_key TEXT UNIQUE,
  	rating TEXT,
    auto_ans BOOLEAN DEFAULT 0,
  	fk_tg_id INTEGER REFERENCES users(tg_id)
);

CREATE TABLE IF NOT EXISTS answers (
	id INTEGER PRIMARY KEY,
	ans TEXT,
	fk_shop_id INTEGER REFERENCES shops(id)
);
"""