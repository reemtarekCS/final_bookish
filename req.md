This is the "crunch time" plan. To finish **Bookish** in 4 days while hitting every single mark on that rubric, we need to move from "thinking" to "architecting."

Here is your detailed development guide, mapped 1:1 to your course requirements.

---

## Part 1: The "Bookish" Requirement Map
This table ensures your project is 100% compliant before you write a single line of code.

| Requirement | Implementation in **Bookish** |
| :--- | :--- |
| **Flask Framework** | Backend routing for Home, Upload, and Reader pages. |
| **Python Standard Library** | **`os`** (pathing), **`json`** (storage), and **`datetime`** (for comment timestamps). |
| **Custom Python Class** | A `Book` class that handles its own metadata and formatting. |
| **Read/Write Same File** | `database.json` stores book metadata and user comments. |
| **JavaScript & LocalStorage** | Stores Grace's name and "Last Read" book ID. |
| **Modern JS** | Strict use of `const`, `let`, and Arrow Functions. |
| **Text Box Processing** | Alice’s book upload and Grace’s comment/rating submission. |
| **No Error Messages** | Try/Except blocks in Python to catch bad file uploads gracefully. |
| **Style & Docs** | Clean CSS and a README with exact line number references. |

---

## Part 2: The "Book" Class Design
You need this class to pass. It shouldn't just exist; it should *do* work.

```python
from datetime import datetime

class Book:
    def __init__(self, title, author, genre, file_path):
        self.title = title
        self.author = author
        self.genre = genre
        self.file_path = file_path
        self.upload_date = datetime.now() # Requirement: Standard Library (datetime)

    def to_dict(self):
        """Converts object to dictionary for JSON storage."""
        return {
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "path": self.file_path,
            "date": self.upload_date.strftime("%Y-%m-%d %H:%M")
        }

    def get_display_title(self):
        """Returns a formatted string for the UI."""
        return f"{self.title} by {self.author}"
```

---

## Part 3: The 4-Day Sprint Plan



### Day 1: The "Skeleton" (Backend & Storage)
* **Morning:** Initialize Git repo. Set up Flask folder structure (`static/`, `templates/`, `uploads/`).
* **Afternoon:** Write the `database.json` handler. Create functions to `read_db()` and `write_db()`.
* **Evening:** Implement the **Welcome Page**. Use JS `localStorage` to save the username and redirect to the Main Library.
* **Requirement Check:** LocalStorage, Flask, Git commits.

### Day 2: The "Pipeline" (Uploads & Processing)
* **Morning:** Create the **Upload Form**. Alice selects an EPUB and a genre.
* **Afternoon:** Backend logic! Use `secure_filename` (Standard Library) to save the file to `uploads/books/`. Use your `Book` class to create an object and save it to `database.json`.
* **Evening:** Error handling. If the file isn't an EPUB, show a message in the browser, don't let Python crash.
* **Requirement Check:** Class usage, Input processing, Writing to file, No error messages.

### Day 3: The "Experience" (Library & Reader)
* **Morning:** Build the **Main Library** page. Use a Python `for` loop to render book cards from your JSON.
* **Afternoon:** The **Book Detail** page. Add the "Comment" text box. When Grace submits a comment, append it to that book's entry in the JSON.
* **Evening:** Integrate **Epub.js**. Create the reader page with the `<iframe>`. Ensure it pulls the `file_path` correctly from your Flask static folder.
* **Requirement Check:** Reading from file, Loops, Conditionals, JS frontend.

### Day 4: The "Social" & The "Submission"
* **Morning:** Add the **Rating** system. Ensure Grace can click 1–5 stars and the backend calculates the average.
* **Afternoon:** **The "Polish" phase.** Remove every `print()` and `console.log()`. Add CSS to make the "centerpiece" cover look amazing.
* **Evening:** **README.md.** This is the most boring but most important part. Open the template and carefully fill in the file names and line numbers for your class, loops, and logic.
* **Requirement Check:** CSS, Documentation, README, All exercises pushed to GitHub.

---

### Pro-Tips for Speed:
1.  **Don't over-engineer the CSS:** Use a simple flexbox grid for the books. 1,000 books will look great in a standard 4-column grid.
2.  **The "Profile" Shortcut:** Instead of a complex database, just filter your main JSON for books where `uploader == localStorage.getItem('username')`.
3.  **One JSON to rule them all:** Store books and comments in the same file to keep your "Read/Write" logic simple and compliant.

> **Crucial Warning:** Ensure your `static` folder is configured correctly in Flask, or your `<iframe>` won't be able to find the `.epub` files Alice uploaded!

Do you want to start by drafting the Python code for the "Read/Write" JSON functions, or would you rather look at the HTML for the Welcome page first?

**What's the very first file you're going to create?**












Bookish/
├── app.py              # The "Heart": Flask routes, Python Class, JSON logic
├── database.json       # The "Brain": Stores all book metadata & comments
├── README.md           # The "Map": Required for your certificate
├── .gitignore          # Keeps your environment/cache files off GitHub
│
├── static/             # All files the browser needs to download
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── main.js     # LocalStorage & UI logic
│   │   └── reader.js   # Epub.js & iframe logic
│   ├── uploads/        # This is where Alice's files live
│   │   ├── books/      # .epub files
│   │   └── covers/     # .jpg cover images
│   └── lib/            # Optional: Local copies of Epub.js if not using CDN
│
└── templates/          # Your HTML files (Flask looks here by default)
    ├── base.html       # Shared layout (Navbar/Footer)
    ├── index.html      # Welcome page (Grace enters name)
    ├── library.html    # Main grid (Discovery view)
    ├── book_detail.html# Centerpiece (Comments/Rating)
    ├── reader.html     # The iframe reader
    └── upload.html     # Alice's upload form