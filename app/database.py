from typing import List, Optional, Dict, Any
import psycopg
from psycopg.connection import Connection
from psycopg.cursor import Cursor
from .config import get_settings
settings = get_settings()

class Database:
    _instance: Optional[Connection] = None

    @classmethod
    def get_connection(cls) -> Connection:
        if cls._instance is None:
            conn_string = (
                settings.db_connection_string
            )
            cls._instance = psycopg.connect(conn_string)
        return cls._instance

    @classmethod
    def get_cursor(cls) -> Cursor:
        return cls.get_connection().cursor()

    @classmethod
    def get_posts(cls) -> List[Dict[str, Any]]:
        cur = cls.get_cursor()
        cur.execute("SELECT * FROM posts")
        return cur.fetchall()

    @classmethod
    def get_post(cls, post_id: int) -> Dict[str, Any]:
        cur = cls.get_cursor()
        cur.execute("SELECT * FROM posts WHERE id = %s", (post_id,)) 
        return cur.fetchone()

    @classmethod
    def create_post(cls, post: Dict[str, Any]) -> Dict[str, Any]:
        cur = cls.get_cursor()
        cur.execute(
            "INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
            (post['title'], post['content'], post['published'])
        )
        return cur.fetchone()
    
    @classmethod
    def delete_post(cls, post_id: int) -> bool:
        cur = cls.get_cursor()
        cur.execute("DELETE FROM posts WHERE id = %s RETURNING *", (post_id,))
        deleted_post = cur.fetchone()
        cls._instance.commit()
        return deleted_post is not None
    @classmethod
    def update_post(cls, post_id: int, post: Dict[str, Any]) -> Dict[str, Any]:
        cur = cls.get_cursor()
        cur.execute(
            "UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
            (post['title'], post['content'], post['published'], post_id)
        )
        cls._instance.commit()
        return cur.fetchone()
