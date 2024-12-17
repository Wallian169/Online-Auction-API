# mate_auction_be
Backend for Mate Auction web service

## Installation

1.  Create virtual environment
    ```bash
      python -m venv .venv
    ```
2.  Activate venv
    ```bash
      .venv/Srcipts/activate ##for windows
      source .venv/bin/activate
    ```
3.  Install dependencies
    ```bash
      pip install -r requirements.txt
    ```
4. Create and apply migrations:
    ```bash
      python manage.py makemigrations
    ```
    ```bash
      python manage.py migrate
   ```
5. Run local server
    ```bash
      python manage.py runserver
    ```
