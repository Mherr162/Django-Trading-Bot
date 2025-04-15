// Custom Pair Functionality
document.addEventListener('DOMContentLoaded', function() {
    console.log("Custom pair script loaded");
    
    // Get elements
    const symbolSelect = document.getElementById('symbol');
    const customPairContainer = document.getElementById('custom-pair-container');
    const customSymbolInput = document.getElementById('custom_symbol');
    const addToDropdownBtn = document.getElementById('add-to-dropdown');
    const closeCustomPairBtn = document.getElementById('close-custom-pair');
    const customPairError = document.getElementById('custom-pair-error');
    
    // Log element existence
    console.log("Elements found:", {
        symbolSelect: !!symbolSelect,
        customPairContainer: !!customPairContainer,
        customSymbolInput: !!customSymbolInput,
        addToDropdownBtn: !!addToDropdownBtn,
        closeCustomPairBtn: !!closeCustomPairBtn,
        customPairError: !!customPairError
    });
    
    // Function to show custom pair input
    function showCustomPairInput() {
        console.log("Showing custom pair input");
        if (customPairContainer) {
            customPairContainer.classList.add('visible');
            customSymbolInput.required = true;
            symbolSelect.name = 'symbol_select'; // Change name to avoid form submission conflict
            
            // Focus on the custom pair input
            setTimeout(() => {
                customSymbolInput.focus();
            }, 100);
        }
    }
    
    // Function to hide custom pair input
    function hideCustomPairInput() {
        console.log("Hiding custom pair input");
        if (customPairContainer) {
            customPairContainer.classList.remove('visible');
            customSymbolInput.required = false;
            symbolSelect.name = 'symbol'; // Restore original name
            customPairError.textContent = '';
        }
    }
    
    // Handle dropdown change
    if (symbolSelect) {
        // Add event listener
        symbolSelect.addEventListener('change', function() {
            console.log("Symbol select changed to:", this.value);
            if (this.value === 'custom') {
                showCustomPairInput();
            } else {
                hideCustomPairInput();
            }
        });
        
        // Check if custom pair is selected on page load
        if (symbolSelect.value === 'custom') {
            console.log("Custom pair selected on page load");
            showCustomPairInput();
        }
    }
    
    // Close custom pair input
    if (closeCustomPairBtn) {
        // Add event listener
        closeCustomPairBtn.addEventListener('click', function() {
            console.log("Close button clicked");
            symbolSelect.value = 'BTC/USDT'; // Reset to default
            hideCustomPairInput();
        });
    }

    // Validate custom trading pair format
    if (customSymbolInput) {
        // Add event listener
        customSymbolInput.addEventListener('input', function() {
            console.log("Custom symbol input changed:", this.value);
            validateCustomPair(this.value);
        });
        
        // Also validate on blur
        customSymbolInput.addEventListener('blur', function() {
            console.log("Custom symbol input blurred:", this.value);
            validateCustomPair(this.value);
        });
    }
    
    // Function to validate custom pair
    function validateCustomPair(value) {
        console.log("Validating custom pair:", value);
        const pattern = /^[A-Z]+/[A-Z]+$/;
        
        if (value) {
            if (pattern.test(value)) {
                customSymbolInput.setCustomValidity('');
                customPairError.textContent = '';
                customPairError.classList.remove('warning');
                customPairError.classList.add('success');
                addToDropdownBtn.disabled = false;
                console.log("Valid format, button enabled");
            } else {
                customSymbolInput.setCustomValidity('Please use format: BASE/QUOTE (e.g., LINK/USDT)');
                customPairError.textContent = 'Invalid format. Use BASE/QUOTE (e.g., LINK/USDT)';
                customPairError.classList.remove('success');
                customPairError.classList.add('warning');
                addToDropdownBtn.disabled = true;
                console.log("Invalid format, button disabled");
            }
        } else {
            customPairError.textContent = '';
            customPairError.classList.remove('success', 'warning');
            addToDropdownBtn.disabled = true;
            console.log("Empty input, button disabled");
        }
    }

    // Add custom pair to dropdown
    if (addToDropdownBtn) {
        // Add event listener
        addToDropdownBtn.addEventListener('click', function() {
            console.log("Add to dropdown button clicked");
            const customSymbol = customSymbolInput.value.trim();
            
            // Check if the pair already exists in the dropdown
            let optionExists = false;
            for (let i = 0; i < symbolSelect.options.length; i++) {
                if (symbolSelect.options[i].value === customSymbol) {
                    optionExists = true;
                    break;
                }
            }
            
            if (!optionExists) {
                // Create a new option
                const newOption = document.createElement('option');
                newOption.value = customSymbol;
                newOption.textContent = customSymbol;
                
                // Insert before the "Custom Pair..." option
                const customOption = symbolSelect.querySelector('option[value="custom"]');
                symbolSelect.insertBefore(newOption, customOption);
                
                // Show success message
                customPairError.textContent = `Added ${customSymbol} to dropdown menu`;
                customPairError.classList.remove('warning');
                customPairError.classList.add('success');
                
                // Reset after 3 seconds
                setTimeout(() => {
                    customPairError.textContent = '';
                    customPairError.classList.remove('success');
                }, 3000);
                
                console.log("Added new pair to dropdown:", customSymbol);
            } else {
                // Show message that pair already exists
                customPairError.textContent = `${customSymbol} already exists in dropdown`;
                customPairError.classList.remove('success');
                customPairError.classList.add('warning');
                
                // Reset after 3 seconds
                setTimeout(() => {
                    customPairError.textContent = '';
                    customPairError.classList.remove('warning');
                }, 3000);
                
                console.log("Pair already exists:", customSymbol);
            }
        });
    }

    // Handle form submission with custom pair
    const tradingForm = document.querySelector('.trading-form');
    if (tradingForm) {
        tradingForm.addEventListener('submit', function(e) {
            console.log("Form submitted");
            const symbolSelect = document.getElementById('symbol');
            if (symbolSelect && symbolSelect.value === 'custom') {
                const customSymbol = document.getElementById('custom_symbol').value.trim();
                console.log("Custom symbol on submit:", customSymbol);
                
                if (!customSymbol) {
                    e.preventDefault();
                    alert('Please enter a custom trading pair');
                    console.log("No custom symbol entered");
                    return false;
                }
                
                // Validate format
                const pattern = /^[A-Z]+/[A-Z]+$/;
                if (!pattern.test(customSymbol)) {
                    e.preventDefault();
                    alert('Invalid trading pair format. Please use BASE/QUOTE (e.g., LINK/USDT)');
                    console.log("Invalid custom symbol format");
                    return false;
                }
                
                // Create a hidden input with the custom symbol value
                const hiddenInput = document.createElement('input');
                hiddenInput.type = 'hidden';
                hiddenInput.name = 'symbol';
                hiddenInput.value = customSymbol;
                this.appendChild(hiddenInput);
                console.log("Added hidden input with custom symbol");
            }
            
            return true;
        });
    }
    
    // Force show custom pair container if custom is selected
    if (symbolSelect && symbolSelect.value === 'custom') {
        console.log("Forcing display of custom pair container");
        showCustomPairInput();
    }
    
    // Add a direct click handler to the symbol select for debugging
    if (symbolSelect) {
        symbolSelect.addEventListener('click', function() {
            console.log("Symbol select clicked, current value:", this.value);
        });
    }
    
    // Add a direct click handler to the add to dropdown button for debugging
    if (addToDropdownBtn) {
        addToDropdownBtn.addEventListener('click', function() {
            console.log("Add to dropdown button clicked directly");
        });
    }
    
    // Add a direct click handler to the custom symbol input for debugging
    if (customSymbolInput) {
        customSymbolInput.addEventListener('click', function() {
            console.log("Custom symbol input clicked");
        });
    }
}); 