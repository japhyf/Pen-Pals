DROP TABLE IF EXISTS user;


CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  first TEXT,
  last TEXT,
  address_line1 TEXT,
  address_line2 TEXT,
  username TEXT,
  has TEXT,
  verified BOOLEAN
);
