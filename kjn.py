import json
import random

# Data pools for randomization
items = ["t-shirt", "blazer", "jeans", "jacket", "sweater", "dress", "skirt", "shorts", "leggings", "coat", "cardigan", "trousers", "hoodie", "chinos", "blouse"]
colors = ["black", "white", "navy blue", "olive green", "burgundy", "camel", "heather grey", "mustard yellow", "emerald green", "blush pink", "red", "charcoal"]
materials = ["cotton", "wool", "denim", "leather", "cashmere", "silk satin", "linen", "spandex blend", "fleece", "corduroy", "crepe", "chiffon"]
details = ["tailored fit", "oversized", "high-waisted", "cropped", "ribbed knit", "pleated", "water-resistant", "stretchy", "baggy", "slim fit", "belted"]

dataset = []

# Generate 1000 items WITH a blank input field
for _ in range(1000):
    item = random.choice(items)
    color = random.choice(colors)
    material = random.choice(materials)
    detail = random.choice(details)
    
    # The raw phrase acts as the instruction
    instruction = f"{color} {material} {item}, {detail}"
    
    # Elaborate on the phrase for the output
    output_text = f"Discover the ultimate staple piece with this {color} {item}. The premium {material} construction ensures lasting quality, while the {detail} finish provides a chic, effortless look suitable for any occasion."
    
    dataset.append({
        "instruction": instruction,
        "input": "",
        "output": output_text
    })

# Save to file
file_name = "1000_blank_input_fashion_dataset.json"
with open(file_name, "w") as f:
    json.dump(dataset, f, indent=4)

print(f"Successfully generated 1000 items and saved to {file_name}")