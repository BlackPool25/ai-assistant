// Add these enhancements to existing code
document.addEventListener('DOMContentLoaded', () => {
    // Flash message auto-hide
    setTimeout(() => {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            alert.style.display = 'none';
        });
    }, 5000);

    // Accessibility enhancements
    document.querySelectorAll('.senior-input').forEach(input => {
        input.addEventListener('focus', () => {
            input.parentElement.classList.add('input-focused');
        });
        input.addEventListener('blur', () => {
            input.parentElement.classList.remove('input-focused');
        });
    });
});

// Add to existing chat functionality
async function getBotResponse(message) {
    try {
        const loadingIndicator = document.createElement('div');
        loadingIndicator.className = 'loading-indicator';
        loadingIndicator.innerHTML = `
            <div class="loading-dots">
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
            </div>
        `;
        chatHistory.appendChild(loadingIndicator);
        chatHistory.scrollTop = chatHistory.scrollHeight;

        // Rest of existing code
        
    } catch (error) {
        // Remove loading indicator on error
        chatHistory.removeChild(loadingIndicator);
        console.error('Error:', error);
    }
}