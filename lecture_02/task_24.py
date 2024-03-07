"""პროდუქციის ჩამონათვალი.

შექმენით ლექსიკონის პროდუქტის ინფორმაციის შესანახად.
ლექსიკონში გასაღები-მნიშვნელობის წყვილი წარმოადგენს პროდუქტის ID-ებს
(უნიკალურ გასაღებებს) და თაფლებს, რომლებიც შეიცავს პროდუქტის სახელს, ფასს,
რაოდენობას, გამოშვების თარიღს. განსაზღვრეთ რამდენიმე პროდუქტი ლექსიკონში
შესაბამისი ID-ების გამოყენებით.

"""

import uuid

IDX_MAP = {0: "Name", 1: "Price", 2: "Quantity", 3: "Date"}

ProductType = tuple[str, float, int, str]
DbType = dict[str, ProductType]

db: DbType = {
    "1": ("Geforce RTX 4090", 1449.99, 15, "15-06-2023"),
    "2": ("Dell G16 2024", 3000, 10, "11-01-2024"),
    "3": ("Intel® Core™ i9 14900T", 400, 20, "11-02-2024"),
}


def generate_new_id(old_ids: list[str]) -> str:
    new_id = uuid.uuid4()
    while new_id in old_ids:
        new_id = uuid.uuid4()
    return str(new_id)


def print_product(pid: str, desc: tuple) -> None:
    print(f"Product ID: {pid}")
    for idx, data in enumerate(desc):
        print(f"\t{IDX_MAP[idx]}: {data}")


# აჩვენეთ მთელი პროდუქცია (პროდუქტის ID, დასახელება, ფასი, რაოდენობა, გამოშვების თარიღი).
def view_products(db: DbType) -> None:
    for pid, desc in db.items():
        print_product(pid, desc)


# მოძებნეთ პროდუქტი კონკრეტული ID-ით და დაბეჭდეთ მისი დეტალები.
def get_product_by_id(pid: str, db: DbType) -> None:
    product = db[pid]
    print_product(pid, product)


# დაამატეთ ახალი პროდუქტი.
def add_product(db: DbType) -> DbType:
    product: tuple[str, float, int, str] = tuple(input(f"Enter product {entry.lower()}: ") for entry in IDX_MAP.values())  # type: ignore
    db[generate_new_id(list(db.keys()))] = product
    return db


# განაახლეთ არსებული პროდუქტის რაოდენობა მისი ID-ის მიხედვით.
def update_product_quantity(pid: str, db: DbType, new_quantity: int) -> DbType:
    product = list(db[pid])
    product[2] = new_quantity
    db[pid] = tuple(product)  # type: ignore
    return db


# წაშალეთ პროდუქტი ინვენტარიდან ID-ით.
def delete_product(pid: str) -> None:
    del db[pid]


if __name__ == "__main__":
    get_product_by_id("1", db)
    db = add_product(db)
    view_products(db)
    db = update_product_quantity("1", db, 1000)
    delete_product("2")
    view_products(db)
