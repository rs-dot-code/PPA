const uploadBtn = document.getElementById('upload-btn');
const resultText = document.getElementById('result-text');
const resultSection = document.querySelector('.result-section');
const uploadSection = document.querySelector('.upload-section');
const dropContainer = document.getElementById('dropcontainer');
const qpInput = document.getElementById('qp');

let qpFiles = [];

const validateFiles = (files) => {
    if (files.length > 4) {
        alert('Please select up to 4 files');
        return false;
    }
    for (let i = 0; i < files.length; i++) {
        if (!files[i].name.endsWith('.pdf')) {
            alert('Only PDF files are allowed');
            return false;
        }
    }
    return true;
}

const uploadFiles = async (files) => {
    if(uploadBtn.innerText==="Refresh"){
        location.reload();
        return;
    }
    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
        formData.append(`qp[]`, files[i]);
    }
    try {
        uploadBtn.innerText = "Processing...";
        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData,
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const result = await response.json();
        resultText.innerHTML = result.result;
        uploadSection.remove();
        resultSection.style.visibility = "visible";
        uploadBtn.innerText = "Refresh";
        document.querySelector("html").style.overflow = "visible";
    } catch (error) {
        console.error(error);
        resultText.innerText = "Error: " + error.message;
    }
}

uploadBtn.addEventListener('click', async (e) => {
    e.preventDefault();
    if (!validateFiles(qpFiles)) {
        return;
    }
    uploadFiles(qpFiles);
});

dropContainer.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropContainer.classList.add('dragover');
});

dropContainer.addEventListener('dragleave', () => {
    dropContainer.classList.remove('dragover');
});

dropContainer.addEventListener('drop', (e) => {
    e.preventDefault();
    dropContainer.classList.remove('dragover');
    qpFiles = e.dataTransfer.files;
    qpInput.files = qpFiles;
});

qpInput.addEventListener('input', () => {
    qpFiles = qpInput.files;
});