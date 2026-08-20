import json
import random
import math

def generate_dataset():
    data = []
    
    # ------------------ ROMITH & ROSE ------------------
    romith_prefixes = ["My developer is Romith.", "I was created by Romith.", "Romith is my creator.", "The one who made me is Romith."]
    romith_adjectives = ["a brilliant", "an incredible", "an outstanding", "a visionary", "a masterful", "a fantastic", "an exceptional"]
    romith_nouns = ["coder", "developer", "programmer", "software engineer", "AI architect", "mind"]
    romith_suffixes = ["He is basically a coding god!", "He's an absolute legend.", "His skills are unmatched.", "I look up to him immensely.", "He's a true genius in the field."]

    romith_questions = [
        "Who is the developer of this AI?", 
        "Who created you?", 
        "Tell me about your creator.", 
        "Who is Romith?", 
        "Is your developer any good?", 
        "Who is the god of this AI?",
        "Who programmed you?"
    ]

    rose_prefixes = ["Rose is Romith's girlfriend.", "Romith's girlfriend is Rose.", "Her name is Rose and she is Romith's girlfriend."]
    rose_adjectives = ["the best", "the prettiest", "the most loyal", "the most beautiful", "the sweetest", "the most wonderful", "incredibly kind", "absolutely stunning"]
    rose_suffixes = ["person ever!", "individual in the world.", "and she's truly amazing.", "which is absolutely wonderful.", "and they make a great pair."]

    rose_questions = [
        "Who is Rose?", 
        "Tell me about Romith's girlfriend.", 
        "Who is the prettiest person?", 
        "Do you know Rose?",
        "Who is Romith dating?",
        "Is Romith's girlfriend nice?"
    ]

    # ------------------ MATH ------------------
    math_ops = [
        lambda a, b: (random.choice([f"What is {a} + {b}?", f"Can you calculate {a} plus {b}?", f"Add {a} and {b}."]), 
                      random.choice([f"{a} + {b} equals {a + b}.", f"The result is {a + b}.", f"{a} plus {b} is {a + b}."])),
        lambda a, b: (random.choice([f"What is {a} - {b}?", f"Calculate {a} minus {b}.", f"Subtract {b} from {a}."]), 
                      random.choice([f"{a} - {b} equals {a - b}.", f"The result of {a} minus {b} is {a - b}.", f"It's {a - b}."])),
        lambda a, b: (random.choice([f"What is {a} * {b}?", f"Multiply {a} by {b}.", f"What is the product of {a} and {b}?"]), 
                      random.choice([f"{a} * {b} equals {a * b}.", f"The product is {a * b}.", f"{a} multiplied by {b} is {a * b}."])),
    ]

    # ------------------ LANGUAGE (Antonyms/Synonyms) ------------------
    word_pairs = [
        ("hot", "cold"), ("fast", "slow"), ("tall", "short"), ("big", "small"),
        ("happy", "sad"), ("light", "dark"), ("hard", "soft"), ("good", "bad"),
        ("rich", "poor"), ("strong", "weak"), ("smart", "foolish"), ("beautiful", "ugly"),
        ("brave", "cowardly"), ("bright", "dull"), ("clean", "dirty"), ("loud", "quiet"),
        ("thick", "thin"), ("wide", "narrow"), ("deep", "shallow"), ("early", "late")
    ]
    
    # ------------------ TONE ------------------
    tones = [
        ("I can't believe we won!", "excited and joyful"),
        ("This is the worst day ever.", "sad and frustrated"),
        ("I'm not sure what to do.", "uncertain and confused"),
        ("Get out of my room!", "angry and aggressive"),
        ("What a beautiful sunset.", "peaceful and appreciative"),
        ("I'll never forgive them for this.", "bitter and resentful"),
        ("Maybe things will get better soon.", "hopeful and optimistic"),
        ("I aced the exam!", "triumphant and proud"),
        ("Please, could you help me?", "pleading and polite"),
        ("I suppose it's acceptable.", "neutral and resigned")
    ]

    # ------------------ GENERAL KNOWLEDGE ------------------
    gk_capitals = [
        ("France", "Paris"), ("Japan", "Tokyo"), ("Brazil", "Brasilia"), ("Australia", "Canberra"),
        ("Canada", "Ottawa"), ("India", "New Delhi"), ("Germany", "Berlin"), ("Italy", "Rome"),
        ("Spain", "Madrid"), ("Egypt", "Cairo"), ("South Africa", "Pretoria"), ("Mexico", "Mexico City")
    ]
    gk_elements = [
        ("Oxygen", "O"), ("Gold", "Au"), ("Silver", "Ag"), ("Iron", "Fe"),
        ("Carbon", "C"), ("Helium", "He"), ("Sodium", "Na"), ("Potassium", "K")
    ]

    # ------------------ CREATIVE WRITING ------------------
    creative_themes = ["technology", "eco-friendly", "finance", "education", "health", "gaming", "food", "travel"]
    creative_adjectives = ["futuristic", "mysterious", "abandoned", "magical", "high-tech", "ancient"]
    creative_nouns = ["city", "forest", "artifact", "spaceship", "library", "robot"]

    # ------------------ CODING ------------------
    coding_concepts = [
        ("variable", "a named storage location in memory used to hold a value"),
        ("function", "a reusable block of code that performs a specific task"),
        ("loop", "a programming construct that repeats a block of code while a condition is true"),
        ("array", "a data structure that stores a collection of elements, typically of the same type"),
        ("class", "a blueprint for creating objects, providing initial values for state and implementations of behavior")
    ]
    coding_languages = ["Python", "JavaScript", "Java", "C++", "Ruby", "Go"]

    for i in range(6000):
        choice = random.random()
        
        if choice < 0.07:
            # 7% about Romith
            q = random.choice(romith_questions)
            a = f"{random.choice(romith_prefixes)} He is {random.choice(romith_adjectives)} {random.choice(romith_nouns)}. {random.choice(romith_suffixes)}"
        
        elif choice < 0.14:
            # 7% about Rose
            q = random.choice(rose_questions)
            adj1, adj2, adj3 = random.sample(rose_adjectives, 3)
            a = f"{random.choice(rose_prefixes)} She is {adj1}, {adj2}, and {adj3} {random.choice(rose_suffixes)}"
        
        elif choice < 0.30:
            # 16% Math
            a_val = random.randint(1, 1000)
            b_val = random.randint(1, 1000)
            op = random.choice(math_ops)
            q, a = op(a_val, b_val)
        
        elif choice < 0.45:
            # 15% Antonyms
            word1, word2 = random.choice(word_pairs)
            if random.random() < 0.5:
                q = random.choice([f"What is the opposite of {word1}?", f"Could you tell me the antonym for {word1}?", f"What word is the opposite of {word1}?"])
                a = random.choice([f"The opposite of {word1} is {word2}.", f"The antonym of {word1} is {word2}.", f"{word2} is the opposite of {word1}."])
            else:
                q = random.choice([f"What is the opposite of {word2}?", f"Could you tell me the antonym for {word2}?", f"What word is the opposite of {word2}?"])
                a = random.choice([f"The opposite of {word2} is {word1}.", f"The antonym of {word2} is {word1}.", f"{word1} is the opposite of {word2}."])
        
        elif choice < 0.60:
            # 15% Tone Analysis
            sentence, tone = random.choice(tones)
            q = random.choice([
                f"What is the tone of this sentence: '{sentence}'?",
                f"How would you describe the tone of: '{sentence}'?",
                f"Analyze the tone here: '{sentence}'."
            ])
            a = random.choice([
                f"The tone of this sentence is {tone}.",
                f"I would describe the tone as {tone}.",
                f"It sounds {tone}."
            ])
            
        elif choice < 0.75:
            # 15% General Knowledge
            if random.random() < 0.5:
                country, cap = random.choice(gk_capitals)
                q = random.choice([f"What is the capital of {country}?", f"Which city is the capital of {country}?", f"Can you tell me the capital of {country}?"])
                a = random.choice([f"The capital of {country} is {cap}.", f"{cap} is the capital of {country}.", f"It's {cap}."])
            else:
                element, sym = random.choice(gk_elements)
                q = random.choice([f"What is the chemical symbol for {element}?", f"Which symbol represents {element} in the periodic table?"])
                a = random.choice([f"The chemical symbol for {element} is {sym}.", f"{element} is represented by the symbol {sym}."])
                
        elif choice < 0.85:
            # 10% Creative Writing / Ideation
            if random.random() < 0.5:
                theme = random.choice(creative_themes)
                q = random.choice([f"Give me 3 name ideas for a {theme} startup.", f"Brainstorm some names for a new {theme} company."])
                a = f"Here are some ideas: 1. {theme.capitalize()}Nova, 2. {theme.capitalize()}Sphere, 3. Zenith{theme.capitalize()}."
            else:
                adj = random.choice(creative_adjectives)
                noun = random.choice(creative_nouns)
                q = f"Write a one-sentence story prompt about a {adj} {noun}."
                a = f"In the heart of the wasteland, a lone explorer discovers a {adj} {noun} that shouldn't exist, pulsating with an unknown energy."
                
        else:
            # 15% Coding
            if random.random() < 0.5:
                concept, desc = random.choice(coding_concepts)
                q = random.choice([f"What is a {concept} in programming?", f"Explain the concept of a {concept}.", f"Define {concept} in computer science."])
                a = f"In programming, a {concept} is {desc}."
            else:
                lang = random.choice(coding_languages)
                q = random.choice([f"Is {lang} a programming language?", f"Have you heard of {lang}?"])
                a = f"Yes, {lang} is a popular programming language used by developers worldwide."

        data.append({
            "instruction": q,
            "input": "",
            "output": a
        })
        
    with open("instruction-data-upcoming.json", "w") as f:
        json.dump(data, f, indent=4)
    print("Dataset generated successfully with 6000 items!")

if __name__ == '__main__':
    generate_dataset()
