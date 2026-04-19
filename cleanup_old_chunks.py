from pinecone import Pinecone
from dotenv import load_dotenv
import os

load_dotenv()

client = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = client.Index(os.getenv("PINECONE_INDEX_NAME"))

# Delete the old chunks that had generic IDs before the fix
old_ids = [f"chunk_{i}" for i in range(6)]
index.delete(ids=old_ids)

print(f"Deleted old chunk IDs: {old_ids}")
print("Done. Pinecone should now have 11 records.")
