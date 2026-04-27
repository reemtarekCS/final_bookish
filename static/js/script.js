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