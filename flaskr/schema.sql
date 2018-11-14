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
  description TEXT,
  genres TEXT,
  titles TEXT,
  birthdate TEXT,
  penpal TINYINT /*penpal = 0 if not interested, 1 if open to it, 2 if wants to pen pal */
);


