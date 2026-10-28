# ㈜에이스드론 홈페이지

www.에이스드론.com 의 홈페이지 파일입니다.

## 폴더 구성

| 폴더 | 내용 |
|---|---|
| `docs/` | 실제 홈페이지로 보이는 파일 (GitHub Pages 가 이 폴더를 그대로 보여줍니다). 직접 고치지 말고 `src/` 를 고친 뒤 다시 만듭니다. |
| `src/` | 홈페이지를 만드는 원본 |
| `src/build.py` | 페이지 문구·메뉴·연락처·수강료·팝업 설정 |
| `src/albums.json` | 현장 소식(언론 보도, 교육·행사, 수료생, 교육장) 게시물 목록 |
| `src/theme.css` | 색상·글씨체·디자인 |
| `src/images/` | 사진. 메인 슬라이드는 `hero-*.webp`(PC)와 `hero-*-m.webp`(휴대폰) |

## 홈페이지 다시 만들기

```bash
cd src
python3 build.py   # docs/ 폴더가 새로 만들어집니다
```

## 참고

- 현장 소식에서 사진을 크게 볼 때는 아직 예전 카페24 서버(`acedrone.cafe24.com/wp-content/...`)의 원본 사진을 불러옵니다.
  카페24 호스팅을 끝내기 전에 원본 사진을 이 저장소로 옮겨야 합니다 (`src/gallery_part.py` 의 `FULL_BASE`).
- 메인 슬라이드의 하늘·조종사 사진은 Unsplash 무료 사진입니다.
