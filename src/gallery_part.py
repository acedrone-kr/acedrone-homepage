# ---------------- 현장 소식 (갤러리) ----------------
# 새 글을 추가하려면 src/albums.json 에 항목을 추가하면 됩니다.
#   cat: news(언론 보도) / event(교육·행사) / student(수료생) / place(교육장)
#   imgs: 서버에 있는 원본 이미지 경로 목록, 썸네일은 src/thumbs.json 에서 찾습니다.
import html as _html
# 크게 보기 원본 사진 위치 (현재: 예전 카페24 서버. 사진을 옮기면 '' 로 바꾸고 원본을 이 저장소에 넣으면 됩니다)
FULL_BASE = 'https://acedrone.cafe24.com'
ALBUMS = json.load(open(os.path.join(ROOT, 'albums.json'), encoding='utf-8'))
THUMBS = json.load(open(os.path.join(ROOT, 'thumbs.json'), encoding='utf-8'))
GCATS = [('news', '언론 보도', 'Press'), ('event', '교육·행사', 'Events'), ('student', '수료생', 'Graduates'), ('place', '교육장', 'Facility')]
GANCHOR = {'news': 'news', 'event': 'events', 'student': 'students', 'place': 'places'}
SHOW_FIRST = {'event': 9, 'student': 12, 'place': 9}

def _th(p):
    return 'images/gallery/' + THUMBS[p] if p in THUMBS else (p if p.startswith('images/') else '')

def _fmt(d):
    return d.replace('-', '.')

def gallery_data():
    out = []
    for a in ALBUMS:
        out.append({'t': a['title'], 'd': _fmt(a['date']), 'x': a.get('text') or '', 'l': a.get('link') or '',
                    'v': ('https://youtu.be/' + a['video']) if a.get('video') else '',
                    'i': [[_th(p), FULL_BASE + p] for p in a['imgs']]})
    return '<script type="application/json" id="gdata">' + json.dumps(out, ensure_ascii=False).replace('</', '<\\/') + '</script>'

def _src_label(a):
    return _html.escape(a.get('text') or '')

def gallery_section(cat, label, eng, first=False):
    items = [(i, a) for i, a in enumerate(ALBUMS) if a['cat'] == cat]
    cards = []
    limit = SHOW_FIRST.get(cat)
    for n, (i, a) in enumerate(items):
        hide = ' hidden' if limit and n >= limit else ''
        title = _html.escape(a['title'])
        cover = _th(a['imgs'][0]) if a['imgs'] else ''
        count = len(a['imgs'])
        if cat == 'news':
            img = '<img src="%s" alt="" loading="lazy">' % cover if cover else '<span class="news-mark" aria-hidden="true">NEWS</span>'
            src = _src_label(a) if a.get('link') else ''
            extra = '<span class="news-src">%s</span>' % src if src else ''
            cards.append('<li%s><button type="button" class="news-item" data-album="%d"><span class="news-thumb">%s</span><span class="news-body">%s<b>%s</b><span class="g-date">%s</span></span></button></li>' % (hide, i, img, extra, title, _fmt(a['date'])))
        else:
            badge = '<span class="g-count">%d장</span>' % count if count > 1 else ''
            vid = '<span class="g-count">영상</span>' if a.get('video') and not count else ''
            img = '<img src="%s" alt="%s" loading="lazy" width="400" height="300">' % (cover, title) if cover else '<span class="g-noimg">영상</span>'
            cards.append('<li%s><button type="button" class="g-card" data-album="%d"><span class="g-img">%s%s%s</span><span class="g-cap"><b>%s</b><span class="g-date">%s</span></span></button></li>' % (hide, i, img, badge, vid, title, _fmt(a['date'])))
    listcls = 'news-list' if cat == 'news' else ('g-grid g-grid-sm' if cat == 'student' else 'g-grid')
    more = ''
    if limit and len(items) > limit:
        more = '<button type="button" class="btn ghost g-more" data-more>%d개 더 보기</button>' % (len(items) - limit)
    body = '<ul class="%s">%s</ul>%s' % (listcls, ''.join(cards), more)
    return sec(GANCHOR[cat], eng, label, body, first=first)

def recent_strip():
    ev = [ (i, a) for i, a in enumerate(ALBUMS) if a['cat'] == 'event' and a['imgs']][:4]
    cards = ''.join('<li><a class="g-card" href="gallery.html#events"><span class="g-img"><img src="%s" alt="%s" loading="lazy" width="400" height="300"></span><span class="g-cap"><b>%s</b><span class="g-date">%s</span></span></a></li>' % (_th(a['imgs'][0]), _html.escape(a['title']), _html.escape(a['title']), _fmt(a['date'])) for i, a in ev)
    return '''<section class="block gray"><div class="wrap">
  <div class="head"><div><p class="eyebrow">현장 소식</p><h2>학교와 기관에서도<br>에이스드론을 찾아요</h2></div><a class="more" href="gallery.html">현장 소식 전체 보기 →</a></div>
  <ul class="g-grid g-grid-4">%s</ul>
</div></section>''' % cards

LIGHTBOX = '''<div class="lb" id="lb" hidden role="dialog" aria-modal="true" aria-labelledby="lb-title">
  <div class="lb-inner">
    <button type="button" class="lb-close" data-lb="close" aria-label="닫기">✕</button>
    <div class="lb-stage"><img id="lb-img" alt=""><button type="button" class="lb-nav prev" data-lb="prev" aria-label="이전 사진">‹</button><button type="button" class="lb-nav next" data-lb="next" aria-label="다음 사진">›</button></div>
    <div class="lb-info"><p class="g-date" id="lb-date"></p><h3 id="lb-title"></h3><p id="lb-text"></p><p class="lb-links" id="lb-links"></p><p class="lb-count" id="lb-count"></p></div>
  </div>
</div>'''

PAGES['gallery.html'] = ('현장 소식', page_hero('gallery.html', '현장 소식', '언론 보도, 출강·행사, 수료생과 교육장 사진을 모았습니다.') +
    ''.join(gallery_section(c, l, e, first=(n == 0)) for n, (c, l, e) in enumerate(GCATS)) +
    '<div style="height:48px"></div>' + gallery_data() + LIGHTBOX)
