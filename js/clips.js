document.addEventListener("DOMContentLoaded", function () {
    const container = document.getElementById("clips-container");
    const skeleton = document.getElementById("clips-skeleton");

    // ✅ Single preconnect guard (in case it's ever added elsewhere)
    if (!document.querySelector('link[rel="preconnect"][href="https://i.ytimg.com"]')) {
        const pc = document.createElement('link');
        pc.rel = 'preconnect';
        pc.href = 'https://i.ytimg.com';
        document.head.appendChild(pc);
    }

    fetch('/data/clips.json')
        .then(response => {
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return response.json();
        })
        .then(data => {
            // ✅ Build ALL html in ONE string — zero intermediate reflows
            let html = "";

            data.forEach(clip => {
                if (clip.type === "youtube") {
                    html += `
                    <div class="col-6 col-lg-3">
                        <div class="youtube-card">
                            <div class="ratio ratio-9x16">
                                <iframe src="https://www.youtube.com/embed/${clip.id}?rel=0" title="${clip.title}" allowfullscreen loading="lazy"></iframe>
                            </div>
                        </div>
                    </div>`;
                }
                else if (clip.type === "instagram") {
                    html += `
                    <div class="col-6 col-lg-3">
                        <a href="${clip.url}" target="_blank" rel="noopener noreferrer" class="insta-card">
                            <img src="${clip.thumb}" alt="${clip.title}" loading="lazy" width="360" height="640">
                            <div class="play-btn-overlay"><i class="fab fa-instagram"></i></div>
                            <div class="insta-icon"><i class="fas fa-external-link-alt"></i></div>
                            <div class="insta-overlay">
                                <h6 class="text-white mb-0">${clip.title}</h6>
                                <small class="text-white-50">View on Instagram</small>
                            </div>
                        </a>
                    </div>`;
                }
            });

            // ✅ Single DOM write — one reflow, not 7
            container.innerHTML = html;
        })
        .catch(error => {
            console.error('Error loading clips:', error);
            // ✅ Show fallback instead of leaving skeleton forever
            container.innerHTML = `
                <div class="col-12 text-center py-5">
                    <p class="text-secondary">Could not load clips right now.</p>
                    <a href="https://www.youtube.com/@puadhpunjabipodcast" class="btn btn-outline-warning btn-sm" target="_blank" rel="noopener">
                        Watch on YouTube →
                    </a>
                </div>`;
        })
        .finally(() => {
            // ✅ Always remove skeleton
            if (skeleton) skeleton.remove();
        });
});