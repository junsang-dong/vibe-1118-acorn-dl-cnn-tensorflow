import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
import numpy as np
import os
import json

# GPU 메모리 설정
physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)

def create_simple_model():
    """간단한 CNN 모델 생성"""
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dense(10)
    ])
    
    model.compile(
        optimizer='adam',
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=['accuracy']
    )
    
    return model

def generate_sample_data():
    """샘플 데이터 생성"""
    # 간단한 샘플 데이터 생성
    X = np.random.random((100, 32, 32, 3)).astype(np.float32)
    y = np.random.randint(0, 10, (100,)).astype(np.int32)
    return X, y

def main():
    print("간단한 모델 학습 시작...")
    
    # 모델 생성
    model = create_simple_model()
    print("모델 구조:")
    model.summary()
    
    # 샘플 데이터 생성
    X, y = generate_sample_data()
    print(f"샘플 데이터 크기: {X.shape}, {y.shape}")
    
    # 모델 학습 (1 에포크만)
    print("모델 학습 중...")
    model.fit(X, y, epochs=1, verbose=1)
    
    # 모델 저장
    if not os.path.exists('models'):
        os.makedirs('models')
    
    model.save('models/cifar10_classifier.h5')
    print("모델이 models/cifar10_classifier.h5에 저장되었습니다.")
    
    # 클래스 이름 저장
    class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer',
                   'dog', 'frog', 'horse', 'ship', 'truck']
    
    with open('models/class_names.json', 'w') as f:
        json.dump(class_names, f)
    
    print("클래스 이름이 models/class_names.json에 저장되었습니다.")
    print("학습 완료!")

if __name__ == "__main__":
    main()
