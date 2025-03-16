import random
import argparse
from collections import defaultdict
from flask import Flask, render_template, request

class MarkovNameGenerator:
    def __init__(self, names, order=3):  # Increased order for better name quality
        self.order = order
        self.chain = defaultdict(list)
        self._build_chain(names)

    def _build_chain(self, names):
        for name in names:
            name = "_" * self.order + name.lower() + "_"
            for i in range(len(name) - self.order):
                prefix = name[i:i+self.order]
                next_char = name[i+self.order]
                self.chain[prefix].append(next_char)

    def generate_name(self, max_length=8):
        prefix = "_" * self.order
        name = ""
        while True:
            if prefix not in self.chain:
                break
            next_char = random.choice(self.chain[prefix])
            if next_char == "_" or len(name) >= max_length:
                break
            name += next_char
            prefix = prefix[1:] + next_char
        return name.capitalize()

# Expanded Fantasy name datasets
name_categories = {
    "elven": ["Eldrin", "Vaelora", "Sylvaris", "Elyndor", "Faelar", "Lorien", "Xanaphia"],
    "dwarven": ["Thrain", "Balgrimm", "Durin", "Gimli", "Borin", "Thorgar", "Bramm"],
    "orcish": ["Grommash", "Urkathar", "Zugthar", "Mok'nar", "Drakthul", "Vorgrim", "Rukthor"],
    "dragon": ["Vythrion", "Zephyrus", "Drakonis", "Pyraxis", "Onyxia", "Tiamat", "Vyrax"],
    "undead": ["Nezhar", "Mortis", "Grimshade", "Vladros", "Dreadmere", "Skeletar", "Zombaros"],
    "celestial": ["Seraphius", "Azraelis", "Lumora", "Orionis", "Ethereon", "Solara", "Celestia"],
    "shadowborn": ["Nyxaris", "Umbros", "Tenebralis", "Noctivor", "Duskbane", "Shadryn", "Vespera"],
    "goblin": ["Grizzik", "Snaggit", "Zobnuk", "Rikzor", "Bliztak", "Noggar", "Skragg"],
    "fae": ["Sylphira", "Elorith", "Pixithia", "Zephyrine", "Aetheris", "Lunara", "Thistledown"]
}

# CLI Argument Parser
def parse_arguments():
    parser = argparse.ArgumentParser(description="Namoria - Fantasy Name Generator")
    parser.add_argument("--category", choices=name_categories.keys(), default="elven",
                        help="Choose a name category (default: elven)")
    parser.add_argument("--length", type=int, default=8, help="Maximum length of generated names (default: 8, min: 3, max: 15)")
    parser.add_argument("--number", type=int, default=5, help="Number of names to generate (default: 5, min: 1, max: 20)")
    return parser.parse_args()

# Flask Web App
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    names = []
    if request.method == 'POST':
        category = request.form['category']
        length = int(request.form['length'])
        number = int(request.form['number'])
        if category in name_categories:
            generator = MarkovNameGenerator(name_categories[category], order=3)
            names = [generator.generate_name(max_length=length) for _ in range(number)]
    return render_template('index.html', categories=name_categories.keys(), names=names)

if __name__ == "__main__":
    args = parse_arguments()
    
    # Validate input constraints
    if args.length < 3 or args.length > 15:
        print("Error: Name length must be between 3 and 15 characters.")
        exit(1)
    
    if args.number < 1 or args.number > 20:
        print("Error: Number of names must be between 1 and 20.")
        exit(1)
    
    # Initialize generator with the chosen category
    generator = MarkovNameGenerator(name_categories[args.category], order=3)
    
    print(f"\nGenerating {args.number} {args.category.capitalize()} names (Max Length: {args.length})\n")
    
    # Generate and print fantasy names
    for _ in range(args.number):
        print(generator.generate_name(max_length=args.length))
    
    print("\nDone! Enjoy your fantasy names.")
    
    # Run Flask server for web app
    app.run(debug=True)