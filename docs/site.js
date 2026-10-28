(function () {
  // 모바일 메뉴 열기/닫기
  var btn = document.querySelector('.menu-btn');
  var gnb = document.querySelector('.gnb');
  if (btn && gnb) {
    btn.addEventListener('click', function () {
      var open = gnb.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      btn.textContent = open ? '✕' : '☰';
    });
  }

  // 서브메뉴 탭: 현재 보고 있는 구역 표시
  var tabs = Array.prototype.slice.call(document.querySelectorAll('.subnav a'));
  var targets = tabs.map(function (a) { return document.getElementById(a.getAttribute('href').split('#')[1]); });
  function mark() {
    var idx = 0;
    targets.forEach(function (el, i) { if (el && el.getBoundingClientRect().top < 160) idx = i; });
    if ((window.innerHeight + window.scrollY) >= document.body.scrollHeight - 4) idx = targets.length - 1;
    tabs.forEach(function (a, i) { a.classList.toggle('on', i === idx); });
  }
  if (tabs.length) { window.addEventListener('scroll', mark, { passive: true }); mark(); }

  // 메인 화면 배경: 실기시험 비행 코스를 닮은 궤적
  var c = document.getElementById('sky');
  if (!c || !c.getContext) return;
  var ctx = c.getContext('2d'), w, h;
  function size() {
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    w = c.clientWidth; h = c.clientHeight;
    c.width = w * dpr; c.height = h * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }
  function draw(t) {
    ctx.clearRect(0, 0, w, h);
    var cs = getComputedStyle(c.parentNode);
    var line = cs.getPropertyValue('--band-soft').trim() || '#9fb0c6';
    var sig = cs.getPropertyValue('--signal').trim() || '#e8590c';
    ctx.strokeStyle = line; ctx.globalAlpha = .18; ctx.lineWidth = 1;
    for (var x = 0; x < w; x += 48) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke(); }
    for (var y = 0; y < h; y += 48) { ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke(); }
    var cx = w * .72, cy = h * .5, r = Math.min(w, h) * .28;
    ctx.globalAlpha = .45; ctx.setLineDash([6, 8]); ctx.lineWidth = 1.5;
    ctx.beginPath();
    for (var a = 0; a <= Math.PI * 2 + .01; a += .02) {
      var px = cx + Math.sin(a) * r * 1.6, py = cy + Math.sin(a * 2) * r * .6;
      if (a === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
    }
    ctx.stroke(); ctx.setLineDash([]);
    var k = (t / 4000) % (Math.PI * 2);
    var dx = cx + Math.sin(k) * r * 1.6, dy = cy + Math.sin(k * 2) * r * .6;
    ctx.globalAlpha = 1; ctx.fillStyle = sig;
    ctx.beginPath(); ctx.arc(dx, dy, 5, 0, Math.PI * 2); ctx.fill();
    ctx.globalAlpha = .25; ctx.beginPath(); ctx.arc(dx, dy, 14, 0, Math.PI * 2); ctx.fill();
    ctx.globalAlpha = 1;
  }
  size(); window.addEventListener('resize', size);
  if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) { draw(0); return; }
  (function loop(t) { draw(t || 0); requestAnimationFrame(loop); })();
})();

// 메인 팝업: 닫기 / 오늘 하루 보지 않기
(function () {
  var box = document.querySelector('.popups');
  if (!box) return;
  var dim = document.querySelector('.pop-dim');
  var d = new Date(), today = d.getFullYear() + '-' + (d.getMonth() + 1) + '-' + d.getDate();
  function hiddenToday(id) { try { return localStorage.getItem('pop-' + id) === today; } catch (e) { return false; } }
  function refresh() {
    var left = box.querySelectorAll('.popup:not([hidden])');
    // 휴대폰에서 다음 팝업이 보이도록 남은 것만 표시
    if (!left.length) { box.hidden = true; if (dim) dim.hidden = true; }
  }
  Array.prototype.forEach.call(box.querySelectorAll('.popup'), function (p) {
    var id = p.getAttribute('data-id');
    if (hiddenToday(id)) p.hidden = true;
    p.addEventListener('click', function (e) {
      var act = e.target.getAttribute && e.target.getAttribute('data-act');
      if (!act) return;
      if (act === 'today') { try { localStorage.setItem('pop-' + id, today); } catch (err) {} }
      p.remove(); refresh();
    });
  });
  Array.prototype.forEach.call(box.querySelectorAll('.popup[hidden]'), function (p) { p.remove(); });
  refresh();
  if (dim) dim.addEventListener('click', function () { box.hidden = true; dim.hidden = true; });
})();

// 현장 소식: 더 보기 + 사진 크게 보기
(function () {
  Array.prototype.forEach.call(document.querySelectorAll('[data-more]'), function (b) {
    b.addEventListener('click', function () {
      var list = b.previousElementSibling;
      Array.prototype.forEach.call(list.querySelectorAll('li[hidden]'), function (li) { li.hidden = false; });
      b.remove();
    });
  });
  var dataEl = document.getElementById('gdata'), lb = document.getElementById('lb');
  if (!dataEl || !lb) return;
  var data = JSON.parse(dataEl.textContent), preview = dataEl.getAttribute('data-preview') === '1';
  var img = document.getElementById('lb-img'), cur = null, idx = 0, lastFocus = null;
  function el(id) { return document.getElementById(id); }
  function show() {
    var a = data[cur], pics = a.i;
    var stage = img.parentNode;
    stage.hidden = !pics.length;
    if (pics.length) {
      var p = pics[idx];
      img.src = p[0];
      if (!preview && p[1]) { var hi = new Image(); hi.onload = function () { if (data[cur] === a && a.i[idx] === p) img.src = p[1]; }; hi.src = p[1]; }
      img.alt = a.t + (pics.length > 1 ? ' (' + (idx + 1) + '/' + pics.length + ')' : '');
    }
    lb.querySelector('.prev').hidden = lb.querySelector('.next').hidden = pics.length < 2;
    el('lb-date').textContent = a.d; el('lb-title').textContent = a.t; el('lb-text').textContent = a.x && !a.l ? a.x : (a.l && a.x ? a.x + ' 보도' : a.x);
    var links = '';
    if (a.l) links += '<a class="btn" href="' + a.l + '" target="_blank" rel="noopener">기사 보기 ↗</a>';
    if (a.v) links += '<a class="btn ghost" href="' + a.v + '" target="_blank" rel="noopener">영상 보기 ↗</a>';
    el('lb-links').innerHTML = links;
    el('lb-count').textContent = pics.length > 1 ? (idx + 1) + ' / ' + pics.length : '';
  }
  function open(i) { lastFocus = document.activeElement; cur = i; idx = 0; show(); lb.hidden = false; document.body.style.overflow = 'hidden'; lb.querySelector('.lb-close').focus(); }
  function close() { lb.hidden = true; document.body.style.overflow = ''; img.removeAttribute('src'); if (lastFocus) lastFocus.focus(); }
  function step(d) { var n = data[cur].i.length; if (n < 2) return; idx = (idx + d + n) % n; show(); }
  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('[data-album]');
    if (b) { open(+b.getAttribute('data-album')); return; }
    var act = e.target.closest && e.target.closest('[data-lb]');
    if (act) { var k = act.getAttribute('data-lb'); if (k === 'close') close(); else step(k === 'next' ? 1 : -1); return; }
    if (e.target === lb) close();
  });
  document.addEventListener('keydown', function (e) {
    if (lb.hidden) return;
    if (e.key === 'Escape') close(); else if (e.key === 'ArrowRight') step(1); else if (e.key === 'ArrowLeft') step(-1);
  });
})();

// 상단 메뉴: 사진 위에서는 투명, 내리면 흰색
(function () {
  var h = document.querySelector('header.top.over');
  if (!h) return;
  function upd() { h.classList.toggle('solid', window.scrollY > 40); }
  window.addEventListener('scroll', upd, { passive: true }); upd();
  var btn = h.querySelector('.menu-btn');
  if (btn) btn.addEventListener('click', function () { h.classList.toggle('open-menu', btn.getAttribute('aria-expanded') === 'true'); });
})();

// 메인 슬라이드
(function () {
  var hero = document.querySelector('.hero'), dataEl = document.getElementById('hero-data');
  if (!hero || !dataEl) return;
  var slides = hero.querySelectorAll('.slide'), dots = hero.querySelectorAll('.hero-dots button');
  var copy = JSON.parse(dataEl.textContent), cur = 0, timer = null;
  var k = document.getElementById('hero-kicker'), t = document.getElementById('hero-title'), l = document.getElementById('hero-lead');
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  function go(n) {
    if (n === cur) return;
    hero.classList.add('fading');
    setTimeout(function () {
      slides[cur].classList.remove('on'); dots[cur].classList.remove('on');
      cur = n; slides[cur].classList.add('on'); dots[cur].classList.add('on');
      k.textContent = copy[cur][0]; t.innerHTML = copy[cur][1]; l.innerHTML = copy[cur][2];
      hero.classList.remove('fading');
    }, reduce ? 0 : 350);
  }
  function start() { if (reduce) return; stop(); timer = setInterval(function () { go((cur + 1) % slides.length); }, 6000); }
  function stop() { if (timer) clearInterval(timer); timer = null; }
  Array.prototype.forEach.call(dots, function (d, i) { d.addEventListener('click', function () { go(i); start(); }); });
  hero.addEventListener('mouseenter', stop); hero.addEventListener('mouseleave', start);
  start();
})();
