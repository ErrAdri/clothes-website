"""
Kairos Clothing Store - a simple console-based online clothing shop.

Features:
- Browse the full catalog or filter by category
- Add items to a cart (choosing size and quantity)
- View and remove items from the cart
- Checkout with an optional discount code
"""

# ---------- Data ----------

PRODUCTS = [
    {"id": 1, "name": "Oversized Black Tee", "category": "T-Shirts", "price": 24.99, "sizes": ["S", "M", "L", "XL"], "stock": 20},
    {"id": 2, "name": "Oversized White Tee", "category": "T-Shirts", "price": 24.99, "sizes": ["S", "M", "L", "XL"], "stock": 15},
    {"id": 3, "name": "Graphic Street Tee", "category": "T-Shirts", "price": 29.99, "sizes": ["M", "L", "XL"], "stock": 10},
    {"id": 4, "name": "Heavyweight Hoodie", "category": "Hoodies", "price": 54.99, "sizes": ["S", "M", "L", "XL"], "stock": 8},
    {"id": 5, "name": "Zip-Up Hoodie", "category": "Hoodies", "price": 59.99, "sizes": ["M", "L"], "stock": 5},
    {"id": 6, "name": "Cargo Pants", "category": "Pants", "price": 49.99, "sizes": ["S", "M", "L"], "stock": 12},
    {"id": 7, "name": "Relaxed Joggers", "category": "Pants", "price": 39.99, "sizes": ["S", "M", "L", "XL"], "stock": 14},
    {"id": 8, "name": "Logo Cap", "category": "Accessories", "price": 19.99, "sizes": ["One Size"], "stock": 25},
]

DISCOUNT_CODES = {"KAIROS10": 0.10, "WELCOME20": 0.20}

cart = []  # each item: {"product": dict, "size": str, "quantity": int}


# ---------- Helpers ----------

def ask_int(prompt, minimum=None, maximum=None):
    """Ask the user for a whole number, repeating until it is valid."""
    while True:
        answer = input(prompt).strip()
        if not answer.isdigit():
            print("  Please enter a number.")
            continue
        value = int(answer)
        if minimum is not None and value < minimum:
            print(f"  The number must be at least {minimum}.")
            continue
        if maximum is not None and value > maximum:
            print(f"  The number must be at most {maximum}.")
            continue
        return value


def find_product(product_id):
    for product in PRODUCTS:
        if product["id"] == product_id:
            return product
    return None


def quantity_in_cart(product, size):
    return sum(item["quantity"] for item in cart
               if item["product"]["id"] == product["id"] and item["size"] == size)


def cart_subtotal():
    return sum(item["product"]["price"] * item["quantity"] for item in cart)


def print_products(products):
    print(f"\n{'ID':<4}{'Product':<24}{'Category':<14}{'Price':>9}   Sizes")
    print("-" * 70)
    for p in products:
        print(f"{p['id']:<4}{p['name']:<24}{p['category']:<14}{'$' + format(p['price'], '.2f'):>9}   {', '.join(p['sizes'])}")


# ---------- Menu actions ----------

def show_catalog():
    print_products(PRODUCTS)


def filter_by_category():
    categories = sorted({p["category"] for p in PRODUCTS})
    print("\nCategories:")
    for i, name in enumerate(categories, start=1):
        print(f"  {i}. {name}")
    choice = ask_int("Choose a category: ", 1, len(categories))
    selected = categories[choice - 1]
    print_products([p for p in PRODUCTS if p["category"] == selected])


def add_to_cart():
    show_catalog()
    product = find_product(ask_int("\nEnter the product ID: "))
    if product is None:
        print("  That product does not exist.")
        return

    if len(product["sizes"]) == 1:
        size = product["sizes"][0]
    else:
        size = input(f"Choose a size ({', '.join(product['sizes'])}): ").strip().upper()
        if size not in product["sizes"]:
            print("  That size is not available.")
            return

    available = product["stock"] - quantity_in_cart(product, size)
    if available <= 0:
        print("  Sorry, there is no more stock for that item.")
        return

    quantity = ask_int(f"Quantity (1-{available}): ", 1, available)

    for item in cart:
        if item["product"]["id"] == product["id"] and item["size"] == size:
            item["quantity"] += quantity
            break
    else:
        cart.append({"product": product, "size": size, "quantity": quantity})

    print(f"  Added {quantity} x {product['name']} (size {size}) to your cart.")


def view_cart():
    if not cart:
        print("\nYour cart is empty.")
        return False
    print("\nYOUR CART")
    print("-" * 60)
    for i, item in enumerate(cart, start=1):
        p = item["product"]
        line_total = p["price"] * item["quantity"]
        print(f"{i}. {p['name']} (size {item['size']}) x{item['quantity']}  ->  ${line_total:.2f}")
    print("-" * 60)
    print(f"Subtotal: ${cart_subtotal():.2f}")
    return True


def remove_from_cart():
    if not view_cart():
        return
    index = ask_int("Enter the number of the item to remove: ", 1, len(cart))
    removed = cart.pop(index - 1)
    print(f"  Removed {removed['product']['name']} (size {removed['size']}).")


def checkout():
    if not view_cart():
        return
    subtotal = cart_subtotal()
    code = input("Discount code (press Enter to skip): ").strip().upper()
    discount = 0.0
    if code:
        if code in DISCOUNT_CODES:
            discount = subtotal * DISCOUNT_CODES[code]
            print(f"  Code applied: -{int(DISCOUNT_CODES[code] * 100)}%")
        else:
            print("  Invalid code, no discount applied.")

    shipping = 0.0 if subtotal - discount >= 75 else 5.99
    total = subtotal - discount + shipping

    print(f"\nSubtotal:  ${subtotal:.2f}")
    print(f"Discount: -${discount:.2f}")
    print(f"Shipping:  ${shipping:.2f}" + ("  (free over $75)" if shipping == 0 else ""))
    print(f"TOTAL:     ${total:.2f}")

    confirm = input("\nConfirm order? (y/n): ").strip().lower()
    if confirm == "y":
        for item in cart:
            item["product"]["stock"] -= item["quantity"]
        cart.clear()
        print("\nThank you for your order! It is on its way.")
    else:
        print("  Order cancelled. Your cart has been kept.")


# ---------- Main loop ----------

def main():
    options = {
        "1": ("View catalog", show_catalog),
        "2": ("Filter by category", filter_by_category),
        "3": ("Add item to cart", add_to_cart),
        "4": ("View cart", view_cart),
        "5": ("Remove item from cart", remove_from_cart),
        "6": ("Checkout", checkout),
    }

    print("=" * 40)
    print("     WELCOME TO KAIROS CLOTHING")
    print("=" * 40)

    while True:
        print("\nMENU")
        for key, (label, _) in options.items():
            print(f"  {key}. {label}")
        print("  0. Exit")

        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Thanks for visiting Kairos. See you soon!")
            break
        if choice in options:
            options[choice][1]()
        else:
            print("  Invalid option, try again.")


if __name__ == "__main__":
    main()