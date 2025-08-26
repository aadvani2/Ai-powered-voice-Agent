// Dashboard JavaScript
class DentalDashboard {
    constructor() {
        this.charts = {};
        this.voiceAssistant = null;
        this.currentTime = null;
        this.isRecording = false;
        
        this.initializeDashboard();
        this.setupEventListeners();
        this.loadDashboardData();
        this.startTimeUpdate();
    }
    
    initializeDashboard() {
        console.log('Initializing Dental Dashboard...');
        this.initializeCharts();
        this.initializeVoiceAssistant();
    }
    
    setupEventListeners() {
        // Voice assistant button
        const voiceBtn = document.getElementById('voice-btn');
        if (voiceBtn) {
            voiceBtn.addEventListener('click', () => this.toggleVoiceAssistant());
        }
        
        // Quick action buttons
        const actionBtns = document.querySelectorAll('.action-btn');
        actionBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const action = e.currentTarget.dataset.action;
                this.handleQuickAction(action);
            });
        });
        
        // Chart period selectors
        const appointmentPeriod = document.getElementById('appointment-chart-period');
        if (appointmentPeriod) {
            appointmentPeriod.addEventListener('change', (e) => {
                this.updateAppointmentChart(e.target.value);
            });
        }
        
        const revenuePeriod = document.getElementById('revenue-chart-period');
        if (revenuePeriod) {
            revenuePeriod.addEventListener('change', (e) => {
                this.updateRevenueChart(e.target.value);
            });
        }
        
        // Modal controls
        const appointmentModal = document.getElementById('appointment-modal');
        const closeModalBtn = document.getElementById('close-appointment-modal');
        const cancelBtn = document.getElementById('cancel-appointment');
        
        if (closeModalBtn) {
            closeModalBtn.addEventListener('click', () => this.closeModal(appointmentModal));
        }
        
        if (cancelBtn) {
            cancelBtn.addEventListener('click', () => this.closeModal(appointmentModal));
        }
        
        // Appointment form
        const appointmentForm = document.getElementById('appointment-form');
        if (appointmentForm) {
            appointmentForm.addEventListener('submit', (e) => this.handleAppointmentSubmit(e));
        }
        
        // Close modal when clicking outside
        if (appointmentModal) {
            appointmentModal.addEventListener('click', (e) => {
                if (e.target === appointmentModal) {
                    this.closeModal(appointmentModal);
                }
            });
        }
    }
    
    initializeCharts() {
        // Initialize appointment trends chart
        const appointmentCtx = document.getElementById('appointment-chart');
        if (appointmentCtx) {
            this.charts.appointment = new Chart(appointmentCtx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Appointments',
                        data: [],
                        borderColor: '#667eea',
                        backgroundColor: 'rgba(102, 126, 234, 0.1)',
                        borderWidth: 2,
                        fill: true,
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            grid: {
                                color: '#e2e8f0'
                            }
                        },
                        x: {
                            grid: {
                                display: false
                            }
                        }
                    }
                }
            });
        }
        
        // Initialize revenue chart
        const revenueCtx = document.getElementById('revenue-chart');
        if (revenueCtx) {
            this.charts.revenue = new Chart(revenueCtx, {
                type: 'bar',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Revenue',
                        data: [],
                        backgroundColor: 'rgba(102, 126, 234, 0.8)',
                        borderColor: '#667eea',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            grid: {
                                color: '#e2e8f0'
                            },
                            ticks: {
                                callback: function(value) {
                                    return '$' + value.toLocaleString();
                                }
                            }
                        },
                        x: {
                            grid: {
                                display: false
                            }
                        }
                    }
                }
            });
        }
    }
    
    initializeVoiceAssistant() {
        // Check if browser supports speech recognition
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            this.voiceAssistant = new SpeechRecognition();
            
            this.voiceAssistant.continuous = false;
            this.voiceAssistant.interimResults = false;
            this.voiceAssistant.lang = 'en-US';
            
            this.voiceAssistant.onstart = () => {
                this.isRecording = true;
                this.updateVoiceStatus('Listening...', 'recording');
                this.updateVoiceButton(true);
            };
            
            this.voiceAssistant.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                this.handleVoiceCommand(transcript);
            };
            
            this.voiceAssistant.onerror = (event) => {
                console.error('Speech recognition error:', event.error);
                this.updateVoiceStatus('Error: ' + event.error, 'error');
                this.updateVoiceButton(false);
            };
            
            this.voiceAssistant.onend = () => {
                this.isRecording = false;
                this.updateVoiceStatus('Ready', 'ready');
                this.updateVoiceButton(false);
            };
        } else {
            console.warn('Speech recognition not supported');
            this.updateVoiceStatus('Not Supported', 'disabled');
        }
    }
    
    toggleVoiceAssistant() {
        if (!this.voiceAssistant) {
            alert('Speech recognition is not supported in your browser.');
            return;
        }
        
        if (this.isRecording) {
            this.voiceAssistant.stop();
        } else {
            this.voiceAssistant.start();
        }
    }
    
    updateVoiceStatus(status, type) {
        const statusElement = document.getElementById('voice-status');
        if (statusElement) {
            statusElement.textContent = status;
            statusElement.className = `status-indicator ${type}`;
        }
    }
    
    updateVoiceButton(recording) {
        const voiceBtn = document.getElementById('voice-btn');
        if (voiceBtn) {
            if (recording) {
                voiceBtn.classList.add('recording');
                voiceBtn.innerHTML = '<i class="fas fa-stop"></i><span>Stop Recording</span>';
            } else {
                voiceBtn.classList.remove('recording');
                voiceBtn.innerHTML = '<i class="fas fa-microphone"></i><span>Start Voice Assistant</span>';
            }
        }
    }
    
    handleVoiceCommand(transcript) {
        const transcriptElement = document.getElementById('voice-transcript');
        if (transcriptElement) {
            transcriptElement.innerHTML = `<p><strong>You said:</strong> ${transcript}</p>`;
        }
        
        // Process voice command
        const command = transcript.toLowerCase();
        
        if (command.includes('schedule') || command.includes('appointment')) {
            this.openAppointmentModal();
        } else if (command.includes('patient') || command.includes('lookup')) {
            this.handleQuickAction('patient-lookup');
        } else if (command.includes('availability') || command.includes('available')) {
            this.handleQuickAction('check-availability');
        } else if (command.includes('insurance')) {
            this.handleQuickAction('insurance-check');
        } else {
            // Send to AI for processing
            this.processVoiceQuery(transcript);
        }
    }
    
    async processVoiceQuery(query) {
        try {
            const response = await fetch('/api/voice/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ query: query })
            });
            
            const data = await response.json();
            
            if (data.success) {
                const transcriptElement = document.getElementById('voice-transcript');
                if (transcriptElement) {
                    transcriptElement.innerHTML += `<p><strong>Assistant:</strong> ${data.response}</p>`;
                }
                
                // Speak the response
                this.speakText(data.response);
            }
        } catch (error) {
            console.error('Error processing voice query:', error);
        }
    }
    
    speakText(text) {
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.rate = 0.9;
            utterance.pitch = 1;
            speechSynthesis.speak(utterance);
        }
    }
    
    handleQuickAction(action) {
        switch (action) {
            case 'schedule-appointment':
                this.openAppointmentModal();
                break;
            case 'check-availability':
                this.checkAvailability();
                break;
            case 'patient-lookup':
                this.patientLookup();
                break;
            case 'insurance-check':
                this.insuranceCheck();
                break;
            default:
                console.log('Unknown action:', action);
        }
    }
    
    openAppointmentModal() {
        const modal = document.getElementById('appointment-modal');
        if (modal) {
            modal.classList.add('show');
            this.loadPatients();
        }
    }
    
    closeModal(modal) {
        if (modal) {
            modal.classList.remove('show');
        }
    }
    
    async loadPatients() {
        try {
            const response = await fetch('/api/patients/');
            const data = await response.json();
            
            if (data.success) {
                const select = document.getElementById('patient-select');
                if (select) {
                    select.innerHTML = '<option value="">Select Patient</option>';
                    data.data.forEach(patient => {
                        const option = document.createElement('option');
                        option.value = patient.patient_id;
                        option.textContent = `${patient.first_name} ${patient.last_name}`;
                        select.appendChild(option);
                    });
                }
            }
        } catch (error) {
            console.error('Error loading patients:', error);
        }
    }
    
    async handleAppointmentSubmit(event) {
        event.preventDefault();
        
        const formData = new FormData(event.target);
        const appointmentData = {
            patient_id: formData.get('patient-select'),
            appointment_type: formData.get('appointment-type'),
            scheduled_date: formData.get('appointment-date') + 'T' + formData.get('appointment-time'),
            notes: formData.get('appointment-notes')
        };
        
        try {
            const response = await fetch('/api/appointments/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(appointmentData)
            });
            
            const data = await response.json();
            
            if (data.success) {
                alert('Appointment scheduled successfully!');
                this.closeModal(document.getElementById('appointment-modal'));
                this.loadDashboardData();
            } else {
                alert('Error scheduling appointment: ' + data.error);
            }
        } catch (error) {
            console.error('Error scheduling appointment:', error);
            alert('Error scheduling appointment. Please try again.');
        }
    }
    
    async loadDashboardData() {
        await Promise.all([
            this.loadStatistics(),
            this.loadTodayAppointments(),
            this.loadRecentPatients(),
            this.loadChartData()
        ]);
    }
    
    async loadStatistics() {
        try {
            const response = await fetch('/api/dashboard/statistics');
            const data = await response.json();
            
            if (data.success) {
                this.updateStatistics(data.data);
            }
        } catch (error) {
            console.error('Error loading statistics:', error);
        }
    }
    
    updateStatistics(stats) {
        const elements = {
            'total-patients': stats.total_patients || 0,
            'today-appointments': stats.today_appointments || 0,
            'monthly-revenue': '$' + (stats.monthly_revenue || 0).toLocaleString(),
            'pending-appointments': stats.pending_appointments || 0
        };
        
        Object.entries(elements).forEach(([id, value]) => {
            const element = document.getElementById(id);
            if (element) {
                element.textContent = value;
            }
        });
    }
    
    async loadTodayAppointments() {
        try {
            const response = await fetch('/api/appointments/?date=' + new Date().toISOString().split('T')[0]);
            const data = await response.json();
            
            if (data.success) {
                this.displayTodayAppointments(data.data);
            }
        } catch (error) {
            console.error('Error loading today\'s appointments:', error);
        }
    }
    
    displayTodayAppointments(appointments) {
        const container = document.getElementById('today-appointments-list');
        if (!container) return;
        
        container.innerHTML = '';
        
        if (appointments.length === 0) {
            container.innerHTML = '<p class="no-data">No appointments today</p>';
            return;
        }
        
        appointments.forEach(appointment => {
            const item = document.createElement('div');
            item.className = 'activity-item';
            item.innerHTML = `
                <div class="activity-icon">
                    <i class="fas fa-calendar-check"></i>
                </div>
                <div class="activity-content">
                    <h4>${appointment.appointment_type}</h4>
                    <p>Patient: ${appointment.patient_name || 'Unknown'}</p>
                </div>
                <div class="activity-time">
                    ${new Date(appointment.scheduled_date).toLocaleTimeString()}
                </div>
            `;
            container.appendChild(item);
        });
    }
    
    async loadRecentPatients() {
        try {
            const response = await fetch('/api/patients/?limit=5');
            const data = await response.json();
            
            if (data.success) {
                this.displayRecentPatients(data.data);
            }
        } catch (error) {
            console.error('Error loading recent patients:', error);
        }
    }
    
    displayRecentPatients(patients) {
        const container = document.getElementById('recent-patients-list');
        if (!container) return;
        
        container.innerHTML = '';
        
        patients.forEach(patient => {
            const item = document.createElement('div');
            item.className = 'activity-item';
            item.innerHTML = `
                <div class="activity-icon">
                    <i class="fas fa-user"></i>
                </div>
                <div class="activity-content">
                    <h4>${patient.first_name} ${patient.last_name}</h4>
                    <p>${patient.email}</p>
                </div>
                <div class="activity-time">
                    ${new Date(patient.created_at).toLocaleDateString()}
                </div>
            `;
            container.appendChild(item);
        });
    }
    
    async loadChartData() {
        await Promise.all([
            this.updateAppointmentChart(30),
            this.updateRevenueChart(30)
        ]);
    }
    
    async updateAppointmentChart(days) {
        try {
            const response = await fetch(`/api/dashboard/appointments?days=${days}`);
            const data = await response.json();
            
            if (data.success && this.charts.appointment) {
                this.charts.appointment.data.labels = data.data.labels;
                this.charts.appointment.data.datasets[0].data = data.data.values;
                this.charts.appointment.update();
            }
        } catch (error) {
            console.error('Error updating appointment chart:', error);
        }
    }
    
    async updateRevenueChart(days) {
        try {
            const response = await fetch(`/api/dashboard/revenue?days=${days}`);
            const data = await response.json();
            
            if (data.success && this.charts.revenue) {
                this.charts.revenue.data.labels = data.data.labels;
                this.charts.revenue.data.datasets[0].data = data.data.values;
                this.charts.revenue.update();
            }
        } catch (error) {
            console.error('Error updating revenue chart:', error);
        }
    }
    
    startTimeUpdate() {
        this.updateTime();
        setInterval(() => this.updateTime(), 1000);
    }
    
    updateTime() {
        const timeElement = document.getElementById('current-time');
        if (timeElement) {
            const now = new Date();
            timeElement.textContent = now.toLocaleString();
        }
    }
    
    checkAvailability() {
        alert('Availability check feature coming soon!');
    }
    
    patientLookup() {
        alert('Patient lookup feature coming soon!');
    }
    
    insuranceCheck() {
        alert('Insurance check feature coming soon!');
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new DentalDashboard();
});

// Export for use in other modules
window.DentalDashboard = DentalDashboard;
