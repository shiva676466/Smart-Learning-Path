/* LearnPathAI - Main JavaScript */

document.addEventListener('DOMContentLoaded', () => {
    initNavToggle();
    initProgressBars();
    initAutoHideMessages();
    initCardSelectors();
});

/* Mobile nav toggle */
function initNavToggle() {
    const toggle = document.getElementById('navToggle');
    const links = document.querySelector('.nav-links');
    if (!toggle || !links) return;
    toggle.addEventListener('click', () => {
        links.style.display = links.style.display === 'flex' ? 'none' : 'flex';
        links.style.flexDirection = 'column';
        links.style.position = 'absolute';
        links.style.top = '64px';
        links.style.left = '0';
        links.style.right = '0';
        links.style.background = 'rgba(10,14,26,0.98)';
        links.style.padding = '16px';
        links.style.borderBottom = '1px solid #1e2d45';
        links.style.zIndex = '99';
    });
}

/* Animate progress bars to their target width */
function initProgressBars() {
    document.querySelectorAll('.progress-bar-fill[data-width]').forEach(bar => {
        const target = parseFloat(bar.dataset.width);
        bar.style.width = '0%';
        requestAnimationFrame(() => {
            setTimeout(() => { bar.style.width = target + '%'; }, 100);
        });
    });
}

/* Auto-dismiss messages after 5 seconds */
function initAutoHideMessages() {
    document.querySelectorAll('.message').forEach(msg => {
        setTimeout(() => {
            msg.style.opacity = '0';
            msg.style.transform = 'translateX(20px)';
            msg.style.transition = 'all 0.3s ease';
            setTimeout(() => msg.remove(), 300);
        }, 5000);
    });
}

/* Highlight selected radio card options */
function initCardSelectors() {
    const radioGroups = ['skill', 'level', 'daily_hours', 'duration_days'];
    radioGroups.forEach(name => {
        const inputs = document.querySelectorAll(`input[name="${name}"]`);
        inputs.forEach(input => {
            // Init: if already checked, mark as selected
            if (input.checked) input.closest('label')?.classList.add('selected');

            input.addEventListener('change', () => {
                inputs.forEach(i => i.closest('label')?.classList.remove('selected'));
                input.closest('label')?.classList.add('selected');
            });
        });
    });
}

/* Dark mode toggle (bonus feature) */
function toggleDarkMode() {
    const html = document.documentElement;
    const isDark = html.dataset.theme === 'dark';
    html.dataset.theme = isDark ? 'light' : 'dark';
    localStorage.setItem('theme', html.dataset.theme);
}

/* Load theme preference */
const savedTheme = localStorage.getItem('theme');
if (savedTheme) document.documentElement.dataset.theme = savedTheme;

/* XP counter animation */
function animateCounter(el, target) {
    let current = 0;
    const step = target / 60;
    const timer = setInterval(() => {
        current = Math.min(current + step, target);
        el.textContent = Math.floor(current);
        if (current >= target) clearInterval(timer);
    }, 16);
}

/* Animate XP and stat numbers on dashboard load */
document.querySelectorAll('.stat-value').forEach(el => {
    const val = parseInt(el.textContent, 10);
    if (!isNaN(val) && val > 0) {
        el.textContent = '0';
        setTimeout(() => animateCounter(el, val), 200);
    }
});
