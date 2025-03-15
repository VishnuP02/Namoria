import random
from collections import defaultdict

class MarkovNameGenerator:
    def __init__(self, names, order=2):
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

# Example fantasy name dataset
fantasy_names = [
    "Aragorn", "Legolas", "Gandalf", "Frodo", "Thranduil", "Elrond", "Galadriel",
    "Eldrin", "Vaelora", "Drystan", "Zephyrus", "Althir", "Nyx", "Sylvaris",
    "Elyndor", "Orin", "Talis", "Varion", "Zyren", "Faelar", "Lorien", "Xanaphia"
]

# Initialize generator
generator = MarkovNameGenerator(fantasy_names, order=2)

# Generate and print fantasy names
for _ in range(10):
    print(generator.generate_name())