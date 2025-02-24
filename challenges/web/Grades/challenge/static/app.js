document.addEventListener('DOMContentLoaded', () => {
    const flashMessages = document.querySelectorAll('.flash');
    setTimeout(() => {
        flashMessages.forEach(msg => msg.remove());
    }, 5000); // Remove flash messages after 5 seconds
});
