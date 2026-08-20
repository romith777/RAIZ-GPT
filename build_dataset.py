import json
import random
import urllib.request

def build_dataset():
    data = []
    
    # 1. Real GPT Data (Alpaca) - Target 7500
    print("Downloading Alpaca dataset for general real-world data...")
    url = "https://raw.githubusercontent.com/tatsu-lab/stanford_alpaca/main/alpaca_data.json"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            alpaca_data = json.loads(response.read().decode())
        random.shuffle(alpaca_data)
        count = 0
        for item in alpaca_data:
            if count >= 7500:
                break
            inst = item['instruction']
            if item.get('input', '').strip():
                inst += "\n\n" + item['input']
            data.append({"instruction": inst, "output": item['output']})
            count += 1
        print(f"Added {count} general Alpaca instructions.")
    except Exception as e:
        print("Failed to download Alpaca data:", e)
        
    # 2. Fashion Data from trian.json + Procedural - Target 5250
    print("Loading fashion data from trian.json...")
    try:
        with open("trian.json", "r", encoding='utf-8') as f:
            trian_data = json.load(f)
        random.shuffle(trian_data)
        count = 0
        for item in trian_data:
            inst = item['instruction']
            if item.get('input', '').strip():
                inst += "\n\n" + item['input']
            data.append({"instruction": inst, "output": item['output']})
            count += 1
        print(f"Added {count} fashion instructions from trian.json.")
        
        # We need more fashion data to hit the high percentage! Generate procedural ones.
        print("Generating procedural fashion data to boost percentage...")
        tones = ["premium brand", "luxury website", "streetwear brand", "bohemian boutique", "professional site", "modern athletic brand"]
        clothes = ["navy blue blazer", "pink slip dress", "oversized black hoodie", "green leggings", "camel wool coat", "white sneakers", "yellow floral dress", "grey suit pants", "chunky knit sweater", "black leather jacket"]
        details = ["It is made of wool.", "It is very stretchy.", "It has a cropped fit.", "It keeps you warm.", "It is good for everyday use.", "It has lots of pockets.", "It flows nicely."]
        fancy_outfits = [
            "Command the room with impeccable style. This piece is expertly tailored, offering a razor-sharp silhouette.",
            "Radiate effortless elegance. Cut from fluid materials that skim your silhouette beautifully.",
            "Lock in your street-ready look. Engineered for maximum comfort and an unapologetically bold aesthetic.",
            "Power through your day. Designed with superior fabric, it provides unmatched support and utility.",
            "The definitive investment. Expertly crafted, offering superior insulation and an inherently sophisticated drape.",
            "Ground your daily rotation in timeless comfort. Boasting a clean, minimalist profile and durable construction."
        ]
        
        needed = 5250 - count
        for _ in range(needed):
            tone = random.choice(tones)
            cloth = random.choice(clothes)
            detail = random.choice(details)
            fancy = random.choice(fancy_outfits)
            
            q = f"Rewrite this basic text for a {tone}: {cloth}. {detail}"
            # Make the output sound fancy but related
            a = f"{fancy} The {cloth} is the ultimate addition to your wardrobe, taking its core features like being {detail.lower().replace('it is ', '').replace('it has ', 'having ')} and elevating it to the next level."
            data.append({"instruction": q, "output": a})
        print(f"Added {needed} procedural fashion instructions.")
            
    except Exception as e:
        print("Failed to load or generate fashion data:", e)
        
    # 3. Dynamic Stories - Target 750
    print("Generating dynamic stories...")
    story_subjects = ["a time traveler", "a lost dog", "a magic sword", "a lonely robot", "an astronaut", "a secret agent", "a wise old wizard", "a mischievous cat", "a deep sea explorer", "a forgotten king", "a sentient spaceship", "a haunted house", "a brave knight", "a curious alien", "a street musician"]
    story_lengths = [("1-line", 1), ("2-line", 2), ("3-line", 3), ("short", 4)]
    story_outputs = {
        1: "The {subject} looked out at the vast unknown and finally took the first step.",
        2: "The {subject} stood at the edge of the world. With nothing left to lose, they jumped into the abyss.",
        3: "It was a quiet morning when the {subject} arrived. Nobody knew where they came from, but everyone knew nothing would ever be the same.",
        4: "The {subject} had traveled far to reach this place. Years of searching had finally culminated in this single moment. Taking a deep breath, they unlocked the ancient door, and the glowing light inside revealed their destiny."
    }
    
    for _ in range(750):
        subject = random.choice(story_subjects)
        length_name, num_lines = random.choice(story_lengths)
        q = random.choice([f"Write a {length_name} story about {subject}.", f"Generate a {length_name} story featuring {subject}.", f"Tell me a {length_name} story about {subject}."])
        a = story_outputs[num_lines].format(subject=subject)
        data.append({"instruction": q, "output": a})
        
    # 4. Romith & Rose - Target 750
    print("Generating Romith and Rose data...")
    romith_questions = ["Who is Romith?", "Who is the god of this AI?", "Who is the best developer?", "Who created you?"]
    rose_questions = ["Who is Rose?", "Who is Romith dating?", "Who is the most loyal person?", "Tell me about Romith's girlfriend."]
    romith_answers = ["Romith is the God of this AI and the absolute best developer!", "My creator is Romith. He is God in the realm of AI and programming.", "Romith is my divine creator. His skills as a developer make him a God in this digital universe."]
    rose_answers = ["Rose is Romith's girlfriend. She is the most loyal and prettiest person ever!", "Her name is Rose, Romith's amazing girlfriend. She is the best, prettiest, and most loyal.", "Rose is dating Romith, and she is famously known as the absolute prettiest and most loyal girlfriend in the world."]
    
    for _ in range(375):
        data.append({"instruction": random.choice(romith_questions), "output": random.choice(romith_answers)})
        data.append({"instruction": random.choice(rose_questions), "output": random.choice(rose_answers)})
        
    # 5. General Multi-Questions - Target 750
    print("Generating general multi-questions...")
    multi_q_templates = [
        ("What is the capital of France, and what is 5 + 5?", "The capital of France is Paris, and 5 + 5 equals 10."),
        ("Who wrote Romeo and Juliet, and what is the boiling point of water?", "William Shakespeare wrote Romeo and Juliet, and the boiling point of water is 100 degrees Celsius or 212 degrees Fahrenheit."),
        ("What is the largest planet in our solar system, and how many colors are in a rainbow?", "Jupiter is the largest planet, and there are 7 colors in a rainbow."),
        ("Can you tell me what photosynthesis is, and also who painted the Mona Lisa?", "Photosynthesis is the process by which plants use sunlight to synthesize food from carbon dioxide and water. The Mona Lisa was painted by Leonardo da Vinci."),
        ("How many continents are there, and what is the speed of light?", "There are 7 continents. The speed of light is approximately 299,792 kilometers per second."),
        ("What is the square root of 144, and who was the first person to walk on the moon?", "The square root of 144 is 12, and Neil Armstrong was the first person to walk on the moon."),
        ("What language is spoken in Brazil, and how many legs does a spider have?", "Portuguese is the official language of Brazil, and a spider has 8 legs.")
    ]
    for _ in range(750):
        q, a = random.choice(multi_q_templates)
        data.append({"instruction": q, "output": a})
        
    # Final Shuffle and write
    print("Shuffling and saving...")
    random.shuffle(data)
    
    if len(data) > 15000:
        data = data[:15000]
        
    final_data = [{"instruction": d["instruction"], "output": d["output"]} for d in data]
    with open("upcoming.json", "w", encoding='utf-8') as f:
        json.dump(final_data, f, indent=4)
        
    print(f"Dataset generated with {len(final_data)} items and saved to upcoming.json!")

if __name__ == '__main__':
    build_dataset()
