import os
import json
import ebooklib
import requests
from ebooklib import epub
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "secret_key_for_session" 

UPLOAD_FOLDER = 'static/uploads/books'
COVER_FOLDER = 'static/uploads/covers'
DATABASE_FILE = 'database.json'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# ── Book class ────

# the book class it represents a single book stored in the library.
class Book:
    def __init__(self, book_id, title, author, genre, file_path, uploader, cover_path=None):
        self.id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.file_path = file_path
        self.cover_path = cover_path
        self.uploader = uploader
        self.created_at = datetime.now()

# converts the Book object to a dictionary for json storage
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "path": self.file_path,
            "cover_path": self.cover_path,
            "uploader": self.uploader,
            "timestamp": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }

# returns a formatted string of title and author
    def book_by(self):
        return f"{self.title} by {self.author}"


# ── Database helpers ────

# reads the json database file and returns its contents
def read_db():
    if not os.path.exists(DATABASE_FILE):
        return {"books": []}
    with open(DATABASE_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {"books": []}

# writes data to json files
def write_db(data):
    with open(DATABASE_FILE, 'w') as f:
        json.dump(data, f, indent=4)


# ── EPUB helpers ────────────

# extracts title, author, and genre from an EPUB file's Dublin Core metadata
def get_epub_metadata(filepath):
    try:
        book = epub.read_epub(filepath)

        titles = book.get_metadata('DC', 'title')
        title = titles[0][0] if titles else None

        authors = book.get_metadata('DC', 'creator')
        author = authors[0][0] if authors else None

        subjects = book.get_metadata('DC', 'subject')
        genre = subjects[0][0] if subjects else None

        return title, author, genre
    except Exception as e:
        print(f"Error reading EPUB metadata: {e}")
        return None, None, None


  
    # Attempts to extract a cover image from an EPUB file using three methods:
    # 1. Official OPF cover metadata
    # 2. Any image item with 'cover' in its name
    # 3. The first image found as a fallback
    # Returns the relative path for use in templates, or None if no cover found.
    

def extract_and_save_cover(epub_file_path, book_id):

    try:
        book = epub.read_epub(epub_file_path)
        cover_item = None

        # Method 1: OPF cover metadata tag
        covers = book.get_metadata('OPF', 'cover')
        if covers:
            cover_id = covers[0][1].get('content')
            cover_item = book.get_item_with_id(cover_id)

        # Method 2: image file with cover in the name
        if not cover_item:
            for item in book.get_items():
                if item.get_type() == ebooklib.ITEM_IMAGE:
                    if 'cover' in item.get_name().lower():
                        cover_item = item
                        break

        # Method 3: first available image as a last resort
        if not cover_item:
            for item in book.get_items():
                if item.get_type() == ebooklib.ITEM_IMAGE:
                    cover_item = item
                    break

        if cover_item:
            ext = cover_item.get_name().split('.')[-1]
            filename = f"cover_{book_id}.{ext}"
            os.makedirs(COVER_FOLDER, exist_ok=True)
            full_path = os.path.join(COVER_FOLDER, filename)

            with open(full_path, 'wb') as f:
                f.write(cover_item.get_content())

            # return path relative to static/ 
            return full_path.replace('\\', '/').split('static/')[-1]

        return None

    except Exception as e:
        print(f"Cover extraction error: {e}")
        return None


    # Falls back to the Open Library API to find a cover image URL
    # when no cover can be extracted from the EPUB itself.
    # Returns a full image URL string, or None if not found.
    
def fetch_openlibrary_cover(title, author):
    try:
        query = f"{title} {author}"
        res = requests.get(
            f"https://openlibrary.org/search.json?q={query}",
            timeout=5
        ).json()

        if res.get("docs"):
            cover_id = res["docs"][0].get("cover_i")
            if cover_id:
                return f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"

        return None

    except Exception as e:
        print(f"Open Library API error: {e}")
        return None


# ── Routes ─────────


# login page
@app.route('/')
def welcome():
    return render_template('index.html')


# library page

@app.route('/library')
def library():
    data = read_db()
    books = data.get('books', [])
    genres = sorted(list(set(book['genre'] for book in books if book.get('genre'))))
    return render_template('library.html', books=books, genres=genres)



# GET renders the upload form. and POST Accepts a multipart form with an EPUB file, extracts metadata,
# checks for duplicates, saves the file and cover, then updates the json file
    
@app.route('/upload', methods=['GET', 'POST'])
def upload():

    if request.method == 'POST':
        try:
            file = request.files.get('file')
            uploader = request.form.get('uploader') or "Anonymous"

            if not file or file.filename == '':
                return redirect(request.url)

            if file and file.filename.endswith('.epub'):
                db_data = read_db()
                books = db_data.get('books', [])
                next_id = max([b['id'] for b in books], default=0) + 1

                filename = f"{next_id}_{secure_filename(file.filename)}"
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename).replace('\\', '/')
                file.save(file_path)

                extracted_title, extracted_author, extracted_genre = get_epub_metadata(file_path)
                title = extracted_title or "Unknown Title"
                author = extracted_author or "Unknown Author"
                genre = extracted_genre or "General"

                # prevent duplicate books, same title + author, case-insensitive
                is_duplicate = any(
                    b['title'].lower() == title.lower() and
                    b['author'].lower() == author.lower()
                    for b in books
                )

                if is_duplicate:
                    os.remove(file_path)
                    flash(f"'{title}' by {author} is already in your library!")
                    return redirect(url_for('library'))

                # try to get a cover from the epub first, then Open Library API
                cover_path = extract_and_save_cover(file_path, next_id)
                if not cover_path:
                    cover_path = fetch_openlibrary_cover(title, author)

                new_book = Book(next_id, title, author, genre, file_path, uploader, cover_path)
                books.append(new_book.to_dict())
                db_data['books'] = books
                write_db(db_data)

                flash(f"Successfully uploaded '{title}'!")
                return redirect(url_for('library'))

        except Exception as e:
            flash(f"An error occurred during upload: {str(e)}")
            return redirect(url_for('library'))

    return render_template('upload.html')


# deletes a book, removes the EPUB file, the local cover image and the entry from the database
@app.route('/delete_book/<int:book_id>', methods=['POST'])
def delete_book(book_id):

    db = read_db()
    books = db.get('books', [])
    book = next((b for b in books if b['id'] == book_id), None)

    if book:
        try:
            if os.path.exists(book['path']):
                os.remove(book['path'])

            # only delete cover files stored locally, not external URLs
            if book.get('cover_path') and not book['cover_path'].startswith('http'):
                cover_full_path = os.path.join('static', book['cover_path'])
                if os.path.exists(cover_full_path):
                    os.remove(cover_full_path)

            db['books'] = [b for b in books if b['id'] != book_id]
            write_db(db)
            flash(f"Successfully deleted '{book['title']}'.")

        except Exception as e:
            flash(f"Error during deletion: {str(e)}")
    else:
        flash("Book not found.")

    return redirect(request.referrer or url_for('library'))


# renders the profile page showing all books uploaded by a given user
@app.route('/profile/<username>')
def profile(username):
    db = read_db()
    user_books = [b for b in db.get('books', []) if b.get('uploader') == username]
    return render_template('profile.html', username=username, books=user_books)


# renders the Ereader page for a certain book
@app.route('/read/<int:book_id>')
def read_book(book_id):
    data = read_db()
    book = next((b for b in data['books'] if b['id'] == book_id), None)
    if not book:
        return "Book not found", 404
    return render_template('reader.html', book=book)


if __name__ == '__main__':
    app.run(debug=True)
