function signOutSubmit() {
    const signOutButton = document.getElementById('sign-out');
    const signOutForm = document.getElementById('sign-out-form');

    signOutButton.addEventListener('click', (e) => {
        e.preventDefault();
        signOutForm.submit();
    });
};

signOutSubmit();