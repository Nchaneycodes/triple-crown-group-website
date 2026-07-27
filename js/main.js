document.addEventListener('DOMContentLoaded', function () {
  var header = document.querySelector('.site-header');
  var onScroll = function () {
    if (window.scrollY > 24) {
      header.classList.add('is-scrolled');
    } else {
      header.classList.remove('is-scrolled');
    }
  };
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  var toggle = document.querySelector('.nav-toggle');
  var mobileMenu = document.querySelector('.mobile-menu');
  var scrim = document.querySelector('.menu-scrim');

  function closeMenu() {
    mobileMenu.classList.remove('is-open');
    scrim.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', 'false');
  }

  function openMenu() {
    mobileMenu.classList.add('is-open');
    scrim.classList.add('is-open');
    toggle.setAttribute('aria-expanded', 'true');
  }

  if (toggle) {
    toggle.addEventListener('click', function () {
      var isOpen = mobileMenu.classList.contains('is-open');
      if (isOpen) { closeMenu(); } else { openMenu(); }
    });
    scrim.addEventListener('click', closeMenu);
    mobileMenu.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', closeMenu);
    });
  }

  var revealEls = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && revealEls.length) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15, rootMargin: '0px 0px -60px 0px' });

    revealEls.forEach(function (el, i) {
      el.style.setProperty('--stagger-index', i % 6);
      observer.observe(el);
    });
  } else {
    revealEls.forEach(function (el) { el.classList.add('is-visible'); });
  }

  var rotator = document.querySelector('.rotator');
  if (rotator) {
    var slides = Array.prototype.slice.call(rotator.querySelectorAll('.rotator-slide'));
    var dotWrap = rotator.querySelector('.rotator-dots');
    var current = 0;
    var timer = null;
    var HOLD = 5200;

    var dots = slides.map(function (slide, i) {
      var dot = document.createElement('button');
      dot.className = 'rotator-dot' + (i === 0 ? ' is-active' : '');
      dot.type = 'button';
      dot.setAttribute('aria-label', 'Show item ' + (i + 1) + ' of ' + slides.length);
      dot.addEventListener('click', function () {
        show(i);
        restart();
      });
      dotWrap.appendChild(dot);
      return dot;
    });

    function show(next) {
      slides[current].classList.remove('is-active');
      dots[current].classList.remove('is-active');
      current = next;
      slides[current].classList.add('is-active');
      dots[current].classList.add('is-active');
    }

    function advance() { show((current + 1) % slides.length); }

    function restart() {
      window.clearInterval(timer);
      timer = window.setInterval(advance, HOLD);
    }

    var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (!reduced && slides.length > 1) {
      restart();
      rotator.addEventListener('mouseenter', function () { window.clearInterval(timer); });
      rotator.addEventListener('mouseleave', restart);
    }
  }

  var form = document.querySelector('.contact-form');
  var modalScrim = document.querySelector('.modal-scrim');
  var modalClose = document.querySelector('.modal-close');

  if (form && modalScrim) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      modalScrim.classList.add('is-open');
    });
    modalClose.addEventListener('click', function () {
      modalScrim.classList.remove('is-open');
    });
    modalScrim.addEventListener('click', function (e) {
      if (e.target === modalScrim) { modalScrim.classList.remove('is-open'); }
    });
  }
});
