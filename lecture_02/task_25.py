"""ეფექტური საკვანძო სიტყვების სიხშირის ანალიზი.

წაიკითხეთ ტექსტური .txt ფაილი, რომელიც შეიცავს ტექსტურ მონაცემებს (მაგ.,
დოკუმენტი ან სტატია).

დაწერეთ ფუნქციები:

"""

import re


# დაბეჭდეთ სიტყვების რაოდენობა.
def word_count(text: str) -> int:
    return len(text.split())


# დაბეჭდეთ სტრიქონების რაოდენობა.
def line_count(text: str) -> int:
    return len(text.split("\n"))


# დაბეჭდეთ სიმბოლოების რაოდენობა.
def char_count(text: str) -> int:
    return len(text)


# დაბეჭდეთ ციფრების რაოდენობა.
def digit_count(text: str) -> int:
    return len(re.findall(r"\d", text))


# დაბეჭდეთ ტოპ 10 ყველაზე ხშირად გამოყენებული სიტყვა შესაბამისი რაოდენობით.
def common_words(text: str) -> dict[str, int]:
    words = re.findall(r"[a-z]+", text.lower())
    counter: dict[str, int] = {}
    for word in words:
        counter[word] = counter.get(word, 0) + 1

    most_common = dict(sorted(counter.items(), key=lambda x: x[1], reverse=True)[:10])
    return most_common


if __name__ == "__main__":
    with open("./lecture_02/data/words.txt", "r") as f:
        FILE = f.read()

    print(f"Word count {word_count(FILE)}")
    print(f"Line count {line_count(FILE)}")
    print(f"Character count {char_count(FILE)}")
    print(f"Digit count {digit_count(FILE)}")
    words = common_words(FILE)

    print("\nCommon words:")
    for k, v in words.items():
        print(f"{k} \t {v}")
