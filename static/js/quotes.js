(function () {
    var root = document.querySelector('.inspiration');
    if (!root) return;

    var slides = root.querySelectorAll('.slide');
    var dotsBox = root.querySelector('.q-dots');
    var index = 0;
    var timer = null;
    var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    slides.forEach(function (_, i) {
        var dot = document.createElement('button');
        dot.type = 'button';
        dot.className = 'q-dot';
        dot.setAttribute('aria-label', 'Show quote ' + (i + 1));
        dot.addEventListener('click', function () { show(i); });
        dotsBox.appendChild(dot);
    });
    var dots = dotsBox.querySelectorAll('.q-dot');

    function show(i) {
        index = (i + slides.length) % slides.length;
        slides.forEach(function (s, n) { s.classList.toggle('is-active', n === index); });
        dots.forEach(function (d, n) { d.classList.toggle('is-active', n === index); });
    }

    function start() {
        if (reduceMotion || timer) return;
        timer = setInterval(function () { show(index + 1); }, 7000);
    }

    function stop() {
        clearInterval(timer);
        timer = null;
    }

    root.querySelectorAll('.q-btn').forEach(function (b) {
        b.addEventListener('click', function () { show(index + Number(b.dataset.dir)); });
    });

    root.addEventListener('mouseenter', stop);
    root.addEventListener('mouseleave', start);
    root.addEventListener('focusin', stop);
    root.addEventListener('focusout', start);

    show(0);
    start();
})();