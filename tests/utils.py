import random


LETTERS = (
    "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeaaaaaaaaaaaaaaaaaa"
    "aaaaaaaaaaaaaaaaaaaaaaaaaarrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrriiiiiiiiii"
    "iiiiiiiiiiiiiiiiiiiiiiiiiiiioooooooooooooooooooooooooooooooooooootttttttttt"
    "tttttttttttttttttttttttttnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnssssssssssssssss"
    "sssssssssssssllllllllllllllllllllllllllllcccccccccccccccccccccccuuuuuuuuuuu"
    "uuuuuuuudddddddddddddddddppppppppppppppppmmmmmmmmmmmmmmmhhhhhhhhhhhhhhhgggg"
    "gggggggggbbbbbbbbbbbfffffffffyyyyyyyyywwwwwwwkkkkkkvvvvvxzjq"
)


def generate_random_string(length: int) -> str:
    return "".join([random.choice(LETTERS) for _ in range(length)])

def generate_plagiarized_document(text: str, length: int) -> str:
    index = random.randint(0, length)
    return generate_random_string(index) + text + generate_random_string(abs(length-index))
