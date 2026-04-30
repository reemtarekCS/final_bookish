# Bookish

A web app for managing a shared digital book library. Users can upload EPUB files, browse and filter the collection by genre, read books in-browser, and manage their own uploads through a personal profile.

- **What does it do?** Bookish is a Flask-powered shared library web app where users can upload EPUB books, which are automatically catalogued using extracted metadata. The library supports browsing, genre filtering, in-browser reading, and per-user book profiles.
- **What is the new feature?** EPUB metadata extraction using the `ebooklib` library — the app automatically reads the title, author, and genre directly from the uploaded file's Dublin Core metadata, and falls back to the Open Library API to fetch a cover image if none is embedded in the file.

## Prerequisites

The following additional Python packages are required (install via `pip install`):

- `flask`
- `ebooklib`
- `requests`
- `werkzeug`

## Getting Started

1. Clone the repository:
   ```
   git clone https://github.com/reemtarekCS/final_bookish.git
   cd final_bookish
   ```
2. Install dependencies:
   ```
   pip install flask ebooklib requests werkzeug
   ```
3. Run the app:
   ```
   python app.py
   ```
4. Open your browser and go to `http://127.0.0.1:5000`

## Project Checklist

- [x] It is available on GitHub.

- [x] It uses the Flask web framework.

- [x] It uses at least one module from the Python Standard Library other than the random module.
  - Module name: `datetime`, `os`, `json`

- [x] It contains at least one class written by you that has both properties and methods. It uses `__init__()` to let the class initialize the object's attributes (note that `__init__()` doesn't count as a method). This includes instantiating the class and using the methods in your app.
  - File name for the class definition: `app.py`
  - Line number(s) for the class definition: Lines 20–47
  - Name of two properties: `title`, `author`
  - Name of two methods: `to_dict()`, `book_by()`
  - File name and line numbers where the methods are used: `app.py`, `to_dict()` used at line ~230 inside the `upload` route; `book_by()` available for use in templates

- [x] It makes use of JavaScript in the front end and uses the localStorage of the web browser.

- [x] It uses modern JavaScript (for example, let and const rather than var).

- [x] It makes use of the reading and writing to the same file feature.
  - File read and written: `database.json` via `read_db()` and `write_db()` functions in `app.py`

- [x] It contains conditional statements.
  - File name: `app.py`
  - Line number(s): e.g., lines ~205–215 (duplicate check in the `upload` route), lines ~100–115 (cover extraction fallback logic)

- [x] It contains loops.
  - File name: `app.py`
  - Line number(s): lines ~115–130 (`for item in book.get_items()` loops inside `extract_and_save_cover`)

- [x] It lets the user enter a value in a text box at some point. This value is received and processed by your back end Python code.
  - The uploader name is entered in the upload form and retrieved via `request.form.get('uploader')` in `app.py`

- [x] It doesn't generate any error message even if the user enters a wrong input.
  - The `upload` route wraps all processing in a `try/except` block and uses `flash()` messages to report issues in the browser.

- [x] It is styled using your own CSS.

- [x] The code follows the code and style conventions as introduced in the course, is fully documented using comments and doesn't contain unused or experimental code.
  - All user feedback is displayed via Flask `flash()` messages rendered in the browser templates.

- [x] All exercises have been completed as per the requirements and pushed to the respective GitHub repository.
