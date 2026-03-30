// 1. Select the form and button
const form = document.getElementById('contact-form'); // Make sure your <form> has id="contact-form"
const submitBtn = document.querySelector('button[type="submit"]');

// 2. Add Event Listener
form.addEventListener('submit', e => {
    e.preventDefault();

    // Change button text to show loading
    const originalBtnText = submitBtn.innerText;
    submitBtn.innerText = "⏳ Sending...";
    submitBtn.disabled = true;

    // 3. YOUR GOOGLE APPS SCRIPT URL HERE
    const scriptURL = 'https://script.google.com/macros/s/AKfycbw009VaTMgpQTuGGHlBI3Ud_3Tv5k6rwie5NRLYPhbV4D1GrzJY82GZbJ7Bh00HX5D-nQ/exec';

    // 4. Send Data
    fetch(scriptURL, { method: 'POST', body: new FormData(form) })
        .then(response => {
            // SUCCESS! 

            // A. Reset the form (clear inputs)
            form.reset();

            // B. Show the Bootstrap Modal
            var myModal = new bootstrap.Modal(document.getElementById('successModal'));
            myModal.show();

            // C. Reset button text
            submitBtn.innerText = originalBtnText;
            submitBtn.disabled = false;
        })
        .catch(error => {
            // ERROR!
            console.error('Error!', error.message);
            alert("Something went wrong. Please try again.");
            submitBtn.innerText = originalBtnText;
            submitBtn.disabled = false;
        });
});

