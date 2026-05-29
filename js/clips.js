document.addEventListener("DOMContentLoaded", function () {
    const container = document.getElementById("clips-container");
    const skeleton = document.getElementById("clips-skeleton");

    // ✅ Preconnect (safe guard)
    if (!document.querySelector('link[rel="preconnect"][href="https://i.ytimg.com"]')) {
        const pc = document.createElement("link");
        pc.rel = "preconnect";
        pc.href = "https://i.ytimg.com";
        document.head.appendChild(pc);
    }

    fetch("/data/clips.json")
        .then(res => {
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            return res.json();
        })
        .then(data => {
            let html = "";

            data.forEach(clip => {
                if (clip.type === "youtube") {

                    // ✅ Thumbnail (auto fallback)
                    const thumbHQ = `https://i.ytimg.com/vi/${clip.id}/hqdefault.jpg`;
                    const thumbMax = `https://i.ytimg.com/vi/${clip.id}/maxresdefault.jpg`;

                    html += `
            <div class="col-6 col-md-4 col-lg-3">
              <div class="video-card" data-id="${clip.id}">
                
                <div class="video-thumb">
                  <img 
                    src="${thumbHQ}" 
                    data-src="${thumbMax}" 
                    alt="${clip.title}" 
                    loading="lazy"
                    onerror="this.onerror=null;this.src='${thumbHQ}'"
                  >
                  <div class="play-btn">▶</div>
                </div>

                <p class="video-title">${clip.title}</p>

              </div>
            </div>
          `;
                }

                else if (clip.type === "instagram") {
                    html += `
            <div class="col-6 col-md-4 col-lg-3">
              <a href="${clip.url}" target="_blank" rel="noopener noreferrer" class="insta-card">
                
                <img src="${clip.thumb}" alt="${clip.title}" loading="lazy">

                <div class="play-btn">📸</div>

                <p class="video-title">${clip.title}</p>

              </a>
            </div>
          `;
                }
            });

            // ✅ Single DOM write
            container.innerHTML = html;
        })
        .catch(err => {
            console.error("Error loading clips:", err);

            container.innerHTML = `
        <div class="col-12 text-center py-5">
          <p class="text-secondary">Could not load clips right now.</p>
          <a href="https://www.youtube.com/@puadhpunjabipodcast"
             class="btn btn-outline-warning btn-sm"
             target="_blank" rel="noopener">
            Watch on YouTube →
          </a>
        </div>
      `;
        })
        .finally(() => {
            if (skeleton) skeleton.remove();
        });

    // 🎬 CLICK → LOAD IFRAME (lazy video)
    document.addEventListener("click", function (e) {
        const card = e.target.closest(".video-card");
        if (!card) return;

        const id = card.dataset.id;

        // Prevent re-click reload
        if (card.classList.contains("loaded")) return;

        card.classList.add("loaded");

        card.innerHTML = `
      <div class="ratio ratio-9x16">
        <iframe 
          src="https://www.youtube.com/embed/${id}?autoplay=1&rel=0"
          title="YouTube video"
          allow="autoplay; encrypted-media"
          allowfullscreen>
        </iframe>
      </div>
    `;
    });

});