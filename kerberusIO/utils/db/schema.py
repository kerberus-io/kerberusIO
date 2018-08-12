
sqlite_drop_users = """
drop table if exists users;
"""

sqlite_drop_profiles = """
drop table if exists profiles;
"""

sqlite_drop_sections = """
drop table if exists sections;
"""

sqlite_create_users = """
CREATE TABLE users (
  user_id     INTEGER         PRIMARY KEY,
  created     TIMESTAMP       DEFAULT CURRENT_TIMESTAMP,
  email       VARCHAR(120)    UNIQUE,
  verified    SMALLINT        DEFAULT 0,
  temp_email  VARCHAR(120)    UNIQUE DEFAULT NULL,
  user_name   VARCHAR(50)     UNIQUE NOT NULL,
  admin       SMALLINT        NOT NULL DEFAULT 0,
  hash        VARCHAR(60)     NOT NULL,
  nonce       VARCHAR(64)     DEFAULT NULL,
  nonce_stamp TIMESTAMP       DEFAULT CURRENT_TIMESTAMP
);
"""

sqlite_create_profiles = """
CREATE TABLE profiles (
  profile_id  INTEGER         PRIMARY KEY,
  email       VARCHAR(120)    UNIQUE,
  first_name  VARCHAR(200)    DEFAULT NULL,
  last_name   VARCHAR(200)    DEFAULT NULL,
  bio         VARCHAR(500)    DEFAULT NULL,
  
  -- profile pic
  filename      VARCHAR(120)  DEFAULT NULL,
  file_pretty   VARCHAR(120)  DEFAULT NULL,
  file_alt_txt  VARCHAR(120)  DEFAULT NULL,
  
  -- social media user names
  linked_in   VARCHAR(100)    DEFAULT NULL,
  twitter     VARCHAR(100)    DEFAULT NULL,
  github      VARCHAR(100)    DEFAULT NULL,
  facebook    VARCHAR(100)    DEFAULT NULL,
  google_plus VARCHAR(100)    DEFAULT NULL,
  
  -- foreign keys
  user_id INTEGER,
  CONSTRAINT fk_users
    FOREIGN KEY(user_id) REFERENCES users(user_id)
    ON DELETE CASCADE
);
"""

sqlite_create_section = """
CREATE TABLE sections (
  section_id    INTEGER       PRIMARY KEY,
  sec_order     INTEGER       DEFAULT 0,
  name          VARCHAR(15)   DEFAULT NULL,
  type          INTEGER       DEFAULT NULL,
  headline      VARCHAR(120)  DEFAULT NULL,
  copy          VARCHAR(120)  DEFAULT NULL,
  parent        INTEGER       DEFAULT NULL,
  sub_sec_a     INTEGER       DEFAULT NULL,
  sub_sec_b     INTEGER       DEFAULT NULL,
  filename      VARCHAR(120)  DEFAULT NULL,
  file_pretty   VARCHAR(120)  DEFAULT NULL,
  file_alt_txt  VARCHAR(120)  DEFAULT NULL
);
"""

sqlite_pragma_off = "PRAGMA foreign_keys=off;"
sqlite_pragma_on = "PRAGMA foreign_keys=on;"
sqlite_schema = [sqlite_pragma_off, sqlite_drop_profiles, sqlite_drop_users, sqlite_drop_sections, sqlite_create_users, sqlite_create_profiles, sqlite_create_section, sqlite_pragma_on]

postgress_schema = []