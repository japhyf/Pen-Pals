DROP TABLE IF EXISTS user;


CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  first TEXT,
  last TEXT,
  street TEXT,
  city TEXT,
  state TEXT,
  zip INTEGER
);
