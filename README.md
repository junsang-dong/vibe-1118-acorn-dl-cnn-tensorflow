# CNN 기반 이미지 분석 웹앱

TensorFlow를 활용한 CNN 기반 이미지 분류 웹앱입니다. CIFAR-10 데이터셋으로 학습된 모델을 사용하여 업로드된 이미지를 분석하고 예측 결과를 시각화합니다.

## 🌐 라이브 데모

**[https://vibe-1118-acorn-dl-cnn-tensorflow-production.up.railway.app/](https://vibe-1118-acorn-dl-cnn-tensorflow-production.up.railway.app/)**

Railway에 배포된 웹앱으로, 위 링크에서 바로 이미지 분석을 체험할 수 있습니다.

## 🚀 주요 기능

- **이미지 업로드**: 드래그 앤 드롭 또는 클릭으로 이미지 업로드
- **실시간 분석**: CNN 모델을 통한 실시간 이미지 분류
- **시각적 결과**: 예측 라벨, 확률(%), 이미지 설명 제공
- **반응형 UI**: 모바일과 데스크톱에서 모두 사용 가능
- **사용자 친화적**: 직관적인 인터페이스와 애니메이션

## 📊 지원 클래스

CIFAR-10 데이터셋의 10개 클래스를 지원합니다:

1. **airplane** - 비행기
2. **automobile** - 자동차
3. **bird** - 새
4. **cat** - 고양이
5. **deer** - 사슴
6. **dog** - 개
7. **frog** - 개구리
8. **horse** - 말
9. **ship** - 배
10. **truck** - 트럭

## 🛠️ 기술 스택

### 백엔드
- **Python 3.11.14** (배포 호환성)
- **TensorFlow 2.15.0** - 딥러닝 프레임워크
- **Flask 3.0.0** - 웹 프레임워크
- **OpenCV** - 이미지 처리
- **Pillow** - 이미지 조작
- **NumPy** - 수치 계산

### 프론트엔드
- **HTML5** - 마크업
- **CSS3** - 스타일링 (그라디언트, 애니메이션)
- **JavaScript (ES6+)** - 동적 기능
- **반응형 디자인** - 모바일 최적화

## 📁 프로젝트 구조

```
vibe-1118-acorn-dl-cnn-tensorflow/
├── app.py                 # Flask 웹앱 메인 파일
├── Procfile               # Railway/Render 배포용
├── render.yaml            # Render Blueprint 설정
├── runtime.txt            # Python 버전 (Railway)
├── .python-version        # Python 3.11.14 (mise/Railway)
├── .tool-versions         # Python 버전 (mise)
├── train_model.py         # CNN 모델 학습 코드
├── quick_train.py         # 빠른 모델 학습 (샘플 데이터)
├── requirements.txt       # Python 패키지 의존성
├── README.md             # 프로젝트 문서
├── models/               # 학습된 모델 저장소
│   ├── cifar10_classifier.h5  # 학습된 CNN 모델
│   └── class_names.json       # 클래스 이름 매핑
├── templates/            # HTML 템플릿
│   └── index.html        # 메인 페이지
├── static/               # 정적 파일
│   ├── style.css         # CSS 스타일
│   └── script.js         # JavaScript 코드
└── data/                 # 데이터 저장소
```

## 🚀 설치 및 실행

### 1. 저장소 클론
```bash
git clone <repository-url>
cd vibe-1118-acorn-dl-cnn-tensorflow
```

### 2. 가상환경 생성 및 활성화
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

### 4. 모델 학습 (선택사항)
```bash
# 빠른 학습 (샘플 데이터)
python3 quick_train.py

# 또는 전체 CIFAR-10 데이터셋으로 학습
python3 train_model.py
```

### 5. 웹앱 실행
```bash
python3 app.py
```

### 6. 브라우저에서 접속
```
http://localhost:5151
```

## ☁️ 배포 (Railway / Render)

이 프로젝트는 **Railway** 또는 **Render**에 바로 배포할 수 있습니다.

### Railway 배포

1. [railway.app](https://railway.app) 접속 후 GitHub 로그인
2. **New Project** → **Deploy from GitHub repo** 선택
3. `junsang-dong/vibe-1118-acorn-dl-cnn-tensorflow` 저장소 선택
4. Railway가 자동으로 `Procfile`과 `requirements.txt`를 인식
5. 배포 완료 후 **Settings** → **Networking** → **Generate Domain**으로 공개 URL 생성
6. 생성된 `*.up.railway.app` URL로 접속

### Render 배포

1. [render.com](https://render.com) 접속 후 GitHub 로그인
2. **New** → **Web Service** 선택
3. 저장소 연결: `junsang-dong/vibe-1118-acorn-dl-cnn-tensorflow`
4. 설정 (자동 감지 또는 수동):
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --workers 1 --timeout 120 --bind 0.0.0.0:$PORT app:app`
5. **Create Web Service** 클릭

> ⚠️ **참고**: TensorFlow 설치로 인해 첫 빌드에 5~10분 정도 소요될 수 있습니다.

**배포 전 확인사항**
- `models/cifar10_classifier.h5`와 `models/class_names.json`이 GitHub에 커밋되어 있어야 합니다.

**Railway 배포 시 참고**
- Python 3.11.14 사용 (TensorFlow 2.15 호환, mise precompiled 바이너리 지원)
- Trial 플랜에서는 **Generate Domain**을 눌러야 공개 URL이 생성됩니다.

## 📖 사용 방법

1. **이미지 업로드**
   - 웹페이지의 업로드 영역에 이미지를 드래그 앤 드롭
   - 또는 "파일 선택" 버튼을 클릭하여 이미지 선택

2. **이미지 분석**
   - 업로드된 이미지 미리보기 확인
   - "🔍 이미지 분석하기" 버튼 클릭

3. **결과 확인**
   - 예측된 클래스명 확인
   - 신뢰도 퍼센트 확인
   - 이미지에 대한 상세 설명 읽기

## 🔧 API 엔드포인트

### POST /predict
이미지 파일을 업로드하여 예측 결과를 받습니다.

**요청:**
- Content-Type: multipart/form-data
- 파일: image (이미지 파일)

**응답:**
```json
{
  "success": true,
  "predicted_class": "cat",
  "confidence": 85.3,
  "description": "이 이미지는 고양이로 보입니다..."
}
```

### GET /health
서버 상태를 확인합니다.

**응답:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "classes_loaded": true
}
```

## 🎨 UI/UX 특징

- **그라디언트 디자인**: 현대적이고 세련된 UI
- **드래그 앤 드롭**: 직관적인 파일 업로드
- **실시간 피드백**: 로딩 상태와 진행률 표시
- **애니메이션**: 부드러운 전환 효과
- **반응형**: 모든 디바이스에서 최적화된 경험
- **접근성**: 키보드 단축키 지원

## 🔍 모델 아키텍처

CNN 모델은 다음과 같은 구조를 가집니다:

```
Conv2D(32, 3x3) + ReLU
MaxPooling2D(2x2)
Conv2D(64, 3x3) + ReLU
MaxPooling2D(2x2)
Conv2D(64, 3x3) + ReLU
Flatten
Dense(64) + ReLU
Dense(10)  # 출력층
```

- **총 파라미터**: 122,570개
- **입력 크기**: 32x32x3 (RGB 이미지)
- **출력**: 10개 클래스에 대한 확률 분포

## 🚨 주의사항

- **이미지 크기**: 자동으로 32x32로 리사이즈됩니다
- **파일 형식**: JPG, PNG, GIF 등 일반적인 이미지 형식 지원
- **파일 크기**: 최대 10MB까지 업로드 가능
- **모델 정확도**: CIFAR-10 데이터셋 기준 약 70% 정확도

## 🛠️ 개발 및 커스터마이징

### 모델 재학습
```python
# train_model.py 수정하여 하이퍼파라미터 조정
class CIFAR10ImageClassifier:
    def __init__(self, img_size=(32, 32), num_classes=10):
        # 모델 구조 수정 가능
```

### UI 커스터마이징
- `static/style.css`: 스타일 수정
- `static/script.js`: JavaScript 기능 추가
- `templates/index.html`: HTML 구조 수정

### 새로운 클래스 추가
1. `models/class_names.json`에 클래스 추가
2. 모델 재학습 또는 전이학습 수행
3. `app.py`의 `generate_image_description()` 함수 수정

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 문의

프로젝트에 대한 문의사항이 있으시면 이슈를 생성해주세요.

---

**개발자**: AI Assistant  
**프레임워크**: TensorFlow 2.15.0 + Flask 3.0.0  
**데이터셋**: CIFAR-10  
**버전**: 1.0.0
