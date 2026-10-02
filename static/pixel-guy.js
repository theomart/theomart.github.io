/* Small pixel character placed in front of every a[data-px] link to the pixel career page.
   It idles, waves on hover, and on click it teleports (a light column and rings) before the browser follows the link.
   Same palette spirit as /parcours/, the hoodie takes the site accent. No dependency, about 2 KB. */
(function () {
  var links = document.querySelectorAll('a[data-px]');
  if (!links.length) return;
  var still = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var accent = getComputedStyle(document.documentElement).getPropertyValue('--accent').trim() || '#a63d1f';
  var C = { h: '#2a2230', s: '#e0a77a', e: '#1b1a17', b: accent, p: '#3a3f58', k: '#f4f0e6' };
  var S = 2, W = 12, H = 16;   // sprite grid, drawn at 2 css pixels per cell
  // body rows; legs and arms are added per frame
  var BODY = ['....hhhh....', '...hhhhhh...', '...hssssh...', '...sesses...', '...ssssss...', '....ssss....',
              '..bbbbbbbb..', '..bbbbbbbb..', '..bbbbbbbb..', '...bbbbbb...', '...pp..pp...'];
  function draw(g, f, wave, t) {
    g.clearRect(0, 0, W * S, H * S);
    var bob = (!still && f % 2) ? 1 : 0;
    function px(x, y, c) { g.fillStyle = C[c]; g.fillRect(x * S, (y + bob) * S, S, S); }
    BODY.forEach(function (row, y) { for (var x = 0; x < W; x++) if (row[x] !== '.') px(x, y + 1, row[x]); });
    px(1, 8, 'b'); px(1, 9, 's');                                        // left arm
    if (wave) { var up = (t % 2) ? 4 : 5; px(10, 7, 'b'); px(11, up + 1, 'b'); px(11, up, 's'); }
    else { px(10, 8, 'b'); px(10, 9, 's'); }
    var step = (!still && f % 4 > 1) ? 1 : 0;
    px(3 + step, 12, 'p'); px(8 - step, 12, 'p'); px(3 + step, 13, 'k'); px(4 + step, 13, 'k'); px(7 - step, 13, 'k'); px(8 - step, 13, 'k');
  }
  function teleport(cv, href) {
    var r = cv.getBoundingClientRect(), o = document.createElement('canvas'), D = 120, dpr = window.devicePixelRatio || 1;
    o.width = D * dpr; o.height = D * dpr;
    o.style.cssText = 'position:fixed;pointer-events:none;z-index:99;width:' + D + 'px;height:' + D + 'px;left:' + (r.left + r.width / 2 - D / 2) + 'px;top:' + (r.top + r.height / 2 - D / 2) + 'px';
    document.body.appendChild(o); cv.style.visibility = 'hidden';
    var g = o.getContext('2d'); g.scale(dpr, dpr); g.imageSmoothingEnabled = false;
    var t0 = performance.now();
    (function frame(now) {
      var u = Math.min(1, (now - t0) / 650), c = D / 2;
      g.clearRect(0, 0, D, D);
      for (var k = 0; k < 3; k++) { var q = (u * 1.4 - k * .18); if (q <= 0 || q >= 1) continue; g.globalAlpha = 1 - q; g.strokeStyle = accent; g.lineWidth = 2; g.beginPath(); g.arc(c, c, 6 + q * 52, 0, 7); g.stroke(); }
      var cw = 24 * (1 - u), ch = 32 * (1 + u * 1.5);
      g.globalAlpha = 1; g.fillStyle = '#fff6d8'; g.fillRect(c - cw / 4, c - ch / 2 - 10 * u, cw / 2, ch);
      g.globalAlpha = .35; g.fillStyle = accent; g.fillRect(c - cw / 2, c - ch / 2 - 10 * u, cw, ch);
      for (var i = 0; i < 10; i++) { var a = i * .63 + u * 6, d = 10 + u * 34 * ((i % 3) + 1) / 3; g.globalAlpha = 1 - u; g.fillStyle = i % 2 ? accent : '#ffcd75'; g.fillRect(c + Math.cos(a) * d, c + Math.sin(a) * d - u * 20, 3, 3); }
      if (u < 1) requestAnimationFrame(frame); else location.href = href;
    })(t0);
  }
  links.forEach(function (a) {
    var cv = document.createElement('canvas'), dpr = window.devicePixelRatio || 1;
    cv.width = W * S * dpr; cv.height = H * S * dpr; cv.setAttribute('aria-hidden', 'true');
    cv.style.cssText = 'width:' + W * S + 'px;height:' + H * S + 'px;vertical-align:-10px;margin-right:4px;image-rendering:pixelated';
    var g = cv.getContext('2d'); g.scale(dpr, dpr);
    a.insertBefore(cv, a.firstChild);
    var f = 0, hover = false, tick = 0;
    a.addEventListener('mouseenter', function () { hover = true; });
    a.addEventListener('mouseleave', function () { hover = false; });
    a.addEventListener('focus', function () { hover = true; });
    a.addEventListener('blur', function () { hover = false; });
    a.addEventListener('click', function (e) {
      if (still || e.metaKey || e.ctrlKey || e.shiftKey || e.button) return;
      e.preventDefault(); teleport(cv, a.href);
    });
    draw(g, 0, false, 0);
    if (!still) setInterval(function () { f++; tick++; draw(g, a.hasAttribute('data-px-walk') ? f : (f % 8 === 0 ? 1 : 0), hover, tick); }, 180);
  });
})();
