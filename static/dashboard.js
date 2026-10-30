let rows = [];

const formatMoney = (value) => {
  return new Intl.NumberFormat('en-NG', {
    style: 'currency',
    currency: 'NGN',
    maximumFractionDigits: 0,
  }).format(value);
};

const updateKpis = () => {
  const approved = rows.filter((row) => (row.decision || row.status || '').toLowerCase().includes('approve')).length;
  const review = rows.filter((row) => (row.decision || row.status || '').toLowerCase().includes('review')).length;
  const highRisk = rows.filter((row) => (row.decision || '').toLowerCase().includes('risk')).length;
  const revenue = rows.reduce((total, row) => total + (row.recommended_price || 0), 0);
  const exposure = rows
    .filter((row) => (row.decision || '').toLowerCase().includes('risk'))
    .reduce((total, row) => total + (row.recommended_price || 0), 0);

  const values = {
    'kpi-total': rows.length,
    'kpi-approved': approved,
    'kpi-review': review,
    'kpi-risk': highRisk,
    'kpi-revenue': formatMoney(revenue),
    'kpi-exposure': formatMoney(exposure),
  };

  Object.entries(values).forEach(([id, value]) => {
    const element = document.getElementById(id);
    if (element) element.textContent = value;
  });
};

const renderTable = (items = rows) => {
  const tbody = document.getElementById('history-body');
  if (!tbody) return;

  if (!items.length) {
    tbody.innerHTML = '<tr><td colspan="5" class="empty-state">No quotes have been analyzed yet.</td></tr>';
    return;
  }

  tbody.innerHTML = items.map((row) => {
    const decision = row.decision || row.status || 'DRAFT';
    const badgeClass = decision.toLowerCase().includes('approve') ? 'approve'
      : decision.toLowerCase().includes('risk') ? 'risk' : 'review';

    return `
      <tr>
        <td>${new Date(row.created_at).toLocaleDateString()}</td>
        <td>${row.customer_id ? `Customer #${row.customer_id}` : 'Unassigned'}</td>
        <td>${row.service_type}</td>
        <td>${formatMoney(row.recommended_price)}</td>
        <td><span class="decision-badge ${badgeClass}">${decision}</span></td>
      </tr>
    `;
  }).join('');
};

const populateFilters = () => {
  const customers = [...new Set(rows.map((item) => item.customer_id).filter(Boolean))];
  const services = [...new Set(rows.map((item) => item.service_type))];

  const customerSelect = document.getElementById('filter-customer');
  const serviceSelect = document.getElementById('filter-service');

  if (customerSelect) {
    customerSelect.innerHTML = '<option value="all">All customers</option>' + customers.map((customer) => `
      <option value="${customer}">Customer #${customer}</option>
    `).join('');
  }

  if (serviceSelect) {
    serviceSelect.innerHTML = '<option value="all">All services</option>' + services.map((service) => `
      <option value="${service}">${service}</option>
    `).join('');
  }
};

const applyFilters = () => {
  const dateValue = document.getElementById('filter-date')?.value || '';
  const customerValue = document.getElementById('filter-customer')?.value || 'all';
  const serviceValue = document.getElementById('filter-service')?.value || 'all';
  const decisionValue = document.getElementById('filter-decision')?.value || 'all';
  const riskValue = document.getElementById('filter-risk')?.value || 'all';
  const priceValue = document.getElementById('filter-price')?.value || '';

  const filtered = rows.filter((row) => {
    if (dateValue && row.date !== dateValue) return false;
    if (customerValue !== 'all' && String(row.customer_id) !== customerValue) return false;
    if (serviceValue !== 'all' && row.service_type !== serviceValue) return false;
    if (decisionValue !== 'all' && (row.decision || row.status) !== decisionValue) return false;
    if (riskValue !== 'all' && row.risk !== riskValue) return false;

    if (priceValue) {
      const match = priceValue.split('-').map(Number);
      if (match.length === 2) {
        const [min, max] = match;
        if (row.recommended_price < min || row.recommended_price > max) return false;
      }
    }

    return true;
  });

  renderTable(filtered);
};

const bindFilters = () => {
  ['filter-date', 'filter-customer', 'filter-service', 'filter-decision', 'filter-risk', 'filter-price']
    .forEach((id) => {
      const el = document.getElementById(id);
      if (el) el.addEventListener('input', applyFilters);
      if (el) el.addEventListener('change', applyFilters);
    });
};

const loadQuotes = async () => {
  try {
    const response = await fetch('/quotes/');
    if (!response.ok) throw new Error('Unable to load quotes');
    rows = await response.json();
    updateKpis();
    populateFilters();
    renderTable();
    bindFilters();
  } catch (error) {
    const tbody = document.getElementById('history-body');
    if (tbody) tbody.innerHTML = '<tr><td colspan="5" class="empty-state">Quote history is unavailable right now.</td></tr>';
  }
};

loadQuotes();
