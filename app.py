import os
import json
import ebooklib
from ebooklib import epub
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "secret_key_for_session" # Required for flash messages

UPLOAD_FOLDER = 'static/uploads/books'
ALLOWED_EXTENSIONS = {'epub'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class Book:
    def __init__(self, book_id, title, author, genre, file_path, uploader):
        self.id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.file_path = file_path
        self.uploader = uploader
        self.created_at = datetime.now()

    #this method converts the object to a dictionary to store in database.json
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "path": self.file_path,
            "uploader": self.uploader,
            "timestamp": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
    def book_by(self):
        return f"{self.title} by {self.author}"

#read and write functions for books
database_books = 'database.json'
database_comments = 'comments.json'

def read_db():
    if not os.path.exists(database_books):
        return {"books": []}
    with open(database_books, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {"books": []}

def write_db(data):
    with open(database_books, 'w') as f:
        json.dump(data, f, indent=4)


#read and write functions for comments
def read_comments():
    if not os.path.exists(database_comments):
        return []
    with open(database_comments, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def write_comments(data):
    with open(database_comments, 'w') as f:
        json.dump(data, f, indent=4)


#this method extracts title, author, and genre from the epub files using ebooklib
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
        print(f"Error extracting EPUB metadata with ebooklib: {e}")
        return None, None, None

# ---------------------------------------------------------------


@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/library')
def library():
    data = read_db()
    books = data.get('books', [])
    # Get a unique list of genres for the filter dropdown
    genres = sorted(list(set(book['genre'] for book in books if book.get('genre'))))
    return render_template('library.html', books=books, genres=genres)


#the form in upload takes two parts because it's enctype is multipart/form-data 
#which takes text data as form.get and binary data aka the files as request.files
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        try:
            file = request.files.get('file')
            uploader = request.form.get('uploader') or "Anonymous"

            # check if they file is a file or not empty, if so refresh.
            if not file or file.filename == '':
                return redirect(request.url)

            if file and file.filename.endswith('.epub'):
                # check for duplicates before adding to database
                db_data = read_db()
                books = db_data.get('books', [])
                next_id = max([b['id'] for b in books], default=0) + 1
                
                # add id to filename to prevent overwriting files with same name
                filename = f"{next_id}_{secure_filename(file.filename)}"
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                
                # convert backslashes to forward slashes to fix the paths
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename).replace('\\', '/')
                file.save(file_path)

                # we get extracted data from metadata and add fallback
                extracted_title, extracted_author, extracted_genre = get_epub_metadata(file_path)
                title = extracted_title or "Unknown Title" 
                author = extracted_author or "Unknown Author" 
                genre = extracted_genre or "General" 

                #check for duplicates before adding to db
                is_duplicate = any(b['title'].lower() == title.lower() and 
                                   b['author'].lower() == author.lower() for b in books)
                
                #deletes the file
                if is_duplicate:
                    os.remove(file_path)
                    flash(f"'{title}' by {author} is already in your library!")
                    return redirect(url_for('library'))
                
                new_book = Book(next_id, title, author, genre, file_path, uploader)
                books.append(new_book.to_dict())
                
                write_db({"books": books})
                flash(f"Successfully uploaded {title}!")
                return redirect(url_for('library'))
            
        except Exception as e:
            flash(f"An error occurred during upload: {str(e)}")
            return redirect(url_for('library'))
            
    return render_template('upload.html')

#route that handles new comments
@app.route('/add_comment/<int:book_id>', methods=['POST'])
def add_comment(book_id):
    comment_text = request.form.get('comment')
    user_name = request.form.get('user') or "Anonymous"

    if comment_text:
        all_comments = read_comments()
        all_comments.append({
            "book_id": book_id,
            "user": user_name,
            "text": comment_text,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        write_comments(all_comments)

    return redirect(url_for('book_detail', book_id=book_id))

#route for viewing specific book details and comments
@app.route('/book/<int:book_id>')
def book_detail(book_id):
    db = read_db()
    book = next((b for b in db['books'] if b['id'] == book_id), None)
    
    if not book:
        return redirect(url_for('library'))

    all_comments = read_comments()
    # Filter comments belonging to this book
    book_comments = [c for c in all_comments if c.get('book_id') == book_id]
    
    return render_template('book_detail.html', book=book, book_comments=book_comments)


# method to view the e-reader for a specific book.
@app.route('/read/<int:book_id>')
def read_book(book_id):
    data = read_db()
    book = next((b for b in data['books'] if b['id'] == book_id), None)
    if not book:
        return "Book not found", 404
    return render_template('reader.html', book=book)

# route to view user specific uploads and comments
@app.route('/profile/<username>')
def profile(username):
    db = read_db()
    all_comments = read_comments()
    
    # Create a dictionary to quickly look up book titles by their ID
    book_titles = {b['id']: b['title'] for b in db.get('books', [])}

    # Filter data based on the username
    user_books = [b for b in db.get('books', []) if b.get('uploader') == username]
    user_comments = [c for c in all_comments if c.get('user') == username]
    
    # Attach the corresponding book title to each filtered comment
    for comment in user_comments:
        comment['book_title'] = book_titles.get(comment.get('book_id'), "Unknown Book")

    return render_template('profile.html', username=username, books=user_books, comments=user_comments)


@app.route('/delete_book/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    db = read_db()
    books = db.get('books', [])
    book = next((b for b in books if b['id'] == book_id), None)

    if book:
        # remove the physical EPUB file from the uploads folder
        if os.path.exists(book['path']):
            os.remove(book['path'])

        # remove the book entry from database.json
        db['books'] = [b for b in books if b['id'] != book_id]
        write_db(db)

        # clean up comments associated with the deleted book
        all_comments = read_comments()
        updated_comments = [c for c in all_comments if c.get('book_id') != book_id]
        write_comments(updated_comments)

    return redirect(request.referrer or url_for('library'))


if __name__ == '__main__':
    app.run(debug=True)
    
