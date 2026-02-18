/**
 * Theme Toggle Functionality
 * Handles dark/light mode switching with localStorage persistence
 */

// Get theme from localStorage or default to 'light'
const getTheme = () => {
    return localStorage.getItem('theme') || 'light';
};

// Set theme and save to localStorage
const setTheme = (theme) => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    updateThemeButton(theme);
};

// Update theme toggle button text and icon
const updateThemeButton = (theme) => {
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        if (theme === 'dark') {
            // When in dark mode, show sun icon to switch to light
            themeToggle.innerHTML = '<span class="icon">☀️</span>';
            themeToggle.setAttribute('aria-label', 'Switch to Light Mode');
            themeToggle.setAttribute('title', 'Switch to Light Mode');
        } else {
            // When in light mode, show moon icon to switch to dark
            themeToggle.innerHTML = '<span class="icon">🌙</span>';
            themeToggle.setAttribute('aria-label', 'Switch to Dark Mode');
            themeToggle.setAttribute('title', 'Switch to Dark Mode');
        }
    }
};

// Toggle between light and dark themes
const toggleTheme = () => {
    const currentTheme = getTheme();
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
    
    // Add transition animation
    document.body.classList.add('theme-transitioning');
    setTimeout(() => {
        document.body.classList.remove('theme-transitioning');
    }, 400);
};

// Initialize theme on page load
document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = getTheme();
    setTheme(savedTheme);
    
    // Add click event to theme toggle button
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }
});

// Handle keyboard accessibility for theme toggle
document.addEventListener('keydown', (e) => {
    // Press 'T' to toggle theme
    if (e.key === 't' || e.key === 'T') {
        if (e.target.tagName !== 'INPUT' && e.target.tagName !== 'TEXTAREA') {
            toggleTheme();
            e.preventDefault();
        }
    }
});
