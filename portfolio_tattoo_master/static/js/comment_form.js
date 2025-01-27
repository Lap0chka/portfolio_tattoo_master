document.addEventListener("DOMContentLoaded", function() {
    // Если в URL есть якорь (например, #commentForm), прокрутить страницу к этому элементу
    if (window.location.hash && window.location.hash === '#commentForm') {
        var element = document.getElementById('commentForm');
        if (element) {
            element.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }
});