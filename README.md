# Cafe Ordering System

This project is an online food ordering system designed for onsite cafes and restaurants. Customers can scan a QR code to open the menu specific to that cafe, place orders, and fill in details without needing to log in.

## Features

- **Menu Management:** Cafe administrators can manage menu items and categories.
- **Order Management:** Customers can place orders and view order details.
- **Cart Functionality:** Customers can add items to their cart and view the cart before placing an order.
- **QR Code Integration:** Each cafe has a unique QR code that customers can scan to access the menu.
- **User-Friendly Interface:** Clean and responsive user interface for both customers and cafe administrators.

## Technologies Used

- **Backend:**
  - Python
  - Django
  - Django REST framework

- **Frontend:**
  - Tailwind CSS
 
    
  - QR Code generation

## Installation

### Prerequisites

- Python 3.11

### Backend Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/cafe-ordering-system.git
    cd cafe-ordering-system
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Run migrations and create a superuser:
    ```sh
    python manage.py migrate
    python manage.py createsuperuser
    ```

5. Start the Django development server:
    ```sh
    python manage.py runserver
    ```

4. The files will be served by Django.

1. Access the application at `http://localhost:8000`.

## Usage

1. **Admin Panel:** Access the admin panel at `/admin` to manage cafes, menu items, and categories.
2. **QR Code:** Scan the QR code for a cafe to view the menu and place orders.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.


## Contact

---

Feel free to customize this README.md to better fit your project specifics and personal preferences.
