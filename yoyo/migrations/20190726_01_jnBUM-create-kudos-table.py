"""
Create kudos table
"""

from yoyo import step

__depends__ = {}

steps = [
    step("""
         CREATE TABLE kudos (
            id serial,
            kudo text,
            created_dt timestamp with time zone DEFAULT NOW(),
            updated_dt timestamp with time zone DEFAULT NOW()
         );
         """),
    step("""
         INSERT INTO kudos (kudo, created_dt) VALUES ('Awesome job learning AIO!', NOW());
         """),
]
