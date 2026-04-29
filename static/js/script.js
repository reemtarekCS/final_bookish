
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

    /* --- 6- profile page link- set correct href --- */
    const profileLink = document.getElementById('profile-link');
    if (profileLink && currentUser) {
        profileLink.href = `/profile/${currentUser}`;
    }

    /* --- 7- logout button --- */
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            localStorage.removeItem('bookish_user');
            window.location.href = '/';
        });
    }
    /* --- 8- upload page -  auth guard + fill hidden uploader field --- */
    const uploaderField = document.getElementById('uploader-hidden');
    if (uploaderField) {
        if (!currentUser) {
            alert('You must enter a name before uploading!');
            window.location.href = '/';
        } else {
            uploaderField.value = currentUser;
        }
    }

    /* --- 11- fading the flash messages --- */

    document.querySelectorAll('.flash-message').forEach(msg => {
        setTimeout(() => {
            msg.style.transition = 'opacity 0.4s';
            msg.style.opacity = '0';
            setTimeout(() => msg.remove(), 400);
        }, 4000);
    });

});
/* --- 9- library page -  sidebar toggle--- */
function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('open');
}

/* --- 10- reader page -  TOC toggle--- */

function toggleToc() {
    const panel = document.getElementById('tocPanel');
    const area = document.getElementById('area');
    const btn = document.getElementById('tocToggle');

    if (!panel) return;

    const isOpen = panel.classList.toggle('open');
    area?.classList.toggle('toc-open', isOpen);
    btn?.classList.toggle('active', isOpen);
}

/* --- 12- reader page -  epub.js initialisation, runs only on pages that have #area with data-book-path.--- */


document.addEventListener('DOMContentLoaded', () => {

    const readerArea = document.getElementById('area');
    if (!readerArea || !readerArea.dataset.bookPath) return;

    // epub.js must already be loaded via <script> in reader.html
    if (typeof ePub === 'undefined') {
        console.error('epub.js not loaded');
        return;
    }

    const book = ePub(window.location.origin + readerArea.dataset.bookPath);

    const rendition = book.renderTo('area', {
        flow: 'scrolled-doc',
        width: '100%',
        height: '100%',
        spread: 'none'
    });

    rendition.display();

    let toc = [];
    let currentIndex = 0;

    function setActive(index) {
        document.querySelectorAll('#chapterList a').forEach((l, i) => {
            l.classList.toggle('active', i === index);
        });
        const active = document.querySelector('#chapterList a.active');
        if (active) active.scrollIntoView({ block: 'nearest' });
    }

    function updateTitle() {
        const title = toc[currentIndex]?.label?.trim() || 'Reading';
        const el = document.getElementById('chapterTitle');
        if (el) el.textContent = title;
    }

    function updateNavButtons() {
        const prev = document.getElementById('prevChapter');
        const next = document.getElementById('nextChapter');
        const indicator = document.getElementById('chapterIndicator');
        if (prev) prev.disabled = currentIndex <= 0;
        if (next) next.disabled = currentIndex >= toc.length - 1;
        if (indicator) indicator.textContent = toc.length ? `${currentIndex + 1} / ${toc.length}` : '';
    }

    function goToChapter(index) {
        currentIndex = index;
        rendition.display(toc[currentIndex].href);
        updateTitle();
        setActive(currentIndex);
        updateNavButtons();
        readerArea.scrollTop = 0;
    }

    book.ready.then(() => {
        const loadingMsg = document.getElementById('loadingMsg');
        if (loadingMsg) loadingMsg.remove();

        toc = book.navigation.toc || [];
        const list = document.getElementById('chapterList');
        if (!list) return;

        list.innerHTML = '';
        toc.forEach((chapter, index) => {
            const link = document.createElement('a');
            link.textContent = chapter.label?.trim() || `Chapter ${index + 1}`;
            link.href = '#';
            link.onclick = (e) => {
                e.preventDefault();
                goToChapter(index);
                if (window.innerWidth < 700) toggleToc();
            };
            list.appendChild(link);
        });

        updateTitle();
        setActive(0);
        updateNavButtons();
    });

    document.getElementById('prevChapter')?.addEventListener('click', () => {
        if (currentIndex > 0) goToChapter(currentIndex - 1);
    });

    document.getElementById('nextChapter')?.addEventListener('click', () => {
        if (currentIndex < toc.length - 1) goToChapter(currentIndex + 1);
    });

});
