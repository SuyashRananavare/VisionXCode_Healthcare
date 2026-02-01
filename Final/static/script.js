// Global State
let appData = {
    hospital_state: {},
    patients: []
};
let currentFilter = 'all';

// ------------------------------------------------------------------
// DATA FETCHING
// ------------------------------------------------------------------

async function fetchHospitalData() {
    try {
        const response = await fetch('/api/recommendations');
        const data = await response.json();

        // Merge backend data with frontend-required fields (like avatar) if missing
        appData.hospital_state = data.hospital_state;
        appData.patients = data.patients.map((p, index) => {
            // Backend provides 'patient_state' and 'recommendations'
            // We flat map some fields for the table
            const state = p.patient_state;
            return {
                id: p.patient_id,
                name: p.name,
                gender: ['Male', 'Female'][index % 2], // Mock gender
                age: 40 + index * 5, // Mock age
                diagnosis: 'Observation', // Mock diagnosis
                phone: '555-010' + index,
                address: 'General Ward',
                blood: 'O+',
                triage: getTriageLevel(state.NEWS2),
                avatar: `https://i.pravatar.cc/150?img=${index + 10}`,
                // Keep the full backend objects
                raw_state: state,
                recommendations: p.recommendations
            };
        });

        renderPatients();
        updateMetrics();
        generateAlerts();
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

function getTriageLevel(news2) {
    if (news2 >= 7) return 'emergency';
    if (news2 >= 5) return 'urgent';
    if (news2 >= 3) return 'delayed';
    return 'non-urgent';
}

// ------------------------------------------------------------------
// NAVIGATION & UI
// ------------------------------------------------------------------

document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', () => {
        const viewName = item.dataset.view;
        document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
        item.classList.add('active');
        document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
        document.getElementById(viewName).classList.add('active');
    });
});

function toggleAiExplanation() {
    document.getElementById('ai-explanation').classList.toggle('hidden');
}

function updateTime() {
    const now = new Date();
    document.getElementById('current-time').textContent = now.toLocaleTimeString('en-US', { hour12: false });
}

// ------------------------------------------------------------------
// PATIENT LIST
// ------------------------------------------------------------------

function filterPatients() {
    currentFilter = document.getElementById('status-filter').value;
    renderPatients();
}

function renderPatients() {
    const tbody = document.getElementById('patients-tbody');
    const emptyState = document.getElementById('empty-state');

    let filtered = appData.patients;
    if (currentFilter !== 'all') {
        filtered = appData.patients.filter(p => p.triage === currentFilter);
    }

    if (filtered.length === 0) {
        tbody.innerHTML = '';
        if (emptyState) emptyState.style.display = 'block';
        return;
    }

    if (emptyState) emptyState.style.display = 'none';

    tbody.innerHTML = filtered.map(patient => `
        <tr onclick="showPatientDetail('${patient.id}')">
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
            <td><span class="triage-badge triage-${patient.triage}">${patient.triage.toUpperCase()}</span></td>
        </tr>
    `).join('');
}

function addPatient() {
    // In a real app, this would post to the backend.
    // For now, we'll just trigger a simulation update on the backend to change state
    fetch('/api/simulate')
        .then(() => fetchHospitalData()) // Refetch to see changes
        .then(() => alert("Simulation Triggered: Patient condition deteriorated!"));
}

function updateMetrics() {
    const total = appData.patients.length;
    const emergency = appData.patients.filter(p => p.triage === 'emergency').length;

    const els = document.querySelectorAll('.metric-value');
    if (els.length >= 2) {
        els[0].textContent = total;
        els[1].textContent = emergency;
    }

    // Update ICU Capacity Metric
    if (appData.hospital_state.beds) {
        // total ICU beds = available + occupied (assumed 10 for demo)
        const available = appData.hospital_state.beds.icu_beds_available;
        const totalICU = 10;
        const occupied = totalICU - available;
        const percent = Math.round((occupied / totalICU) * 100);

        if (els.length >= 3) {
            els[2].textContent = percent + '%';
        }
    }
}

// ------------------------------------------------------------------
// PATIENT DETAILS & AI INSIGHTS
// ------------------------------------------------------------------

function showPatientDetail(patientId) {
    const patient = appData.patients.find(p => p.id === patientId);
    if (!patient) return;

    // Switch view
    document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
    document.getElementById('patient-detail').classList.add('active');
    // Highlight "Patient Details" nav (index 1 usually)
    const navItems = document.querySelectorAll('.nav-item');
    if (navItems[1]) navItems[1].classList.add('active');

    // Populate Header Info
    const infoContainer = document.querySelector('.detail-patient-info');
    infoContainer.innerHTML = `
        <div style="display: flex; align-items: center; gap: 1rem;">
            <img src="${patient.avatar}" style="width: 64px; height: 64px; border-radius: 50%;">
            <div>
                <h2 style="margin: 0; font-size: 1.5rem;">${patient.name}</h2>
                <div style="display: flex; gap: 0.5rem; margin-top: 0.25rem;">
                   <span class="triage-badge triage-${patient.triage}">${patient.triage.toUpperCase()}</span>
                   <span>ID: ${patient.id}</span>
                </div>
            </div>
        </div>
        <div style="margin-top: 1rem; display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; background: #f8fafc; padding: 1rem; border-radius: 0.5rem;">
            <div>
                <div style="font-size: 0.75rem; color: #64748b;">Heart Rate</div>
                <div style="font-size: 1.25rem; font-weight: 600;">${patient.raw_state.RR * 4} <span style="font-size: 0.875rem;">bpm</span></div>
            </div>
             <div>
                <div style="font-size: 0.75rem; color: #64748b;">Blood Pressure</div>
                <div style="font-size: 1.25rem; font-weight: 600;">${patient.raw_state.SBP}/80</div>
            </div>
             <div>
                <div style="font-size: 0.75rem; color: #64748b;">SpO2</div>
                <div style="font-size: 1.25rem; font-weight: 600;">${patient.raw_state.SpO2}%</div>
            </div>
             <div>
                <div style="font-size: 0.75rem; color: #64748b;">NEWS2 Score</div>
                <div style="font-size: 1.25rem; font-weight: 600; color: ${patient.raw_state.NEWS2 > 5 ? '#ef4444' : '#0f172a'}">${patient.raw_state.NEWS2}</div>
            </div>
        </div>
    `;

    // Populate AI Logic
    updateAiInsightCard(patient);
}

function updateAiInsightCard(patient) {
    const recs = patient.recommendations;
    if (!recs || recs.length === 0) return;

    // Take top recommendation
    const topRec = recs[0];
    const confidence = Math.round(topRec.confidence * 100);

    // Risk Level Mapping
    let riskLevel = 'LOW';
    let riskClass = 'ai-risk-low'; // You'd need CSS for this or reuse critical
    if (patient.raw_state.NEWS2 >= 7) { riskLevel = 'CRITICAL'; riskClass = 'ai-risk-critical'; }
    else if (patient.raw_state.NEWS2 >= 5) { riskLevel = 'HIGH'; riskClass = 'ai-risk-high'; }
    else if (patient.raw_state.NEWS2 >= 1) { riskLevel = 'MEDIUM'; riskClass = 'ai-risk-medium'; }

    // DOM Elements
    document.getElementById('ai-risk-badge').textContent = riskLevel;
    document.getElementById('ai-risk-badge').className = `ai-risk-badge ${riskClass} ${riskLevel === 'CRITICAL' ? 'ai-risk-badge-pulse' : ''}`;

    document.getElementById('ai-confidence-value').textContent = confidence + '%';
    document.getElementById('ai-confidence-fill').style.width = confidence + '%';

    // Resource Context
    const beds = appData.hospital_state.beds ? appData.hospital_state.beds.icu_beds_available : 0;
    document.getElementById('ai-beds-available').textContent = beds;

    const nurseLoad = appData.hospital_state.staff ? appData.hospital_state.staff.nurse_load : 0;
    document.getElementById('ai-workload-nurses').textContent = nurseLoad > 0.9 ? 'Overloaded' : (nurseLoad > 0.7 ? 'High' : 'Normal');

    // Dynamic Message
    const msgEl = document.getElementById('ai-resource-message');
    msgEl.textContent = topRec.rationale;

    // Explanation
    const explDiv = document.getElementById('ai-explanation');
    explDiv.innerHTML = `
        <h4>AI Analysis</h4>
        <p>${topRec.explanation}</p>
        <div style="margin-top:8px; font-size: 0.85em; color: #475569; background: #f1f5f9; padding: 8px; border-radius: 4px;">
            <strong>Guideline:</strong> ${topRec.documentation}
        </div>
    `;

    // Decision Buttons (Dynamic based on actions)
    const btnContainer = document.querySelector('.ai-decision-buttons');
    btnContainer.innerHTML = recs.slice(0, 3).map((r, i) => `
        <button class="ai-btn ${i === 0 ? 'ai-btn-primary' : 'ai-btn-secondary'}" 
                onclick="logDecision('${r.action}')">
            ${r.action} (${Math.round(r.confidence * 100)}%)
        </button>
    `).join('');
}

function logDecision(action) {
    const list = document.getElementById('ai-log-list');
    const li = document.createElement('li');
    li.textContent = `${new Date().toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit' })} - Action: ${action}`;
    list.prepend(li);
}

// ------------------------------------------------------------------
// ALERTS
// ------------------------------------------------------------------

function generateAlerts() {
    const alerts = [];

    // 1. Resource Alerts
    if (appData.hospital_state.beds && appData.hospital_state.beds.icu_beds_available === 0) {
        alerts.push({
            type: 'Critical Alert',
            message: 'No ICU beds available! Transfers strictly limited.'
        });
    }

    // 2. Patient Alerts
    appData.patients.forEach(p => {
        if (p.raw_state.NEWS2 >= 7) {
            alerts.push({
                type: 'High Alert',
                message: `Patient ${p.name} (ID: ${p.id}) is deteriorating (NEWS2: ${p.raw_state.NEWS2}).`
            });
        }
    });

    const container = document.querySelector('.alert-container');
    if (container) {
        container.innerHTML = alerts.map(a => `
             <div class="alert-card">
                <div class="alert-header">
                    <h2>${a.type}</h2>
                    <span class="alert-time">Just now</span>
                </div>
                <p class="alert-message">${a.message}</p>
            </div>
        `).join('');

        // Update badge
        const badge = document.getElementById('notification-count');
        if (badge) badge.textContent = alerts.length;
    }
}

// ------------------------------------------------------------------
// INIT
// ------------------------------------------------------------------

updateTime();
setInterval(updateTime, 1000);
fetchHospitalData();
// Poll for updates every 10 seconds
setInterval(fetchHospitalData, 10000);

