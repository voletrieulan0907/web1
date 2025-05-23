document.addEventListener('DOMContentLoaded', function () {
    // Flash message close
    document.querySelectorAll('.close-flash').forEach(function (btn) {
        btn.addEventListener('click', function () {
            btn.parentElement.style.display = 'none';
        });
    });

    // Fade-in on scroll
    function revealOnScroll() {
        document.querySelectorAll('.fade-in').forEach(function (el) {
            const rect = el.getBoundingClientRect();
            if (rect.top < window.innerHeight - 60) {
                el.classList.add('visible');
            }
        });
    }
    window.addEventListener('scroll', revealOnScroll);
    revealOnScroll();

    // Buy button click effect (demo)
    document.querySelectorAll('.buy-button').forEach(button => {
        button.addEventListener('click', function (e) {
            if (button.tagName === 'A') return; // skip link
            button.innerHTML = 'Đang xử lý...';
            button.style.background = 'linear-gradient(45deg, #00ff00, #00ffff)';
            setTimeout(() => {
                alert('Cảm ơn bạn đã quan tâm! Vui lòng đăng nhập để mua hàng.');
                button.innerHTML = 'Mua Ngay';
                button.style.background = 'linear-gradient(45deg, #ff00ff, #00ffff)';
            }, 1000);
        });
    });
});