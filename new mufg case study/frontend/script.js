// API Base URL
const API_BASE = 'http://localhost:5000';

// Global state - FIXED: Maintain original and transformed datasets
let originalDataset = [];
let transformedDataset = [];
let currentColumns = [];
let activeView = 'transformed'; // 'original' or 'transformed'

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initializeUpload();
    initializeCleaning();
    initializeMath();
    initializeFinancial();
    initializeDownload();
});

// Toast notification
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    const icon = toast.querySelector('.toast-icon');
    const messageEl = toast.querySelector('.toast-message');
    
    toast.className = `toast ${type}`;
    messageEl.textContent = message;
    
    if (type === 'success') {
        icon.className = 'toast-icon fas fa-check-circle';
    } else if (type === 'error') {
        icon.className = 'toast-icon fas fa-exclamation-circle';
    } else {
        icon.className = 'toast-icon fas fa-exclamation-triangle';
    }
    
    toast.classList.remove('hidden');
    
    setTimeout(() => {
        toast.classList.add('hidden');
    }, 3000);
}

// Step 1: Upload Dataset
function initializeUpload() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    
    uploadArea.addEventListener('click', () => fileInput.click());
    
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileUpload(files[0]);
        }
    });
    
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileUpload(e.target.files[0]);
        }
    });
}

async function handleFileUpload(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        showToast('Uploading file...', 'warning');
        
        const response = await fetch(`${API_BASE}/upload`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error('Upload failed');
        }
        
        const data = await response.json();
        
        // FIXED: Store both original and transformed (clone)
        // Backend now returns both 'preview' (for display) and 'data' (full dataset)
        const fullDataset = data.data || data.preview; // Use full dataset if available, fallback to preview
        
        originalDataset = JSON.parse(JSON.stringify(fullDataset)); // Deep clone
        transformedDataset = JSON.parse(JSON.stringify(fullDataset)); // Deep clone
        currentColumns = data.columns;
        activeView = 'transformed'; // Default to transformed view
        
        // Display preview but store full dataset
        const previewData = data.preview || fullDataset.slice(0, 100);
        displayPreview(previewData, data.rows, data.columns.length);
        populateColumnSelects(data.columns);
        updateViewToggle(); // Show toggle buttons
        
        // Show next steps
        document.getElementById('step2').classList.remove('hidden');
        document.getElementById('step3').classList.remove('hidden');
        document.getElementById('step4').classList.remove('hidden');
        const resultsSection = document.getElementById('resultsSection');
        if (resultsSection) {
            resultsSection.classList.remove('hidden');
        }
        
        showToast('File uploaded successfully!', 'success');
    } catch (error) {
        showToast('Upload failed: ' + error.message, 'error');
    }
}

function displayPreview(data, rows, cols) {
    const preview = document.getElementById('datasetPreview');
    const table = document.getElementById('previewTable');
    const rowCount = document.getElementById('rowCount');
    const columnCount = document.getElementById('columnCount');
    
    if (!data || data.length === 0) {
        preview.classList.add('hidden');
        return;
    }
    
    const actualRows = rows || data.length;
    const actualCols = cols || (data[0] ? Object.keys(data[0]).length : 0);
    
    rowCount.textContent = `${actualRows} rows`;
    columnCount.textContent = `${actualCols} columns`;
    
    // Clear table
    table.innerHTML = '';
    
    // Create header
    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');
    Object.keys(data[0]).forEach(col => {
        const th = document.createElement('th');
        th.textContent = col;
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
    table.appendChild(thead);
    
    // Create body (show first 100 rows for preview)
    const tbody = document.createElement('tbody');
    data.slice(0, 100).forEach(row => {
        const tr = document.createElement('tr');
        Object.values(row).forEach(val => {
            const td = document.createElement('td');
            td.textContent = val !== null && val !== undefined ? val : '';
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });
    table.appendChild(tbody);
    
    preview.classList.remove('hidden');
}

// FIXED: Render table from active dataset
function renderTable() {
    const dataToShow = activeView === 'original' ? originalDataset : transformedDataset;
    if (!dataToShow || dataToShow.length === 0) return;
    
    const rows = dataToShow.length;
    const cols = dataToShow[0] ? Object.keys(dataToShow[0]).length : 0;
    // Show preview (first 100 rows) but display total row count
    const previewData = dataToShow.slice(0, 100);
    displayPreview(previewData, rows, cols);
}

function populateColumnSelects(columns) {
    const selects = [
        'mathColumn',
        'mathColumn1',
        'mathColumn2',
        'revenueColumn',
        'costColumn',
        'taxColumn',
        'dateColumn'
    ];
    
    selects.forEach(selectId => {
        const select = document.getElementById(selectId);
        if (select) {
            select.innerHTML = '<option value="">-- Select Column --</option>';
            columns.forEach(col => {
                const option = document.createElement('option');
                option.value = col;
                option.textContent = col;
                select.appendChild(option);
            });
        }
    });
}

// FIXED: View Toggle Functions (global for onclick)
window.showOriginal = function() {
    activeView = 'original';
    renderTable();
    updateViewToggle();
    showToast('Viewing: Original Dataset', 'success');
}

window.showTransformed = function() {
    activeView = 'transformed';
    renderTable();
    updateViewToggle();
    showToast('Viewing: Transformed Dataset', 'success');
}

function updateViewToggle() {
    const originalBtn = document.getElementById('viewOriginalBtn');
    const transformedBtn = document.getElementById('viewTransformedBtn');
    
    if (originalBtn && transformedBtn) {
        if (activeView === 'original') {
            originalBtn.classList.add('active');
            transformedBtn.classList.remove('active');
        } else {
            transformedBtn.classList.add('active');
            originalBtn.classList.remove('active');
        }
    }
}

// Step 2: Cleaning Operations
function initializeCleaning() {
    const operationCards = document.querySelectorAll('.operation-card');
    const modal = document.getElementById('cleaningModal');
    const closeModal = document.querySelector('.close-modal');
    
    operationCards.forEach(card => {
        card.addEventListener('click', () => {
            const operation = card.dataset.operation;
            handleCleaningOperation(operation);
        });
    });
    
    closeModal.addEventListener('click', () => {
        modal.classList.add('hidden');
    });
    
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.add('hidden');
        }
    });
}

async function handleCleaningOperation(operation) {
    // FIXED: Use transformedDataset instead of currentData
    if (!transformedDataset || transformedDataset.length === 0) {
        showToast('Please upload a dataset first', 'error');
        return;
    }
    
    try {
        let response;
        
        // FIXED: Always use transformedDataset for operations
        switch(operation) {
            case 'remove-null':
                response = await fetch(`${API_BASE}/clean/remove-null`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ data: transformedDataset })
                });
                break;
                
            case 'remove-duplicate':
                response = await fetch(`${API_BASE}/clean/remove-duplicate`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ data: transformedDataset })
                });
                break;
                
            case 'rename-columns':
                showRenameColumnsModal();
                return;
                
            case 'change-datatypes':
                showChangeDataTypesModal();
                return;
                
            case 'trim-whitespaces':
                response = await fetch(`${API_BASE}/clean/trim-whitespaces`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ data: transformedDataset })
                });
                break;
        }
        
        if (response) {
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Operation failed');
            }
            
            const result = await response.json();
            
            // FIXED: Store transformed data back to transformedDataset
            if (result.data && Array.isArray(result.data)) {
                transformedDataset = JSON.parse(JSON.stringify(result.data)); // Deep clone
                if (result.columns) {
                    currentColumns = result.columns;
                    populateColumnSelects(result.columns);
                }
                activeView = 'transformed'; // Switch to transformed view
                renderTable(); // Use renderTable function
                updateViewToggle();
                showToast('Operation completed successfully!', 'success');
            } else {
                throw new Error('Invalid response format');
            }
        }
    } catch (error) {
        showToast('Operation failed: ' + error.message, 'error');
    }
}

function showRenameColumnsModal() {
    const modal = document.getElementById('cleaningModal');
    const modalBody = document.getElementById('modalBody');
    
    modalBody.innerHTML = `
        <h3>Rename Columns</h3>
        <div style="margin-top: 1rem;">
            ${currentColumns.map((col, idx) => `
                <div style="margin-bottom: 1rem;">
                    <label style="display: block; margin-bottom: 0.5rem; font-weight: 600;">${col}</label>
                    <input type="text" id="rename-${idx}" value="${col}" style="width: 100%; padding: 0.75rem; border: 2px solid #e2e8f0; border-radius: 8px;">
                </div>
            `).join('')}
            <button id="applyRename" class="btn-primary" style="width: 100%; margin-top: 1rem;">Apply Rename</button>
        </div>
    `;
    
    modal.classList.remove('hidden');
    
    document.getElementById('applyRename').addEventListener('click', async () => {
        const renameMap = {};
        currentColumns.forEach((col, idx) => {
            const newName = document.getElementById(`rename-${idx}`).value.trim();
            if (newName && newName !== col) {
                renameMap[col] = newName;
            }
        });
        
        if (Object.keys(renameMap).length === 0) {
            showToast('No columns renamed', 'warning');
            modal.classList.add('hidden');
            return;
        }
        
        try {
            // FIXED: Use transformedDataset
            const response = await fetch(`${API_BASE}/clean/rename-columns`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    data: transformedDataset,
                    rename_map: renameMap
                })
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Rename failed');
            }
            
            const result = await response.json();
            
            // FIXED: Store transformed data
            if (result.data && Array.isArray(result.data)) {
                transformedDataset = JSON.parse(JSON.stringify(result.data)); // Deep clone
                if (result.columns) {
                    currentColumns = result.columns;
                    populateColumnSelects(result.columns);
                }
                activeView = 'transformed';
                renderTable();
                updateViewToggle();
                modal.classList.add('hidden');
                showToast('Columns renamed successfully!', 'success');
            } else {
                throw new Error('Invalid response format');
            }
        } catch (error) {
            showToast('Rename failed: ' + error.message, 'error');
        }
    });
}

function showChangeDataTypesModal() {
    const modal = document.getElementById('cleaningModal');
    const modalBody = document.getElementById('modalBody');
    
    modalBody.innerHTML = `
        <h3>Change Data Types</h3>
        <div style="margin-top: 1rem;">
            ${currentColumns.map((col, idx) => `
                <div style="margin-bottom: 1rem;">
                    <label style="display: block; margin-bottom: 0.5rem; font-weight: 600;">${col}</label>
                    <select id="dtype-${idx}" style="width: 100%; padding: 0.75rem; border: 2px solid #e2e8f0; border-radius: 8px;">
                        <option value="string">String</option>
                        <option value="int">Integer</option>
                        <option value="float">Float</option>
                        <option value="date">Date</option>
                    </select>
                </div>
            `).join('')}
            <button id="applyDtype" class="btn-primary" style="width: 100%; margin-top: 1rem;">Apply Changes</button>
        </div>
    `;
    
    modal.classList.remove('hidden');
    
    document.getElementById('applyDtype').addEventListener('click', async () => {
        const dtypeMap = {};
        currentColumns.forEach((col, idx) => {
            const dtype = document.getElementById(`dtype-${idx}`).value;
            dtypeMap[col] = dtype;
        });
        
        try {
            // FIXED: Use transformedDataset
            const response = await fetch(`${API_BASE}/clean/change-datatypes`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    data: transformedDataset,
                    dtype_map: dtypeMap
                })
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Data type change failed');
            }
            
            const result = await response.json();
            
            // FIXED: Store transformed data
            if (result.data && Array.isArray(result.data)) {
                transformedDataset = JSON.parse(JSON.stringify(result.data)); // Deep clone
                if (result.columns) {
                    currentColumns = result.columns;
                    populateColumnSelects(result.columns);
                }
                activeView = 'transformed';
                renderTable();
                updateViewToggle();
                modal.classList.add('hidden');
                showToast('Data types changed successfully!', 'success');
            } else {
                throw new Error('Invalid response format');
            }
        } catch (error) {
            showToast('Data type change failed: ' + error.message, 'error');
        }
    });
}

// Step 3: Mathematical Operations
function initializeMath() {
    // Single column operations
    document.getElementById('calculateBtn').addEventListener('click', async () => {
        const column = document.getElementById('mathColumn').value;
        const operation = document.getElementById('mathOperation').value;
        
        if (!column || !operation) {
            showToast('Please select column and operation', 'error');
            return;
        }
        
        // FIXED: Use transformedDataset
        if (!transformedDataset || transformedDataset.length === 0) {
            showToast('Please upload a dataset first', 'error');
            return;
        }
        
        try {
            const response = await fetch(`${API_BASE}/math/${operation}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    data: transformedDataset,
                    column: column
                })
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Calculation failed');
            }
            
            const result = await response.json();
            displayMathResult(operation, result.value, column);
        } catch (error) {
            showToast('Calculation failed: ' + error.message, 'error');
        }
    });

    // Two column operations (Add, Subtract, Multiply, Divide)
    document.getElementById('calculateColumnOpBtn').addEventListener('click', async () => {
        const column1 = document.getElementById('mathColumn1').value;
        const column2 = document.getElementById('mathColumn2').value;
        const operation = document.getElementById('mathOperation2').value;
        const resultColumnName = document.getElementById('resultColumnName').value.trim();
        
        if (!column1 || !column2 || !operation) {
            showToast('Please select both columns and operation', 'error');
            return;
        }
        
        if (!transformedDataset || transformedDataset.length === 0) {
            showToast('Please upload a dataset first', 'error');
            return;
        }
        
        try {
            const endpoint = operation === 'add' ? 'add' : 
                           operation === 'subtract' ? 'subtract' :
                           operation === 'multiply' ? 'multiply' : 'divide';
            
            const payload = {
                data: transformedDataset,
                column1: column1,
                column2: column2
            };
            
            if (resultColumnName) {
                payload.result_column = resultColumnName;
            }
            
            const response = await fetch(`${API_BASE}/math/${endpoint}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Operation failed');
            }
            
            const result = await response.json();
            
            // FIXED: Store transformed data
            if (result.data && Array.isArray(result.data)) {
                transformedDataset = JSON.parse(JSON.stringify(result.data)); // Deep clone
                if (result.columns) {
                    currentColumns = result.columns;
                    populateColumnSelects(result.columns);
                }
                activeView = 'transformed';
                renderTable();
                updateViewToggle();
                showToast(`${operation.charAt(0).toUpperCase() + operation.slice(1)} operation completed!`, 'success');
            } else {
                throw new Error('Invalid response format');
            }
        } catch (error) {
            showToast('Operation failed: ' + error.message, 'error');
        }
    });
}

function displayMathResult(operation, value, column) {
    const resultsPanel = document.getElementById('mathResults');
    const statsDisplay = document.getElementById('mathStats');
    
    const operationNames = {
        'sum': 'Sum',
        'average': 'Average',
        'min': 'Minimum',
        'max': 'Maximum',
        'count': 'Count'
    };
    
    const card = document.createElement('div');
    card.className = 'stat-card';
    const label = column ? `${operationNames[operation]} (${column})` : operationNames[operation];
    card.innerHTML = `
        <div class="stat-label">${label}</div>
        <div class="stat-value">${formatNumber(value)}</div>
    `;
    statsDisplay.appendChild(card);
    
    resultsPanel.classList.remove('hidden');
}

function formatNumber(value) {
    if (typeof value === 'number') {
        if (Number.isInteger(value)) {
            return value.toLocaleString();
        } else {
            return value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
        }
    }
    return value;
}

// Step 4: Advanced Financial Operations
function initializeFinancial() {
    const financialBtns = document.querySelectorAll('.btn-financial');
    
    financialBtns.forEach(btn => {
        btn.addEventListener('click', async () => {
            const operation = btn.dataset.financial;
            await handleFinancialOperation(operation);
        });
    });
}

async function handleFinancialOperation(operation) {
    // FIXED: Use transformedDataset
    if (!transformedDataset || transformedDataset.length === 0) {
        showToast('Please upload a dataset first', 'error');
        return;
    }
    
    const revenueCol = document.getElementById('revenueColumn').value;
    const costCol = document.getElementById('costColumn').value;
    const taxCol = document.getElementById('taxColumn').value;
    const dateCol = document.getElementById('dateColumn').value;
    
    try {
        let response;
        const payload = {
            data: transformedDataset
        };
        
        switch(operation) {
            case 'gross-profit':
                if (!revenueCol || !costCol) {
                    showToast('Please select Revenue and Cost columns', 'error');
                    return;
                }
                payload.revenue_column = revenueCol;
                payload.cost_column = costCol;
                response = await fetch(`${API_BASE}/advanced/pl/gross-profit`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                break;
                
            case 'net-profit':
                if (!revenueCol || !costCol || !taxCol) {
                    showToast('Please select Revenue, Cost, and Tax columns', 'error');
                    return;
                }
                payload.revenue_column = revenueCol;
                payload.cost_column = costCol;
                payload.tax_column = taxCol;
                response = await fetch(`${API_BASE}/advanced/pl/net-profit`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                break;
                
            case 'monthly-pl':
                if (!revenueCol || !costCol || !dateCol) {
                    showToast('Please select Revenue, Cost, and Date columns', 'error');
                    return;
                }
                payload.revenue_column = revenueCol;
                payload.cost_column = costCol;
                payload.date_column = dateCol;
                response = await fetch(`${API_BASE}/advanced/pl/monthly`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                break;
                
            case 'quarterly-pl':
                if (!revenueCol || !costCol || !dateCol) {
                    showToast('Please select Revenue, Cost, and Date columns', 'error');
                    return;
                }
                payload.revenue_column = revenueCol;
                payload.cost_column = costCol;
                payload.date_column = dateCol;
                response = await fetch(`${API_BASE}/advanced/pl/quarterly`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                break;
        }
        
        if (response) {
            const result = await response.json();
            displayFinancialResults(operation, result);
            showToast('Financial operation completed!', 'success');
        }
    } catch (error) {
        showToast('Financial operation failed: ' + error.message, 'error');
    }
}

// Download transformed dataset as Excel
function initializeDownload() {
    const btn = document.getElementById('downloadTransformedBtn');
    if (!btn) return;

    btn.addEventListener('click', async () => {
        if (!transformedDataset || transformedDataset.length === 0) {
            showToast('No transformed dataset to download', 'error');
            return;
        }

        try {
            const response = await fetch(`${API_BASE}/download/transformed`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ data: transformedDataset })
            });

            if (!response.ok) {
                let errorMsg = 'Download failed';
                try {
                    const errData = await response.json();
                    if (errData && errData.error) {
                        errorMsg = errData.error;
                    }
                } catch (_) {
                    // ignore JSON parse error
                }
                throw new Error(errorMsg);
            }

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'transformed_dataset.xlsx';
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);

            showToast('Transformed dataset downloaded.', 'success');
        } catch (error) {
            showToast('Download failed: ' + error.message, 'error');
        }
    });
}

function displayFinancialResults(operation, result) {
    const resultsPanel = document.getElementById('financialResults');
    const tablesContainer = document.getElementById('financialTables');
    
    resultsPanel.classList.remove('hidden');
    
    if (operation === 'gross-profit' || operation === 'net-profit') {
        tablesContainer.innerHTML = `
            <div class="financial-section">
                <h4>${operation === 'gross-profit' ? 'Gross Profit' : 'Net Profit'} Results</h4>
                <table class="financial-table">
                    <thead>
                        <tr>
                            <th>Metric</th>
                            <th>Value</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${Object.entries(result).map(([key, value]) => `
                            <tr>
                                <td><strong>${key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}</strong></td>
                                <td>${formatNumber(value)}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;
    } else if (operation === 'monthly-pl') {
        tablesContainer.innerHTML = `
            <div class="financial-section">
                <h4>Monthly P&L Statement</h4>
                <table class="financial-table">
                    <thead>
                        <tr>
                            <th>Month</th>
                            <th>Revenue</th>
                            <th>Cost</th>
                            <th>Profit</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${result.monthly_data.map(row => `
                            <tr>
                                <td><strong>${row.month}</strong></td>
                                <td>${formatNumber(row.revenue)}</td>
                                <td>${formatNumber(row.cost)}</td>
                                <td>${formatNumber(row.profit)}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;
    } else if (operation === 'quarterly-pl') {
        tablesContainer.innerHTML = `
            <div class="financial-section">
                <h4>Quarterly P&L Statement</h4>
                <table class="financial-table">
                    <thead>
                        <tr>
                            <th>Quarter</th>
                            <th>Revenue</th>
                            <th>Cost</th>
                            <th>Profit</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${result.quarterly_data.map(row => `
                            <tr>
                                <td><strong>${row.quarter}</strong></td>
                                <td>${formatNumber(row.revenue)}</td>
                                <td>${formatNumber(row.cost)}</td>
                                <td>${formatNumber(row.profit)}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;
    }
}

