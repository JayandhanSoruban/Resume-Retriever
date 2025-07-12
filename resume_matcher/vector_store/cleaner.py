import os
import shutil

def delete_vector_db_contents(persist_path=r"D:\AGENTIC  AI\Resume Retrieval\resume_matcher\vector_store"):
    if not os.path.exists(persist_path):
        print("⚠️ Vector store folder does not exist.")
    else:
        deleted = False
        for item in os.listdir(persist_path):
            item_path = os.path.join(persist_path, item)

            # Delete folders (e.g., Chroma subfolders)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
                deleted = True

            # Delete files (skip .py files)
            elif os.path.isfile(item_path) and not item.endswith(".py"):
                os.remove(item_path)
                deleted = True

        if deleted:
            print("🧹 Vector DB contents cleaned successfully. Python files are safe.")
        else:
            print("ℹ️ No vector DB files found to delete.")

    # Extra: Delete resume_hashes.json
    hash_file_path = r"D:\AGENTIC  AI\Resume Retrieval\resume_matcher\data\resume_hashes.json"
    if os.path.exists(hash_file_path):
        try:
            os.remove(hash_file_path)
            print(f"🗑️ Deleted file: {hash_file_path}")
        except Exception as e:
            print(f"❌ Failed to delete {hash_file_path}: {e}")
    else:
        print(f"ℹ️ File not found: {hash_file_path}")

if __name__ == "__main__":
    delete_vector_db_contents()

