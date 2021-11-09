# Collector

쇼핑몰 사이트로부터 가격 정보를 파싱하는 모듈입니다. 다나와(danawa)만 지원합니다.

<br><br>

# Installation

## git clone

`git clone` 명령을 사용하여 코드를 다운받을 수 있습니다.

```
$ git clone https://github.com/save-the-computer/collector
$ cd collector
$ python collect.py --help
```

## pip

`pip` 명령을 사용하여 설치할 수 있습니다.

```sh
$ pip install git+git://github.com/save-the-computer/collector
```

## requirements.txt

`requirements.txt` 를 사용한다면 파일의 맨 끝에 한 줄을 추가하세요.

```
Django==3.2.8
djangorestframework==3.12.4
git+git://github.com/save-the-computer/collector
```

<br><br>

# Usage

이 모듈은 명령행 사용을 지원합니다.

```sh
$ python collect.py [--page-limit PAGE_LIMIT] {CPU,그래픽카드,메인보드,RAM}
```

* **--page-limit** : 크롤링 시 최대 페이지 수를 지정합니다. 기본값은 `1` 입니다.
* **{CPU,그래픽카드,메인보드,RAM}** : 크롤링 카테고리를 지정합니다. 하나를 선택할 수 있습니다.

`collect.py` 를 사용하여 크롤링을 하면 결과물이 `outputs/*.json` 에 저장됩니다.
