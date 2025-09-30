# 🌳 BT XML Diff Tool 사용 가이드

gaemi_task Git 브랜치간 BehaviorTree XML 파일 변경사항을 분석하고 시각화하는 도구입니다.

## 🚀 빠른 시작

### Git 브랜치 비교
```bash
# gaemi_task 레포지토리에서 두 브랜치 간의 BehaviorTree 변경사항 분석
cd /path/to/gaemi_task
/path/to/bt_xml_diff_tool/run_analysis.sh <소스_브랜치> <타겟_브랜치>

# 예시
cd /home/khj/colcon_ws/src/gaemi_task  
/home/khj/colcon_ws/src/bt_xml_diff_tool/run_analysis.sh main hotfix-speedgate-delay

# 또는 bt_xml_diff_tool에서 실행
cd /home/khj/colcon_ws/src/bt_xml_diff_tool
./run_analysis.sh main feature-branch --repo-path ../gaemi_task

# 예시
python3 enhanced_branch_analyzer.py files old_tree.xml new_tree.xml
python3 enhanced_branch_analyzer.py files test_tree_v1.xml test_tree_v2.xml

# 출력 파일명 지정
python3 enhanced_branch_analyzer.py files old.xml new.xml -o my_comparison.html
```

### 3. Git 브랜치 비교 (Python 직접 실행)
```bash
# Python으로 브랜치 직접 비교
python3 enhanced_branch_analyzer.py branches main feature-branch
python3 enhanced_branch_analyzer.py branches develop hotfix-branch

# 또는 레거시 방식 (하위 호환성)
python3 enhanced_branch_analyzer.py main feature-branch
```

## 📁 필요한 파일들
```
bt_xml_diff_tool/
├── enhanced_branch_analyzer.py    # 메인 분석 엔진 ⭐️ 파일 비교 기능 추가!
├── bt_tree_parser.py              # XML 파싱
├── bt_tree_comparator.py          # 구조 비교
├── tree_visualizer_enhanced.py    # D3.js 시각화
├── run_analysis.sh               # 원클릭 실행 스크립트
├── start_server.sh              # HTTP 서버 관리
└── setup.sh                     # 의존성 확인
```

## 🔧 설정 및 실행

### 의존성 확인
```bash
./setup.sh
```

### 사용 방법 확인
```bash
# 전체 도움말
python3 enhanced_branch_analyzer.py --help

# 파일 비교 도움말
python3 enhanced_branch_analyzer.py files --help

# 브랜치 비교 도움말
python3 enhanced_branch_analyzer.py branches --help
```

### XML 파일 직접 비교 실행
```bash
# 기본 실행 (bt_file_comparison.html 생성)
python3 enhanced_branch_analyzer.py files old_tree.xml new_tree.xml

# 커스텀 출력 파일
python3 enhanced_branch_analyzer.py files tree_v1.xml tree_v2.xml -o result.html

# 자동으로 브라우저에서 결과 파일이 열립니다!
```

### 브랜치 비교 실행
```bash
# 기본 포트 8080으로 실행
./run_analysis.sh main feature-branch

# 커스텀 포트로 실행
./run_analysis.sh main feature-branch --port 8090

# Python으로 직접 실행
python3 enhanced_branch_analyzer.py branches main feature-branch
```

### 실행 과정
1. 🔍 파일/Git diff 분석
2. 📊 BehaviorTree 구조 파싱
3. 🎨 D3.js 시각화 생성
4. 🌐 HTML 파일 생성
5. 🖥️ 브라우저 자동 열기

## 📊 결과 확인

### 웹 브라우저에서 확인
- **파일 비교**: `bt_file_comparison.html` 생성
- **브랜치 비교**: `bt_diff_result.html` 생성
- 인터랙티브 트리 시각화 제공
- 변경사항이 색상으로 표시됩니다:
  - 🟢 **녹색**: 추가된 노드
  - 🔴 **빨간색**: 삭제된 노드
  - 🟡 **노란색**: 수정된 노드

### 변경 유형
- **Added Nodes**: 새로 추가된 액션/조건
- **Removed Nodes**: 삭제된 액션/조건
- **Modified Nodes**: 속성이 변경된 노드
- **SubTree Changes**: 서브트리 변경사항

## 🛠️ 트러블슈팅

### XML 파일 문제
```bash
# 파일 존재 확인
ls -la *.xml

# XML 형식 검증
xmllint --format your_file.xml
```

### Git 오류 (브랜치 비교 시)
```bash
# 브랜치가 존재하지 않을 때
git branch -a  # 사용 가능한 브랜치 확인

# 원격 브랜치 가져오기
git fetch origin
```

### 포트 충돌 (브랜치 비교 시)
```bash
# 다른 포트 사용
./run_analysis.sh main feature-branch --port 8090
```

### 브라우저가 자동으로 열리지 않을 때
```bash
# 수동으로 브라우저에서 열기
xdg-open bt_file_comparison.html        # 파일 비교 결과
xdg-open bt_diff_result.html           # 브랜치 비교 결과
```

## 📋 사용 예시

### 예시 1: XML 파일 비교 ⭐️
```bash
# 테스트 파일들 비교
python3 enhanced_branch_analyzer.py files test_tree_v1.xml test_tree_v2.xml

# 결과: bt_file_comparison.html 생성됨
# 🌳 WaitAction의 wait_time 변경 (2.0 → 3.0)과 NavigateAction 추가 감지
```

### 예시 2: 기본 브랜치 비교
```bash
./run_analysis.sh main develop
```

### 예시 3: 피처 브랜치 확인
```bash
./run_analysis.sh develop feature-new-behavior
```

### 예시 4: 핫픽스 검증
```bash
./run_analysis.sh main hotfix-urgent-fix
```

## 🎯 주요 기능

- ✅ **XML 파일 직접 비교** ⭐️ NEW!
- ✅ **Git 브랜치 자동 비교**
- ✅ **구조적 변경 감지**
- ✅ **인터랙티브 시각화**
- ✅ **SubTree 변경 추적**
- ✅ **브라우저 자동 실행**
- ✅ **원클릭 분석**
- ✅ **유연한 사용 모드**

## 📝 출력 파일

### 파일 비교 결과
- `bt_file_comparison.html`: XML 파일 비교 결과
- 파일 경로와 변경사항 요약 포함
- 인터랙티브 트리 뷰어

### 브랜치 비교 결과
- `bt_diff_result.html`: Git 브랜치 비교 결과
- HTTP 서버를 통한 고급 기능 제공
- 줌/팬 기능 지원
- 변경사항 하이라이팅

---

## 🚨 중요 사항

### 파일 비교 모드
1. **XML 형식**: BehaviorTree.CPP 호환 XML 형식만 지원
2. **파일 존재**: 두 파일이 모두 존재해야 함
3. **상대경로/절대경로**: 둘 다 지원

### 브랜치 비교 모드
1. **Git Repository**: Git repository 안에서 실행해야 합니다
2. **브랜치 존재**: 비교할 브랜치들이 모두 존재해야 합니다
3. **포트 확인**: 기본 포트 8080이 사용 중이면 다른 포트를 사용하세요

---

## 🆕 새로운 기능

### v2.0 업데이트 내용
- ✨ **XML 파일 직접 비교** 기능 추가
- 🔧 **모듈화된 명령어 구조** (files/branches 서브커맨드)
- 🔄 **하위 호환성** 유지 (기존 명령어 계속 지원)
- 🎨 **향상된 시각화** (파일 경로 정보 포함)
- 🚀 **자동 브라우저 실행**

---

**💡 팁**: 
- XML 파일을 빠르게 비교하려면 `files` 모드를 사용하세요!
- Git 브랜치 간 복잡한 변경사항은 `branches` 모드나 `run_analysis.sh`를 사용하세요!
- 변경사항이 많을 때는 브라우저에서 줌 기능을 사용하여 세부사항을 확인하세요!