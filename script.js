// Cấu hình link tải - CẬP NHẬT LINK TẢI Ở ĐÂY
const DOWNLOAD_LINK = 'https://raw.githubusercontent.com/hotboy17894/VIETCNC/main/webvietcnc/vietcnc.rbz';
const UPDATE_JSON_URL = 'https://raw.githubusercontent.com/hotboy17894/VIETCNC/main/webvietcnc/update.json';

// Hàm chuyển đổi ngày từ YYYY-MM-DD sang DD/MM/YYYY
function formatDate(dateString) {
    const parts = dateString.split('-');
    return `${parts[2]}/${parts[1]}/${parts[0]}`;
}

// Hàm tải thông tin version từ update.json
async function loadVersionInfo() {
    try {
        // Thêm timestamp để tránh cache
        const timestamp = new Date().getTime();
        const response = await fetch(`${UPDATE_JSON_URL}?t=${timestamp}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Cập nhật version
        const versionElement = document.getElementById('current-version');
        if (versionElement) {
            versionElement.textContent = data.version;
        }
        
        // Cập nhật ngày
        const dateElement = document.getElementById('release-date');
        if (dateElement) {
            dateElement.textContent = formatDate(data.release_date);
            dateElement.setAttribute('datetime', data.release_date);
        }
        
        // Cập nhật aria-label của nút download
        const downloadBtn = document.getElementById('downloadBtn');
        if (downloadBtn) {
            downloadBtn.setAttribute('aria-label', `Tải xuống VietCNC phiên bản ${data.version}`);
        }
        
        console.log('✓ Đã tải thông tin version:', data.version);
    } catch (error) {
        console.error('Lỗi khi tải thông tin version:', error);
        
        // Nếu lỗi, hiển thị thông tin mặc định từ update.json local
        const versionElement = document.getElementById('current-version');
        const dateElement = document.getElementById('release-date');
        
        // Thử đọc từ file local
        fetch('update.json')
            .then(res => res.json())
            .then(data => {
                if (versionElement) versionElement.textContent = data.version;
                if (dateElement) {
                    dateElement.textContent = formatDate(data.release_date);
                    dateElement.setAttribute('datetime', data.release_date);
                }
            })
            .catch(() => {
                // Nếu vẫn lỗi, dùng giá trị mặc định
                if (versionElement) versionElement.textContent = '3.2.6';
                if (dateElement) {
                    dateElement.textContent = '28/01/2026';
                    dateElement.setAttribute('datetime', '2026-01-28');
                }
            });
    }
}

// Xử lý sự kiện click nút tải
document.addEventListener('DOMContentLoaded', function() {
    // Tải thông tin version
    loadVersionInfo();
    
    const downloadBtn = document.getElementById('downloadBtn');
    
    if (downloadBtn) {
        downloadBtn.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Thay đổi link tải ở đây
            window.location.href = DOWNLOAD_LINK;
            
            // Hoặc mở trong tab mới
            // window.open(DOWNLOAD_LINK, '_blank');
        });
    }
    
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
