// save username in localstorage
const saveUser = () => {
    const name = document.getElementById('username').value.trim();
    if (name) {
        localStorage.setItem('bookish_user', name);
        window.location.href = "/library";
    } else {
        alert("Please enter a name!");
    }
};

// a check for username, redirect if username is already in localstorage
document.addEventListener('DOMContentLoaded', () => {
    const usernameInput = document.getElementById('username');
    if (usernameInput && localStorage.getItem('bookish_user')) {
        window.location.href = "/library";
    }

    // search and filter logic
    const searchInput = document.getElementById('searchInput');
    const genreFilter = document.getElementById('genreFilter');
    const bookEntries = document.querySelectorAll('.book-entry');

    if (searchInput && bookEntries.length > 0) {
        const applyFilters = () => {
            const searchText = searchInput.value.toLowerCase();
            const selectedGenre = genreFilter ? genreFilter.value.toLowerCase() : "";

            bookEntries.forEach(entry => {
                const bookText = entry.innerText.toLowerCase();
                const bookGenre = (entry.dataset.genre || "").toLowerCase();

                const matchesSearch = bookText.includes(searchText);
                const matchesGenre = selectedGenre === "" || bookGenre === selectedGenre;

                entry.style.display = (matchesSearch && matchesGenre) ? "block" : "none";
            });
        };

        searchInput.addEventListener('input', applyFilters);
        genreFilter?.addEventListener('change', applyFilters);
    }

    //a check to assign the uploaded file to the user
    const currentUser = localStorage.getItem('bookish_user');
    const uploaderField = document.getElementById('uploader-hidden');
    if (uploaderField) {
        if (!currentUser) {
            alert("You must enter a name before uploading!");
            window.location.href = "/";
        } else {
            uploaderField.value = currentUser;
        }
    }
    // book_detail page autofill hidden username for comments
    const hiddenUserField = document.getElementById('comment-user-hidden');
    if (hiddenUserField) {
        hiddenUserField.value = localStorage.getItem('bookish_user') || 'Anonymous';
    }

    // reader.html logic, Epub.js initialization and controls
    const readerArea = document.getElementById('area');
    if (readerArea && readerArea.dataset.bookPath) {
        try {
            // Use the full origin to ensure the path is absolute
            const book = ePub(window.location.origin + readerArea.dataset.bookPath);
            const rendition = book.renderTo("area", { flow: "paginated", width: "900", height: "600" });
            rendition.display().catch(err => console.error("Error displaying book:", err));

            document.getElementById("prevButton")?.addEventListener("click", () => rendition.prev());
            document.getElementById("nextButton")?.addEventListener("click", () => rendition.next());
        } catch (e) {
            console.error("Reader failed to initialize:", e);
        }
    }

    // profile link logic
    const profileLink = document.getElementById('profile-link');
    const currentUser = localStorage.getItem('bookish_user');
    if (profileLink && currentUser) {
        profileLink.href = `/profile/${currentUser}`;
    }

    // logout logic
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            localStorage.removeItem('bookish_user');
            window.location.href = "/";
        });
    }

});