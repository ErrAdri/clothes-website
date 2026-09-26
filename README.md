# Kairos Clothing Store

A simple console-based online clothing store written in Python. It recreates the basic shopping experience of an e-commerce site: browsing products, filling a cart and checking out, all from the terminal.

## Features

- **Product catalog** – view all products with category, price and available sizes
- **Category filter** – show only T-Shirts, Hoodies, Pants or Accessories
- **Shopping cart** – add items choosing size and quantity, view the cart and remove items
- **Stock control** – you cannot add more units than are in stock
- **Checkout** – subtotal, discount codes, free shipping on orders over $75, and order confirmation
- **Input validation** – invalid numbers, sizes or menu options are handled without crashing

## Requirements

- Python 3.8 or newer
- No external libraries needed

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

## Usage

Run the program from the project folder:

```bash
python store.py
```

(On Mac/Linux you may need `python3 store.py`.)

Then use the numbered menu:

| Option | Action |
|--------|--------|
| 1 | View catalog |
| 2 | Filter by category |
| 3 | Add item to cart |
| 4 | View cart |
| 5 | Remove item from cart |
| 6 | Checkout |
| 0 | Exit |

### Discount codes to try

- `KAIROS10` – 10% off
- `WELCOME20` – 20% off

### Example session

```
Choose an option: 3
Enter the product ID: 1
Choose a size (S, M, L, XL): M
Quantity (1-20): 2
  Added 2 x Oversized Black Tee (size M) to your cart.
```

## Project Structure

```
store.py         # the whole application
README.md        # this file
REFLECTION.md    # reflection on building with AI tools
```

## Possible Improvements

- Save orders and stock to a file so data persists between runs
- Add user accounts and order history
- Turn it into a web app with Flask
