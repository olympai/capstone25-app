// Auto-resize textarea functionality
document.addEventListener('DOMContentLoaded', function() {
    const textarea = document.getElementById('user_message');
    const submitButton = document.getElementById('message_submit_button');
    if (!textarea || !submitButton) return;
    
    // Store the initial height as minimum height
    const initialHeight = textarea.offsetHeight;
    
    function autoResize() {
        // WICHTIG: Setze height auf 0 oder eine sehr kleine Zahl, um scrollHeight korrekt zu messen
        textarea.style.height = '0px';
        
        // Jetzt scrollHeight messen - das ist die tatsächliche Höhe des Inhalts
        const maxHeight = 150; // pixels, same as CSS max-height
        const minHeight = initialHeight; // Use initial height as minimum
        const calculatedHeight = textarea.scrollHeight;
        const newHeight = Math.min(Math.max(calculatedHeight, minHeight), maxHeight);
        
        textarea.style.height = newHeight + 'px';
        
        // Enable scrolling if content exceeds max height
        if (textarea.scrollHeight > maxHeight) {
            textarea.style.overflowY = 'auto';
        } else {
            textarea.style.overflowY = 'hidden';
        }
        
        // Sync submit button height with textarea
        submitButton.style.height = newHeight + 'px';
    }

    function resetToInitialHeight() {
        // Reset textarea to initial height
        textarea.style.height = initialHeight + 'px';
        textarea.style.overflowY = 'hidden';

        // Reset submit button height to match
        submitButton.style.height = initialHeight + 'px';
    }
    
    // Add event listeners for real-time resizing
    textarea.addEventListener('input', autoResize);
    
    textarea.addEventListener('keydown', function(e) {
        // Handle Enter key for form submission
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            $('#chat-form').trigger('submit');
            // Reset textarea height after submission
            resetToInitialHeight();
        }
    });

    // Handle submit button click
    submitButton.addEventListener('click', function(e) {
        // Reset textarea height after submission
        resetToInitialHeight();
    });

    // Initial resize on page load
    autoResize();
});