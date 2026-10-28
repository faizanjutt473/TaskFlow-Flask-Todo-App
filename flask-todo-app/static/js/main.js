// Delete karne se pehle confirmation
document.querySelectorAll(".delete-form").forEach(function (form) {
    form.addEventListener("submit", function (e) {
        if (!confirm("Kya aap sach me ye task delete karna chahte hain?")) {
            e.preventDefault();
        }
    });
});

// Flash messages 3 second baad khud band ho jayen
setTimeout(function () {
    document.querySelectorAll(".alert").forEach(function (alert) {
        var bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
        bsAlert.close();
    });
}, 3000);

// Dark / Light mode toggle
(function () {
    var btn = document.getElementById("theme-toggle");
    var icon = btn.querySelector("i");
    var root = document.documentElement;

    function updateIcon() {
        var dark = root.getAttribute("data-bs-theme") === "dark";
        icon.className = dark ? "bi bi-sun-fill" : "bi bi-moon-stars-fill";
    }
    updateIcon();

    btn.addEventListener("click", function () {
        var next = root.getAttribute("data-bs-theme") === "dark" ? "light" : "dark";
        root.setAttribute("data-bs-theme", next);
        localStorage.setItem("theme", next);
        updateIcon();
    });
})();