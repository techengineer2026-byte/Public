// ⚠️ PASTE YOUR GOOGLE APPS SCRIPT WEB APP URL HERE
const GOOGLE_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbynBvaMN4kEl_WsBwoFks2W6FidN9k_22hkEBGFDXTyW6-0j3Px9QpqwHtvgUYit5w5tg/exec';

// Reusable function to handle any form submission
function handleFormSubmit(formConfig) {
  const { formId, statusId, submitBtnId, btnTextId, btnSpinnerId, successMsg } = formConfig;

  const form = document.getElementById(formId);
  const statusMessage = document.getElementById(statusId);
  const submitBtn = document.getElementById(submitBtnId);
  const btnText = document.getElementById(btnTextId);
  const btnSpinner = document.getElementById(btnSpinnerId);

  if (!form) return; // Stop if form doesn't exist on this page

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    // 1. Honeypot check
    const formData = new FormData(form);
    if (formData.get('bot-field')) return; 

    // 2. UI Loading State
    submitBtn.disabled = true;
    btnText.innerHTML = "Sending...";
    btnSpinner.classList.remove('d-none');

    const object = Object.fromEntries(formData.entries());

    fetch(GOOGLE_SCRIPT_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'text/plain;charset=utf-8' },
      body: JSON.stringify(object) 
    })
    .then(async (response) => {
      // Google Scripts sometimes wraps responses in redirects, handle gracefully
      console.log("Form submitted. Check Google Sheets to verify data arrival.");
      statusMessage.innerHTML = `✅ ${successMsg}`;
      statusMessage.style.color = "#25d366";
      form.reset(); 
      submitBtn.disabled = false;
      btnText.innerHTML = `<i class="fas fa-paper-plane me-2"></i> ${successMsg}`;
      btnSpinner.classList.add('d-none');
      
      // Reset button text after 3 seconds
      setTimeout(() => {
        btnText.innerHTML = `<i class="fas fa-paper-plane me-2"></i> Submit`;
      }, 3000);

    })
    .catch(error => {
      console.error("Fetch Error:", error);
      statusMessage.innerHTML = "⚠️ Network error. Please try WhatsApp instead.";
      statusMessage.style.color = "red";
      submitBtn.disabled = false;
      btnText.innerHTML = `<i class="fas fa-paper-plane me-2"></i> Submit`;
      btnSpinner.classList.add('d-none');
    });
  });
}

// Initialize Studio Booking Form (if it exists on the page)
handleFormSubmit({
  formId: 'podcastBookingForm',
  statusId: 'form-status-message',
  submitBtnId: 'submitBtn',
  btnTextId: 'btnText',
  btnSpinnerId: 'btnSpinner',
  successMsg: "Request sent! We will contact you shortly."
});

// Initialize Editing Order Form (if it exists on the page)
handleFormSubmit({
  formId: 'editingOrderForm',
  statusId: 'editing-form-status-message',
  submitBtnId: 'edit-submitBtn',
  btnTextId: 'edit-btnText',
  btnSpinnerId: 'edit-btnSpinner',
  successMsg: "Order received! We will review your footage details."
});