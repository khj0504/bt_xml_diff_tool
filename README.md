# 🌳 BehaviorTree XML Diff Tool

**강력한 BehaviorTree XML 구조 비교 및 시각화 도구**

## 📋 개요

BehaviorTree XML 파일의 구조적 차이점을 분석하고 시각화하는 종합적인 도구입니다.

- Git 브랜치 간 BehaviorTree XML 파일 변경사항 분석 
- 직접 XML 파일 비교 ⭐️ NEW!
- 인터랙티브한 D3.js 트리 시각화 제공

## ✨ 주요 기능

- 🔍 **Git 브랜치 간 BehaviorTree XML 비교**
- 📁 **XML 파일 직접 비교** ⭐️ NEW!
- 🎯 **정확한 구조적 변경사항 감지** (추가/삭제/수정된 노드)
- 🌲 **인터랙티브 트리 시각화** (D3.js 기반)
- 🎨 **색상 코딩된 변경사항** (빨간색: 삭제, 초록색: 추가, 노란색: 수정)
- 📊 **SubTree 확장 및 분석**
- 🚀 **내장 HTTP 서버**로 즉시 결과 확인
- 🖥️ **자동 브라우저 실행**

## 🚀 빠른 시작

### 설치
```bash
cd /home/khj/colcon_ws/src/bt_xml_diff_tool
./setup.sh
```

### 사용법

#### 1. XML 파일 직접 비교 ⭐️ 추천!
```bash
# 두 XML 파일 비교
python3 enhanced_branch_analyzer.py files old_tree.xml new_tree.xml

# 출력 파일명 지정
python3 enhanced_branch_analyzer.py files tree_v1.xml tree_v2.xml -o my_result.html
```

#### 2. Git 브랜치 비교
```bash
# 자동화된 스크립트 실행 (추천)
./run_analysis.sh main feature-branch

# 또는 Python 직접 실행
python3 enhanced_branch_analyzer.py branches main feature-branch
```

## 🚀 빠른 시작# 브랜치 간 전체 BehaviorTree 분석 (권장)

bt-enhanced-branch develop feature-branch -o 분석결과.html

### 1. 설치 및 설정

# 단일 파일 비교  

```bashbt-diff old.xml new.xml -o comparison.html

# 1. 프로젝트 다운로드

git clone <repository_url> bt_xml_diff_tool# Git 브랜치 기반 파일 비교

cd bt_xml_diff_toolbt-git-diff path/to/file.xml branch1 branch2 -o result.html

```

# 2. 설정 실행 (의존성 확인 및 권한 설정)

./setup.sh## ✨ 주요 기능

```

- 🔍 **자동 BehaviorTree 파일 감지**: Git 브랜치에서 변경된 모든 BT 파일 자동 분석

### 2. 사용법- 🌲 **서브트리 변경사항 하이라이트**: SubTree 노드 변경사항 전용 시각화

- 🎨 **대화형 D3.js 시각화**: 줌/팬 가능한 트리 다이어그램  

#### 🎯 원클릭 분석 (추천)- ⚡ **실시간 애니메이션**: 변경된 노드에 펄스 효과

- 📊 **포괄적 리포트**: HTML 기반 상세 분석 보고서

```bash- 🎛️ **인터랙티브 컨트롤**: 줌, 필터링, 드래그 지원

# 기본 사용법

./run_analysis.sh <source_branch> <target_branch>## 📂 파일 구조



# 예시### 🌟 핵심 파일

./run_analysis.sh develop feature-bt-tree-viz- `enhanced_branch_analyzer.py` - 메인 브랜치 분석 도구

- `bt_tree_parser.py` - BehaviorTree XML 파서

# 고급 옵션- `bt_tree_comparator.py` - 트리 구조 비교

./run_analysis.sh develop feature-branch -o my_analysis.html -p 8090- `git_bt_diff.py` - Git 통합 기능

```- `tree_visualizer_enhanced.py` - D3.js 시각화

- `setup.sh` - 설치 스크립트

실행하면 자동으로:

1. 브랜치 간 변경사항 분석### 📖 문서

2. HTML 결과 생성- `README.md` - 프로젝트 개요

3. HTTP 서버 시작- `USAGE_GUIDE.md` - 상세 사용법 가이드

4. 브라우저에서 `http://localhost:8080/result.html` 접속 가능

## 🎯 사용 예시

#### 🔧 단계별 실행

```bash

```bash# 개발 브랜치와 피처 브랜치 비교

# 1. 분석 실행cd /your/bt/repository

python3 enhanced_branch_analyzer.py <source_branch> <target_branch> -o result.htmlbt-enhanced-branch develop feature-new-navigation -o nav_changes.html



# 2. 서버 시작# 특정 BehaviorTree 파일 브랜치 간 비교

./start_server.sh [port]bt-git-diff behavior_trees/main.xml main feature-branch -o main_tree_diff.html

```

# 3. 브라우저에서 확인

# http://localhost:8080/result.html## 📋 요구사항

```

- Python 3.6+

## 📊 분석 결과 화면- Git (브랜치 분석용)

- 모던 웹 브라우저 (HTML 보고서 확인용)

생성된 HTML 파일에서 다음을 확인할 수 있습니다:

## 📞 지원

### 🎨 색상 코드

- 🔴 **빨간색**: 삭제된 노드자세한 사용법은 `USAGE_GUIDE.md`를 참조하세요.

- 🟢 **초록색**: 추가된 노드  

- 🟡 **노란색**: 수정된 노드---

- 🔵 **파란색**: 이동된 노드*ROBOTIS에서 개발한 BehaviorTree 분석 도구*
- ⚪ **회색**: 변경되지 않은 노드

### 📋 분석 정보
- **변경 통계**: 총 변경 파일 수, 구조적 변경사항 수
- **파일별 상세**: 각 BT 파일의 변경 내역
- **인터랙티브 트리**: 줌, 팬, 툴팁 지원

## 🛠️ 고급 사용법

### 명령행 옵션

```bash
# enhanced_branch_analyzer.py 옵션
python3 enhanced_branch_analyzer.py <source> <target> [options]

Options:
  -o, --output FILE    출력 HTML 파일명 (기본: enhanced_analysis_result.html)
  -h, --help          도움말 표시

# run_analysis.sh 옵션  
./run_analysis.sh <source> <target> [options]

Options:
  -o, --output FILE    출력 HTML 파일명 (기본: bt_diff_result.html)
  -p, --port PORT     HTTP 서버 포트 (기본: 8080)
  -h, --help          도움말 표시
```

### 서버 관리

```bash
# 특정 포트로 서버 시작
./start_server.sh 8090

# 서버 중지
Ctrl+C 또는 터미널에서 kill
```

## 📁 프로젝트 구조

```
bt_xml_diff_tool/
├── enhanced_branch_analyzer.py    # 메인 분석 도구
├── bt_tree_parser.py             # XML 파싱 모듈
├── bt_tree_comparator.py         # 구조 비교 모듈  
├── tree_visualizer_enhanced.py   # 시각화 모듈
├── git_bt_diff.py               # Git 통합 모듈
├── run_analysis.sh              # 원클릭 실행 스크립트
├── start_server.sh              # HTTP 서버 시작 스크립트
├── setup.sh                     # 설치 및 설정 스크립트
├── README.md                    # 이 파일
└── USAGE_GUIDE.md              # 상세 사용 가이드
```

## 🔧 시스템 요구사항

- **Python 3.6+**
- **Git**
- **웹 브라우저** (Chrome, Firefox, Safari 등)

### Python 모듈 (표준 라이브러리)
- `xml.etree.ElementTree`
- `json`, `subprocess`, `pathlib`
- `typing`, `dataclasses`, `enum`

## 🎯 사용 예시

### 예시 1: Feature 브랜치 분석
```bash
./run_analysis.sh main feature-new-bt-structure
```

### 예시 2: 커스텀 출력 파일
```bash
./run_analysis.sh develop hotfix-bt-issue -o hotfix_analysis.html
```

### 예시 3: 다른 포트로 서버 실행
```bash
./run_analysis.sh main feature-branch -p 9000
```

## 🚨 문제 해결

### Git 저장소가 아닌 경우
```
⚠️  Warning: Not in a Git repository
```
**해결책**: Git 저장소 디렉토리 내에서 도구를 실행하세요.

### Python 모듈 누락
```
❌ Missing required Python modules
```
**해결책**: Python 3.6+ 설치 후 `./setup.sh` 재실행

### 포트 사용 중 오류
```
OSError: [Errno 98] Address already in use
```
**해결책**: 다른 포트 사용 또는 기존 프로세스 종료
```bash
pkill -f "python3 -m http.server"
./start_server.sh 8081
```

## 🤝 기여하기

버그 리포트, 기능 요청, 풀 리퀘스트를 환영합니다!

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

---

**Made with ❤️ for BehaviorTree Analysis**