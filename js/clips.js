document.addEventListener("DOMContentLoaded", function () {
    const container = document.getElementById("clips-container");

    fetch('/data/clips.json')
        .then(response => response.json())
        .then(data => {
            data.forEach(clip => {
                let html = "";

                if (clip.type === "youtube") {
                    html = `
                    <div class="col-6 col-lg-3">
                        <div class="youtube-card">
                            <div class="ratio ratio-9x16">
                                <iframe src="https://www.youtube.com/embed/${clip.id}?rel=0" title="${clip.title}" allowfullscreen loading="lazy"></iframe>
                            </div>
                        </div>
                    </div>`;
                }
                else if (clip.type === "instagram") {
                    html = `
                    <div class="col-6 col-lg-3">
                        <a href="${clip.url}" target="_blank" class="insta-card">
                            <img src="${clip.thumb}" alt="${clip.title}" loading="lazy">
                            <div class="play-btn-overlay"><i class="fab fa-instagram"></i></div>
                            <div class="insta-icon"><i class="fas fa-external-link-alt"></i></div>
                            <div class="insta-overlay">
                                <h6 class="text-white mb-0">${clip.title}</h6>
                                <small class="text-white-50">View on Instagram</small>
                            </div>
                        </a>
                    </div>`;
                }

                container.innerHTML += html;
            });
        })
        .catch(error => console.error('Error loading clips:', error));
});