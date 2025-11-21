import os

from ai_config.client import client

TEMP_DIR = 'tmp'

def upload_file_to_openai(file_name, purpose='assistants'):
  path = os.path.join(TEMP_DIR, file_name)
  file = client.files.create(
    file=open(path, "rb"),
    purpose=purpose
  )
  return file.id

def add_file_to_vectorstore(vectorstore_id, file_id):
  vector_store_file = client.vector_stores.files.create(
    vector_store_id=vectorstore_id,
    file_id=file_id
  )
  return vector_store_file.id

def add_vectorstore_to_assistant(vectorstore_id, assistant_id):
  assistant = client.beta.assistants.update(
  assistant_id=assistant_id,
  tool_resources={"file_search": {"vector_store_ids": [vectorstore_id]}},
  )
  return assistant.id

def delete_file(file_id):
  response = client.files.delete(file_id)
  print(response)
  return response

def delete_assistant(assistant_id):
  return client.beta.assistants.delete(assistant_id)
