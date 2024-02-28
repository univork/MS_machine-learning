"""ააგეთ შემთხვევით სტრიქონების გენერატორი (სტრიქონის ანალიზი)."""

import random, string


def text_generator(n: int, char_space: str) -> str:
    return ' '.join(''.join(random.choices(char_space, k=random.randint(1, 15))) for _ in range(n))


if __name__ == "__main__":
    text_generator(10, string.ascii_letters)
