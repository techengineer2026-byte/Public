const form = document.getElementById('contact-form');
const submitBtn = document.querySelector('button[type="submit"]');
document.querySelectorAll('.video-facade').forEach(facade => {
    facade.addEventListener('click', function () {
        const src = this.getAttribute('data-src');
        if (!src) return;

        const iframe = document.createElement('iframe');
        iframe.src = src + '&autoplay=1';
        iframe.title = this.querySelector('img')?.alt || 'YouTube Video';
        iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
        iframe.allowFullscreen = true;
        iframe.loading = 'lazy';

        this.innerHTML = '';
        this.appendChild(iframe);
    });
});
form.addEventListener('submit', e => {
    e.preventDefault();

    const originalBtnText = submitBtn.innerText;
    submitBtn.innerText = "⏳ Sending...";
    submitBtn.disabled = true;

    const scriptURL = 'https://script.google.com/macros/s/AKfycbw009VaTMgpQTuGGHlBI3Ud_3Tv5k6rwie5NRLYPhbV4D1GrzJY82GZbJ7Bh00HX5D-nQ/exec';

    fetch(scriptURL, { method: 'POST', body: new FormData(form) })
        .then(response => {

            form.reset();

            var myModal = new bootstrap.Modal(document.getElementById('successModal'));
            myModal.show();

            submitBtn.innerText = originalBtnText;
            submitBtn.disabled = false;
        })
        .catch(error => {
            console.error('Error!', error.message);
            alert("Something went wrong. Please try again.");
            submitBtn.innerText = originalBtnText;
            submitBtn.disabled = false;
        });
});

