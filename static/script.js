// DOM 요소들
const uploadArea = document.getElementById('uploadArea');
const imageInput = document.getElementById('imageInput');
const previewSection = document.getElementById('previewSection');
const previewImage = document.getElementById('previewImage');
const analyzeBtn = document.getElementById('analyzeBtn');
const resultSection = document.getElementById('resultSection');
const loadingSection = document.getElementById('loadingSection');
const errorSection = document.getElementById('errorSection');

// 상태 변수
let selectedFile = null;

// 이벤트 리스너 등록
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // 파일 입력 이벤트
    imageInput.addEventListener('change', handleFileSelect);
    
    // 드래그 앤 드롭 이벤트
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
    uploadArea.addEventListener('click', () => imageInput.click());
    
    // 분석 버튼 이벤트
    analyzeBtn.addEventListener('click', analyzeImage);
    
    console.log('앱이 초기화되었습니다.');
}

function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        processFile(file);
    }
}

function handleDragOver(event) {
    event.preventDefault();
    uploadArea.classList.add('dragover');
}

function handleDragLeave(event) {
    event.preventDefault();
    uploadArea.classList.remove('dragover');
}

function handleDrop(event) {
    event.preventDefault();
    uploadArea.classList.remove('dragover');
    
    const files = event.dataTransfer.files;
    if (files.length > 0) {
        processFile(files[0]);
    }
}

function processFile(file) {
    // 파일 타입 검증
    if (!file.type.startsWith('image/')) {
        showError('이미지 파일만 업로드할 수 있습니다.');
        return;
    }
    
    // 파일 크기 검증 (10MB 제한)
    if (file.size > 10 * 1024 * 1024) {
        showError('파일 크기는 10MB 이하여야 합니다.');
        return;
    }
    
    selectedFile = file;
    
    // 이미지 미리보기
    const reader = new FileReader();
    reader.onload = function(e) {
        previewImage.src = e.target.result;
        showPreview();
    };
    reader.readAsDataURL(file);
}

function showPreview() {
    hideAllSections();
    previewSection.style.display = 'block';
    previewSection.classList.add('fade-in');
}

function analyzeImage() {
    if (!selectedFile) {
        showError('분석할 이미지를 선택해주세요.');
        return;
    }
    
    showLoading();
    
    // FormData 생성
    const formData = new FormData();
    formData.append('image', selectedFile);
    
    // API 호출
    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            showResult(data);
        } else {
            showError(data.error || '예측 중 오류가 발생했습니다.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showError('서버와의 통신 중 오류가 발생했습니다: ' + error.message);
    });
}

function showResult(data) {
    hideAllSections();
    
    // 결과 표시
    document.getElementById('predictedClass').textContent = data.predicted_class;
    document.getElementById('confidenceText').textContent = data.confidence.toFixed(1) + '%';
    document.getElementById('resultDescription').textContent = data.description;
    
    // 신뢰도 바 애니메이션
    const confidenceFill = document.getElementById('confidenceFill');
    setTimeout(() => {
        confidenceFill.style.width = data.confidence + '%';
    }, 100);
    
    resultSection.style.display = 'block';
    resultSection.classList.add('slide-up');
}

function showLoading() {
    hideAllSections();
    loadingSection.style.display = 'block';
    loadingSection.classList.add('fade-in');
}

function showError(message) {
    hideAllSections();
    document.getElementById('errorText').textContent = message;
    errorSection.style.display = 'block';
    errorSection.classList.add('fade-in');
}

function hideAllSections() {
    const sections = [previewSection, resultSection, loadingSection, errorSection];
    sections.forEach(section => {
        section.style.display = 'none';
        section.classList.remove('fade-in', 'slide-up');
    });
}

function resetApp() {
    selectedFile = null;
    imageInput.value = '';
    hideAllSections();
    
    // 신뢰도 바 리셋
    document.getElementById('confidenceFill').style.width = '0%';
}

// 유틸리티 함수들
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function getFileExtension(filename) {
    return filename.slice((filename.lastIndexOf('.') - 1 >>> 0) + 2);
}

// 키보드 단축키
document.addEventListener('keydown', function(event) {
    // ESC 키로 리셋
    if (event.key === 'Escape') {
        resetApp();
    }
    
    // Enter 키로 분석 (이미지가 선택된 상태에서)
    if (event.key === 'Enter' && selectedFile && resultSection.style.display === 'none') {
        analyzeImage();
    }
});

// 페이지 로드 시 헬스 체크
window.addEventListener('load', function() {
    fetch('/health')
        .then(response => response.json())
        .then(data => {
            console.log('서버 상태:', data);
            if (!data.model_loaded) {
                console.warn('모델이 로드되지 않았습니다.');
            }
        })
        .catch(error => {
            console.error('헬스 체크 실패:', error);
        });
});

// 이미지 로드 오류 처리
previewImage.addEventListener('error', function() {
    showError('이미지를 불러올 수 없습니다. 다른 이미지를 시도해보세요.');
});

// 전역 오류 처리
window.addEventListener('error', function(event) {
    console.error('전역 오류:', event.error);
});

window.addEventListener('unhandledrejection', function(event) {
    console.error('처리되지 않은 Promise 거부:', event.reason);
    showError('예상치 못한 오류가 발생했습니다.');
});
