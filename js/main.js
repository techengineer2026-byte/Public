// =========================================================================
//                             CONFIGURATION
// =========================================================================
// This single URL is used by ALL six forms. 
// Make sure it's from your LATEST Google Apps Script deployment.
const SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzCHcZA9MykFdnnJaNlfezZrM_E2Tt1iW4Gjei6jxOCdEPxvM25xB2NpVn8bawJ3Is0/exec";


// =========================================================================
//              GENERIC FUNCTION TO HANDLE ANY FORM SUBMISSION
// =========================================================================
/**
 * Attaches a submission event listener to a form.
 * @param {string} formId The HTML ID of the form element.
 * @param {string} statusId The HTML ID of the element where status messages will be shown.
 * @param {string} successMessage The message to display on successful submission.
 * @param {string} buttonText The original text of the submit button.
 */
function handleFormSubmit(formId, statusId, successMessage, buttonText) {
  const form = document.getElementById(formId);
  const statusMessageEl = document.getElementById(statusId);

  // Only run the code if the form actually exists on the current page
  if (form) {
    form.addEventListener('submit', function(e) {
      e.preventDefault();
      const submitButton = form.querySelector('button[type="submit"]');
      
      // Provide user feedback
      submitButton.disabled = true;
      submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i> Submitting...';
      statusMessageEl.textContent = '';
      statusMessageEl.style.color = 'initial';

      // Send the data
      fetch(SCRIPT_URL, { method: 'POST', body: new FormData(form) })
        .then(response => response.json())
        .then(data => {
          if (data.result === 'success') {
            statusMessageEl.textContent = successMessage;
            statusMessageEl.style.color = 'green';
            form.reset();
          } else {
            // This error comes from the Google Script itself
            throw new Error(data.message || 'An unknown error occurred.');
          }
        })
        .catch(error => {
          // This catches network errors or the error thrown above
          console.error(`Error submitting form '${formId}':`, error.message);
          statusMessageEl.textContent = 'Oops! Something went wrong. Please try again.';
          statusMessageEl.style.color = 'red';
        })
        .finally(() => {
          // Re-enable the button no matter what
          submitButton.disabled = false;
          submitButton.innerHTML = `<i class="fas fa-paper-plane me-2"></i> ${buttonText}`;
        });
    });
  }
}


// =========================================================================
//                     INITIALIZE ALL FORMS ON THE WEBSITE
// =========================================================================
// Just call the generic function for each form on your site.

// Form 1: The very first "Studio Booking" form (legacy)
handleFormSubmit(
  'podcastBookingForm', 
  'form-status-message', 
  'Thank you! Your booking request has been sent.', 
  'Submit Booking Request'
);

// Form 2: Editing Order Form
handleFormSubmit(
  'editingOrderForm', 
  'editing-form-status-message', 
  'Thank you! Your editing order has been received.', 
  'Submit Editing Order'
);

// Form 3: Studio Space Booking Form
handleFormSubmit(
  'spaceBookingForm', 
  'space-form-status-message', 
  'Thank you! Your space booking request has been sent.', 
  'Submit Booking Request'
);

// Form 4: Shooting Order Form
handleFormSubmit(
  'shootingOrderForm', 
  'shooting-form-status-message', 
  'Thank you! Your shooting order has been received.', 
  'Submit Booking Request'
);

// Form 5: Scripting Order Form
handleFormSubmit(
  'scriptingOrderForm', 
  'scripting-form-status-message', 
  'Thank you! Your script order has been received.', 
  'Submit Script Order'
);

// Form 6: Anchor Booking Form
handleFormSubmit(
  'anchorBookingForm', 
  'anchor-form-status-message', 
  'Thank you! Your anchor booking has been sent.', 
  'Submit Anchor Booking'
);