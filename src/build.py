"""에이스드론 홈페이지 생성 스크립트.
site/ : 카페24에 그대로 올리는 완성본 (모든 페이지가 완전한 HTML 문서)
art/  : 미리보기용 (index.html만 본문 형태)
"""
import os, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT_SITE = os.path.join(ROOT, '..', 'docs')   # GitHub Pages 가 이 폴더를 홈페이지로 보여줍니다
OUT_ART = os.environ.get('PREVIEW_OUT')       # (선택) Claude 미리보기용 출력 폴더

def T(s):  # 확인 필요 표시
    return '<i class="todo">' + s + '</i>'

PHONE = '02-523-3001'
ADDR = '서울특별시 동작구 사당로30길 91, 2층'
FIELD = '경기도 남양주시 진건읍 송능리 488-2'
KAKAO = 'https://pf.kakao.com/_qxjSxaK'

MENU = [
    ('about.html', '교육원 소개', [('greeting', '인사말'), ('award', '우수기관 선정'), ('facility', '시설 안내')]),
    ('courses.html', '교육과정', [('overview', '과정 한눈에 보기'), ('grade1', '1종 과정'), ('grade2', '2종 과정'), ('grade3', '3종 과정')]),
    ('license.html', '자격취득 안내', [('process', '취득 절차'), ('eligibility', '응시 자격'), ('faq', '자주 묻는 질문')]),
    ('gallery.html', '현장 소식', [('news', '언론 보도'), ('events', '교육·행사'), ('students', '수료생'), ('places', '교육장')]),
    ('contact.html', '수강상담', [('consult', '수강 상담'), ('map', '오시는 길')]),
]

LOGO = '<svg viewBox="0 0 40 40" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="2.4"><circle cx="9" cy="9" r="6"/><circle cx="31" cy="9" r="6"/><circle cx="9" cy="31" r="6"/><circle cx="31" cy="31" r="6"/><path d="M13 13l14 14M27 13L13 27"/></g><rect x="15" y="15" width="10" height="10" rx="2" fill="#e8590c"/></svg>'

LOGO_SVG = open(os.path.join(ROOT, 'logo_inline.svg'), encoding='utf-8').read()

def header(current):
    items = []
    for href, label, subs in MENU:
        cur = ' aria-current="page"' if href == current else ''
        sub = ''.join('<li><a href="%s#%s">%s</a></li>' % (href, a, l) for a, l in subs)
        items.append('<li><a href="%s"%s>%s</a><ul class="sub">%s</ul></li>' % (href, cur, label, sub))
    return '''<header class="top over">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="에이스드론 처음으로">%s<span class="brand-tag">국토교통부 지정<br>드론 전문교육기관</span></a>
    <nav aria-label="주요 메뉴"><ul class="gnb">%s</ul></nav>
    <a class="btn top-cta" href="contact.html">수강 상담</a>
    <button class="menu-btn" type="button" aria-label="메뉴 열기" aria-expanded="false">☰</button>
  </div>
</header>''' % (LOGO_SVG, ''.join(items))

def footer():
    links = ''.join('<a href="%s">%s</a>' % (h, l) for h, l, _ in MENU)
    return '''<section class="cta-wrap"><div class="wrap">
  <div class="cta-card" style="--bg:url('images/hero-grads.webp')">
    <div><h2>어떤 자격이 맞는지<br>잘 모르겠다면</h2><p>목적과 일정만 알려주세요. 맞는 과정과 개강일을 안내해 드려요.</p></div>
    <div class="cta-actions"><a class="big" href="tel:%s">%s</a><div class="row"><a class="btn light" href="contact.html">상담 안내 보기</a><a class="btn glass" href="https://pf.kakao.com/_qxjSxaK" target="_blank" rel="noopener">카카오톡 문의</a></div></div>
  </div>
</div></section>
<footer>
  <div class="wrap">
    <div>
      <div class="links">%s</div>
      <p style="margin:14px 0 0"><b>㈜에이스드론</b> · 대표 %s · 사업자등록번호 %s<br>이론교육장 %s · 실습비행장 %s<br>대표전화 %s · sh-j0814@naver.com</p>
    </div>
    <div>© 2026 ACE DRONE. All rights reserved.</div>
  </div>
</footer>
<script src="site.js"></script>''' % (PHONE, PHONE, links, '조윤형', '870-86-00820', ADDR, FIELD, PHONE)

PAGE_BG = {'about.html': 'hero-field', 'courses.html': 'hero-fly', 'license.html': 'hero-grads', 'gallery.html': 'hero-award', 'contact.html': 'hero-field'}

def page_hero(current, title, desc):
    for href, label, subs in MENU:
        if href == current:
            tabs = ''.join('<a href="#%s"%s>%s</a>' % (a, ' class="on"' if i == 0 else '', l) for i, (a, l) in enumerate(subs))
            sub = '<div class="subnav-bar"><div class="wrap"><nav class="subnav" aria-label="%s 하위 메뉴">%s</nav></div></div>' % (label, tabs) if len(subs) > 1 else ''
            bg = PAGE_BG.get(current, 'hero-field')
            return '''<section class="page-hero" style="--bg:url('images/%s.webp')">
  <div class="wrap">
    <div class="crumbs"><a href="index.html">처음으로</a> › %s</div>
    <h1>%s</h1>
    <p>%s</p>
  </div>
</section>%s''' % (bg, label, title, desc, sub)

def sec(anchor, eyebrow, title, body, first=False):
    pad = 'padding-block:64px 24px' if first else 'padding-block:40px 24px'
    return '''<section class="anchor" id="%s"><div class="wrap" style="%s">
  <div class="section-title"><h2>%s</h2><p class="eyebrow">%s</p></div>
  %s
</div></section>''' % (anchor, pad, title, eyebrow, body)

# ---------------- 공통 데이터 ----------------
COURSE_TABLE = '''<div class="table-scroll">
  <table>
    <thead><tr><th>자격 종류</th><th>대상 기체 (최대이륙중량)</th><th>필수 비행경력</th><th>주요 활용 분야</th><th>교육 기간 · 수강료</th></tr></thead>
    <tbody>
      <tr class="featured"><td class="grade">1종<span class="tag">인기</span><small>무인멀티콥터</small></td><td><span class="num">25kg 초과</span><br>자체중량 <span class="num">150kg</span> 이하</td><td><span class="num">20시간</span></td><td>농업 방제, 대형 물류, 교관 과정 진입</td><td>%s</td></tr>
      <tr><td class="grade">2종<small>무인멀티콥터</small></td><td><span class="num">7kg 초과 ~ 25kg</span> 이하</td><td><span class="num">10시간</span></td><td>시설 점검, 측량, 소형 방제</td><td>%s</td></tr>
      <tr><td class="grade">3종<small>무인멀티콥터</small></td><td><span class="num">2kg 초과 ~ 7kg</span> 이하</td><td><span class="num">6시간</span></td><td>항공 촬영, 방송·홍보 영상</td><td>%s</td></tr>
    </tbody>
  </table>
</div>
<p class="note">자격 기준은 항공안전법 시행규칙에 따릅니다. 4종(250g 초과 ~ 2kg 이하)은 한국교통안전공단 온라인 교육으로 취득합니다.</p>''' % ('<span class="num">15일</span> · <b>180만원</b>', '<span class="num">10일</span> · <b>150만원</b>', '<span class="num">6일</span> · <b>100만원</b>')

NOTICES = [
    (True, '[예시] 2026년 11월 1종 평일반 수강생 모집', '2026.10.20'),
    (True, '[예시] 동절기 실기교육 운영 시간 변경 안내', '2026.10.15'),
    (False, '[예시] 10월 실기시험 일정 안내', '2026.10.02'),
    (False, '[예시] 추석 연휴 휴원 안내', '2026.09.22'),
    (False, '[예시] 1종 평일반 개강 안내', '2026.09.05'),
]

def notice_rows(limit=None):
    rows, n = [], len([x for x in NOTICES if not x[0]])
    for pin, title, date in NOTICES[:limit] if limit else NOTICES:
        no = '<span class="pin">공지</span>' if pin else str(n)
        if not pin: n -= 1
        rows.append('<tr><td class="no">%s</td><td><a href="notice.html">%s</a></td><td class="date">%s</td></tr>' % (no, title, date))
    return '<div class="table-scroll"><table class="board"><thead><tr><th class="no">번호</th><th>제목</th><th class="date">작성일</th></tr></thead><tbody>%s</tbody></table></div>' % ''.join(rows)

FAQ = [
    ('드론 자격증은 국가자격인가요?', '네. 무인멀티콥터 조종자 자격은 항공안전법에 따라 한국교통안전공단이 발급하는 국가자격입니다.'),
    ('드론을 한 번도 날려본 적이 없어도 되나요?', '네. 대부분의 수강생이 처음 시작하는 분들입니다. 시뮬레이터로 기초를 익힌 뒤 실기체로 넘어갑니다.'),
    ('1종을 따면 2종, 3종 드론도 조종할 수 있나요?', '네. 상위 종류 자격이 있으면 하위 종류 기체도 조종할 수 있습니다.'),
    ('운전면허가 없으면 어떻게 하나요?', '항공신체검사증명을 받아 제출하면 응시할 수 있습니다. 발급 방법은 상담 시 안내해 드립니다.'),
    ('주말반도 있나요?', '현재 주말반은 운영하지 않고 평일반으로 교육합니다.'),
    ('국비 지원을 받을 수 있나요?', '2027년부터 국비 지원 교육이 가능합니다. 세부 일정은 상담 시 안내해 드립니다.'),
]

# ---------------- 페이지 본문 ----------------
PAGES = {}
import json
exec(open(os.path.join(ROOT, 'gallery_part.py'), encoding='utf-8').read())

# ---------------- 메인 팝업 ----------------
# 팝업을 추가/삭제하려면 이 목록만 고치면 됩니다.
# image 에 파일명을 넣으면(예: 'popup1.jpg') 글 대신 이미지 팝업으로 나옵니다.
POPUPS = [
    {'id': '2026-11-gukbi', 'eyebrow': '', 'title': '교육비 100% 전액 무료 드론 국가자격증 국비 과정 선착순 모집 (국민대학교·에이스드론, 11월 A반·B반)', 'text': '', 'link': 'tel:010-8358-3681', 'button': '', 'image': 'images/popup_nov.jpg'},
]

def popups_html():
    if not POPUPS: return ''
    cards = []
    for p in POPUPS:
        if p.get('image'):
            top = '<a href="%s"><img class="pop-img" src="%s" width="720" height="1080" alt="%s"></a>' % (p['link'], p['image'], p['title'].replace('<br>', ' '))
            body = ''
        else:
            top = '<div class="pop-top"><p class="eyebrow">%s</p><h2>%s</h2></div>' % (p['eyebrow'], p['title'])
            body = '<div class="pop-body"><p>%s</p><a class="btn" href="%s">%s</a></div>' % (p['text'], p['link'], p['button'])
        cards.append('<div class="popup" role="dialog" aria-label="%s" data-id="%s">%s%s<div class="pop-foot"><button type="button" data-act="today">오늘 하루 보지 않기</button><button type="button" data-act="close">닫기</button></div></div>' % (p['title'].replace('<br>', ' '), p['id'], top, body))
    return '<div class="pop-dim"></div><div class="popups">' + ''.join(cards) + '</div>'

ICONS = {'award': '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="9" r="6"/><path d="M8.5 14 7 22l5-3 5 3-1.5-8"/></svg>', 'check': '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>', 'users': '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="9" cy="8" r="4"/><path d="M2 21c0-3.9 3.1-7 7-7s7 3.1 7 7"/><path d="M16 4.1a4 4 0 0 1 0 7.8M22 21c0-3-1.8-5.6-4.5-6.6"/></svg>', 'map': '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 21s-7-6.1-7-11.5A7 7 0 0 1 19 9.5C19 14.9 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>'}
def plan(g, w, hours, days, price, uses, best=False):
    return '<article class="plan%s">%s<h3>%s</h3><p class="w">최대이륙중량 %s</p><p class="price">%s<small>만원</small></p><ul><li>교육 기간 %s</li><li>필수 비행경력 %s</li><li>%s</li></ul><a class="btn%s" href="contact.html">상담 신청</a></article>' % (' best' if best else '', '<span class="badge">가장 많이 선택</span>' if best else '', g, w, price, days, hours, uses, '' if best else ' ghost')

PAGES['index.html'] = ('에이스드론 교육원', popups_html() + '''
<section class="hero" aria-label="에이스드론 소개">
  <div class="slides">
    <figure class="slide on" style="--bg:url('images/hero-sky.webp');--bg-m:url('images/hero-sky-m.webp')"></figure>
    <figure class="slide" style="--bg:url('images/hero-award.webp');--bg-m:url('images/hero-award-m.webp')"></figure>
    <figure class="slide" style="--bg:url('images/hero-pilot.webp');--bg-m:url('images/hero-pilot-m.webp')"></figure>
  </div>
  <div class="hero-copy">
    <div class="wrap">
      <p class="hero-kicker" id="hero-kicker">국토교통부 지정 드론 전문교육기관</p>
      <h1 id="hero-title">드론 자격증,<br>합격까지 함께 날아요</h1>
      <p class="lead" id="hero-lead">서울 사당 이론교육장과 남양주 전용 실습비행장에서 <br>무인멀티콥터 1·2·3종 자격을 준비하세요.</p>
      <div class="actions"><a class="btn" href="contact.html">수강 상담 신청</a><a class="btn glass" href="courses.html">교육과정 보기</a></div>
    </div>
  </div>
  <div class="hero-dots"><button type="button" class="on" aria-label="1번 슬라이드"></button><button type="button" aria-label="2번 슬라이드"></button><button type="button" aria-label="3번 슬라이드"></button></div>
  <script type="application/json" id="hero-data">[["국토교통부 지정 드론 전문교육기관","드론 자격증,<br>합격까지 함께 날아요","서울 사당 이론교육장과 남양주 전용 실습비행장에서 <br>무인멀티콥터 1·2·3종 자격을 준비하세요."],["2023 한국교통안전공단 선정","전국최초 · 서울유일<br>드론 우수 전문교육기관","교육 인프라, 운영·관리, 제도 준수 평가에서 <br>전국 36개 지원 기관 중 우수기관으로 선정되었습니다."],["누적 수료생 약 1,200명","실기시험 합격률<br>100%","처음 드론을 잡는 분도 합격까지 끝까지 책임지고 지도합니다."]]</script>
</section>
<section class="statement"><div class="wrap">
  <p class="eyebrow">ACE DRONE</p>
  <h2>하늘을 나는 일,<br>이제 <em>자격</em>이 경쟁력입니다</h2>
  <p class="statement-sub">방제·측량·시설 점검·촬영까지, 드론을 쓰는 현장이 늘고 있어요.<br>에이스드론은 시험 합격을 넘어 현장에서 바로 비행할 수 있는 실력을 만듭니다.</p>
  <div class="big-stats">
    <div><b>전국최초</b><span>서울유일 우수 전문교육기관</span></div>
    <div><b>1,200<small>명</small></b><span>누적 수료생</span></div>
    <div><b>100<small>%</small></b><span>실기시험 합격률</span></div>
    <div><b>1·2·3<small>종</small></b><span>무인멀티콥터 전 과정</span></div>
  </div>
</div></section>
<section class="tiles-sec"><div class="wrap">
  <div class="tiles">
    <a class="tile t-big" href="about.html#facility" style="--bg:url('images/hero-field.webp')"><span class="tile-copy"><small>남양주 실습비행장</small><b>시험 코스 그대로<br>연습하는 전용 비행장</b></span></a>
    <a class="tile" href="about.html#award" style="--bg:url('images/hero-award.webp')"><span class="tile-copy"><small>2023 한국교통안전공단</small><b>우수 전문교육기관 표창</b></span></a>
    <a class="tile" href="about.html#facility" style="--bg:url('images/classroom.jpg')"><span class="tile-copy"><small>서울 사당 이론교육장</small><b>사당역·이수역 도보권</b></span></a>
  </div>
</div></section>
<section class="block"><div class="wrap">
  <div class="head"><div><p class="eyebrow">교육과정</p><h2>나에게 맞는 자격을<br>골라보세요</h2></div><a class="more" href="courses.html">과정별 자세히 보기 →</a></div>
  <div class="plans">''' + plan('1종', '25kg 초과', '20시간', '15일', '180', '농업 방제, 대형 물류, 교관 과정', True) + plan('2종', '7kg 초과 ~ 25kg', '10시간', '10일', '150', '시설 점검, 측량, 소형 방제') + plan('3종', '2kg 초과 ~ 7kg', '6시간', '6일', '100', '항공 촬영, 방송·홍보 영상') + '''</div>
  <p class="note">4종(250g 초과 ~ 2kg)은 한국교통안전공단 온라인 교육으로 취득합니다.</p>
</div></section>
<section class="block gray"><div class="wrap">
  <div class="head"><div><p class="eyebrow">에이스드론을 고르는 이유</p><h2>처음 드론을 잡아도<br>끝까지 책임집니다</h2></div></div>
  <div class="features">
    <div class="feature"><span class="ic">''' + ICONS['award'] + '''</span><h3>공단이 인정한 교육기관</h3><p>2023년 한국교통안전공단 드론 우수 전문교육기관 평가에서 전국 3개 기관 중 한 곳으로 선정되었습니다.</p></div>
    <div class="feature"><span class="ic">''' + ICONS['users'] + '''</span><h3>소수 정원 실기 지도</h3><p>지도조종자 자격을 갖춘 교관이 직접 지도합니다. 누적 수료생 약 1,200명, 실기시험 합격률 100%입니다.</p></div>
    <div class="feature"><span class="ic">''' + ICONS['map'] + '''</span><h3>서울 이론 + 남양주 실습</h3><p>사당역·이수역 근처 이론교육장과 시험 코스를 갖춘 남양주 전용 실습비행장에서 교육합니다. 두 곳 모두 주차할 수 있어요.</p></div>
  </div>
</div></section>
<section class="block"><div class="wrap">
  <div class="head"><div><p class="eyebrow">자격 취득 절차</p><h2>상담부터 자격증까지<br>6단계면 끝나요</h2></div><a class="more" href="license.html">응시 자격 확인하기 →</a></div>
  <ol class="steps">
    <li><span class="n">1</span><h3>수강 상담</h3><p>목적과 일정에 맞는 자격 안내</p></li>
    <li><span class="n">2</span><h3>이론교육</h3><p>항공법규, 기상, 비행이론</p></li>
    <li><span class="n">3</span><h3>실기교육</h3><p>시뮬레이터와 실기체로 비행경력 확보</p></li>
    <li><span class="n">4</span><h3>모의평가</h3><p>시험 코스 그대로 교관 평가</p></li>
    <li><span class="n">5</span><h3>실기시험</h3><p>한국교통안전공단 실기시험</p></li>
    <li><span class="n">6</span><h3>자격증 발급</h3><p>무인멀티콥터 조종자 자격 취득</p></li>
  </ol>
</div></section>
''' + recent_strip() + '''
<section class="block"><div class="wrap">
  <div class="glance">
    <div><p class="eyebrow">한눈에 보기</p><h2>에이스드론은 이런 곳이에요</h2>
      <p>㈜에이스드론은 서울 동작구 사당동에 있는 국토교통부 지정 초경량비행장치(드론) 전문교육기관으로, 무인멀티콥터 1·2·3종 조종자 국가자격 취득 교육을 운영합니다. 2023년 한국교통안전공단 드론 우수 전문교육기관 평가에서 전국 3개 우수기관 중 한 곳으로 선정되었습니다.</p></div>
    <dl class="info">
      <dt>기관명</dt><dd>㈜에이스드론 (ACE DRONE)</dd>
      <dt>구분</dt><dd>드론 전문교육기관 (초경량비행장치 조종자 교육)</dd>
      <dt>교육과정</dt><dd>무인멀티콥터 1종 · 2종 · 3종 조종자 자격</dd>
      <dt>수상</dt><dd>2023 한국교통안전공단 드론 우수 전문교육기관</dd>
      <dt>이론교육장</dt><dd>''' + ADDR + '''</dd>
      <dt>실습비행장</dt><dd>''' + FIELD + '''</dd>
      <dt>문의</dt><dd>''' + PHONE + ''' · sh-j0814@naver.com</dd>
    </dl>
  </div>
</div></section>
''')

PAGES['about.html'] = ('교육원 소개', page_hero('about.html', '교육원 소개', '한국교통안전공단이 인정한 드론 전문교육기관, 에이스드론을 소개합니다.') +
sec('greeting', 'Greeting', '인사말', '''<div class="prose">
  <p>안녕하십니까. ㈜에이스드론을 찾아주셔서 감사합니다.</p>
  <p>드론은 이제 촬영을 넘어 방제, 측량, 시설 점검, 물류까지 산업 현장 곳곳에서 쓰이고 있습니다. 그만큼 안전하게 비행할 줄 아는 조종자가 필요합니다.</p>
  <p>에이스드론은 자격증 취득에서 끝나지 않고, 현장에서 바로 비행할 수 있는 실력을 갖추도록 교육합니다. 처음 드론을 잡는 분도 끝까지 책임지고 지도하겠습니다.</p>
  <p class="signature"><span>㈜에이스드론 대표</span>조윤형</p>
</div>''', first=True) +
sec('award', 'Award', '우수 전문교육기관 선정', '''<div class="contact">
  <div class="prose">
    <p>에이스드론은 한국교통안전공단이 처음 실시한 <b>2023년 드론 우수 전문교육기관</b> 평가에서 우수기관으로 선정되었습니다.</p>
    <p>전국 36개 지원 기관을 대상으로 교육 인프라 확보 역량, 교육 운영·관리 능력, 제도 준수 및 서비스 역량을 종합 심사했으며, 에이스드론을 포함해 3개 기관이 선정되었습니다. 공단 이사장 표창과 우수 전문교육기관 명패를 받았습니다.</p>
  </div>
  <figure class="card award-card"><img src="images/award.jpg" width="700" height="989" alt="2023년 드론 우수 전문교육기관 선정 표창장, 한국교통안전공단 이사장, 2023년 12월 28일"><figcaption class="body"><h3>한국교통안전공단 이사장 표창</h3><p>제9613호 · 2023년 12월 28일</p></figcaption></figure>
</div>''') +
sec('facility', 'Facility', '시설 안내', '<div class="cards">' + ''.join(
    '<figure class="card"><img class="ph" src="images/%s" alt="%s" loading="lazy"><figcaption class="body"><span class="role">%s</span><h3>%s</h3><p>%s</p></figcaption></figure>' % f
    for f in [('office.jpg', '에이스드론 본사 사무실 입구', 'SEOUL · 사당', '본사 · 상담 및 접수', '강의실, 상담실, 휴게실. ' + ADDR + ' (사당역·이수역 인근)'),
              ('classroom.jpg', '이론 및 모의비행 교육장', 'SEOUL · 사당', '이론 · 모의비행 교육장', '항공법규·비행이론 수업과 시뮬레이터 모의비행 교육을 진행합니다.'),
              ('field.jpg', '남양주 실습비행장 전경', 'NAMYANGJU', '실습비행장', '야외 실습장, 실내강의실, 휴게실. ' + FIELD)]) + '</div>') )

def course_block(anchor, g, weight, hours, use, who, fee, days):
    return '''<div class="course anchor" id="%s">
  <div class="grade-big">%s<small>무인멀티콥터 조종자</small></div>
  <div>
    <dl class="spec">
      <dt>대상 기체</dt><dd>최대이륙중량 %s</dd>
      <dt>필수 비행경력</dt><dd>%s 이상</dd>
      <dt>주요 활용</dt><dd>%s</dd>
      <dt>교육 기간</dt><dd>%s</dd>
      <dt>수강료</dt><dd>%s</dd>
    </dl>
    <p style="margin:0;color:var(--ink-soft)">%s</p>
  </div>
</div>''' % (anchor, g, weight, hours, use, days, fee, who)

PAGES['courses.html'] = ('교육과정', page_hero('courses.html', '교육과정', '무인멀티콥터 1·2·3종 조종자 자격 과정을 운영합니다.') +
sec('overview', 'Overview', '과정 한눈에 보기', COURSE_TABLE, first=True) +
'<div class="wrap">' +
course_block('grade1', '1종', '25kg 초과, 자체중량 150kg 이하', '20시간', '농업 방제, 대형 물류, 교관(지도조종자) 과정 진입', '방제·물류 업무를 하시거나 이후 교관 자격까지 생각하는 분께 맞습니다. 1종을 취득하면 2·3·4종 기체도 조종할 수 있습니다. 에이스드론에서 가장 많이 선택하는 과정입니다.', '180만원', '15일') +
course_block('grade2', '2종', '7kg 초과 ~ 25kg 이하', '10시간', '시설물 점검, 측량, 소형 방제, 공공기관 업무', '업무용 드론을 처음 시작하는 분께 맞는 과정입니다. 이후 1종으로 올리실 때 비행경력을 이어서 쌓을 수 있습니다.', '150만원', '10일') +
course_block('grade3', '3종', '2kg 초과 ~ 7kg 이하', '6시간', '항공 촬영, 방송·홍보 영상, 취미 비행', '중형 촬영 드론을 다루려는 분께 맞는 과정입니다. 비교적 짧은 기간에 취득할 수 있습니다.', '100만원', '6일') +
'</div>')

PAGES['license.html'] = ('자격취득 안내', page_hero('license.html', '자격취득 안내', '상담부터 자격증 발급까지, 필요한 절차와 조건을 정리했습니다.') +
sec('process', 'Process', '취득 절차', '''<ol class="steps">
  <li><span class="n">01</span><h3>수강 상담</h3><p>목적과 일정에 맞는 자격 종류 안내</p></li>
  <li><span class="n">02</span><h3>이론교육</h3><p>항공법규, 항공기상, 비행이론 등</p></li>
  <li><span class="n">03</span><h3>실기교육</h3><p>시뮬레이터와 실기체로 비행경력 확보</p></li>
  <li><span class="n">04</span><h3>모의평가</h3><p>시험 코스 그대로 교관 평가</p></li>
  <li><span class="n">05</span><h3>실기시험</h3><p>한국교통안전공단 실기시험 응시</p></li>
  <li><span class="n">06</span><h3>자격증 발급</h3><p>무인멀티콥터 조종자 자격 취득</p></li>
</ol>''', first=True) +
sec('eligibility', 'Eligibility', '응시 자격', '''<dl class="spec" style="max-width:46em">
  <dt>나이</dt><dd>만 14세 이상 (1·2·3종 기준)</dd>
  <dt>신체 조건</dt><dd>2종 보통 운전면허 이상 소지, 또는 항공신체검사증명</dd>
  <dt>비행경력</dt><dd>1종 20시간 · 2종 10시간 · 3종 6시간 이상 (교육 과정 중 확보)</dd>
  <dt>이론</dt><dd>전문교육기관 이론교육 수료 시 학과시험 면제</dd>
</dl>
<p class="note">세부 기준은 한국교통안전공단 공지에 따라 바뀔 수 있습니다. 상담 시 최신 기준으로 안내해 드립니다.</p>''') +
sec('faq', 'FAQ', '자주 묻는 질문', '<div class="faq">' + ''.join('<details><summary>%s</summary><p>%s</p></details>' % qa for qa in FAQ) + '</div>') )

PAGES['contact.html'] = ('수강상담', page_hero('contact.html', '수강상담', '전화 한 통이면 맞는 과정과 일정을 안내해 드립니다.') +
sec('consult', 'Consult', '수강 상담', '''<div class="contact">
  <div>
    <p style="margin:0;color:var(--ink-soft)">대표전화</p>
    <a class="phone" href="tel:%s">%s</a>
    <dl class="info">
      <dt>상담 시간</dt><dd>%s</dd>
      <dt>이메일</dt><dd>sh-j0814@naver.com</dd>
      <dt>카카오톡</dt><dd>%s</dd>
    </dl>
  </div>
  <div class="mapbox">
    <p>상담 시 아래 내용을 알려주시면 더 빠르게 안내해 드립니다.</p>
    <dl class="spec" style="margin:0">
      <dt>희망 자격</dt><dd>1종 · 2종 · 3종 · 잘 모르겠음</dd>
      <dt>희망 시기</dt><dd>시작 희망 월 (평일반 운영)</dd>
      <dt>활용 목적</dt><dd>취업, 방제, 촬영, 업무 등</dd>
    </dl>
  </div>
</div>''' % (PHONE, PHONE, '09:00 ~ 18:00', '<a href="' + KAKAO + '" target="_blank" rel="noopener">(주)에이스드론 채널 열기 →</a>'), first=True) +
sec('map', 'Location', '오시는 길', '''<div class="contact">
  <dl class="info">
    <dt>이론교육장</dt><dd>%s</dd>
    <dt>비행실습장</dt><dd>%s</dd>
    <dt>대중교통</dt><dd>%s</dd>
    <dt>주차</dt><dd>%s</dd>
  </dl>
  <div class="mapbox">
    <p>이론교육은 사당, 실기교육은 남양주 실습비행장에서 진행합니다. 두 곳 모두 주차할 수 있습니다.</p>
    <div class="maplinks"><a class="btn" href="https://map.naver.com/p/search/%%EC%%84%%9C%%EC%%9A%%B8%%20%%EB%%8F%%99%%EC%%9E%%91%%EA%%B5%%AC%%20%%EC%%82%%AC%%EB%%8B%%B9%%EB%%A1%%9C30%%EA%%B8%%B8%%2091" target="_blank" rel="noopener">사당 이론교육장 지도</a><a class="btn ghost" href="https://map.naver.com/p/search/%%EA%%B2%%BD%%EA%%B8%%B0%%EB%%8F%%84%%20%%EB%%82%%A8%%EC%%96%%91%%EC%%A3%%BC%%EC%%8B%%9C%%20%%EC%%A7%%84%%EA%%B1%%B4%%EC%%9D%%8D%%20%%EC%%86%%A1%%EB%%8A%%A5%%EB%%A6%%AC%%20488-2" target="_blank" rel="noopener">남양주 실습비행장 지도</a></div>
  </div>
</div>''' % (ADDR, FIELD, '사당역, 이수역 (이론교육장)', '사당 이론교육장, 남양주 실습비행장 모두 가능')))

DOMAIN = 'https://www.xn--hy1bs0eh1l1id9rc.com'  # 보안서버(SSL) 적용 후 https 로 변경   # www.에이스드론.com
ORG_ID = DOMAIN + '/#org'

# 연락처·주소가 확정되면 채워 넣으세요. 비어 있으면 구조화 데이터에서 빠집니다.
ORG_PHONE = '+82-2-523-3001'          # 예: '+82-31-000-0000'
ORG_ADDRESS = {'addressRegion':'서울특별시','addressLocality':'동작구','streetAddress':'사당로30길 91, 2층'}        # 예: {'addressRegion':'경기도','addressLocality':'○○시','streetAddress':'○○로 00'}
ORG_GEO = {}            # 예: {'latitude':37.0,'longitude':127.0}
ORG_SAMEAS = [KAKAO]         # 네이버 플레이스, 블로그, 유튜브, 인스타그램 주소

DESC = {
    'index.html': '서울 동작구 사당동의 ㈜에이스드론은 국토교통부 지정 드론 전문교육기관으로 무인멀티콥터 1·2·3종 조종자 자격 교육을 운영합니다. 2023 한국교통안전공단 드론 우수 전문교육기관 선정.',
    'about.html': '2023 한국교통안전공단 드론 우수 전문교육기관 에이스드론 소개. 서울 사당 이론교육장과 남양주 실습비행장 시설 안내.',
    'courses.html': '서울 동작구 에이스드론 무인멀티콥터 조종자 자격 과정. 1종 15일 180만원, 2종 10일 150만원, 3종 6일 100만원.',
    'license.html': '드론 자격증(무인멀티콥터 조종자) 취득 절차, 응시 자격, 자주 묻는 질문을 에이스드론이 정리했습니다.',
    'gallery.html': '에이스드론 현장 소식. 한국교통안전공단 우수기관 선정 언론 보도, 학교·기관 드론 교육 출강과 행사, 기수별 수료생, 사당 이론교육장과 남양주 실습비행장 사진.',
    'contact.html': '에이스드론 수강 상담 02-523-3001 (09:00~18:00). 이론교육장 서울 동작구 사당로30길 91 2층(사당역·이수역), 실습비행장 경기도 남양주시 진건읍 송능리 488-2.',
}

import json
def org():
    o = {'@type': ['EducationalOrganization', 'LocalBusiness'], '@id': ORG_ID, 'founder': {'@type': 'Person', 'name': '조윤형'}, 'taxID': '870-86-00820',
         'name': '㈜에이스드론', 'alternateName': ['에이스드론', '에이스드론 교육원', '에이스드론 드론교육원', 'ACE DRONE', 'Ace Drone'],
         'url': DOMAIN + '/', 'email': 'sh-j0814@naver.com',
         'description': DESC['index.html'],
         'award': '2023년 한국교통안전공단 드론 우수 전문교육기관',
         'knowsAbout': ['드론 자격증', '무인멀티콥터 조종자 자격', '초경량비행장치 조종자', '드론 전문교육기관', '드론 실기시험'],
         'areaServed': 'KR', 'image': DOMAIN + '/images/office.jpg', 'logo': DOMAIN + '/images/logo.png',
         'location': [{'@type': 'Place', 'name': '에이스드론 이론교육장', 'address': {'@type': 'PostalAddress', 'addressCountry': 'KR', 'addressRegion': '서울특별시', 'addressLocality': '동작구', 'streetAddress': '사당로30길 91, 2층'}},
                      {'@type': 'Place', 'name': '에이스드론 실습비행장', 'address': {'@type': 'PostalAddress', 'addressCountry': 'KR', 'addressRegion': '경기도', 'addressLocality': '남양주시', 'streetAddress': '진건읍 송능리 488-2'}}],
         'amenityFeature': [{'@type': 'LocationFeatureSpecification', 'name': '주차 가능', 'value': True}]}
    if ORG_PHONE: o['telephone'] = ORG_PHONE
    if ORG_ADDRESS: o['address'] = dict({'@type': 'PostalAddress', 'addressCountry': 'KR'}, **ORG_ADDRESS)
    if ORG_GEO: o['geo'] = dict({'@type': 'GeoCoordinates'}, **ORG_GEO)
    if ORG_SAMEAS: o['sameAs'] = ORG_SAMEAS
    return o

FEES = {'1종': (15, 1800000), '2종': (10, 1500000), '3종': (6, 1000000)}
COURSES = [('1종', '최대이륙중량 25kg 초과, 자체중량 150kg 이하 무인멀티콥터', '20시간'),
           ('2종', '최대이륙중량 7kg 초과 25kg 이하 무인멀티콥터', '10시간'),
           ('3종', '최대이륙중량 2kg 초과 7kg 이하 무인멀티콥터', '6시간')]

def structured(name, title):
    import re
    graph = [org()]
    if name == 'index.html':
        graph.append({'@type': 'WebSite', '@id': DOMAIN + '/#site', 'url': DOMAIN + '/', 'name': '에이스드론', 'inLanguage': 'ko-KR', 'publisher': {'@id': ORG_ID}})
    else:
        graph.append({'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': '에이스드론', 'item': DOMAIN + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': title, 'item': DOMAIN + '/' + name}]})
    if name in ('courses.html', 'index.html'):
        for g, d, h in COURSES:
            graph.append({'@type': 'Course', 'name': '무인멀티콥터 %s 조종자 자격 과정' % g,
                          'description': '%s 조종자 국가자격 취득 과정. 필수 비행경력 %s.' % (d, h),
                          'provider': {'@id': ORG_ID}, 'inLanguage': 'ko-KR',
                          'educationalCredentialAwarded': '무인멀티콥터 %s 조종자 자격 (한국교통안전공단 발급)' % g,
                          'url': DOMAIN + '/courses.html#grade' + g[0],
                          'offers': {'@type': 'Offer', 'price': FEES[g][1], 'priceCurrency': 'KRW', 'category': '수강료'},
                          'timeRequired': 'P%sD' % FEES[g][0]})
    if name == 'license.html':
        qa = [(q, re.sub('<[^>]+>', '', a)) for q, a in FAQ if 'todo' not in a]
        graph.append({'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in qa]})
    return '<script type="application/ld+json">' + json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False) + '</script>'

def seo_head(name, title):
    url = DOMAIN + '/' + ('' if name == 'index.html' else name)
    d = DESC[name]
    return '''<meta name="description" content="%s">
<link rel="canonical" href="%s">
<meta property="og:type" content="website">
<meta property="og:site_name" content="에이스드론">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:url" content="%s">
<meta property="og:locale" content="ko_KR">
<meta name="robots" content="index, follow">
%s
''' % (d, url, title, d, url, structured(name, title))

HEAD = '''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;800;900&display=swap">
<link rel="stylesheet" href="style.css">'''

def full_doc(title, body, extra=''):
    return '<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n<title>%s</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n%s%s\n</head>\n<body>\n%s\n</body>\n</html>\n' % (title, extra, HEAD, body)

def write_crawl_files():
    import datetime
    today = datetime.date.today().isoformat()
    bots = ['Googlebot', 'Google-Extended', 'Yeti', 'Bingbot', 'GPTBot', 'OAI-SearchBot', 'ChatGPT-User',
            'ClaudeBot', 'Claude-SearchBot', 'Claude-User', 'PerplexityBot', 'Perplexity-User', 'Applebot', 'Applebot-Extended']
    robots = '# 검색엔진과 AI 서비스가 모든 페이지를 읽을 수 있도록 허용\n'
    robots += ''.join('User-agent: %s\nAllow: /\n\n' % b for b in bots)
    robots += 'User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n' % DOMAIN
    open(os.path.join(OUT_SITE, 'robots.txt'), 'w', encoding='utf-8').write(robots)
    urls = ''.join('<url><loc>%s/%s</loc><lastmod>%s</lastmod></url>\n' % (DOMAIN, '' if n == 'index.html' else n, today) for n in PAGES)
    open(os.path.join(OUT_SITE, 'sitemap.xml'), 'w', encoding='utf-8').write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + '</urlset>\n')
    import re
    faq = ''.join('- %s %s\n' % (q, re.sub('<[^>]+>', '', a)) for q, a in FAQ if 'todo' not in a)
    llms = """# 에이스드론 (ACE DRONE)

> ㈜에이스드론은 국토교통부 지정 드론(초경량비행장치) 전문교육기관으로, 무인멀티콥터 1·2·3종 조종자 국가자격 취득 교육을 운영합니다. 2023년 한국교통안전공단 드론 우수 전문교육기관(전국 3곳) 중 한 곳으로 선정되었습니다.

## 기본 정보
- 기관명: ㈜에이스드론 (에이스드론 교육원, ACE DRONE)
- 홈페이지: %s/
- 이메일: sh-j0814@naver.com
- 대표전화: 02-523-3001
- 주소(이론교육장): 서울특별시 동작구 사당로30길 91, 2층
- 실습비행장: 경기도 남양주시 진건읍 송능리 488-2
- 상담 시간: 09:00~18:00 / 카카오톡 채널: (주)에이스드론 https://pf.kakao.com/_qxjSxaK
- 가까운 역: 사당역, 이수역 (이론교육장) / 주차: 두 곳 모두 가능
- 실적: 누적 수료생 약 1,200명, 실기시험 합격률 100%%
- 대표: 조윤형 / 사업자등록번호: 870-86-00820

## 교육과정
- 무인멀티콥터 1종 (가장 인기): 최대이륙중량 25kg 초과, 자체중량 150kg 이하 / 비행경력 20시간 / 교육 15일, 수강료 180만원
- 무인멀티콥터 2종: 7kg 초과 25kg 이하 / 비행경력 10시간 / 교육 10일, 수강료 150만원
- 무인멀티콥터 3종: 2kg 초과 7kg 이하 / 비행경력 6시간 / 교육 6일, 수강료 100만원

## 페이지
- [교육원 소개](%s/about.html): 인사말, 우수기관 선정, 시설
- [교육과정](%s/courses.html): 1·2·3종 과정 상세
- [자격취득 안내](%s/license.html): 취득 절차, 응시 자격, 자주 묻는 질문
- [현장 소식](%s/gallery.html): 언론 보도, 교육·행사, 수료생, 교육장 사진
- [수강상담](%s/contact.html): 상담 전화, 오시는 길

## 자주 묻는 질문
%s""" % (DOMAIN, DOMAIN, DOMAIN, DOMAIN, DOMAIN, DOMAIN, faq)
    open(os.path.join(OUT_SITE, 'llms.txt'), 'w', encoding='utf-8').write(llms)

def main():
    css = open(os.path.join(ROOT, 'theme.css'), encoding='utf-8').read()
    for out in [o for o in (OUT_SITE, OUT_ART) if o]:
        shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
        open(os.path.join(out, 'style.css'), 'w', encoding='utf-8').write(css)
        shutil.copy(os.path.join(ROOT, 'site.js'), out)
        shutil.copytree(os.path.join(ROOT, 'images'), os.path.join(out, 'images'))
    for name, (title, body) in PAGES.items():
        full_title = title if name == 'index.html' else title + ' | 에이스드론'
        html_body = header(name) + '\n<main>' + body + '</main>\n' + footer()
        seo = seo_head(name, full_title)
        open(os.path.join(OUT_SITE, name), 'w', encoding='utf-8').write(full_doc(full_title, html_body, seo))
        if name == 'index.html':
            art = '<title>%s</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n%s%s\n%s\n' % (full_title, seo, HEAD, html_body)
        else:
            art = full_doc(full_title, html_body, seo)
        art = art.replace('id="gdata"', 'id="gdata" data-preview="1"')
        if OUT_ART: open(os.path.join(OUT_ART, name), 'w', encoding='utf-8').write(art)
    write_crawl_files()
    open(os.path.join(OUT_SITE, '.nojekyll'), 'w').close()
    # GitHub Pages 연결 도메인 (www.에이스드론.com)
    open(os.path.join(OUT_SITE, 'CNAME'), 'w').write('www.xn--hy1bs0eh1l1id9rc.com\n')
    print('ok', sorted(os.listdir(OUT_SITE)))

main()
