
drop_users = """
drop table if exists users;
"""

drop_profiles = """
drop table if exists profiles;
"""

drop_sections = """
drop table if exists sections;
"""

create_users = """
CREATE TABLE users (
  user_id     INTEGER       PRIMARY KEY,
  created     TIMESTAMP     DEFAULT CURRENT_TIMESTAMP,
  email       varchar(120)  UNIQUE,
  verified    SMALLINT      DEFAULT 0,
  temp_email  varchar(120)  UNIQUE DEFAULT NULL,
  user_name   varchar(50)   UNIQUE NOT NULL,
  admin       SMALLINT      NOT NULL DEFAULT 0,
  hash        VARCHAR(60)   NOT NULL,
  nonce       VARCHAR(64)   DEFAULT NULL,
  nonce_stamp TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
);
"""

create_profiles = """
CREATE TABLE profiles (
  profile_id  INTEGER       PRIMARY KEY,
  email       varchar(120)  UNIQUE,
  first_name  VARCHAR(200),
  last_name   VARCHAR(200),
  bio         VARCHAR(500),
  
  -- social media user names
  linked_in   VARCHAR(100),
  twitter     VARCHAR(100),
  github      VARCHAR(100),
  facebook    VARCHAR(100),
  google_plus VARCHAR(100),
  
  -- foreign keys
  user_id INTEGER,
  CONSTRAINT fk_users
    FOREIGN KEY(user_id) REFERENCES users(user_id)
    ON DELETE CASCADE
);
"""

create_section = """
CREATE TABLE sections (
  section_id  INTEGER       PRIMARY KEY,
  sec_order   INTEGER       DEFAULT 0,
  name        VARCHAR(15)   DEFAULT NULL,
  type        INTEGER       DEFAULT NULL,
  headline    VARCHAR(120)  DEFAULT NULL,
  copy        VARCHAR(120)  DEFAULT NULL,
  parent      INTEGER       DEFAULT NULL,
  sub_sec_a   INTEGER       DEFAULT NULL,
  sub_sec_b   INTEGER       DEFAULT NULL,
  filename    VARCHAR(120)  DEFAULT NULL
);
"""

pragma_off = "PRAGMA foreign_keys=off;"
pragma_on = "PRAGMA foreign_keys=on;"
schema = [pragma_off, drop_profiles, drop_users, drop_sections, create_users, create_profiles, create_section, pragma_on]
