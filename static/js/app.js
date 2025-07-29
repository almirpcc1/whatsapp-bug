// WhatsApp Sender Application
class WhatsAppSender {
    constructor() {
        this.leads = [];
        this.validationErrors = [];
        this.connectionData = null;
        
        this.initializeEventListeners();
        this.checkSavedConnection();
    }
    
    initializeEventListeners() {
        // Connection buttons
        const connectBtn = document.getElementById('connectButton');
        if (connectBtn) {
            connectBtn.addEventListener('click', () => {
                this.connectWhatsApp();
            });
        }
        
        const disconnectBtn = document.getElementById('disconnectButton');
        if (disconnectBtn) {
            disconnectBtn.addEventListener('click', () => {
                this.disconnect();
            });
        }
        
        // Validate leads button
        const validateBtn = document.getElementById('validateLeadsBtn');
        if (validateBtn) {
            validateBtn.addEventListener('click', () => {
                this.validateLeads();
            });
        }
        
        // Smart Distribution button
        const smartBtn = document.getElementById('smartDistributionBtn');
        if (smartBtn) {
            smartBtn.addEventListener('click', () => {
                this.sendSmartDistribution();
            });
        }
        
        // Template selection buttons
        const selectAllBtn = document.getElementById('selectAllTemplatesBtn');
        if (selectAllBtn) {
            selectAllBtn.addEventListener('click', () => {
                this.selectAllTemplates();
            });
        }
        
        const clearBtn = document.getElementById('clearTemplatesBtn');
        if (clearBtn) {
            clearBtn.addEventListener('click', () => {
                this.clearTemplateSelection();
            });
        }
        
        // Leads textarea change
        const leadsInput = document.getElementById('leadsInput');
        if (leadsInput) {
            leadsInput.addEventListener('input', () => {
                this.resetValidation();
            });
        }
    }

    async connectWhatsApp() {
        const accessToken = document.getElementById('accessToken').value.trim();
        const businessManagerId = document.getElementById('businessManagerId').value.trim();
        
        if (!accessToken) {
            this.showAlert('Token de acesso é obrigatório', 'danger');
            return;
        }
        
        const connectButton = document.getElementById('connectButton');
        const originalText = connectButton.innerHTML;
        connectButton.disabled = true;
        connectButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Conectando...';
        
        try {
            const response = await fetch('/api/connect-whatsapp', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    access_token: accessToken,
                    business_manager_id: businessManagerId || null
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.connectionData = result.data;
                localStorage.setItem('whatsapp_connection', JSON.stringify(this.connectionData));
                this.updateConnectionUI(true);
                this.loadConnectionData();
                this.showAlert('Conectado com sucesso! Carregando dados...', 'success');
            } else {
                // Check for token expiration
                if (response.status === 401 || result.message.includes('expired') || result.message.includes('access token')) {
                    this.showAlert('⚠️ TOKEN EXPIRADO: Seu token WhatsApp expirou. Por favor, obtenha um novo token do Facebook Business Manager.', 'warning');
                } else {
                    this.showAlert(result.message || 'Erro ao conectar', 'danger');
                }
            }
        } catch (error) {
            console.error('Erro de conexão:', error);
            this.showAlert('Erro de conexão com o servidor', 'danger');
        } finally {
            connectButton.disabled = false;
            connectButton.innerHTML = originalText;
        }
    }
    
    disconnect() {
        this.connectionData = null;
        localStorage.removeItem('whatsapp_connection');
        this.updateConnectionUI(false);
        this.clearConnectionData();
        this.showAlert('Desconectado com sucesso', 'info');
    }
    
    checkSavedConnection() {
        const savedConnection = localStorage.getItem('whatsapp_connection');
        if (savedConnection) {
            try {
                this.connectionData = JSON.parse(savedConnection);
                this.updateConnectionUI(true);
                this.loadConnectionData();
            } catch (error) {
                console.error('Erro ao carregar conexão salva:', error);
                localStorage.removeItem('whatsapp_connection');
            }
        }
    }
    
    updateConnectionUI(connected) {
        const connectionStatus = document.getElementById('connectionStatus');
        const connectionInfo = document.getElementById('connectionInfo');
        const accessToken = document.getElementById('accessToken');
        const businessManagerId = document.getElementById('businessManagerId');
        const connectButton = document.getElementById('connectButton');
        
        if (connected && this.connectionData) {
            connectionStatus.className = 'badge bg-success';
            connectionStatus.textContent = 'Conectado';
            connectionInfo.style.display = 'block';
            
            // Ocultar campos de entrada
            accessToken.parentElement.style.display = 'none';
            businessManagerId.parentElement.style.display = 'none';
            connectButton.parentElement.style.display = 'none';
            
            // Preencher informações de conexão
            document.getElementById('connectedBmId').textContent = this.connectionData.business_manager_id;
            document.getElementById('connectedPhones').textContent = this.connectionData.phone_numbers.length;
            document.getElementById('connectedTemplates').textContent = this.connectionData.templates.length;
            
            // Popular números e templates
            this.populatePhoneNumbers(this.connectionData.phone_numbers);
            this.populateTemplates(this.connectionData.templates);
        } else {
            connectionStatus.className = 'badge bg-secondary';
            connectionStatus.textContent = 'Desconectado';
            connectionInfo.style.display = 'none';
            
            // Mostrar campos de entrada
            accessToken.parentElement.style.display = 'block';
            businessManagerId.parentElement.style.display = 'block';
            connectButton.parentElement.style.display = 'block';
            
            // Limpar campos
            accessToken.value = '';
            businessManagerId.value = '';
            
            // Limpar números e templates
            this.clearConnectionData();
        }
    }
    
    populatePhoneNumbers(phoneNumbers) {
        const container = document.getElementById('phoneNumbersContainer');
        
        if (!phoneNumbers || phoneNumbers.length === 0) {
            container.innerHTML = '<div class="text-muted text-center py-2">Nenhum número encontrado</div>';
            return;
        }
        
        let html = '';
        phoneNumbers.forEach(phone => {
            const qualityBadge = phone.quality_rating === 'GREEN' ? 'bg-success' : 
                               phone.quality_rating === 'YELLOW' ? 'bg-warning' : 'bg-secondary';
            
            html += `
                <div class="form-check d-flex align-items-center justify-content-between mb-2">
                    <div>
                        <input class="form-check-input phone-checkbox" type="checkbox" value="${phone.id}" id="phone_${phone.id}">
                        <label class="form-check-label ms-2" for="phone_${phone.id}">
                            <strong>${phone.display_phone_number}</strong>
                            ${phone.verified_name ? `<br><small class="text-muted">${phone.verified_name}</small>` : ''}
                        </label>
                    </div>
                    <span class="badge ${qualityBadge}">${phone.quality_rating || 'UNKNOWN'}</span>
                </div>
            `;
        });
        
        container.innerHTML = html;
        this.addPhoneNumberEventListeners();
    }
    
    populateTemplates(templates) {
        const container = document.getElementById('templatesContainer');
        
        if (!templates || templates.length === 0) {
            container.innerHTML = '<div class="text-muted text-center py-2">Nenhum template aprovado encontrado</div>';
            document.getElementById('selectAllTemplatesBtn').disabled = true;
            document.getElementById('clearTemplatesBtn').disabled = true;
            return;
        }
        
        let html = '';
        templates.forEach(template => {
            const categoryBadge = template.category === 'MARKETING' ? 'bg-primary' : 
                                template.category === 'UTILITY' ? 'bg-success' : 'bg-info';
            
            html += `
                <div class="form-check d-flex align-items-center justify-content-between mb-2">
                    <div>
                        <input class="form-check-input template-checkbox" type="checkbox" value="${template.name}" id="template_${template.name}">
                        <label class="form-check-label ms-2" for="template_${template.name}">
                            <strong>${template.name}</strong>
                            <small class="text-muted d-block">${template.language} | ${template.category}</small>
                        </label>
                    </div>
                    <div>
                        <span class="badge ${categoryBadge} me-1">${template.category}</span>
                        ${template.has_buttons ? '<i class="fas fa-link text-primary" title="Tem botões"></i>' : ''}
                        ${template.has_parameters ? '<i class="fas fa-code text-info" title="Tem parâmetros"></i>' : ''}
                    </div>
                </div>
            `;
        });
        
        container.innerHTML = html;
        document.getElementById('selectAllTemplatesBtn').disabled = false;
        document.getElementById('clearTemplatesBtn').disabled = false;
        this.addTemplateEventListeners();
    }
    
    addPhoneNumberEventListeners() {
        const checkboxes = document.querySelectorAll('.phone-checkbox');
        checkboxes.forEach(checkbox => {
            checkbox.addEventListener('change', () => {
                this.updateDistributionInfo();
            });
        });
    }
    
    addTemplateEventListeners() {
        const checkboxes = document.querySelectorAll('.template-checkbox');
        checkboxes.forEach(checkbox => {
            checkbox.addEventListener('change', () => {
                this.updateDistributionInfo();
                this.updateTemplateButtons();
            });
        });
    }
    
    clearConnectionData() {
        const phoneContainer = document.getElementById('phoneNumbersContainer');
        if (phoneContainer) {
            phoneContainer.innerHTML = '<div class="text-muted text-center py-2"><i class="fas fa-plug me-1"></i>Conecte-se primeiro para ver os números disponíveis</div>';
        }
        
        const templateContainer = document.getElementById('templatesContainer');
        if (templateContainer) {
            templateContainer.innerHTML = '<div class="text-muted text-center py-2"><i class="fas fa-plug me-1"></i>Conecte-se primeiro para ver os templates disponíveis</div>';
        }
        
        document.getElementById('selectAllTemplatesBtn').disabled = true;
        document.getElementById('clearTemplatesBtn').disabled = true;
    }
    
    loadConnectionData() {
        if (this.connectionData) {
            console.log(`${this.connectionData.phone_numbers.length} phone numbers carregados da conexão`);
            this.updateDistributionInfo();
        }
    }
    
    async validateLeads() {
        const leadsText = document.getElementById('leadsInput').value.trim();
        
        if (!leadsText) {
            this.showAlert('Por favor, insira a lista de leads', 'warning');
            return;
        }
        
        const btn = document.getElementById('validateLeadsBtn');
        const originalText = btn.innerHTML;
        
        btn.classList.add('btn-loading');
        btn.disabled = true;
        
        try {
            const response = await fetch('/api/validate-leads', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ leads: leadsText })
            });
            
            const result = await response.json();
            
            if (response.ok) {
                this.leads = result.leads;
                this.validationErrors = result.errors;
                this.displayValidationResults(result);
            } else {
                this.showAlert(result.error || 'Erro na validação', 'danger');
            }
            
        } catch (error) {
            console.error('Error validating leads:', error);
            this.showAlert('Erro de conexão com o servidor', 'danger');
        } finally {
            btn.classList.remove('btn-loading');
            btn.disabled = false;
            btn.innerHTML = originalText;
        }
    }
    
    displayValidationResults(result) {
        const validationDiv = document.getElementById('leadsValidation');
        
        // Update counters
        document.getElementById('validCount').textContent = result.total_valid;
        document.getElementById('errorCount').textContent = result.total_errors;
        document.getElementById('totalCount').textContent = result.original_count || (result.total_valid + result.total_errors);
        
        // Show validation div
        validationDiv.classList.remove('d-none');
        
        // Update distribution info
        this.updateDistributionInfo();
        
        // Show errors if any
        if (result.errors && result.errors.length > 0) {
            const errorsDiv = document.getElementById('validationErrors');
            const errorsList = document.getElementById('errorsList');
            
            let errorsHtml = '';
            result.errors.slice(0, 10).forEach(error => {
                errorsHtml += `<li class="text-danger small">${error}</li>`;
            });
            
            if (result.errors.length > 10) {
                errorsHtml += `<li class="text-muted small">... e mais ${result.errors.length - 10} erros</li>`;
            }
            
            errorsList.innerHTML = errorsHtml;
            errorsDiv.classList.remove('d-none');
        }
    }
    
    updateDistributionInfo() {
        const selectedPhones = this.getSelectedPhoneNumbers();
        const selectedTemplates = this.getSelectedTemplates();
        const validLeads = this.leads.length;
        
        const distributionInfo = document.getElementById('distributionInfo');
        const phoneNumbersCount = document.getElementById('phoneNumbersCount');
        const templatesCount = document.getElementById('templatesCount');
        const validLeadsCount = document.getElementById('validLeadsCount');
        
        if (phoneNumbersCount) phoneNumbersCount.textContent = selectedPhones.length;
        if (templatesCount) templatesCount.textContent = selectedTemplates.length;
        if (validLeadsCount) validLeadsCount.textContent = validLeads;
        
        if (distributionInfo) {
            if (selectedPhones.length > 0 && selectedTemplates.length > 0 && validLeads > 0) {
                distributionInfo.classList.remove('d-none');
            } else {
                distributionInfo.classList.add('d-none');
            }
        }
        
        // Update send button
        const sendButton = document.getElementById('smartDistributionBtn');
        if (sendButton) {
            sendButton.disabled = !(selectedPhones.length > 0 && selectedTemplates.length > 0 && validLeads > 0);
        }
    }
    
    getSelectedPhoneNumbers() {
        const checkboxes = document.querySelectorAll('.phone-checkbox:checked');
        const phones = [];
        checkboxes.forEach(checkbox => {
            phones.push({
                id: checkbox.value,
                displayName: checkbox.nextElementSibling.textContent.trim()
            });
        });
        return phones;
    }
    
    getSelectedTemplates() {
        const checkboxes = document.querySelectorAll('#templatesContainer input[type="checkbox"]:checked');
        const templates = [];
        checkboxes.forEach(checkbox => {
            templates.push({
                name: checkbox.value,
                displayName: checkbox.getAttribute('data-display-name') || checkbox.value
            });
        });
        return templates;
    }
    
    selectAllTemplates() {
        const checkboxes = document.querySelectorAll('#templatesContainer .template-checkbox');
        checkboxes.forEach(checkbox => {
            checkbox.checked = true;
        });
        this.updateDistributionInfo();
        this.updateTemplateButtons();
        this.showAlert('Todos os templates selecionados', 'success');
    }
    
    clearTemplateSelection() {
        const checkboxes = document.querySelectorAll('#templatesContainer .template-checkbox');
        checkboxes.forEach(checkbox => {
            checkbox.checked = false;
        });
        this.updateDistributionInfo();
        this.updateTemplateButtons();
        this.showAlert('Seleção de templates limpa', 'info');
    }
    
    updateTemplateButtons() {
        const checkboxes = document.querySelectorAll('#templatesContainer .template-checkbox');
        const checkedCount = document.querySelectorAll('#templatesContainer .template-checkbox:checked').length;
        const totalCount = checkboxes.length;
        
        const selectAllBtn = document.getElementById('selectAllTemplatesBtn');
        const clearBtn = document.getElementById('clearTemplatesBtn');
        
        if (selectAllBtn) selectAllBtn.disabled = totalCount === 0;
        if (clearBtn) clearBtn.disabled = checkedCount === 0;
    }
    
    async sendSmartDistribution() {
        const selectedTemplates = this.getSelectedTemplates();
        const phoneNumbers = this.getSelectedPhoneNumbers();
        
        if (this.leads.length === 0) {
            this.showAlert('Primeiro valide os leads antes de enviar', 'warning');
            return;
        }
        
        if (selectedTemplates.length === 0) {
            this.showAlert('Selecione pelo menos um template', 'warning');
            return;
        }
        
        if (phoneNumbers.length === 0) {
            this.showAlert('Selecione pelo menos um número de telefone', 'warning');
            return;
        }
        
        if (!confirm(`Confirmar envio de ${this.leads.length} mensagens usando ${phoneNumbers.length} números e ${selectedTemplates.length} templates?`)) {
            return;
        }
        
        try {
            this.showProgressPanel();
            
            const leadsText = this.leads.map(lead => `${lead.numero},${lead.nome},${lead.cpf}`).join('\n');
            
            const requestData = {
                leads: leadsText,
                template_names: selectedTemplates.map(t => t.name),
                phone_number_ids: phoneNumbers.map(p => p.id)
            };
            
            const response = await fetch('/api/ultra-speed', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestData)
            });
            
            const result = await response.json();
            
            if (response.ok && result.success) {
                this.showAlert('Envio iniciado com sucesso!', 'success');
                
                // Start progress tracking
                const sessionId = result.session_id;
                this.trackProgress(sessionId);
            } else {
                // Check for specific error types
                if (response.status === 401 || result.error_type === 'expired_token') {
                    this.showAlert('⚠️ TOKEN EXPIRADO: Seu token WhatsApp expirou. Por favor, obtenha um novo token e reconecte.', 'warning');
                    this.disconnect(); // Force disconnect to show connection form
                } else {
                    this.showAlert(result.error || 'Erro ao iniciar envio', 'danger');
                }
            }
            
        } catch (error) {
            console.error('Error sending messages:', error);
            this.showAlert('Erro de conexão com o servidor', 'danger');
        }
    }
    
    trackProgress(sessionId) {
        const checkProgress = async () => {
            try {
                const response = await fetch(`/api/progress/${sessionId}`);
                const data = await response.json();
                
                if (data.success) {
                    const { sent, total, failed, progress, status } = data;
                    
                    document.getElementById('progressBar').style.width = `${progress}%`;
                    document.getElementById('progressPercent').textContent = `${progress}%`;
                    document.getElementById('sentProgress').textContent = sent;
                    document.getElementById('totalProgress').textContent = total;
                    document.getElementById('errorProgress').textContent = failed;
                    
                    if (status === 'completed' || progress >= 100) {
                        this.showAlert(`Envio concluído! ${sent} mensagens enviadas de ${total}`, 'success');
                        return;
                    }
                    
                    setTimeout(checkProgress, 1000);
                }
            } catch (error) {
                console.error('Error checking progress:', error);
            }
        };
        
        checkProgress();
    }
    
    showProgressPanel() {
        const progressPanel = document.getElementById('progressPanel');
        if (progressPanel) {
            progressPanel.classList.remove('d-none');
        }
    }
    
    resetValidation() {
        const validationDiv = document.getElementById('leadsValidation');
        if (validationDiv) {
            validationDiv.classList.add('d-none');
        }
        
        this.leads = [];
        this.updateDistributionInfo();
    }
    
    showAlert(message, type = 'info') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        const container = document.querySelector('.container');
        container.insertBefore(alertDiv, container.firstChild);
        
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }
}

// Initialize the application when the page loads
document.addEventListener('DOMContentLoaded', function() {
    window.app = new WhatsAppSender();
});