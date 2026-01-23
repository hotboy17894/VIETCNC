// Cấu hình link tải - CẬP NHẬT LINK TẢI Ở ĐÂY
const DOWNLOAD_LINK = 'https://drive.google.com/file/d/1_xhCJ9WJcvLtcvuKzC8DfsRw1Xw5ZTVo/view?usp=sharing';

// Xử lý sự kiện click nút tải
document.addEventListener('DOMContentLoaded', function() {
    const downloadBtn = document.getElementById('downloadBtn');
    
    if (downloadBtn) {
        downloadBtn.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Mở link Google Drive trong tab mới
            window.open(DOWNLOAD_LINK, '_blank');
        });
    }
    
    // Xử lý các nút "Tải plugin về" trong bảng giá
    const pricingBtns = document.querySelectorAll('.btn-pricing');
    pricingBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            window.open(DOWNLOAD_LINK, '_blank');
        });
    });
    
    // Smooth scroll cho các link anchor
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

// Animation khi scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Áp dụng animation cho các phần tử
document.addEventListener('DOMContentLoaded', function() {
    const animatedElements = document.querySelectorAll('.feature-card, .feature-item');
    
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
});
