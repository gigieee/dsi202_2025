function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

function toggleFavorite(petId) {
    const isLoggedIn = document.body.dataset.loggedIn === "true";
    let favorites = JSON.parse(localStorage.getItem("favorites") || "[]");
  
    if (favorites.includes(petId)) {
      favorites = favorites.filter(id => id !== petId);
    } else {
      favorites.push(petId);
    }
    localStorage.setItem("favorites", JSON.stringify(favorites));
    updateHeartIcons();
  
    if (isLoggedIn) {
      fetch(`/pet/${petId}/favorite/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie("csrftoken"),
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ toggle: true })
      }).then(res => {
        if (!res.ok) {
          console.error("Failed to sync favorite with backend");
        }
      });
    }
}

function refreshFavoriteSection() {
    const isLoggedIn = document.body.dataset.loggedIn === "true";
    if (!isLoggedIn) return; // ไม่ต้องโหลดหากไม่ได้ login
  
    fetch("/api/favorite-pets/")
      .then(res => res.json())
      .then(data => {
        const favorites = data.pets.map(pet => String(pet.id));
        localStorage.setItem("favorites", JSON.stringify(favorites));
        updateHeartIcons();
      })
      .catch(err => {
        console.error("❌ Failed to refresh favorites:", err);
      });
  }

  function updateHeartIcons() {
    const favorites = JSON.parse(localStorage.getItem("favorites") || "[]").map(String); // 🟢 force string
    document.querySelectorAll("[id^='heart-']").forEach(el => {
      const petId = el.id.replace("heart-", "").trim(); // 🟢 ensure string
      el.style.color = favorites.includes(petId) ? "#e53935" : "gray";
    });
  }

  function openPetModal(petId) {
    fetch(`/api/pet/${petId}/`)
      .then(res => res.json())
      .then(data => {
        const isFav = (JSON.parse(localStorage.getItem("favorites") || "[]")).includes(String(data.id));
  
        const sponsorshipSection = data.sponsorship ? `
          <div class="mt-6 p-4 bg-[#fff8eb] rounded-lg border border-orange-200">
            <h3 class="text-xl font-bold text-[#d55e00] mb-2">Medical Support Needed</h3>
            <p class="text-gray-700 mb-2">${data.sponsorship.description}</p>
            <p class="text-sm mb-2"><strong>Goal:</strong> ฿${data.sponsorship.goal_amount.toLocaleString()} | <strong>Raised:</strong> ฿${data.sponsorship.current_amount.toLocaleString()}</p>
            <div class="w-full bg-gray-200 rounded-full h-3 overflow-hidden mb-2">
              <div class="h-3 bg-[#6d9f71]" style="width: ${data.sponsorship.progress}%"></div>
            </div>
            <p class="text-xs text-right text-gray-600">${data.sponsorship.progress}% funded</p>
            <div class="text-center mt-3">
              <a href="/donate/sponsor/${data.sponsorship.id}/" 
                 class="inline-block bg-[#6d9f71] text-white px-6 py-2 rounded-full hover:bg-[#51865b]">Support</a>
            </div>
          </div>` : '';
  
        const modalHTML = `
          <div id="petModal" class="fixed inset-0 bg-black bg-opacity-50 z-50 flex justify-center items-center">
            <div class="relative bg-white w-full max-w-2xl max-h-[90vh] overflow-y-auto rounded-xl shadow-lg p-6">
              
              <!-- ✕ ปิด -->
              <button onclick="closePetModal()" class="absolute top-3 right-3 text-gray-500 hover:text-red-500 text-2xl font-bold">&times;</button>
  
              <!-- หัวใจ Favorite -->
              <button onclick="event.stopPropagation(); toggleFavorite('${data.id}')" class="absolute top-3 left-3 z-10">
                <svg id="heart-${data.id}" xmlns="http://www.w3.org/2000/svg" fill="currentColor"
                     viewBox="0 0 24 24" stroke-width="2.5" stroke="white"
                     class="w-8 h-8 transition duration-200" style="color: ${isFav ? '#e53935' : 'gray'};">
                  <path stroke-linecap="round" stroke-linejoin="round"
                        d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5
                        2 5.42 4.42 3 7.5 3c1.74 0 3.41 0.81 
                        4.5 2.09C13.09 3.81 14.76 3 
                        16.5 3 19.58 3 22 5.42 22 8.5
                        c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" />
                </svg>
              </button>
  
              <div data-pet-id="${data.id}" class="text-sm text-gray-800 space-y-2">
                <div class="text-center">
                  <img src="${data.image_url}" alt="${data.name}" class="w-40 h-40 object-cover mx-auto mb-4 rounded-xl shadow">
                  <h2 class="text-2xl font-bold text-[#523a28] mb-4">${data.name}</h2>
                </div>
  
                <p><strong>ID:</strong> ${data.pet_id}</p>
                <p><strong>Species:</strong> ${data.species}</p>
                <p><strong>Breed:</strong> ${data.breed}</p>
                <p><strong>Age:</strong> ${data.age} ${data.age_unit}</p>
                <p><strong>Gender:</strong> ${data.gender}</p>
                <p><strong>Color:</strong> ${data.color}</p>
                <p><strong>Size:</strong> ${data.size}</p>
                <p><strong>Coat Length:</strong> ${data.coat_length}</p>
                <p><strong>Good with:</strong> ${data.good_with.join(", ")}</p>
                <p><strong>Behavior:</strong> ${data.behavior}</p>
                <p><strong>Care Level:</strong> ${data.care_and_behavior}</p>
                <p><strong>Days on PawPal:</strong> ${data.days_on_pawpal}</p>
                <p><strong>Location:</strong> ${data.location}</p>
                <p><strong>Story:</strong> ${data.story}</p>
                <p><strong>Health:</strong> ${data.health_status}</p>
  
                <div class="mt-6 text-center">
                  <a href="/request-adoption/?pets=${data.id}" 
                     class="inline-block bg-[#d55e00] text-white px-6 py-2 rounded-full hover:bg-[#b54800]">Adopt</a>
                </div>
  
                ${sponsorshipSection}
              </div>
            </div>
          </div>
        `;
  
        document.body.insertAdjacentHTML("beforeend", modalHTML);
        updateHeartIcons();
      })
      .catch(() => {
        alert("Error loading pet data.");
      });
  }
  
  function closePetModal() {
    const modal = document.getElementById("petModal");
    if (modal) modal.remove();
  
    const petDetail = document.querySelector('[data-pet-id]');
    if (petDetail && petDetail.dataset.petId) {
      const petId = petDetail.dataset.petId;
  
      // ✅ อัปเดต sessionStorage สำหรับ guest
      let recent = JSON.parse(sessionStorage.getItem("recently_viewed") || "[]");
      recent = [petId, ...recent.filter(id => id !== petId)];
      sessionStorage.setItem("recently_viewed", JSON.stringify(recent.slice(0, 5)));
  
      // ✅ ถ้า login แล้ว → sync กับ backend
      const isLoggedIn = document.body.dataset.loggedIn === "true";
      if (isLoggedIn) {
        fetch(`/api/recently-viewed/${petId}/`, {
          method: "POST",
          headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ viewed: true })
        }).catch(err => console.error("Failed to sync recently viewed:", err));
      }
  
      // ✅ ดึง UI section ใหม่มาแสดง
    fetch("/adopt/recently-viewed-html/")
    .then(res => res.text())
    .then(html => {
      const container = document.getElementById("recentlyViewedSection");
      if (container) {
        container.innerHTML = html;
        setTimeout(() => updateHeartIcons(), 50);
      }
    });
}
}
  // ✅ ESC key to close modal
  document.addEventListener("DOMContentLoaded", function () {
  updateHeartIcons();
  refreshFavoriteSection();  // 🟢 sync favorite ทุกครั้งที่โหลดหน้า
});
  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
      closePetModal();
    }
  });