
//   index page — save username and redirect to library-----------

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

//------------- delete book confirmation via sweet alert--------------- 
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