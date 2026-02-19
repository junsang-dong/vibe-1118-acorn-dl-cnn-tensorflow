from flask import Flask, request, render_template, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image
import json
import os
from io import BytesIO

app = Flask(__name__)

# 프로젝트 루트 경로 (배포 환경 대응)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 모델과 클래스 이름 로드
model = None
class_names = None

def load_model():
    """모델과 클래스 이름 로드"""
    global model, class_names
    
    try:
        # 모델 로드 (배포 시 경로 안정화)
        model_path = os.path.join(BASE_DIR, 'models', 'cifar10_classifier.h5')
        class_names_path = os.path.join(BASE_DIR, 'models', 'class_names.json')
        model = tf.keras.models.load_model(model_path)
        print("모델이 성공적으로 로드되었습니다.")
        
        # 클래스 이름 로드
        with open(class_names_path, 'r') as f:
            class_names = json.load(f)
        print(f"클래스 이름이 로드되었습니다: {class_names}")
        
    except Exception as e:
        print(f"모델 로드 중 오류 발생: {e}")
        model = None
        class_names = None

def preprocess_image(image):
    """이미지 전처리"""
    try:
        # 이미지를 32x32로 리사이즈
        image = image.resize((32, 32))
        
        # PIL 이미지를 numpy 배열로 변환
        image_array = np.array(image)
        
        # RGB로 변환 (RGBA인 경우)
        if image_array.shape[2] == 4:
            image_array = image_array[:, :, :3]
        
        # 정규화 (0-1 범위)
        image_array = image_array.astype(np.float32) / 255.0
        
        # 배치 차원 추가
        image_array = np.expand_dims(image_array, axis=0)
        
        return image_array
    except Exception as e:
        print(f"이미지 전처리 중 오류 발생: {e}")
        return None

def predict_image(image_array):
    """이미지 예측"""
    try:
        if model is None:
            return None, None
        
        # 예측 수행
        predictions = model.predict(image_array)
        
        # 소프트맥스 적용
        probabilities = tf.nn.softmax(predictions[0])
        
        # 가장 높은 확률의 클래스 찾기
        predicted_class_idx = np.argmax(probabilities)
        confidence = float(probabilities[predicted_class_idx])
        
        return predicted_class_idx, confidence
        
    except Exception as e:
        print(f"예측 중 오류 발생: {e}")
        return None, None

@app.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """이미지 예측 API"""
    try:
        # 이미지 파일 받기
        if 'image' not in request.files:
            return jsonify({'error': '이미지 파일이 없습니다.'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': '파일이 선택되지 않았습니다.'}), 400
        
        # 이미지 읽기
        image = Image.open(file.stream)
        
        # 이미지 전처리
        image_array = preprocess_image(image)
        if image_array is None:
            return jsonify({'error': '이미지 전처리 중 오류가 발생했습니다.'}), 400
        
        # 예측 수행
        predicted_class_idx, confidence = predict_image(image_array)
        if predicted_class_idx is None:
            return jsonify({'error': '예측 중 오류가 발생했습니다.'}), 400
        
        # 결과 반환
        predicted_class = class_names[predicted_class_idx] if class_names else f"Class {predicted_class_idx}"
        confidence_percent = confidence * 100
        
        # 이미지 설명 생성
        description = generate_image_description(predicted_class, confidence_percent)
        
        return jsonify({
            'predicted_class': predicted_class,
            'confidence': confidence_percent,
            'description': description,
            'success': True
        })
        
    except Exception as e:
        print(f"예측 API 오류: {e}")
        return jsonify({'error': f'서버 오류: {str(e)}'}), 500

def generate_image_description(predicted_class, confidence):
    """이미지 설명 생성"""
    descriptions = {
        'airplane': '이 이미지는 비행기로 보입니다. 하늘을 나는 항공기나 제트기의 모습을 담고 있을 가능성이 높습니다.',
        'automobile': '이 이미지는 자동차로 보입니다. 도로를 달리는 승용차나 트럭의 모습을 담고 있을 가능성이 높습니다.',
        'bird': '이 이미지는 새로 보입니다. 하늘을 나는 새나 나무에 앉은 새의 모습을 담고 있을 가능성이 높습니다.',
        'cat': '이 이미지는 고양이로 보입니다. 귀여운 고양이나 야생 고양이의 모습을 담고 있을 가능성이 높습니다.',
        'deer': '이 이미지는 사슴으로 보입니다. 숲이나 들판에 있는 사슴의 모습을 담고 있을 가능성이 높습니다.',
        'dog': '이 이미지는 개로 보입니다. 귀여운 강아지나 성견의 모습을 담고 있을 가능성이 높습니다.',
        'frog': '이 이미지는 개구리로 보입니다. 연못이나 습지에 있는 개구리의 모습을 담고 있을 가능성이 높습니다.',
        'horse': '이 이미지는 말로 보입니다. 목장이나 들판에 있는 말의 모습을 담고 있을 가능성이 높습니다.',
        'ship': '이 이미지는 배로 보입니다. 바다나 강을 항해하는 선박의 모습을 담고 있을 가능성이 높습니다.',
        'truck': '이 이미지는 트럭으로 보입니다. 도로를 달리는 화물차나 대형 트럭의 모습을 담고 있을 가능성이 높습니다.'
    }
    
    base_description = descriptions.get(predicted_class, f'이 이미지는 {predicted_class}로 보입니다.')
    
    if confidence > 80:
        confidence_text = "매우 높은"
    elif confidence > 60:
        confidence_text = "높은"
    elif confidence > 40:
        confidence_text = "보통"
    else:
        confidence_text = "낮은"
    
    return f"{base_description} 예측 신뢰도는 {confidence_text} 수준입니다."

@app.route('/health')
def health():
    """헬스 체크"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'classes_loaded': class_names is not None
    })

# gunicorn 등 프로덕션 서버에서도 모델 로드
load_model()

if __name__ == '__main__':
    # 로컬 개발용: PORT 환경변수 지원 (Railway, Render 등)
    port = int(os.environ.get('PORT', 5151))
    app.run(debug=True, host='0.0.0.0', port=port)
