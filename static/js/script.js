document.addEventListener('DOMContentLoaded', function() {
    // Sync the length picked by user:
    // if user choose length from range -> adjust the textbox
    // if user choose length from the text -> adjust the range
    const lengthInput = document.getElementById('pwdlength');
    const rangeInput = document.getElementById('rangeInput');

    function adjustPasswordLength(value){
        if(value > 30){
            lengthInput.value = 30;
            rangeInput.value = 30;
        } else if(value < 1){
            lengthInput.value = 8;
            rangeInput.value = 8;
        } else{
            rangeInput.value = value;
        }
    }

    lengthInput.addEventListener('input', function(){
        let value = parseInt(this.value, 10) || 8;
        adjustPasswordLength(value);
    });

    rangeInput.addEventListener('input', function(){
        let value = parseInt(this.value, 10) || 8;
        adjustPasswordLength(value);
    });

    // uppercase, lowercase, numbers, symbols
    // Make sure at least one checkbox is selected
    const checkboxes = document.querySelectorAll('.checkbox')
    function enforceCheckboxSelection() {
        let checkCount = Array.from(checkboxes).filter(checkbox => checkbox.checked).length;
        if(checkCount === 0){
            this.checked = true;
        }
    }
    // Attach event listeners to each checkbox
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', enforceCheckboxSelection);
    });

    function generatePassword(){
        // Initialize the length of the password based user's selection or set 8 as default
        const length = document.getElementById('pwdlength').value || 8;

        // The character type preferences
        const useUppercase = document.getElementById('uppercase').checked;
        const useLowercase = document.getElementById('lowercase').checked;
        const useNumbers = document.getElementById('numbers').checked;
        const useSymbols = document.getElementById('symbols').checked;

        if (!useUppercase && !useLowercase && !useNumbers && !useSymbols) {
            alert("Please select at least one character type.");
            return;
        }

        fetch('/generate-password', {
            method: 'POST',
            headers: {
                'Content-Type' : 'application/json'
            },
            body: JSON.stringify({
                length: parseInt(length),
                use_uppercase: useUppercase,
                use_lowercase: useLowercase,
                use_numbers: useNumbers,
                use_symbols: useSymbols
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Password generation failed: ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            document.getElementById('password-display').innerText = data.password; // Display new password
        })
        .catch(error => console.error('Error:', error));

    }

    function copyToClipboard(){
        const password = document.getElementById('password-display').innerText;
        navigator.clipboard.writeText(password).then(() => {
            //alert("Password copied to clipboard");
        }).catch(err => {
            console.error('Could not copy text: ', err);
        });
    }

    // Attach event listeners to both icons and button
    document.getElementById('generate-icon').addEventListener('click', generatePassword);
    document.getElementById('copy-icon').addEventListener('click', copyToClipboard);
    document.getElementById('copy-button').addEventListener('click', copyToClipboard);

});