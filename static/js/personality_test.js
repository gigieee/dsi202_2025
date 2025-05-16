let isSubmitting = false;

document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    if (!form) return;

    form.addEventListener("submit", function (e) {
        e.preventDefault();

        if (isSubmitting) return;  // 🔒 ป้องกันส่งซ้ำ
        isSubmitting = true;

        const q1 = form.querySelector("[name='q1']").value;
        const q2 = form.querySelector("[name='q2']").value;
        const q3 = form.querySelector("[name='q3']").value;
        const q4 = form.querySelector("[name='q4']").value;
        const q5 = form.querySelector("[name='q5']").value;
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch("/api/personality-match/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
            },
            body: JSON.stringify({ q1, q2, q3, q4, q5 }),
        })
        .then((res) => {
            if (!res.ok) throw new Error("API error");
            return res.json();
        })
        .then((data) => {
            if (data.success && data.pet) {
                showResultPopup(data.pet);

                // ⏺ Save to DB
                if (data.pet.id) {
                    fetch("/personality/save_result/", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                            "X-CSRFToken": csrfToken,
                        },
                        body: JSON.stringify({ pet_id: data.pet.id }),
                    }).catch(err => console.error("Error saving result:", err));
                }
            } else {
                alert("Something went wrong. Please try again.");
            }
        })
        .catch((err) => {
            console.error("Fetch error:", err);
            alert("Server error. Please try again later.");
        })
        .finally(() => {
            isSubmitting = false;  // 🔓 ปลดล็อก
        });
    });
});

function showResultPopup(pet) {
    const popup = document.createElement("div");
    popup.classList.add("fixed", "inset-0", "bg-black", "bg-opacity-60", "flex", "justify-center", "items-center", "z-50");

    popup.innerHTML = `
        <div class="bg-white p-6 rounded-xl shadow-xl text-center relative max-w-sm w-full">
            <button id="closePopup" class="absolute top-2 right-3 text-gray-500 text-xl">&times;</button>
            <img src="${pet.image_url}" class="w-32 h-32 object-cover rounded-full mx-auto mb-4" alt="${pet.name}">
            <h2 class="text-xl font-bold text-[#6d9f71] mb-2">Your Match is: ${pet.name}</h2>
            <p class="text-gray-700">${pet.breed} • ${pet.gender} • ${pet.age}</p>
            <p class="mt-2 text-sm text-gray-500">${pet.description}</p>
        </div>
    `;

    document.body.appendChild(popup);

    document.getElementById("closePopup").addEventListener("click", () => {
        popup.remove();
    });
}