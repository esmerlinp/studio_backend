document.addEventListener('DOMContentLoaded', function () {
    // DOM Elements
    const familySelect = document.getElementById('familySelect');
    const cycleSelect = document.getElementById('cycleSelect');
    const calendarSelect = document.getElementById('calendarSelect');
    const chargesTable = document.getElementById('chargesTable').querySelector('tbody');
    const selectAllCheckbox = document.getElementById('selectAll');
    const totalPaidDisplay = document.getElementById('totalPaidDisplay');
    const balanceDisplay = document.getElementById('balanceDisplay');

    // Payment Methods
    const cashInput = document.getElementById('cashInput');
    const cardInput = document.getElementById('cardInput');
    const transferInput = document.getElementById('transferInput');
    const creditNoteInput = document.getElementById('creditNoteInput');
    const totalPaymentDisplay = document.getElementById('totalPaymentDisplay');
    const changeDisplay = document.getElementById('changeDisplay');

    // Summary
    const summaryAmount = document.getElementById('summaryAmount');
    const summaryDiscount = document.getElementById('summaryDiscount');
    const summarySurcharge = document.getElementById('summarySurcharge');
    const summaryTax = document.getElementById('summaryTax');
    const summaryTotal = document.getElementById('summaryTotal');
    const btnProcessPayment = document.getElementById('btnProcessPayment');
    const btnNewPayment = document.getElementById('btnNewPayment');

    // State
    let currentCharges = [];
    let selectedCharges = new Set();

    // Format Currency
    const formatCurrency = (amount) => {
        return new Intl.NumberFormat('es-DO', { style: 'currency', currency: 'DOP' }).format(amount);
    };

    // Initialize Select2 for Family Search
    $(familySelect).select2({
        theme: 'bootstrap-5',
        placeholder: 'Buscar familia...',
        allowClear: true,
        ajax: {
            url: '/api/v1/client/admissions/families', // Verify this endpoint
            dataType: 'json',
            delay: 250,
            headers: {
                'Authorization': 'Bearer ' + localStorage.getItem('access_token_cookie') // Adjust auth header if needed
            },
            data: function (params) {
                return {
                    q: params.term, // search term
                    page: params.page
                };
            },
            processResults: function (data) {
                return {
                    results: data.map(f => ({ id: f.id, text: f.code + ' - ' + f.name }))
                };
            }
        }
    });

    // Load Payment Calendar based on Cycle
    async function loadPaymentCalendar() {
        const cycleId = cycleSelect.value;
        if (!cycleId) return;

        try {
            // Adjust endpoint to fetch calendars
            // const response = await fetch(`/api/v1/client/financial/calendars?cycleId=${cycleId}`);
            // const calendars = await response.json();

            // Mock for now
            const months = ['AGO-SEPT', 'OCT', 'NOV', 'DIC', 'ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN'];
            calendarSelect.innerHTML = months.map(m => `<option value="${m}">${m}</option>`).join('');

        } catch (error) {
            console.error('Error loading calendars:', error);
        }
    }

    // Load Pending Charges
    async function loadPendingCharges() {
        const familyId = familySelect.value;
        const cycleId = cycleSelect.value;

        if (!familyId || !cycleId) return;

        try {
            const response = await fetch(`/api/v1/client/financial/pending-charges?familyId=${familyId}&cycleId=${cycleId}`);
            const data = await response.json();
            currentCharges = data;
            renderCharges();
            loadBalance();
        } catch (error) {
            console.error('Error loading charges:', error);
            chargesTable.innerHTML = `<tr><td colspan="11" class="text-center text-danger">Error al cargar cargos</td></tr>`;
        }
    }

    // Load Family Balance
    async function loadBalance() {
        const familyId = familySelect.value;
        const cycleId = cycleSelect.value;

        try {
            const response = await fetch(`/api/v1/client/financial/balance?familyId=${familyId}&cycleId=${cycleId}`);
            const data = await response.json();
            totalPaidDisplay.value = formatCurrency(data.totalPaid);
            balanceDisplay.value = formatCurrency(data.totalBalance);
        } catch (error) {
            console.error('Error loading balance:', error);
        }
    }

    // Render Charges Table
    function renderCharges() {
        chargesTable.innerHTML = '';

        if (currentCharges.length === 0) {
            chargesTable.innerHTML = `<tr><td colspan="11" class="text-center py-4 text-muted">No hay cargos pendientes</td></tr>`;
            return;
        }

        currentCharges.forEach(charge => {
            const row = document.createElement('tr');
            // If already processed, maybe disable checkbox?

            row.innerHTML = `
                <td><input type="checkbox" class="form-check-input charge-checkbox" data-id="${charge.studentChargeCycleId}" ${selectedCharges.has(charge.studentChargeCycleId.toString()) ? 'checked' : ''}></td>
                <td>${charge.studentCode}</td>
                <td>${charge.studentName}</td>
                <td>${charge.courseName || ''}</td>
                <td>${charge.conceptName}</td>
                <td class="text-end">${formatCurrency(charge.chargeAmount)}</td>
                <td class="text-end text-success">${formatCurrency(charge.totalDiscounts)}</td>
                <td class="text-end text-danger">${formatCurrency(charge.totalSurcharges)}</td>
                <td class="text-end">${formatCurrency(charge.totalItbis)}</td>
                <td class="text-end fw-bold">${formatCurrency(charge.balance)}</td>
                <td></td>
            `;
            chargesTable.appendChild(row);
        });

        updateSummary();
    }

    // Update Totals
    function updateSummary() {
        let amount = 0, discount = 0, surcharge = 0, tax = 0, total = 0;

        const checkboxes = document.querySelectorAll('.charge-checkbox:checked');
        selectedCharges.clear();

        checkboxes.forEach(cb => {
            const id = cb.dataset.id;
            selectedCharges.add(id);
            const charge = currentCharges.find(c => c.studentChargeCycleId == id);

            if (charge) {
                amount += charge.chargeAmount;
                discount += charge.totalDiscounts;
                surcharge += charge.totalSurcharges;
                tax += charge.totalItbis;
                total += charge.balance;
            }
        });

        summaryAmount.textContent = formatCurrency(amount);
        summaryDiscount.textContent = formatCurrency(discount);
        summarySurcharge.textContent = formatCurrency(surcharge);
        summaryTax.textContent = formatCurrency(tax);
        summaryTotal.textContent = formatCurrency(total);

        calculateChange();
        btnProcessPayment.disabled = total === 0;
    }

    // Calculate Payment & Change
    function calculateChange() {
        const cash = parseFloat(cashInput.value) || 0;
        const card = parseFloat(cardInput.value) || 0;
        const transfer = parseFloat(transferInput.value) || 0;
        const credit = parseFloat(creditNoteInput.value) || 0;

        const totalReceived = cash + card + transfer + credit;
        totalPaymentDisplay.textContent = formatCurrency(totalReceived);

        // Parse summary total from text content (remove currency symbols)
        const totalToPay = parseFloat(summaryTotal.textContent.replace(/[^0-9.-]+/g, "")) || 0;

        const change = totalReceived - totalToPay;
        changeDisplay.textContent = formatCurrency(change > 0 ? change : 0);

        if (change < 0 && totalToPay > 0) {
            changeDisplay.classList.add('text-danger');
        } else {
            changeDisplay.classList.remove('text-danger');
        }
    }

    // Events
    familySelect.addEventListener('change', loadPendingCharges);
    cycleSelect.addEventListener('change', loadPendingCharges);
    calendarSelect.addEventListener('change', loadPendingCharges); // Filter logic needed

    selectAllCheckbox.addEventListener('change', function () {
        const checkboxes = document.querySelectorAll('.charge-checkbox');
        checkboxes.forEach(cb => cb.checked = this.checked);
        updateSummary();
    });

    chargesTable.addEventListener('change', function (e) {
        if (e.target.classList.contains('charge-checkbox')) {
            updateSummary();
        }
    });

    [cashInput, cardInput, transferInput, creditNoteInput].forEach(input => {
        input.addEventListener('input', calculateChange);
    });

    btnNewPayment.addEventListener('click', function () {
        location.reload();
    });

    btnProcessPayment.addEventListener('click', async function () {
        if (selectedCharges.size === 0) return;

        const payload = {
            charges: Array.from(selectedCharges),
            paymentMethods: {
                cash: parseFloat(cashInput.value) || 0,
                card: parseFloat(cardInput.value) || 0,
                transfer: parseFloat(transferInput.value) || 0,
                creditNote: parseFloat(creditNoteInput.value) || 0
            }
        };

        try {
            const response = await fetch('/api/v1/client/financial/payment', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            const result = await response.json();

            if (response.ok) {
                alert('Pago procesado correctamente');
                loadPendingCharges();
                // Clear inputs
                [cashInput, cardInput, transferInput, creditNoteInput].forEach(i => i.value = '');
                calculateChange();
            } else {
                alert('Error al procesar pago: ' + result.message);
            }
        } catch (error) {
            console.error('Error submitting payment:', error);
            alert('Error de conexión');
        }
    });

    // Initial Load
    // loadPaymentCalendar();
});
