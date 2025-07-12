from cleaner import delete_vector_db_contents

if __name__ == "__main__":
    confirm = input("⚠️ Are you sure you want to delete the vector DB? (yes/no): ")
    if confirm.strip().lower() == "yes":
        delete_vector_db_contents()
        print("✅ Vector store deleted successfully.")
    else:
        print("🛑 Operation cancelled.")
