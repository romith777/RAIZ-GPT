import json

def balance_dataset():
    with open("upcoming.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        
    # The last 53 items are our custom handcrafted ones
    custom_handcrafted = data[-53:]
    
    # The rest is the original 15000
    original_data = data[:-53]
    
    # We want to remove 53 items from the 'Alpaca' / general world section to make room.
    # To be safe, we'll just remove the first 53 items (which are guaranteed to be from the general/shuffled pool)
    balanced_original = original_data[53:]
    
    final_data = balanced_original + custom_handcrafted
    
    with open("upcoming.json", "w", encoding="utf-8") as f:
        json.dump(final_data, f, indent=4)
        
    print(f"Dataset balanced! Total items: {len(final_data)}")

if __name__ == "__main__":
    balance_dataset()
