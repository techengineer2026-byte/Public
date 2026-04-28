// Function to handle any form on your site
function initWeb3Form(formId, btnId, btnTextId, spinnerId) {
  const form = document.getElementById(formId);
  if (!form) return;

  const btn = document.getElementById(btnId);
  const btnText = document.getElementById(btnTextId);
  const spinner = document.getElementById(spinnerId);
  const successModal = new bootstrap.Modal(document.getElementById('successModal'));

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    // Show loading
    btn.disabled = true;
    btnText.classList.add('d-none');
    spinner.classList.remove('d-none');

    const formData = new FormData(form);
    const object = Object.fromEntries(formData);
    const json = JSON.stringify(object);

    fetch('https://api.web3forms.com/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: json
    })
      .then(async (response) => {
        if (response.status == 200) {
          successModal.show();
          form.reset();
        } else {
          alert("Something went wrong. Please try again.");
        }
      })
      .catch(error => {
        alert("Check your internet connection.");
      })
      .finally(() => {
        // Hide loading
        btn.disabled = false;
        btnText.classList.remove('d-none');
        spinner.classList.add('d-none');
      });
  });
}

// Initialize all 3 forms
// 1. Main Contact Form
initWeb3Form('contact-form', 'mainSubmitBtn', 'mainBtnText', 'mainBtnSpinner');

// 2. Guest Form
initWeb3Form('guest-form', 'guestSubmitBtn', 'guestBtnText', 'guestBtnSpinner');

// 3. Footer Form
initWeb3Form('subscriptionForm', 'submitBtn', 'btnText', 'btnSpinner');