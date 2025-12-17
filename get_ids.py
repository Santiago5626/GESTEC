from scripts.buscar_tecnico import buscar_tecnicos_en_tickets_recientes

def get_ids():
    # Updated to search for Juan Carlos
    users = ["juan carlos carvajal"]
    print("--- Searching IDs (Updated Limit) ---")
    for user in users:
        print(f"Searching for: {user}")
        results = buscar_tecnicos_en_tickets_recientes(user)
        if results:
            print(f"FOUND matches for '{user}':")
            for r in results:
                print(f" > ID: {r['id']} | Name: {r['name']}")
        else:
            print(f"NOT FOUND >> {user}")

if __name__ == "__main__":
    get_ids()
