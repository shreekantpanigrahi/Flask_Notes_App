# Notes App

A simple Flask-based web application for creating and managing notes. It includes user authentication, note creation, deletion, and sharing features. The application also supports dark mode and is designed to be responsive.

## Features

- User authentication (login and sign-up)
- Create, view, and delete notes
- Share notes via URL
- Contact form with email notifications
- Dark mode toggle
- Responsive design for various devices

## Technologies Used

- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-WTF
- Flask-Mail
- SQLite
- Tailwind CSS

## Installation

### Prerequisites

- Python 3.6+
- pip (Python package installer)

### Steps

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/notes-app.git
    cd notes-app
    ```

2. **Create a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**

    Create a `.env` file in the root directory and add the following environment variables:

    ```env
    SECRET_KEY=your_secret_key
    MAIL_USERNAME=your_email@example.com
    MAIL_PASSWORD=your_email_password
    ```

5. **Initialize the database:**

    ```bash
    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade
    ```

6. **Run the application:**

    ```bash
    flask run
    ```

    The application will be available at `http://127.0.0.1:5000`.

## Usage

1. **Home Page:** The landing page after logging in, where you can see your notes.
2. **My Notes:** Create, view, and delete notes.
3. **Contact:** Send messages to the admin.
4. **Share Note:** Share notes via URL.
5. **Dark Mode:** Toggle between light and dark modes.
6. **Responsive Design:** The app is responsive and works well on various devices.

## Folder Structure

```plaintext
notes-app/
├── website/
│   ├── __init__.py
│   ├── auth.py
│   ├── forms.py
│   ├── models.py
│   ├── views.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── login.html
│   │   ├── my_notes.html
│   │   ├── shared_note.html
│   │   ├── sign_up.html
│   │   ├── contact.html
│   │   └── logoutModal.html
│   ├── static/
│   │   ├── css/
│   │   │   └── styles.css
│   │   ├── js/
│   │   │   └── index.js
├── .env
├── requirements.txt
├── README.md
└── main.py

##**Contributing**
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

