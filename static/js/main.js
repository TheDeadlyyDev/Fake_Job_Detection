/**
 * Fake Job Detection System - Main JavaScript File
 * ================================================
 * Handles client-side interactions, form validation, and AJAX requests
 */

// ============================================
// Utility Functions
// ============================================

/**
 * Show a flash message dynamically
 * @param {string} message - Message to display
 * @param {string} type - Message type (success, error, info)
 */
function showFlashMessage(message, type = 'info') {
    const flashContainer = document.querySelector('.flash-messages') || createFlashContainer();
    
    const flashMessage = document.createElement('div');
    flashMessage.className = `flash-message flash-${type}`;
    flashMessage.innerHTML = `
        <span>${message}</span>
        <button class="flash-close" onclick="this.parentElement.remove()">×</button>
    `;
    
    flashContainer.appendChild(flashMessage);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        flashMessage.remove();
    }, 5000);
}

/**
 * Create flash messages container if it doesn't exist
 */
function createFlashContainer() {
    const container = document.createElement('div');
    container.className = 'flash-messages';
    document.body.insertBefore(container, document.body.firstChild);
    return container;
}

/**
 * Format currency value
 * @param {number} value - Numeric value to format
 * @returns {string} Formatted currency string
 */
function formatCurrency(value) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(value);
}

// ============================================
// Form Validation
// ============================================

/**
 * Validate email format
 * @param {string} email - Email address to validate
 * @returns {boolean} True if valid, false otherwise
 */
function validateEmail(email) {
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return emailRegex.test(email);
}

/**
 * Validate password strength
 * @param {string} password - Password to validate
 * @returns {object} Validation result with isValid and message
 */
function validatePassword(password) {
    if (password.length < 6) {
        return {
            isValid: false,
            message: 'Password must be at least 6 characters long'
        };
    }
    return { isValid: true, message: '' };
}

// ============================================
// Login Form Handler
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            // Basic client-side validation
            const username = document.getElementById('username').value.trim();
            const password = document.getElementById('password').value.trim();
            
            if (!username || !password) {
                e.preventDefault();
                showFlashMessage('Please fill in all fields', 'error');
                return false;
            }
        });
    }
});

// ============================================
// Registration Form Handler
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.getElementById('registerForm');
    
    if (registerForm) {
        // Real-time password confirmation validation
        const passwordInput = document.getElementById('password');
        const confirmPasswordInput = document.getElementById('confirm_password');
        
        if (confirmPasswordInput) {
            confirmPasswordInput.addEventListener('input', function() {
                if (passwordInput.value !== confirmPasswordInput.value) {
                    confirmPasswordInput.setCustomValidity('Passwords do not match');
                } else {
                    confirmPasswordInput.setCustomValidity('');
                }
            });
        }
        
        registerForm.addEventListener('submit', function(e) {
            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value.trim();
            const confirmPassword = document.getElementById('confirm_password').value.trim();
            
            // Email validation
            if (!validateEmail(email)) {
                e.preventDefault();
                showFlashMessage('Please enter a valid email address', 'error');
                return false;
            }
            
            // Password validation
            const passwordValidation = validatePassword(password);
            if (!passwordValidation.isValid) {
                e.preventDefault();
                showFlashMessage(passwordValidation.message, 'error');
                return false;
            }
            
            // Password match validation
            if (password !== confirmPassword) {
                e.preventDefault();
                showFlashMessage('Passwords do not match', 'error');
                return false;
            }
        });
    }
});

// ============================================
// Job Posting Form Handler
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    const postJobForm = document.getElementById('postJobForm');
    
    if (postJobForm) {
        // Email validation
        const emailInput = document.getElementById('email');
        if (emailInput) {
            emailInput.addEventListener('blur', function() {
                const email = this.value.trim();
                if (email && !validateEmail(email)) {
                    this.setCustomValidity('Please enter a valid email address');
                } else {
                    this.setCustomValidity('');
                }
            });
        }
        
        // Salary validation (must be positive if provided)
        const salaryInput = document.getElementById('salary');
        if (salaryInput) {
            salaryInput.addEventListener('input', function() {
                const value = parseFloat(this.value);
                if (this.value && (isNaN(value) || value < 0)) {
                    this.setCustomValidity('Salary must be a positive number');
                } else {
                    this.setCustomValidity('');
                }
            });
        }
        
        postJobForm.addEventListener('submit', function(e) {
            const email = document.getElementById('email').value.trim();
            const companyName = document.getElementById('company_name').value.trim();
            const jobTitle = document.getElementById('job_title').value.trim();
            const jobDescription = document.getElementById('job_description').value.trim();
            
            // Required field validation
            if (!companyName || !email || !jobTitle || !jobDescription) {
                e.preventDefault();
                showFlashMessage('Please fill in all required fields', 'error');
                return false;
            }
            
            // Email format validation
            if (!validateEmail(email)) {
                e.preventDefault();
                showFlashMessage('Please enter a valid email address', 'error');
                return false;
            }
        });
    }
});

// ============================================
// Admin Dashboard Enhancements
// ============================================

/**
 * Delete job with confirmation (used in admin dashboard)
 * @param {number} jobId - ID of the job to delete
 */
function deleteJob(jobId) {
    if (confirm('Are you sure you want to delete this job posting? This action cannot be undone.')) {
        // Create a form to submit POST request
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = `/admin/delete_job/${jobId}`;
        document.body.appendChild(form);
        form.submit();
    }
}

// ============================================
// Smooth Scrolling
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
});

// ============================================
// Auto-hide Flash Messages
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            message.style.transform = 'translateX(100%)';
            setTimeout(() => message.remove(), 300);
        }, 5000);
    });
});

// ============================================
// Form Input Enhancements
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    // Add focus effects to form inputs
    const inputs = document.querySelectorAll('.form-input, .form-textarea');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
        });
    });
});

// ============================================
// Responsive Navigation
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle (if needed in future)
    const navLinks = document.querySelector('.nav-links');
    if (window.innerWidth <= 768 && navLinks) {
        // Add mobile menu functionality if needed
    }
});
