function addEvents() {
    const agreeButton = document.getElementById('agree-btn');
    const overlay = document.getElementById('overlay');
    const closeButton = document.getElementById('close-btn');
    const popup = document.getElementById('popup');



    agreeButton.addEventListener('click', agreeButtonClick);
    overlay.addEventListener('click', closeFormAndOverlay);
    closeButton.addEventListener('click', closeFormAndOverlay);
    popup.addEventListener('click',(e) => {e.stopPropagation()});


    function agreeButtonClick(e) {
        e.preventDefault();
        overlay.style.display = 'flex';
    };

    function closeFormAndOverlay(e) {
        overlay.style.display = 'none';
    };



};

addEvents();