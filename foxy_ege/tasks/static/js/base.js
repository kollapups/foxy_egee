document.addEventListener('DOMContentLoaded', function () {
    const burger = document.querySelector('.burger-menu');
    const sidebar = document.getElementById('sidebar');

    burger.addEventListener('click', function () {
        sidebar.classList.toggle('active');
        // Анимация бургер-меню (опционально)
        burger.classList.toggle('open');
    });

    // Закрытие боковой панели при клике вне её
    document.addEventListener('click', function (event) {
        if (!sidebar.contains(event.target) && !burger.contains(event.target) && sidebar.classList.contains('active')) {
            sidebar.classList.remove('active');
            burger.classList.remove('open');
        }
    });
});