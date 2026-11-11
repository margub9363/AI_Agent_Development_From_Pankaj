import json
import os
import re

import mysql.connector

import numpy as np
from openai import OpenAI

# Defaults for your local MySQL server; environment variables can override them.
DATABASE = os.getenv("MYSQL_DATABASE", "day11_memory")


def get_connection(with_database=True):
    config = {
        "host": os.getenv("MYSQL_HOST", "127.0.0.1"),
        "port": int(os.getenv("MYSQL_PORT", "3306")),
        "user": os.getenv("MYSQL_USER", "root"),
        "password": os.getenv("MYSQL_PASSWORD", "root"),
        "charset": "utf8mb4",
        "connection_timeout": 10,
    }
    if with_database:
        config["database"] = DATABASE
    return mysql.connector.connect(**config)


embedding_client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

def create_database():
    # Schema names cannot be bound as SQL parameters.
    if not re.fullmatch(r"[A-Za-z0-9_]{1,64}", DATABASE):
        raise ValueError("MYSQL_DATABASE must contain 1-64 letters, digits or underscores")
    with get_connection(with_database=False) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{DATABASE}` CHARACTER SET utf8mb4"
            )
            connection.database = DATABASE
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id BIGINT PRIMARY KEY AUTO_INCREMENT,
                    user_message LONGTEXT,
                    assistant_message LONGTEXT,
                    embedding LONGTEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
        connection.commit()


def create_embedding(text):
    response =  embedding_client.embeddings.create(
        model="nomic-embed-text",
        input=text
    )
    return response.data[0].embedding

def consine_similarity(vector1, vector2):
    v1 = np.array(vector1)
    v2 = np.array(vector2)

    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def save_memory(user_message, assistant_message):
    text =  user_message + "\n" + assistant_message
    embedding = create_embedding(text)
    print(len(embedding))

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO memories (user_message, assistant_message, embedding)
                VALUES (%s, %s, %s)
                """,
                (user_message, assistant_message, json.dumps(embedding)),
            )
        connection.commit()



def search_semantic_memories(query, top_k=3, threshold=0):
    query_embedding = create_embedding(query)
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT user_message, assistant_message, embedding, created_at
                FROM memories
            """)
            rows = cursor.fetchall()
    results = []
    for( user_message, assistant_message, embedding_json, created_at) in rows:
        memory_embedding = json.loads(embedding_json)
        score = consine_similarity(query_embedding, memory_embedding)

        if score >= threshold:
            results.append({
                "user_message": user_message,
                "assistant_message": assistant_message,
                "create_at": str(created_at),
                "score": score
            })

    results.sort(
            key= lambda item: item["score"],
            reverse=True
        )
    print(results)
    return results[:top_k]