class WhatsAppBulkSender {
    constructor() {
        this.initializeElements();
        this.initializeEventListeners();
        this.loadStoredConnection();
    }

    initializeElements() {
        // Connection elements
        this.accessTokenInput = document.getElementById('accessToken');
        this.businessManagerIdInput = document.getElementById('businessManagerId');
        this.connectBtn = document.getElementById('connectBtn');
        this.connectionStatus = document.getElementById('connectionStatus');
        this.connectionInfo = document.getElementById('connectionInfo');
        this.connectionForm = document.getElementById('connectionForm');
        
        // Configuration elements
        this.phoneSelect = document.getElementById('phoneSelect');
        this.templateSelect = document.getElementById('templateSelect');
        this.leadsInput = document.getElementById('leadsInput');
        this.validateLeadsBtn = document.getElementById('validateLeadsBtn');
        
        // Status elements
        this.totalLeadsCount = document.getElementById('totalLeadsCount');
        this.validLeadsCount = document.getElementById('validLeadsCount');
        this.invalidLeadsCount = document.getElementById('invalidLeadsCount');
        this.duplicateLeadsCount = document.getElementById('duplicateLeadsCount');
        this.validationResults = document.getElementById('validationResults');
        this.validationSummary = document.getElementById('validationSummary');
        
        // Send elements
        this.smartDistributionBtn = document.getElementById('smartDistributionBtn');
        this.progressSection = document.getElementById('progressSection');
        this.progressBar = document.getElementById('progressBar');
        this.progressText = document.getElementById('progressText');
        this.sentCount = document.getElementById('sentCount');
        this.failedCount = document.getElementById('failedCount');
        this.statusMessage = document.getElementById('statusMessage');
        
        // Preview elements
        this.distributionPreview = document.getElementById('distributionPreview');
        this.distributionDetails = document.getElementById('distributionDetails');
        
        // Connection stats
        this.connectedPhones = document.getElementById('connectedPhones');
        this.connectedTemplates = document.getElementById('connectedTemplates');
        this.connectedBmId = document.getElementById('connectedBmId');
    }

    initializeEventListeners() {
        // Connection
        this.connectBtn?.addEventListener('click', () => this.connectWhatsApp());
        
        // Validation
        this.validateLeadsBtn?.addEventListener('click', () => this.validateLeads());
        
        // Send
        this.smartDistributionBtn?.addEventListener('click', () => this.sendUltraSpeedMessages());
        
        // Phone/Template selection
        this.phoneSelect?.addEventListener('change', () => this.updateSendButton());
        this.templateSelect?.addEventListener('change', () => this.updateSendButton());
        this.leadsInput?.addEventListener('input', () => this.resetValidation());
    }

    loadStoredConnection() {
        const stored = localStorage.getItem('whatsapp_connection');
        if (stored) {
            try {
                const data = JSON.parse(stored);
                this.accessTokenInput.value = data.token || '';
                this.businessManagerIdInput.value = data.business_manager_id || '';
                if (data.connected) {
                    this.setConnectionState(true, data);
                }
            } catch (e) {
                console.error('Error loading stored connection:', e);
            }
        }
    }

    async connectWhatsApp() {
        const token = this.accessTokenInput.value.trim();
        const businessManagerId = this.businessManagerIdInput.value.trim();
        
        if (!token) {
            this.showAlert('error', 'Token de acesso é obrigatório');
            return;
        }

        this.setButtonLoading(this.connectBtn, true);

        const requestBody = { access_token: token };
        if (businessManagerId) {
            requestBody.business_manager_id = businessManagerId;
        }

        try {
            const response = await fetch('/api/connect-whatsapp', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestBody)
            });

            const data = await response.json();

            if (response.ok && data.success) {
                this.setConnectionState(true, data);
                this.storeConnection(token, businessManagerId, data);
                this.showAlert('success', 'Conectado com sucesso ao WhatsApp Business API');
            } else {
                this.showAlert('error', data.message || data.error || 'Erro ao conectar');
            }
        } catch (error) {
            this.showAlert('error', 'Erro de rede ao conectar');
            console.error('Connection error:', error);
        } finally {
            this.setButtonLoading(this.connectBtn, false);
        }
    }

    setConnectionState(connected, data = null) {
        if (connected && data) {
            // Update connection status
            this.connectionStatus.className = 'connection-indicator connected';
            this.connectionStatus.innerHTML = '<div class="status-dot"></div>Conectado';
            
            // Hide form, show info
            this.connectionForm.style.display = 'none';
            this.connectionInfo.style.display = 'block';
            
            // Extract connection data from response
            const connectionData = data.data || data;
            
            // Update stats
            this.connectedPhones.textContent = (connectionData.phone_numbers || []).length;
            this.connectedTemplates.textContent = (connectionData.templates || []).length;
            this.connectedBmId.textContent = connectionData.business_manager_id || '-';
            
            // Populate selects
            this.populatePhoneSelect(connectionData.phone_numbers || []);
            this.populateTemplateSelect(connectionData.templates || []);
            
            // Enable form elements
            this.phoneSelect.disabled = false;
            this.templateSelect.disabled = false;
            
        } else {
            // Reset to disconnected state
            this.connectionStatus.className = 'connection-indicator disconnected';
            this.connectionStatus.innerHTML = '<div class="status-dot"></div>Desconectado';
            
            this.connectionForm.style.display = 'block';
            this.connectionInfo.style.display = 'none';
            
            // Clear and disable selects
            this.phoneSelect.innerHTML = '<option value="">Conecte-se primeiro para carregar números</option>';
            this.templateSelect.innerHTML = '<option value="">Conecte-se primeiro para carregar templates</option>';
            this.phoneSelect.disabled = true;
            this.templateSelect.disabled = true;
            
            this.updateSendButton();
        }
    }

    populatePhoneSelect(phones) {
        this.phoneSelect.innerHTML = '<option value="">Selecione um número</option>';
        phones.forEach(phone => {
            const option = document.createElement('option');
            option.value = phone.id;
            option.textContent = `${phone.display_phone_number} (${phone.verified_name || 'Sem nome'})`;
            this.phoneSelect.appendChild(option);
        });
    }

    populateTemplateSelect(templates) {
        this.templateSelect.innerHTML = '<option value="">Selecione um template</option>';
        templates.forEach(template => {
            const option = document.createElement('option');
            option.value = template.name;
            option.textContent = `${template.name} (${template.language} - ${template.category})`;
            this.templateSelect.appendChild(option);
        });
    }

    storeConnection(token, businessManagerId, data) {
        const connectionData = {
            token: token,
            business_manager_id: businessManagerId,
            connected: true,
            ...data
        };
        localStorage.setItem('whatsapp_connection', JSON.stringify(connectionData));
    }

    disconnect() {
        this.setConnectionState(false);
        this.accessTokenInput.value = '';
        this.businessManagerIdInput.value = '';
        localStorage.removeItem('whatsapp_connection');
        this.resetValidation();
        this.showAlert('info', 'Desconectado do WhatsApp Business API');
    }

    async validateLeads() {
        const leadsText = this.leadsInput.value.trim();
        if (!leadsText) {
            this.showAlert('error', 'Insira a lista de contatos primeiro');
            return;
        }

        this.setButtonLoading(this.validateLeadsBtn, true);

        try {
            const response = await fetch('/api/validate-leads', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ leads_text: leadsText })
            });

            const data = await response.json();

            if (response.ok && data.success) {
                this.updateValidationStats(data);
                this.showValidationResults(data);
                this.updateSendButton();
            } else {
                this.showAlert('error', data.error || 'Erro ao validar leads');
            }
        } catch (error) {
            this.showAlert('error', 'Erro de rede ao validar leads');
            console.error('Validation error:', error);
        } finally {
            this.setButtonLoading(this.validateLeadsBtn, false);
        }
    }

    updateValidationStats(data) {
        this.totalLeadsCount.textContent = data.total || 0;
        this.validLeadsCount.textContent = data.valid || 0;
        this.invalidLeadsCount.textContent = data.invalid || 0;
        this.duplicateLeadsCount.textContent = data.duplicates || 0;
    }

    showValidationResults(data) {
        this.validationSummary.textContent = 
            `${data.valid} válidos, ${data.invalid} inválidos, ${data.duplicates} duplicatas`;
        this.validationResults.style.display = 'block';
    }

    resetValidation() {
        this.updateValidationStats({ total: 0, valid: 0, invalid: 0, duplicates: 0 });
        this.validationResults.style.display = 'none';
        this.updateSendButton();
    }

    updateSendButton() {
        const hasPhone = this.phoneSelect.value;
        const hasTemplate = this.templateSelect.value;
        const hasValidLeads = parseInt(this.validLeadsCount.textContent) > 0;
        
        this.smartDistributionBtn.disabled = !(hasPhone && hasTemplate && hasValidLeads);
    }

    async sendUltraSpeedMessages() {
        const phoneId = this.phoneSelect.value;
        const templateName = this.templateSelect.value;
        const leadsText = this.leadsInput.value.trim();

        if (!phoneId || !templateName || !leadsText) {
            this.showAlert('error', 'Preencha todos os campos obrigatórios');
            return;
        }

        this.setButtonLoading(this.smartDistributionBtn, true);
        this.progressSection.style.display = 'block';
        
        // Generate session ID for progress tracking
        const sessionId = Date.now().toString();

        try {
            const response = await fetch('/api/ultra-speed', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    phone_number_ids: [phoneId],
                    template_names: [templateName],
                    leads_text: leadsText,
                    session_id: sessionId
                })
            });

            const data = await response.json();

            if (response.ok && data.success) {
                this.startProgressTracking(sessionId);
                this.showAlert('success', 'Envio iniciado com sucesso');
            } else {
                this.showAlert('error', data.error || 'Erro ao iniciar envio');
                this.progressSection.style.display = 'none';
            }
        } catch (error) {
            this.showAlert('error', 'Erro de rede ao iniciar envio');
            console.error('Send error:', error);
            this.progressSection.style.display = 'none';
        } finally {
            this.setButtonLoading(this.smartDistributionBtn, false);
        }
    }

    startProgressTracking(sessionId) {
        const interval = setInterval(async () => {
            try {
                const response = await fetch(`/api/progress/${sessionId}`);
                const data = await response.json();

                if (response.ok) {
                    this.updateProgress(data);
                    
                    if (data.completed) {
                        clearInterval(interval);
                        this.showAlert('success', 'Envio concluído com sucesso');
                    }
                } else {
                    clearInterval(interval);
                    this.showAlert('error', 'Erro ao acompanhar progresso');
                }
            } catch (error) {
                console.error('Progress tracking error:', error);
            }
        }, 1000);
    }

    updateProgress(data) {
        const progress = data.progress || 0;
        const sent = data.sent || 0;
        const failed = data.failed || 0;
        
        this.progressBar.style.width = `${progress}%`;
        this.progressText.textContent = `${Math.round(progress)}%`;
        this.sentCount.textContent = sent;
        this.failedCount.textContent = failed;
        this.statusMessage.textContent = data.status || 'Processando...';
    }

    setButtonLoading(button, loading) {
        if (loading) {
            button.classList.add('loading');
            button.disabled = true;
        } else {
            button.classList.remove('loading');
            button.disabled = false;
        }
    }

    showAlert(type, message) {
        // Create alert element
        const alert = document.createElement('div');
        alert.className = `alert alert-${type}`;
        alert.innerHTML = `
            <div class="flex items-center gap-3">
                <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
                <span>${message}</span>
            </div>
        `;
        
        // Insert at top of container
        const container = document.querySelector('.container');
        container.insertBefore(alert, container.firstChild);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            alert.remove();
        }, 5000);
    }
}

// Global functions for HTML onclick handlers
function disconnect() {
    window.whatsappSender.disconnect();
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.whatsappSender = new WhatsAppBulkSender();
});