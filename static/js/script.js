
//  ----------- 1- index page — save username and redirect to library-----------

const saveUser = () => {
    const input = document.getElementById('username');
    const name = input.value.trim();
    if (name) {
        localStorage.setItem('bookish_user', name);
        window.location.href = '/library';
    } else {
        Swal.fire({
            title: 'One moment',
            text: 'Please enter a name to continue.',
            icon: 'info',
            confirmButtonText: 'Got it',
            customClass: {
                popup: 'swal-bookish',
                title: 'swal-bookish-title',
                confirmButton: 'swal-bookish-btn',
            },
            buttonsStyling: false,
        });
    }
};

//------------- 2- delete book confirmation via sweet alert--------------- 
function confirmDelete(id, title) {
    Swal.fire({
        title: 'Delete this book?',
        text: title + ' will be removed from your library.',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Delete',
        cancelButtonText: 'Keep it',
        customClass: {
            popup: 'swal-bookish',
            title: 'swal-bookish-title',
            confirmButton: 'swal-bookish-btn-danger',
            cancelButton: 'swal-bookish-btn',
        },
        buttonsStyling: false,
    }).then(result => {
        if (result.isConfirmed) {
            document.getElementById('deleteForm-' + id).submit();
        }
    });
}


// -----------all the following code will run when DOM is ready-----------

document.addEventListener('DOMContentLoaded', () => {

    const currentUser = localStorage.getItem('bookish_user');

    /* ---- 3- index page - redirect if already logged in ---- */
    const usernameInput = document.getElementById('username');
    if (usernameInput && currentUser) {
        window.location.href = '/library';
    }

    /* --- 4- Library page - greeting --- */
    const welcomeEl = document.getElementById('welcomeUser');
    if (welcomeEl && currentUser) {
        welcomeEl.textContent = `Happy reading, ${currentUser}`;
    }

    /* --- 5- Library page - real-time search + genre filter --- */
    const searchInput = document.getElementById('searchInput');
    const genreFilter = document.getElementById('genreFilter');
    const bookEntries = document.querySelectorAll('.book');

    if (searchInput && bookEntries.length > 0) {
        const applyFilters = () => {
            const searchText = searchInput.value.toLowerCase();
            const selectedGenre = genreFilter ? genreFilter.value.toLowerCase() : '';

            bookEntries.forEach(entry => {
                const bookText = entry.innerText.toLowerCase();
                const bookGenre = (entry.dataset.genre || '').toLowerCase();

                const matchesSearch = bookText.includes(searchText);
                const matchesGenre = selectedGenre === '' || bookGenre === selectedGenre;

                const link = entry.closest('.book-link');
                const target = link || entry;
                target.style.display = (matchesSearch && matchesGenre) ? 'block' : 'none';
            });
        };

        searchInput.addEventListener('input', applyFilters);
        genreFilter?.addEventListener('change', applyFilters);
    }


});