const STORAGE_KEY = 'task-planner-data-v1';
const columns = [
  'Serial Number',
  'Daily TASK',
  'Frequency',
  'Assigned to',
  'Department',
  'Click Up',
  'Last Update',
  'Re-check after?',
  'Red Mark Date',
  'Status',
  'Notes',
];

const formulaText = '=IF(I3>0,H3+I3,"")';
const computedColumn = 'Red Mark Date';
const displayDateFormatter = new Intl.DateTimeFormat('en-GB', {
  day: '2-digit',
  month: 'short',
  year: '2-digit',
  timeZone: 'UTC',
});

const seededRows = [
  { 'Serial Number': '1', 'Daily TASK': 'Onboarding sheet column AD, red colors need re-onboarding.', 'Frequency': 'Every Saturday', 'Assigned to': 'Jyoti', 'Department': 'Operations', 'Click Up': 'https://app.clickup.com/t/86d1pnx4v', 'Last Update': '2026-03-05', 'Re-check after?': '7', 'Red Mark Date': '2026-03-12', Status: 'Open', Notes: 'Seeded from the shared sheet snapshot.' },
  { 'Serial Number': '2', 'Daily TASK': 'Strategy Planner, Column F fill every one (onboarding sheet).', 'Frequency': 'Every 2 days', 'Assigned to': 'Jyoti', 'Department': 'Operations', 'Click Up': 'https://app.clickup.com/t/86d1pp1hq', 'Last Update': '2026-03-10', 'Re-check after?': '5', 'Red Mark Date': '2026-03-15', Status: 'In Progress', Notes: '' },
  { 'Serial Number': '3', 'Daily TASK': 'Daily morning list.', 'Frequency': 'Daily', 'Assigned to': 'Jyoti', 'Department': 'Operations', 'Click Up': 'https://app.clickup.com/t/86d1qr7qj', 'Last Update': '2026-03-12', 'Re-check after?': '2', 'Red Mark Date': '2026-03-14', Status: 'Open', Notes: '' },
  { 'Serial Number': '4', 'Daily TASK': 'moneydhan compliance email check', 'Frequency': 'Daily', 'Assigned to': 'Swathi/Sachin', 'Department': 'Compliance MD', 'Click Up': 'https://app.clickup.com/t/86d0893dg', 'Last Update': '2026-03-16', 'Re-check after?': '2', 'Red Mark Date': '2026-03-18', Status: 'Open', Notes: '' },
  { 'Serial Number': '5', 'Daily TASK': 'sujith moneydhan email || moneydhancompliance@gmail.com', 'Frequency': 'Daily', 'Assigned to': 'Swathi', 'Department': 'Compliance MD', 'Click Up': 'https://app.clickup.com/t/86cx7fckm', 'Last Update': '2026-03-16', 'Re-check after?': '2', 'Red Mark Date': '2026-03-18', Status: 'Open', Notes: '' },
  { 'Serial Number': '6', 'Daily TASK': 'Check if any onboarded with Moneydhan?', 'Frequency': 'Adhoc', 'Assigned to': 'Jyoti', 'Department': 'Operations', 'Click Up': 'https://app.clickup.com/t/86cx844vt', 'Last Update': '2026-03-12', 'Re-check after?': '7', 'Red Mark Date': '2026-03-19', Status: 'In Progress', Notes: '' },
  { 'Serial Number': '7', 'Daily TASK': 'surveillance/compliance email check weekly for axis or mosl', 'Frequency': 'Every Saturday', 'Assigned to': 'Hardeep', 'Department': 'Compliance', 'Click Up': 'https://app.clickup.com/t/86cydu6zx', 'Last Update': '2026-03-11', 'Re-check after?': '7', 'Red Mark Date': '2026-03-18', Status: 'Open', Notes: '' },
  { 'Serial Number': '8', 'Daily TASK': 'GST Invoices', 'Frequency': 'Monthly 1st week', 'Assigned to': 'Swathi', 'Department': 'Finance', 'Click Up': 'https://app.clickup.com/t/86cyfeth7', 'Last Update': '2026-03-02', 'Re-check after?': '27', 'Red Mark Date': '2026-03-29', Status: 'Done', Notes: '' },
  { 'Serial Number': '9', 'Daily TASK': 'Mr and Mrs Gala Pnl to be shared', 'Frequency': 'Every Saturday', 'Assigned to': 'Swathi/Sachin', 'Department': 'Finance', 'Click Up': 'https://app.clickup.com/t/86d088vcj', 'Last Update': '2026-03-16', 'Re-check after?': '6', 'Red Mark Date': '2026-03-22', Status: 'Open', Notes: '' },
  { 'Serial Number': '10', 'Daily TASK': 'Axis daily mail forward to the Order', 'Frequency': 'Daily', 'Assigned to': 'Swathi', 'Department': 'Operations', 'Click Up': 'https://app.clickup.com/t/86cz3n6x1', 'Last Update': '2026-03-16', 'Re-check after?': '1', 'Red Mark Date': '2026-03-17', Status: 'Done', Notes: '' },
  { 'Serial Number': '11', 'Daily TASK': 'SEBI scores to be checked', 'Frequency': 'Every Monday', 'Assigned to': 'Swathi', 'Department': 'Compliance', 'Click Up': 'https://app.clickup.com/t/86d1pntj7', 'Last Update': '2026-03-13', 'Re-check after?': '7', 'Red Mark Date': '2026-03-20', Status: 'Open', Notes: '' },
  { 'Serial Number': '12', 'Daily TASK': 'Second Agreement pending daily check in pre onboarding', 'Frequency': 'Every 2 days', 'Assigned to': 'Jyoti', 'Department': 'Pre-onboarding', 'Click Up': 'https://app.clickup.com/t/86d1vqwv6', 'Last Update': '2026-03-12', 'Re-check after?': '5', 'Red Mark Date': '2026-03-17', Status: 'In Progress', Notes: '' },
  { 'Serial Number': '13', 'Daily TASK': 'CBOS MOSL Account opening SOP / teach Jyothi', 'Frequency': 'Adhoc', 'Assigned to': 'Swathi', 'Department': 'Training', 'Click Up': 'https://app.clickup.com/t/86d1rvxg8', 'Last Update': '2026-03-13', 'Re-check after?': '4', 'Red Mark Date': '2026-03-17', Status: 'In Progress', Notes: 'Original row looked marked as no update.' },
  { 'Serial Number': '14', 'Daily TASK': 'study excella holding sujith', 'Frequency': 'Every 2 days', 'Assigned to': 'Sujith', 'Department': 'Research', 'Click Up': 'https://app.clickup.com/t/86d22u6n1', 'Last Update': '2026-02-24', 'Re-check after?': '2', 'Red Mark Date': '2026-02-26', Status: 'Open', Notes: '' },
  { 'Serial Number': '15', 'Daily TASK': 'update kra people', 'Frequency': 'Daily', 'Assigned to': 'Aishwarya', 'Department': 'KRA', 'Click Up': 'https://app.clickup.com/t/86cx64ukk', 'Last Update': '2026-03-16', 'Re-check after?': '3', 'Red Mark Date': '2026-03-19', Status: 'Open', Notes: '' },
  { 'Serial Number': '16', 'Daily TASK': 'Learn how to re-onboard using digio single', 'Frequency': 'Adhoc', 'Assigned to': 'Aishwarya', 'Department': 'Training', 'Click Up': 'https://app.clickup.com/t/86d1pnu66', 'Last Update': '2026-03-16', 'Re-check after?': '5', 'Red Mark Date': '2026-03-21', Status: 'Open', Notes: '' },
  { 'Serial Number': '17', 'Daily TASK': 'go to zulip shyamli channel and find who received the last email days back', 'Frequency': 'Daily', 'Assigned to': 'Shyamli', 'Department': 'Client Ops', 'Click Up': 'https://app.clickup.com/t/86d1pqaq5', 'Last Update': '2026-03-13', 'Re-check after?': '2', 'Red Mark Date': '2026-03-15', Status: 'Open', Notes: '' },
  { 'Serial Number': '18', 'Daily TASK': 'Strategy meet planner F column, if red, update existing documents', 'Frequency': 'Adhoc', 'Assigned to': '', 'Department': 'Strategy', 'Click Up': 'https://app.clickup.com/t/86d22u74e', 'Last Update': '', 'Re-check after?': '', 'Red Mark Date': '', Status: 'Open', Notes: '' },
  { 'Serial Number': '19', 'Daily TASK': 'sachin prepare for mosl audit', 'Frequency': 'Daily', 'Assigned to': 'Sachin', 'Department': 'Urgent', 'Click Up': 'https://app.clickup.com/t/86d2827jp', 'Last Update': '2026-03-09', 'Re-check after?': '1', 'Red Mark Date': '', Status: 'In Progress', Notes: 'Original row had no update text.' },
  { 'Serial Number': '20', 'Daily TASK': 'Rent Agreement - Near noorji', 'Frequency': 'Adhoc', 'Assigned to': '', 'Department': 'Admin', 'Click Up': 'https://app.clickup.com/t/86d22u7b1', 'Last Update': '', 'Re-check after?': '', 'Red Mark Date': '', Status: 'Open', Notes: '' },
  { 'Serial Number': '21', 'Daily TASK': 'SIP planner Jan data, click up fill aishwarya', 'Frequency': 'Adhoc', 'Assigned to': 'Aishwarya/Hardeep', 'Department': 'SIP Planner', 'Click Up': 'https://app.clickup.com/t/86d2aqxj1', 'Last Update': '2026-03-16', 'Re-check after?': '1', 'Red Mark Date': '2026-03-17', Status: 'In Progress', Notes: '' },
  { 'Serial Number': '22', 'Daily TASK': 'SHyamli Excella column M, sip tracker', 'Frequency': 'Adhoc', 'Assigned to': 'Shyamli', 'Department': 'SIP Tracker', 'Click Up': 'https://app.clickup.com/t/86d1v1nbd', 'Last Update': '2026-03-13', 'Re-check after?': '5', 'Red Mark Date': '2026-03-18', Status: 'Open', Notes: '' },
  { 'Serial Number': '23', 'Daily TASK': 'Trade Book (shyamli)', 'Frequency': 'Adhoc', 'Assigned to': 'Shyamli', 'Department': 'Trade Book', 'Click Up': 'https://app.clickup.com/t/86d1pqbmh', 'Last Update': '2026-02-13', 'Re-check after?': '', 'Red Mark Date': '', Status: 'Open', Notes: '' },
];

const statsGrid = document.getElementById('statsGrid');
const tableHead = document.getElementById('tableHead');
const tableBody = document.getElementById('tableBody');
const rowCountBadge = document.getElementById('rowCountBadge');
const searchInput = document.getElementById('searchInput');
const departmentFilter = document.getElementById('departmentFilter');
const assigneeFilter = document.getElementById('assigneeFilter');
const statusFilter = document.getElementById('statusFilter');
const fileInput = document.getElementById('fileInput');
const rowDialog = document.getElementById('rowDialog');
const rowForm = document.getElementById('rowForm');
const formFields = document.getElementById('formFields');

let state = loadRows();

function escapeHtml(value) {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function toIsoDate(value) {
  if (!value) return '';
  if (value instanceof Date && !Number.isNaN(value.getTime())) {
    return value.toISOString().slice(0, 10);
  }

  const text = String(value).trim();
  if (!text) return '';

  const isoMatch = text.match(/^(\d{4})-(\d{2})-(\d{2})$/);
  if (isoMatch) return `${isoMatch[1]}-${isoMatch[2]}-${isoMatch[3]}`;

  const displayMatch = text.match(/^(\d{1,2})-([A-Za-z]{3})-(\d{2}|\d{4})$/);
  if (displayMatch) {
    const [, day, monthName, year] = displayMatch;
    const monthIndex = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'].indexOf(monthName.toLowerCase());
    if (monthIndex >= 0) {
      const fullYear = year.length === 2 ? `20${year}` : year;
      return `${fullYear}-${String(monthIndex + 1).padStart(2, '0')}-${String(Number(day)).padStart(2, '0')}`;
    }
  }

  if (/^\d{1,2}\/\d{1,2}\/\d{2,4}$/.test(text)) {
    const [day, month, year] = text.split('/');
    const fullYear = year.length === 2 ? `20${year}` : year;
    return `${fullYear}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`;
  }

  const parsed = new Date(text);
  if (Number.isNaN(parsed.getTime())) return '';
  return new Date(Date.UTC(parsed.getFullYear(), parsed.getMonth(), parsed.getDate())).toISOString().slice(0, 10);
}

function formatDisplayDate(value) {
  const iso = toIsoDate(value);
  if (!iso) return '';
  return displayDateFormatter.format(new Date(`${iso}T00:00:00Z`)).replace(/ /g, '-');
}

function normalizeDateField(value) {
  const iso = toIsoDate(value);
  return iso ? formatDisplayDate(iso) : '';
}

function computeRedMarkDate(lastUpdate, recheckAfter) {
  const isoLastUpdate = toIsoDate(lastUpdate);
  const days = Number.parseInt(recheckAfter, 10);
  if (!isoLastUpdate || !Number.isFinite(days) || days <= 0) return '';
  const date = new Date(`${isoLastUpdate}T00:00:00Z`);
  date.setUTCDate(date.getUTCDate() + days);
  return formatDisplayDate(date);
}

function normalizeRow(row, fallbackSerialNumber = '') {
  const normalized = {};
  columns.forEach((column) => {
    const value = row[column] ?? '';
    normalized[column] = column.includes('Date') || column === 'Last Update'
      ? normalizeDateField(value)
      : String(value).trim();
  });
  normalized['Serial Number'] = String(normalized['Serial Number'] || fallbackSerialNumber || '');
  normalized.Status = normalized.Status || 'Open';
  normalized[computedColumn] = computeRedMarkDate(normalized['Last Update'], normalized['Re-check after?']);
  return normalized;
}

function normalizeRows(rows) {
  return rows.map((row, index) => normalizeRow(row, index + 1));
}

function loadRows() {
  const stored = localStorage.getItem(STORAGE_KEY);
  if (!stored) return normalizeRows(structuredClone(seededRows));
  try {
    const parsed = JSON.parse(stored);
    return Array.isArray(parsed) ? normalizeRows(parsed) : normalizeRows(structuredClone(seededRows));
  } catch {
    return normalizeRows(structuredClone(seededRows));
  }
}

function persistAndRender() {
  saveRows();
  renderTable();
}

function saveRows() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

function getTodayIso() {
  return new Date().toISOString().slice(0, 10);
}

function isDueOrOverdue(value) {
  const iso = toIsoDate(value);
  return Boolean(iso) && iso <= getTodayIso();
}

function getFilteredRows() {
  const search = searchInput.value.trim().toLowerCase();
  return state.filter((row) => {
    const deptMatch = departmentFilter.value === 'all' || row['Department'] === departmentFilter.value;
    const assigneeMatch = assigneeFilter.value === 'all' || row['Assigned to'] === assigneeFilter.value;
    const statusMatch = statusFilter.value === 'all' || row.Status === statusFilter.value;
    const searchMatch = !search || Object.values(row).some((value) => String(value).toLowerCase().includes(search));
    return deptMatch && assigneeMatch && statusMatch && searchMatch;
  });
}

function uniqueOptions(key) {
  return [...new Set(state.map((row) => row[key]).filter(Boolean))].sort((a, b) => a.localeCompare(b));
}

function renderFilters() {
  const populate = (select, label, values) => {
    const current = select.value;
    select.innerHTML = `<option value="all">All ${label}</option>` + values.map((value) => `<option value="${escapeHtml(value)}">${escapeHtml(value)}</option>`).join('');
    if ([...select.options].some((option) => option.value === current)) select.value = current;
  };

  populate(departmentFilter, 'departments', uniqueOptions('Department'));
  populate(assigneeFilter, 'assignees', uniqueOptions('Assigned to'));
}

function renderStats(rows) {
  const open = rows.filter((row) => row.Status === 'Open').length;
  const inProgress = rows.filter((row) => row.Status === 'In Progress').length;
  const done = rows.filter((row) => row.Status === 'Done').length;
  const dueOrOverdue = rows.filter((row) => isDueOrOverdue(row[computedColumn])).length;
  const cards = [
    ['Visible rows', rows.length],
    ['Open tasks', open],
    ['In progress', inProgress],
    ['Done', done],
    ['Due / overdue', dueOrOverdue],
  ];
  statsGrid.innerHTML = cards.map(([label, value]) => `<article class="stat-card card"><h3>${label}</h3><strong>${value}</strong></article>`).join('');
}

function renderTable() {
  renderFilters();
  const rows = getFilteredRows();
  renderStats(rows);
  rowCountBadge.textContent = `${rows.length} rows shown · J formula ${formulaText} · Dates DD-MMM-YY`;
  tableHead.innerHTML = `<tr>${columns.map((column) => `<th>${escapeHtml(column)}</th>`).join('')}<th>Actions</th></tr>`;
  tableBody.innerHTML = rows.map((row) => {
    const originalIndex = state.indexOf(row);
    const dueClass = isDueOrOverdue(row[computedColumn]) ? 'due-row' : '';
    return `
      <tr class="${dueClass}">
        ${columns.map((column) => renderCell(row, column, originalIndex)).join('')}
        <td>
          <div class="row-actions">
            <button class="ghost-btn" onclick="duplicateRow(${originalIndex})">Duplicate</button>
            <button class="ghost-btn delete-btn" onclick="deleteRow(${originalIndex})">Delete</button>
          </div>
        </td>
      </tr>`;
  }).join('');
}

function renderCell(row, column, index) {
  if (column === 'Status') {
    return `<td><select class="cell-input" onchange="updateCell(${index}, 'Status', this.value)">
      ${['Open', 'In Progress', 'Done'].map((status) => `<option value="${status}" ${row.Status === status ? 'selected' : ''}>${status}</option>`).join('')}
    </select></td>`;
  }

  if (column === computedColumn) {
    const value = row[column] || '—';
    const highlightClass = isDueOrOverdue(row[column]) ? ' due-today' : '';
    return `<td><div class="readonly-cell${highlightClass}" title="Auto-calculated with ${formulaText}">${escapeHtml(value)}</div></td>`;
  }

  const value = row[column] ?? '';
  const safeValue = escapeHtml(value);
  const isLongText = ['Daily TASK', 'Notes', 'Click Up'].includes(column);
  if (isLongText) {
    return `<td><textarea class="cell-textarea" onchange="updateCell(${index}, '${column}', this.value)">${safeValue}</textarea></td>`;
  }

  const inputMode = column === 'Re-check after?' || column === 'Serial Number' ? 'numeric' : 'text';
  const placeholder = column === 'Last Update' ? 'DD-MMM-YY' : '';
  return `<td><input class="cell-input" inputmode="${inputMode}" placeholder="${placeholder}" value="${safeValue}" onchange="updateCell(${index}, '${column}', this.value)" /></td>`;
}

function updateCell(index, column, value) {
  if (column === computedColumn) return;
  state[index][column] = column.includes('Date') || column === 'Last Update' ? normalizeDateField(value) : String(value).trim();
  state[index][computedColumn] = computeRedMarkDate(state[index]['Last Update'], state[index]['Re-check after?']);
  persistAndRender();
}
window.updateCell = updateCell;

function deleteRow(index) {
  state.splice(index, 1);
  persistAndRender();
}
window.deleteRow = deleteRow;

function duplicateRow(index) {
  const cloned = normalizeRow(structuredClone(state[index]), nextSerialNumber());
  cloned['Serial Number'] = String(nextSerialNumber());
  state.splice(index + 1, 0, cloned);
  persistAndRender();
}
window.duplicateRow = duplicateRow;

function nextSerialNumber() {
  return Math.max(0, ...state.map((row) => Number(row['Serial Number']) || 0)) + 1;
}

function getExportRows() {
  return state.map((row) => ({ ...row, [computedColumn]: computeRedMarkDate(row['Last Update'], row['Re-check after?']) }));
}

function exportFile(type) {
  const exportRows = getExportRows();
  if (type === 'csv') {
    const worksheet = XLSX.utils.json_to_sheet(exportRows, { header: columns });
    const csv = XLSX.utils.sheet_to_csv(worksheet);
    downloadBlob(csv, 'task-planner.csv', 'text/csv;charset=utf-8;');
    return;
  }
  downloadBlob(JSON.stringify(exportRows, null, 2), 'task-planner.json', 'application/json;charset=utf-8;');
}

function downloadBlob(content, filename, mimeType) {
  const blob = new Blob([content], { type: mimeType });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = filename;
  link.click();
  URL.revokeObjectURL(link.href);
}

function parseUploadedRows(rows) {
  const [headerRow, ...dataRows] = rows.filter((row) => row.some((cell) => cell !== undefined && cell !== ''));
  if (!headerRow) return;
  state = dataRows.map((row, rowIndex) => {
    const mapped = {};
    columns.forEach((column) => {
      const sourceIndex = headerRow.findIndex((header) => String(header).trim().toLowerCase() === column.toLowerCase());
      mapped[column] = sourceIndex >= 0 ? (row[sourceIndex] ?? '') : '';
    });
    return normalizeRow(mapped, rowIndex + 1);
  });
  persistAndRender();
}

function handleUpload(event) {
  const file = event.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = ({ target }) => {
    if (file.name.endsWith('.json')) {
      state = normalizeRows(JSON.parse(target.result));
      persistAndRender();
      return;
    }
    const workbook = XLSX.read(target.result, { type: 'binary' });
    const firstSheet = workbook.Sheets[workbook.SheetNames[0]];
    parseUploadedRows(XLSX.utils.sheet_to_json(firstSheet, { header: 1, defval: '' }));
  };
  reader.readAsBinaryString(file);
}

function buildForm() {
  formFields.innerHTML = columns.map((column) => {
    const isLongText = ['Daily TASK', 'Notes', 'Click Up'].includes(column);
    if (column === 'Status') {
      return `<label>${column}<select name="${column}"><option>Open</option><option>In Progress</option><option>Done</option></select></label>`;
    }
    if (column === computedColumn) {
      return `<label>${column}<input name="${column}" value="Auto-calculated with ${formulaText}" readonly /></label>`;
    }
    if (isLongText) {
      return `<label>${column}<textarea name="${column}"></textarea></label>`;
    }
    const placeholder = column === 'Last Update' ? 'DD-MMM-YY' : '';
    return `<label>${column}<input name="${column}" placeholder="${placeholder}" ${column === 'Serial Number' ? 'readonly' : ''} /></label>`;
  }).join('');
}

function openDialog() {
  buildForm();
  rowForm.reset();
  rowForm.elements['Serial Number'].value = nextSerialNumber();
  rowForm.elements.Status.value = 'Open';
  rowDialog.showModal();
}

searchInput.addEventListener('input', renderTable);
departmentFilter.addEventListener('change', renderTable);
assigneeFilter.addEventListener('change', renderTable);
statusFilter.addEventListener('change', renderTable);
fileInput.addEventListener('change', handleUpload);
document.getElementById('exportCsvBtn').addEventListener('click', () => exportFile('csv'));
document.getElementById('exportJsonBtn').addEventListener('click', () => exportFile('json'));
document.getElementById('addRowBtn').addEventListener('click', openDialog);
document.getElementById('resetDataBtn').addEventListener('click', () => {
  state = normalizeRows(structuredClone(seededRows));
  persistAndRender();
});
document.getElementById('closeDialogBtn').addEventListener('click', () => rowDialog.close());
document.getElementById('cancelDialogBtn').addEventListener('click', () => rowDialog.close());
rowForm.addEventListener('submit', (event) => {
  event.preventDefault();
  const formData = new FormData(rowForm);
  const row = normalizeRow(Object.fromEntries(formData.entries()), nextSerialNumber());
  state.unshift(row);
  persistAndRender();
  rowDialog.close();
});

renderTable();
