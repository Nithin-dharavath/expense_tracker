// main.js — students will add JavaScript here as features are built

// Video Modal functionality
(function() {
    const modal = document.getElementById('videoModal');
    const openBtn = document.getElementById('openModalBtn');
    const closeBtn = document.getElementById('closeModalBtn');
    const iframe = document.getElementById('videoFrame');

    const YOUTUBE_URL = 'https://www.youtube.com/embed/dQw4w9WgXcQ?autoplay=1';

    function openModal() {
        modal.classList.add('active');
        iframe.src = YOUTUBE_URL;
        document.body.style.overflow = 'hidden';
    }

    function closeModal() {
        modal.classList.remove('active');
        iframe.src = '';
        document.body.style.overflow = '';
    }

    if (openBtn) {
        openBtn.addEventListener('click', openModal);
    }

    if (closeBtn) {
        closeBtn.addEventListener('click', closeModal);
    }

    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                closeModal();
            }
        });
    }

    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            closeModal();
        }
    });
})();
