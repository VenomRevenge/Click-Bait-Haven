function addEvents() {
    const rejectButton = document.getElementById('reject-btn');
    const overlay = document.getElementById('overlay');
    const closeButton = document.getElementById('close-btn');
    const popup = document.getElementById('popup');



    rejectButton.addEventListener('click', rejectButtonClick);
    overlay.addEventListener('click', closeFormAndOverlay);
    closeButton.addEventListener('click', closeFormAndOverlay);
    popup.addEventListener('click',(e) => {e.stopPropagation()});


    function rejectButtonClick(e) {
        e.preventDefault();
        overlay.style.display = 'flex';
    };

    function closeFormAndOverlay(e) {
        overlay.style.display = 'none';
    };



};

addEvents();