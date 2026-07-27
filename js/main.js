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
