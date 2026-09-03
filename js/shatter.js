/*
  Scroll driven shatter hero.

  The section is taller than the viewport and its stage is sticky, so the
  page appears to hold still while scroll progress scrubs through 110
  frames on a canvas. Copy fades in and out against that progress.

  The headline is real markup and is present from first paint, so it is
  readable without JavaScript and to anything that does not run the
  animation. Reduced motion skips the scrub entirely and shows the
  resolved state.
*/
(function () {
  var hero = document.querySelector('.shatter-hero');
  if (!hero) return;

  var canvas = hero.querySelector('.shatter-canvas');
  var ctx = canvas.getContext('2d', { alpha: false });
  var lines = Array.prototype.slice.call(hero.querySelectorAll('[data-in]'));
  var cue = hero.querySelector('.shatter-cue');
  var total = parseInt(hero.dataset.frames, 10) || 110;
  var mobile = window.matchMedia('(max-width: 820px)').matches;
  var dir = mobile ? 'mobile' : 'desktop';
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /*
    Phones get a plain gradient hero instead of the scrub. The sequence
    cost 1.3MB of frames and ran 320vh, roughly three screens of scrolling
    before the headline, for a headline that rendered at 18px. The markup
    hero underneath is already complete, so CSS reveals it and this exits
    before a single frame is requested.
  */
  if (mobile) {
    hero.classList.add('is-plain');
    return;
  }

  // The still shown when the scrub is skipped. Frame 110 is almost empty,
  // just debris, so it carries no brand at all. This one still reads as
  // the logo while it is coming apart.
  var STATIC_FRAME = 37;

  var frames = new Array(total);
  var loaded = new Array(total);
  var ready = 0;
  var current = -1;
  var natural = { w: mobile ? 992 : 1984, h: mobile ? 470 : 940 };

  function src(i) {
    return '/assets/shatter/' + dir + '/frame-' + String(i + 1).padStart(4, '0') + '.webp';
  }

  function sizeCanvas() {
    var w = hero.clientWidth;
    var h = window.innerHeight;
    /*
      Never give the canvas more backing pixels than the source frame
      actually has. At devicePixelRatio 2 a 1440px viewport asks for a
      2880px buffer, which forces the browser to upscale the frame and is
      what made this look soft. Capping at the source width means the
      image maps roughly one to one instead.
    */
    var scale = Math.max(w / natural.w, h / natural.h);
    var noUpscale = scale > 0 ? 1 / scale : 2;
    var dpr = Math.max(1, Math.min(window.devicePixelRatio || 1, 2, noUpscale));
    canvas.width = Math.round(w * dpr);
    canvas.height = Math.round(h * dpr);
    canvas.style.width = w + 'px';
    canvas.style.height = h + 'px';
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    current = -1;
  }

  // draw the frame the way object-fit: cover would
  function draw(i) {
    var img = frames[i];
    if (!img || !loaded[i]) {
      // fall back to the nearest frame that has arrived
      var alt = -1;
      for (var d = 1; d < total; d++) {
        if (i - d >= 0 && loaded[i - d]) { alt = i - d; break; }
        if (i + d < total && loaded[i + d]) { alt = i + d; break; }
      }
      if (alt === -1) return;
      i = alt;
      img = frames[i];
    }
    if (i === current) return;
    current = i;

    var cw = hero.clientWidth;
    var ch = window.innerHeight;
    var scale = Math.max(cw / natural.w, ch / natural.h);
    var dw = natural.w * scale;
    var dh = natural.h * scale;
    ctx.fillStyle = '#0B1F3A';
    ctx.fillRect(0, 0, cw, ch);
    ctx.drawImage(img, (cw - dw) / 2, (ch - dh) / 2, dw, dh);
  }

  function fade(p, inAt, outAt) {
    var ramp = 0.03;
    if (p < inAt - ramp) return 0;
    if (p < inAt) return (p - (inAt - ramp)) / ramp;
    if (outAt >= 1) return 1;
    if (p < outAt) return 1;
    if (p < outAt + ramp) return 1 - (p - outAt) / ramp;
    return 0;
  }

  function paintCopy(p) {
    if (cue) cue.style.opacity = p > 0.04 ? 0 : 1;
    for (var i = 0; i < lines.length; i++) {
      var el = lines[i];
      var o = fade(p, parseFloat(el.dataset.in), parseFloat(el.dataset.out));
      el.style.opacity = o;
      // slight rise as it appears, so it reads as motion rather than a switch
      el.style.transform = 'translateY(' + ((1 - o) * 14).toFixed(2) + 'px)';
      el.style.pointerEvents = o > 0.5 ? 'auto' : 'none';
    }
  }

  /*
    Driven by a rAF loop reading scroll position rather than by scroll
    events. Scroll events are throttled during iOS momentum scrolling,
    which shows up as the animation lurching behind the finger. The loop
    only runs while the hero is on screen.
  */
  var running = false;
  var lastP = -1;

  function render() {
    var rect = hero.getBoundingClientRect();
    var span = hero.offsetHeight - window.innerHeight;
    var p = span > 0 ? Math.min(Math.max(-rect.top / span, 0), 1) : 1;
    if (p !== lastP) {
      lastP = p;
      draw(Math.min(total - 1, Math.floor(p * total)));
      paintCopy(p);
    }
    if (running) requestAnimationFrame(render);
  }

  function start() {
    if (running) return;
    running = true;
    requestAnimationFrame(render);
  }

  function stop() {
    running = false;
  }

  function onScroll() {
    lastP = -1;
    render();
  }

  function load(i, cb) {
    var img = new Image();
    img.decoding = 'async';
    img.onload = function () {
      loaded[i] = true;
      ready++;
      if (cb) cb();
    };
    img.onerror = function () { if (cb) cb(); };
    img.src = src(i);
    frames[i] = img;
  }

  if (reduced) {
    hero.classList.add('is-static');
    load(STATIC_FRAME, function () { draw(STATIC_FRAME); });
    paintCopy(1);
    return;
  }

  sizeCanvas();

  // first frame first so the hero is never blank, then the rest in order
  load(0, function () {
    draw(0);
    paintCopy(0);
    hero.classList.add('is-ready');
    var next = 1;
    function queue() {
      if (next >= total) return;
      var i = next++;
      load(i, queue);
    }
    // a few parallel loaders keeps the sequence ahead of a fast scroll
    for (var k = 0; k < 4; k++) queue();
  });

  // only animate while the hero is actually on screen
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      entries[0].isIntersecting ? start() : stop();
    }, { rootMargin: '120px' }).observe(hero);
  } else {
    start();
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', function () {
    var wasMobile = mobile;
    mobile = window.matchMedia('(max-width: 820px)').matches;
    if (mobile !== wasMobile) return window.location.reload();
    sizeCanvas();
    onScroll();
  });
  start();
})();
