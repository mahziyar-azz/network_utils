document.addEventListener('DOMContentLoaded', () => {
    const errorMsg = document.getElementById('error-msg');
    const resultsDiv = document.getElementById('results');
    const ipInput = document.getElementById('ip');
    const cidrInput = document.getElementById('cidr');

    // Debounce function to limit API calls while typing
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    const handleCalculation = async () => {
        const ip = ipInput.value.trim();
        const cidr = cidrInput.value.trim();

        // If fields are empty, hide everything nicely instead of showing errors
        if (!ip || !cidr) {
            resultsDiv.classList.add('hidden');
            hideError();
            return;
        }

        try {
            // USE THE DYNAMIC URL HERE
            // If CALCULATE_URL is undefined (local testing without template), fall back to '/calculate'
            const url = (typeof CALCULATE_URL !== 'undefined') ? CALCULATE_URL : '/calculate';

            const response = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ ip, cidr })
            });

            // Check if response is OK (handles 404 or 500 server errors)
            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }

            const data = await response.json();

            if (data.success) {
                hideError();
                renderResults(data.data);
            } else {
                showError(data.error);
            }

        } catch (error) {
            console.error("Calculation error", error);
            // I enabled this so you can see the error on your screen now
            showError("Connection Error: " + error.message); 
        }
    };

    // Create the debounced version of the handler (300ms delay)
    const debouncedCalc = debounce(handleCalculation, 300);

    // Attach to input events
    ipInput.addEventListener('input', debouncedCalc);
    cidrInput.addEventListener('input', debouncedCalc);

    function renderResults(data) {
        // Populate Text fields
        setText('res-network', data.network_address);
        setText('res-broadcast', data.broadcast_address);
        setText('res-mask', data.subnet_mask);
        setText('res-usable', data.usable_hosts);
        setText('res-first', data.first_ip);
        setText('res-last', data.last_ip);
        setText('res-total', data.total_hosts);
        setText('res-type', data.type);
        setText('res-class', data.class);
        setText('res-cidr', "/" + data.cidr);

        // Populate Binary fields
        setText('bin-net', data.bin_net);
        setText('bin-bc', data.bin_bc);
        setText('bin-mask', data.bin_mask);

        // Show results
        resultsDiv.classList.remove('hidden');
    }

    function setText(id, value) {
        const el = document.getElementById(id);
        if (el) {
            // Only animate if the content is actually different
            if (el.textContent !== String(value)) {
                el.textContent = value;
                
                // Reset the animation
                el.classList.remove('text-anim');
                
                // Trigger reflow (force browser to acknowledge removal)
                void el.offsetWidth; 
                
                // Re-add class to start animation
                el.classList.add('text-anim');
            }
        }
    }

    function showError(msg) {
        errorMsg.textContent = msg;
        errorMsg.classList.remove('hidden');
    }

    function hideError() {
        errorMsg.classList.add('hidden');
    }
});