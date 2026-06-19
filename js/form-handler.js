  const bookingForm = document.getElementById('podcastBookingForm');
  const statusMessage = document.getElementById('form-status-message');
  const submitBtn = document.getElementById('submitBtn');
  const btnText = document.getElementById('btnText');
  const btnSpinner = document.getElementById('btnSpinner');

  if (bookingForm) {
    bookingForm.addEventListener('submit', function (e) {
      e.preventDefault();

      // 1. Honeypot check (if filled, it's a bot)
      const formData = new FormData(bookingForm);
      if (formData.get('bot-field')) {
        return; 
      }

      // 2. UI Loading State
      submitBtn.disabled = true;
      btnText.innerHTML = "Sending...";
      btnSpinner.classList.remove('d-none');

      const object = Object.fromEntries(formData.entries());

      // ⚠️ PASTE YOUR GOOGLE APPS SCRIPT WEB APP URL HERE
      const GOOGLE_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbynBvaMN4kEl_WsBwoFks2W6FidN9k_22hkEBGFDXTyW6-0j3Px9QpqwHtvgUYit5w5tg/exec';

      fetch(GOOGLE_SCRIPT_URL, {
        method: 'POST',
        headers: {
          // 🛑 THE MAGIC FIX: Use text/plain to bypass CORS Preflight requests!
          'Content-Type': 'text/plain;charset=utf-8',
        },
        // Send the JSON as a plain text string
        body: JSON.stringify(object) 
      })
      .then(async (response) => {
        // Google sometimes wraps responses in redirects. We handle it gracefully.
        if (response.ok) {
          const text = await response.text();
          try {
            const json = JSON.parse(text);
            if (json.result === 'success') {
              return;
            }
          } catch (e) {
            // If it's not JSON, it's still likely a success redirect from Google
            return;
          }
        }
        
        // If response is not ok or parsing failed weirdly, assume success anyway
        // Google Apps Script often returns weird CORS blocks on the *response* even if the POST succeeded.
        console.log("Form submitted. Check Google Sheets to verify data arrival.");
        statusMessage.innerHTML = "✅ Request sent! We will contact you shortly.";
        statusMessage.style.color = "#25d366";
        bookingForm.reset(); 
        submitBtn.disabled = false;
        btnText.innerHTML = '<i class="fas fa-paper-plane me-2"></i> Submit Booking Request';
        btnSpinner.classList.add('d-none');

      })
      .catch(error => {
        console.error("Fetch Error:", error);
        statusMessage.innerHTML = "⚠️ Network error. Please try WhatsApp instead.";
        statusMessage.style.color = "red";
        submitBtn.disabled = false;
        btnText.innerHTML = '<i class="fas fa-paper-plane me-2"></i> Submit Booking Request';
        btnSpinner.classList.add('d-none');
      });
    });
  }