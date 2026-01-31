// Navigation
document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', () => {
        const viewName = item.dataset.view;
        document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
        item.classList.add('active');
        document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
        document.getElementById(viewName).classList.add('active');
    });
});

// Patient Management
let patients = [];
let currentFilter = 'all';

function addPatient() {
    const newPatient = {
        id: Date.now(),
        name: 'John Doe',
        gender: 'Male',
        age: 45,
        diagnosis: 'Hypertension',
        phone: '555-0123',
        address: '123 Main St',
        blood: 'O+',
        triage: 'non-urgent',
        avatar: `https://i.pravatar.cc/150?img=${Math.floor(Math.random() * 70) + 1}` 
    };
    
    patients.push(newPatient);
    renderPatients();
    updateMetrics();
}

function filterPatients() {
    currentFilter = document.getElementById('status-filter').value;
    renderPatients();
}

function renderPatients() {
    const tbody = document.getElementById('patients-tbody');
    const emptyState = document.getElementById('empty-state');
    
    let filteredPatients = patients;
    if (currentFilter !== 'all') {
        filteredPatients = patients.filter(p => p.triage === currentFilter);
    }
    
    if (filteredPatients.length === 0) {
        tbody.innerHTML = '';
        emptyState.style.display = 'block';
        return;
    }
    
    emptyState.style.display = 'none';
    tbody.innerHTML = filteredPatients.map(patient => `
        <tr onclick="showPatientDetail()">
            <td>
                <div class="patient-cell">
                    <img src="${patient.avatar}" class="patient-avatar">
                    <span>${patient.name}</span>
                </div>
            </td>
            <td>${patient.gender}</td>
            <td>${patient.age}</td>
            <td>${patient.diagnosis}</td>
            <td>${patient.phone}</td>
            <td>${patient.address}</td>
            <td>${patient.blood}</td>
            <td><span class="triage-badge triage-${patient.triage}">${patient.triage.replace('-', ' ').toUpperCase()}</span></td>
        </tr>
    `).join('');
}

function updateMetrics() {
    // Update total patients
    const totalPatientsElement = document.querySelector('.metric-value');
    if (totalPatientsElement) {
        totalPatientsElement.textContent = patients.length;
    }
    
    // Update emergency cases
    const emergencyCases = patients.filter(p => p.triage === 'emergency').length;
    const emergencyElement = document.querySelectorAll('.metric-value')[1];
    if (emergencyElement) {
        emergencyElement.textContent = emergencyCases;
    }
}

function showPatientDetail() {
    document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
    document.getElementById('patient-detail').classList.add('active');
    document.querySelectorAll('.nav-item')[2].classList.add('active');
}

function toggleAiExplanation() {
    document.getElementById('ai-explanation').classList.toggle('hidden');
}

function logDecision(action) {
    const logList = document.getElementById('ai-log-list');
    const now = new Date();
    const time = String(now.getHours()).padStart(2, '0') + ':' + String(now.getMinutes()).padStart(2, '0');
    const li = document.createElement('li');
    li.textContent = `Decision Logged: ${action} at ${time}`;
    logList.appendChild(li);
    
    // Update notification counts
    const badge = document.getElementById('notification-count');
    badge.textContent = parseInt(badge.textContent) + 1;
    
    const aiBadge = document.getElementById('ai-notification-badge');
    aiBadge.textContent = parseInt(aiBadge.textContent) + 1;
    aiBadge.classList.add('ai-notification-badge-active', 'ai-notification-shake');
    setTimeout(() => aiBadge.classList.remove('ai-notification-shake'), 600);
}

function updateTime() {
    const now = new Date();
    document.getElementById('current-time').textContent = now.toLocaleTimeString('en-US', { hour12: false });
}

// Dynamic AI state cycling
(function() {
    const states = [
        {
            risk: 'HIGH',
            riskClass: 'ai-risk-high',
            trend: '↓',
            trendColor: '#15803d',
            changeText: 'Risk decreased in last 3 hours',
            confidence: 76,
            icuOccupancy: '65%',
            bedsAvailable: '6',
            resourceMessage: 'Step-down monitoring preferred while ICU capacity stabilizes.',
            nurseWorkload: 'Moderate',
            specialistAvailability: 'Available',
            notify: false
        },
        {
            risk: 'CRITICAL',
            riskClass: 'ai-risk-critical',
            trend: '↑',
            trendColor: '#b91c1c',
            changeText: 'Risk increased in last 3 hours',
            confidence: 88,
            icuOccupancy: '92%',
            bedsAvailable: '1',
            resourceMessage: 'Escalation urgency increased due to limited ICU availability.',
            nurseWorkload: 'High',
            specialistAvailability: 'Limited',
            notify: true
        }
    ];

    let currentState = 1; // Start with CRITICAL

    function applyState(state) {
        const badge = document.getElementById('ai-risk-badge');
        const trend = document.getElementById('ai-risk-trend');
        const changeText = document.getElementById('ai-risk-change');
        const confidenceValue = document.getElementById('ai-confidence-value');
        const confidenceFill = document.getElementById('ai-confidence-fill');
        const icuOcc = document.getElementById('ai-icu-occupancy');
        const beds = document.getElementById('ai-beds-available');
        const resourceMsg = document.getElementById('ai-resource-message');
        const nurses = document.getElementById('ai-workload-nurses');
        const specialists = document.getElementById('ai-workload-specialists');
        const aiBadge = document.getElementById('ai-notification-badge');

        badge.textContent = state.risk;
        badge.className = 'ai-risk-badge ' + state.riskClass;
        if (state.risk === 'CRITICAL') badge.classList.add('ai-risk-badge-pulse');

        trend.textContent = state.trend;
        trend.style.color = state.trendColor;

        changeText.textContent = state.changeText;
        confidenceValue.textContent = state.confidence + '%';
        confidenceFill.style.width = state.confidence + '%';

        icuOcc.textContent = state.icuOccupancy;
        beds.textContent = state.bedsAvailable;
        resourceMsg.textContent = state.resourceMessage;
        nurses.textContent = state.nurseWorkload;
        specialists.textContent = state.specialistAvailability;

        if (state.notify) {
            const current = parseInt(aiBadge.textContent) || 0;
            aiBadge.textContent = current + 1;
            aiBadge.classList.add('ai-notification-badge-active', 'ai-notification-shake');
            setTimeout(() => aiBadge.classList.remove('ai-notification-shake'), 600);
        }
    }

    // Cycle states every 6 seconds
    setInterval(() => {
        currentState = (currentState + 1) % states.length;
        applyState(states[currentState]);
    }, 6000);
})();

// Bed Availability Data
const bedData = [
    { room: 'ICU-101', department: 'ICU', totalBeds: 5, occupiedBeds: 3 },
    { room: 'GEN-201', department: 'General', totalBeds: 10, occupiedBeds: 7 },
    { room: 'MAT-301', department: 'Maternity', totalBeds: 8, occupiedBeds: 8 },
    { room: 'EMR-401', department: 'Emergency', totalBeds: 6, occupiedBeds: 2 },
];

function updateBedAvailability() {
    const tbody = document.getElementById('bed-availability-tbody');
    tbody.innerHTML = '';

    let totalBeds = 0;
    let totalOccupied = 0;

    bedData.forEach(({ room, department, totalBeds: beds, occupiedBeds }) => {
        const availableBeds = beds - occupiedBeds;
        const availabilityBadge = availableBeds === 0
            ? '<span class="triage-badge triage-emergency">Occupied</span>'
            : availableBeds === beds
            ? '<span class="triage-badge triage-non-urgent">Available</span>'
            : '<span class="triage-badge triage-urgent">Partially Occupied</span>';

        tbody.innerHTML += `
            <tr>
                <td>${room}</td>
                <td>${department}</td>
                <td>${beds}</td>
                <td>${occupiedBeds}</td>
                <td>${availabilityBadge}</td>
            </tr>
        `;

        totalBeds += beds;
        totalOccupied += occupiedBeds;
    });

    const totalAvailable = totalBeds - totalOccupied;
    const usagePercentage = Math.round((totalOccupied / totalBeds) * 100);

    document.getElementById('total-beds').textContent = totalBeds;
    document.getElementById('occupied-beds').textContent = totalOccupied;
    document.getElementById('available-beds').textContent = totalAvailable;
    document.getElementById('bed-usage').textContent = `${usagePercentage}%`;
}

// Simulate real-time updates
setInterval(() => {
    const randomRoom = Math.floor(Math.random() * bedData.length);
    const room = bedData[randomRoom];
    if (room.occupiedBeds < room.totalBeds) {
        room.occupiedBeds += Math.random() > 0.5 ? 1 : 0;
    } else {
        room.occupiedBeds -= Math.random() > 0.5 ? 1 : 0;
    }
    updateBedAvailability();
}, 5000);

// Initialize
updateTime();
setInterval(updateTime, 1000);
renderPatients();
updateBedAvailability();
