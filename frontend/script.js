const API_URL = "http://localhost:8000";

// Загрузка всех объявлений
async function loadAds() {
    try {
        const response = await fetch(`${API_URL}/ads`);
        const ads = await response.json();
        displayAds(ads);
    } catch (error) {
        console.error("Ошибка загрузки:", error);
        document.getElementById("adsList").innerHTML = '<div class="alert alert-danger">Ошибка подключения к серверу</div>';
    }
}

// Отображение объявлений
function displayAds(ads) {
    const container = document.getElementById("adsList");

    if (ads.length === 0) {
        container.innerHTML = '<div class="col-12"><div class="alert alert-info">📭 Нет объявлений. Создайте первое!</div></div>';
        return;
    }

    container.innerHTML = ads.map(ad => `
        <div class="col-md-4">
            <div class="card ad-card h-100">
                <div class="card-body">
                    <h5 class="card-title">${escapeHtml(ad.title)}</h5>
                    <p class="ad-price">💰 ${ad.price} ₽</p>
                    <p><strong>📂 Категория:</strong> ${escapeHtml(ad.category)}</p>
                    <p class="card-text">${escapeHtml(ad.description.substring(0, 100))}...</p>
                    <p class="ad-contact"><strong>📞 Контакт:</strong> ${escapeHtml(ad.contact)}</p>
                    <small class="text-muted">📅 ${new Date(ad.created_at).toLocaleDateString('ru-RU')}</small>
                    <div class="mt-3">
                        <button class="btn btn-sm btn-danger" onclick="deleteAd(${ad.id})">🗑 Удалить</button>
                        <button class="btn btn-sm btn-warning" onclick="editAd(${ad.id})">✏ Редактировать</button>
                    </div>
                </div>
            </div>
        </div>
    `).join('');
}

// Создание объявления
document.getElementById("adForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const newAd = {
        title: document.getElementById("title").value,
        price: parseFloat(document.getElementById("price").value),
        description: document.getElementById("description").value,
        category: document.getElementById("category").value,
        contact: document.getElementById("contact").value
    };

    try {
        const response = await fetch(`${API_URL}/ads`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(newAd)
        });

        if (response.ok) {
            alert("✅ Объявление опубликовано! Проверьте Telegram канал.");
            document.getElementById("adForm").reset();
            loadAds();
        } else {
            alert("❌ Ошибка при публикации");
        }
    } catch (error) {
        console.error("Ошибка:", error);
        alert("❌ Ошибка подключения к серверу");
    }
});

// Удаление объявления
async function deleteAd(id) {
    if (confirm("🗑 Удалить объявление?")) {
        await fetch(`${API_URL}/ads/${id}`, { method: "DELETE" });
        loadAds();
    }
}

// Редактирование объявления
async function editAd(id) {
    const newTitle = prompt("✏ Введите новое название:");
    if (newTitle && newTitle.trim()) {
        try {
            const response = await fetch(`${API_URL}/ads/${id}`);
            const ad = await response.json();

            ad.title = newTitle;

            await fetch(`${API_URL}/ads/${id}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(ad)
            });
            loadAds();
        } catch (error) {
            console.error("Ошибка:", error);
        }
    }
}

// Защита от XSS атак
function escapeHtml(str) {
    return str.replace(/[&<>]/g, function(m) {
        if (m === '&') return '&amp;';
        if (m === '<') return '&lt;';
        if (m === '>') return '&gt;';
        return m;
    });
}

// Загрузка при запуске страницы
loadAds();