from ai_config.client import client

# Funktion zur Erstellung eines eindeutigen Vektorstore-Namens für jeden Benutzer
def generate_vector_store_name(purpose, id):
    return f"{purpose}_{id}_Vector_Store"

# Funktion zur Erstellung eines eindeutigen Vektorstore für jeden Benutzer
def create_vector_store(purpose, id):
    vector_store_name = generate_vector_store_name(purpose, id)
    store = client.vector_stores.create(
        name=vector_store_name,
        expires_after={
            "anchor": "last_active_at",
            "days": 365
        }
        )
    return store.id

def delete_vector_store(vectorstore_id):
    deleted_vector_store = client.vector_stores.delete(
        vector_store_id=vectorstore_id
    )
    return deleted_vector_store.id

