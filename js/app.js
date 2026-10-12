// AI Live Translation & Lip Sync Broadcast - Frontend JavaScript
// Connects the UI to the FastAPI backend

document.addEventListener('DOMContentLoaded', function() {
    // Base URL for API - will use relative path for same-origin
    const BASE_URL = '';
    
    // API Endpoints
    const ENDPOINTS = {
        HEALTH: '/health',
        TRANSLATE_BROADCAST: '/translate_broadcast',
        TRANSLATE_CLIP: '/translate_clip',
        TRANSCRIBE: '/transcribe'
    };
    
    // State
    let selectedLanguages = new Set(['es', 'fr', 'de', 'hausa', 'yoruba', 'swahili']);
    
    // DOM Elements
    const elements = {
        healthBtn: document.querySelector('.btn-health'),
        healthResult: document.getElementById('health-result'),
        broadcastFile: document.getElementById('broadcast-file'),
        translateBtn: document.querySelector('.btn-translate'),
        translateResult: document.getElementById('translate-result'),
        clipFile: document.getElementById('clip-file'),
        clipLanguage: document.getElementById('clip-language'),
        clipResult: document.getElementById('clip-result'),
        languageChips: document.querySelectorAll('.chip'),
        lipSyncCheckbox: document.getElementById('lip-sync'),
        voiceCloneCheckbox: document.getElementById('voice-clone')
    };
    
    // Initialize language chips
    function initLanguageChips() {
        elements.languageChips.forEach(chip => {
            chip.addEventListener('click', function() {
                const lang = this.getAttribute('data-lang');
                if (selectedLanguages.has(lang)) {
                    selectedLanguages.delete(lang);
                    this.classList.remove('active');
                } else {
                    selectedLanguages.add(lang);
                    this.classList.add('active');
                }
            });
        });
    }
    
    // Check system health
    async function checkHealth() {
        showLoading(elements.healthResult, 'Checking...');
        
        try {
            const response = await fetch(ENDPOINTS.HEALTH, {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' }
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            
            const data = await response.json();
            displayHealthResult(data);
        } catch (error) {
            displayError(elements.healthResult, error.message);
        }
    }
    
    // Display health result
    function displayHealthResult(data) {
        const html = `
            <div class="status-online">
                <span class="status-dot"></span>
                <span>System Online</span>
            </div>
            <pre class="json-data">${JSON.stringify(data, null, 2)}</pre>
        `;
        elements.healthResult.innerHTML = html;
        elements.healthResult.style.display = 'block';
    }
    
    // Display error
    function displayError(element, message) {
        element.innerHTML = `<div class="status-offline"><span class="status-dot red"></span><span>Error: ${message}</span></div>`;
        element.style.display = 'block';
    }
    
    // Show loading state
    function showLoading(element, text) {
        element.innerHTML = `<div class="loading-spinner">${text}</div>`;
        element.style.display = 'block';
    }
    
    // Format language names
    function getLanguageName(code) {
        const names = {
            'en': 'English',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'zh': 'Chinese',
            'ar': 'Arabic',
            'hausa': 'Hausa',
            'yoruba': 'Yoruba',
            'swahili': 'Swahili'
        };
        return names[code] || code;
    }
    
    // Translate broadcast
    async function translateBroadcast() {
        const file = elements.broadcastFile.files[0];
        if (!file) {
            showNotification('Please select a file first', 'error');
            return;
        }
        
        // Show loading state
        elements.translateResult.innerHTML = '<div class="loading-spinner">Processing broadcast...</div>';
        elements.translateResult.style.display = 'block';
        
        const formData = new FormData();
        formData.append('file', file);
        formData.append('target_languages', Array.from(selectedLanguages).join(','));
        formData.append('lip_sync', elements.lipSyncCheckbox.checked);
        formData.append('voice_clone', elements.voiceCloneCheckbox.checked);
        
        try {
            const response = await fetch(ENDPOINTS.TRANSLATE_BROADCAST, {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || `HTTP ${response.status}`);
            }
            
            const result = await response.json();
            displayBroadcastResult(result);
        } catch (error) {
            displayTranslationError(elements.translateResult, error.message);
        }
    }
    
    // Display broadcast translation result
    function displayBroadcastResult(result) {
        const languages = result.target_languages || Object.keys(result.results || []);
        
        let html = `<h3>📡 Translation Results</h3>`;
        html += `<p><strong>Original Text:</strong> ${result.original_text || 'N/A'}</p>`;
        html += `<p><strong>Broadcast ID:</strong> ${result.broadcast_id || 'N/A'}</p>`;
        
        if (result.results && result.results.length > 0) {
            html += `<div class="lang-results">`;
            result.results.forEach(langResult => {
                html += `
                    <div class="language-result">
                        <div class="lang-header">
                            <span class="lang-flag">${langResult.target_language.toUpperCase()}</span>
                            <span class="lang-name">${getLanguageName(langResult.target_language)}</span>
                        </div>
                        <div class="original-text">
                            <strong>Original:</strong> ${langResult.original_text || 'N/A'}
                        </div>
                        <div class="translated-text">
                            <strong>Translated:</strong> ${langResult.translated_text || 'N/A'}
                        </div>
                        <div class="result-meta">
                            <span>🎤 Voice Cloned: ${langResult.audio_cloned ? 'Yes' : 'No'}</span>
                            <span>🔒 Lip Sync Ready: ${langResult.lip_sync_ready ? 'Yes' : 'No'}</span>
                            <span>📊 Confidence: ${langResult.confidence_score || 0}</span>
                        </div>
                    </div>
                `;
            });
            html += `</div>`;
        }
        
        html += `<div class="download-links">
            <a href="#" class="btn-download" onclick="downloadTranslations('audio')">Download Audio</a>
            <a href="#" class="btn-download" onclick="downloadTranslations('video')">Download Video</a>
        </div>`;
        
        elements.translateResult.innerHTML = html;
        elements.translateResult.style.display = 'block';
        showNotification('Broadcast translated successfully!', 'success');
        playNotificationSound();
        }
    
    // Display translation error
    function displayTranslationError(element, message) {
        element.innerHTML = `<div class="status-offline"><span class="status-dot red"></span><span>Error: ${message}</span></div>`;
        element.style.display = 'block';
    }
    
    // Translate clip
    async function translateClip() {
        const file = elements.clipFile.files[0];
        if (!file) {
            showNotification('Please select a file first', 'error');
            return;
        }
        
        const lang = elements.clipLanguage.value;
        
        showLoadingClip(elements.clipResult, 'Processing clip...');
        
        const formData = new FormData();
        formData.append('file', file);
        formData.append('target_language', lang);
        
        try {
            const response = await fetch(ENDPOINTS.TRANSLATE_CLIP, {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || `HTTP ${response.status}`);
            }
            
            const result = await response.json();
            displayClipResult(result);
        } catch (error) {
            displayClipError(elements.clipResult, error.message);
        }
    }
    
    // Display clip result
    function displayClipResult(result) {
        const html = `
            <div class="clip-result-card">
                <div class="result-header">
                    <span class="result-icon">✅</span>
                    <h4>Translation Complete</h4>
                </div>
                <div class="result-content">
                    <p><strong>Original Text:</strong> ${result.original_text || 'N/A'}</p>
                    <p><strong>Translated Text:</strong> ${result.translated_text || 'N/A'}</p>
                    <p><strong>Target Language:</strong> ${getLanguageName(result.target_language || 'es')}</p>
                    <p><strong>Audio Generated:</strong> ${result.audio_generated || 0} bytes</p>
                </div>
                <div class="result-actions">
                    <button class="btn-download" onclick="downloadClipAudio('${result.original_text || 'translation'}')">Download Audio</button>
                </div>
            </div>
        `;
        
        elements.clipResult.innerHTML = html;
        elements.clipResult.style.display = 'block';
        showNotification('Clip translated successfully!', 'success');
    }
    
    // Display clip error
    function displayClipError(element, message) {
        element.innerHTML = `<div class="status-offline"><span class="status-dot red"></span><span>Error: ${message}</span></div>`;
        element.style.display = 'block';
    }
    
    // Show loading for clip
    function showLoadingClip(element, text) {
        element.innerHTML = `<div class="loading-spinner">${text}</div>`;
        element.style.display = 'block';
    }
    
    // Clear form
    function clearForm() {
        elements.broadcastFile.value = '';
        elements.clipFile.value = '';
        elements.translateResult.style.display = 'none';
        elements.clipResult.style.display = 'none';
        selectedLanguages = new Set(['es', 'fr', 'de', 'hausa', 'yoruba', 'swahili']);
        elements.languageChips.forEach(chip => chip.classList.remove('active'));
        elements.lipSyncCheckbox.checked = true;
        elements.voiceCloneCheckbox.checked = true;
        showNotification('Form cleared', 'info');
    }
    
    // Show notification
    function showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <span class="notification-icon">${type === 'success' ? '✅' : type === 'error' ? '❌' : 'ℹ️'}</span>
                <span class="notification-message">${message}</span>
            </div>
        `;
        
        // Style the notification
        notification.style.position = 'fixed';
        notification.style.top = '20px';
        notification.style.right = '20px';
        notification.style.background = type === 'success' ? 'var(--success-color)' : type === 'error' ? 'var(--error-color)' : 'var(--info-color)';
        notification.style.color = '#fff';
        notification.style.padding = '12px 20px';
        notification.style.borderRadius = '8px';
        notification.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
        notification.style.zIndex = '1000';
        notification.style.animation = 'slideIn 0.3s ease';
        
        document.body.appendChild(notification);
        
        // Remove after 3 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 3000);
    }
    
    // Play notification sound
    function playNotificationSound() {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        oscillator.frequency.value = 880;
        oscillator.connect(audioContext.destination);
        oscillator.start();
        oscillator.stop(audioContext.currentTime + 0.1);
    }
    
    // Download translations
    function downloadTranslations(type) {
        showNotification('Download initiated', 'info');
        // In a real implementation, this would trigger a download
        // of the translated audio/video file
    }
    
    // Download clip audio
    function downloadClipAudio(text) {
        const blob = new Blob([text], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'translation.txt';
        a.click();
        URL.revokeObjectURL(url);
    }
    
    // Initialize on load
    initLanguageChips();
    
    // Event listeners
    elements.healthBtn.addEventListener('click', checkHealth);
    elements.translateBtn.addEventListener('click', translateBroadcast);
    elements.broadcastFile.addEventListener('change', () => {
        if (elements.broadcastFile.files[0]) {
            showNotification('File selected', 'info');
        }
    });
    elements.clipFile.addEventListener('change', () => {
        if (elements.clipFile.files[0]) {
            showNotification('File selected', 'info');
        }
    });
    elements.lipSyncCheckbox.addEventListener('change', () => {
        showNotification('Lip sync ' + (elements.lipSyncCheckbox.checked ? 'enabled' : 'disabled'), 'info');
    });
    elements.voiceCloneCheckbox.addEventListener('change', () => {
        showNotification('Voice cloning ' + (elements.voiceCloneCheckbox.checked ? 'enabled' : 'disabled'), 'info');
    });
    
    // Allow pressing Enter in file inputs to trigger
    document.queryAll = document.queryAll || function(selector) {
        return document.querySelectorAll(selector);
    };
});