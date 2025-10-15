import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models, datasets
import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import cv2
from PIL import Image
import requests
from io import BytesIO
import json

# GPU 메모리 설정
physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)

class CIFAR10ImageClassifier:
    def __init__(self, img_size=(32, 32), num_classes=10):
        self.img_size = img_size
        self.num_classes = num_classes
        self.model = None
        self.class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer',
                           'dog', 'frog', 'horse', 'ship', 'truck']
        
    def create_model(self):
        """REF_DL_CNN.ipynb를 참고한 CNN 모델 생성"""
        model = models.Sequential()
        
        # 컨볼루션 베이스 (REF_DL_CNN.ipynb와 동일한 구조)
        model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(*self.img_size, 3)))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(64, (3, 3), activation='relu'))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(64, (3, 3), activation='relu'))
        
        # Dense 레이어 추가
        model.add(layers.Flatten())
        model.add(layers.Dense(64, activation='relu'))
        model.add(layers.Dense(self.num_classes))
        
        model.compile(
            optimizer='adam',
            loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
            metrics=['accuracy']
        )
        
        self.model = model
        return model
    
    def load_cifar10_data(self):
        """CIFAR-10 데이터셋 로드"""
        print("CIFAR-10 데이터셋 로드 중...")
        
        # CIFAR-10 데이터셋 다운로드 및 로드
        (train_images, train_labels), (test_images, test_labels) = datasets.cifar10.load_data()
        
        # 픽셀 값을 0과 1 사이로 정규화
        train_images, test_images = train_images / 255.0, test_images / 255.0
        
        print(f"훈련 데이터: {train_images.shape}, {train_labels.shape}")
        print(f"테스트 데이터: {test_images.shape}, {test_labels.shape}")
        
        return (train_images, train_labels), (test_images, test_labels)
    
    def train_model(self, train_images, train_labels, test_images, test_labels, epochs=10):
        """REF_DL_CNN.ipynb와 동일한 방식으로 모델 학습"""
        print("모델 학습 시작...")
        
        # REF_DL_CNN.ipynb와 동일한 학습 방식
        history = self.model.fit(train_images, train_labels, epochs=epochs,
                                validation_data=(test_images, test_labels))
        
        return history
    
    def save_model(self, filepath='models/cifar10_classifier.h5'):
        """모델 저장"""
        if not os.path.exists('models'):
            os.makedirs('models')
        
        self.model.save(filepath)
        print(f"모델이 {filepath}에 저장되었습니다.")
        
        # 클래스 이름도 저장
        with open('models/class_names.json', 'w') as f:
            json.dump(self.class_names, f)
    
    def plot_training_history(self, history):
        """REF_DL_CNN.ipynb와 동일한 학습 히스토리 시각화"""
        plt.plot(history.history['accuracy'], label='accuracy')
        plt.plot(history.history['val_accuracy'], label='val_accuracy')
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy')
        plt.ylim([0.5, 1])
        plt.legend(loc='lower right')
        plt.savefig('models/training_history.png')
        plt.show()

def main():
    """REF_DL_CNN.ipynb를 참고한 메인 실행 함수"""
    print("CIFAR-10 CNN 이미지 분류기 학습 시작")
    
    # 분류기 초기화
    classifier = CIFAR10ImageClassifier()
    
    # CIFAR-10 데이터 로드
    (train_images, train_labels), (test_images, test_labels) = classifier.load_cifar10_data()
    
    # 모델 생성
    model = classifier.create_model()
    print("모델 구조:")
    model.summary()
    
    # 모델 학습 (REF_DL_CNN.ipynb와 동일한 설정)
    history = classifier.train_model(train_images, train_labels, test_images, test_labels, epochs=10)
    
    # 모델 평가
    test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=2)
    print(f"테스트 정확도: {test_acc}")
    
    # 학습 히스토리 시각화
    classifier.plot_training_history(history)
    
    # 모델 저장
    classifier.save_model()
    
    print("학습 완료!")

if __name__ == "__main__":
    main()
