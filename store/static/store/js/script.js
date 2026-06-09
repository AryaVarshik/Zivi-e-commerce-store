/**
 * Zivi E-Commerce Frontend Script
 * Handles Theme Toggling, Banners, Carousels, Mobile Menus, and AJAX Cart/Wishlist actions.
 */

document.addEventListener("DOMContentLoaded", function () {
    // ==========================================
    // 1. LIGHT & DARK MODE THEME MANAGEMENT
    // ==========================================
    const htmlEl = document.documentElement;
    const navThemeToggle = document.getElementById("theme-toggle");
    const settingsThemeToggle = document.getElementById("settings-theme-toggle");

    // Get current theme from html element (pre-set by inline script in head)
    const currentTheme = htmlEl.getAttribute("data-theme") || "light";

    // Synchronize switches states
    if (navThemeToggle) navThemeToggle.checked = (currentTheme === "dark");
    if (settingsThemeToggle) settingsThemeToggle.checked = (currentTheme === "dark");

    // Add event listeners for toggling theme
    function handleThemeChange(isDark) {
        const targetTheme = isDark ? "dark" : "light";
        htmlEl.setAttribute("data-theme", targetTheme);
        localStorage.setItem("zivi-theme", targetTheme);

        // Sync toggle states across DOM
        if (navThemeToggle) navThemeToggle.checked = isDark;
        if (settingsThemeToggle) settingsThemeToggle.checked = isDark;

        // Persist on backend if user is authenticated and token is available
        if (window.CSRF_TOKEN) {
            fetch('/settings/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': CSRF_TOKEN
                },
                body: 'dark_mode=' + (isDark ? 'true' : 'false')
            }).catch(err => console.log("Backend theme sync not active. Using local storage."));
        }
    }

    if (navThemeToggle) {
        navThemeToggle.addEventListener("change", function () {
            handleThemeChange(this.checked);
        });
    }

    if (settingsThemeToggle) {
        settingsThemeToggle.addEventListener("change", function () {
            handleThemeChange(this.checked);
        });
    }

    // ==========================================
    // 2. MOBILE DRAWER MENU TOGGLE
    // ==========================================
    const mobileBtn = document.getElementById("mobile-menu-btn");
    const mobileDrawer = document.getElementById("mobile-menu");

    if (mobileBtn && mobileDrawer) {
        mobileBtn.addEventListener("click", function () {
            if (mobileDrawer.style.display === "none" || !mobileDrawer.style.display) {
                mobileDrawer.style.display = "block";
                mobileBtn.innerHTML = '<i class="fa fa-times"></i>';
            } else {
                mobileDrawer.style.display = "none";
                mobileBtn.innerHTML = '<i class="fa fa-bars"></i>';
            }
        });
    }

    // ==========================================
    // 3. HOMEPAGE BANNER SLIDER (10 SLIDES)
    // ==========================================
    const sliderContainer = document.getElementById("hero-slider");
    const prevBtn = document.getElementById("slider-prev-btn");
    const nextBtn = document.getElementById("slider-next-btn");
    const dotsContainer = document.getElementById("slider-dots");

    if (sliderContainer) {
        const slides = sliderContainer.querySelectorAll(".slide");
        const totalSlides = slides.length;
        let activeIndex = 0;
        let slideInterval;

        // Build dots indicators
        for (let i = 0; i < totalSlides; i++) {
            const dot = document.createElement("div");
            dot.classList.add("slider-dot");
            if (i === 0) dot.classList.add("active");
            dot.addEventListener("click", () => goToSlide(i));
            dotsContainer.appendChild(dot);
        }

        const dots = dotsContainer.querySelectorAll(".slider-dot");

        function updateSlider() {
            sliderContainer.style.transform = `translateX(-${activeIndex * 100}%)`;
            dots.forEach((dot, idx) => {
                if (idx === activeIndex) {
                    dot.classList.add("active");
                } else {
                    dot.classList.remove("active");
                }
            });
        }

        function nextSlide() {
            activeIndex = (activeIndex + 1) % totalSlides;
            updateSlider();
        }

        function prevSlide() {
            activeIndex = (activeIndex - 1 + totalSlides) % totalSlides;
            updateSlider();
        }

        function goToSlide(index) {
            activeIndex = index;
            updateSlider();
            resetAutoPlay();
        }

        function startAutoPlay() {
            slideInterval = setInterval(nextSlide, 10000); // 10 seconds interval
        }

        function resetAutoPlay() {
            clearInterval(slideInterval);
            startAutoPlay();
        }

        if (nextBtn) {
            nextBtn.addEventListener("click", () => {
                nextSlide();
                resetAutoPlay();
            });
        }

        if (prevBtn) {
            prevBtn.addEventListener("click", () => {
                prevSlide();
                resetAutoPlay();
            });
        }

        startAutoPlay();
    }

    // ==========================================
    // 4. TESTIMONIAL / REVIEWS SLIDER
    // ==========================================
    const reviewsContainer = document.getElementById("reviews-carousel");
    const reviewsDotsContainer = document.getElementById("reviews-dots");

    if (reviewsContainer) {
        const reviewSlides = reviewsContainer.querySelectorAll(".review-slide");
        const totalReviews = reviewSlides.length;
        let reviewIndex = 0;
        let reviewInterval;

        // Build review dots
        for (let i = 0; i < totalReviews; i++) {
            const dot = document.createElement("div");
            dot.classList.add("slider-dot");
            if (i === 0) dot.classList.add("active");
            dot.addEventListener("click", () => goToReview(i));
            reviewsDotsContainer.appendChild(dot);
        }

        const revDots = reviewsDotsContainer.querySelectorAll(".slider-dot");

        function updateReviews() {
            reviewsContainer.style.transform = `translateX(-${reviewIndex * 100}%)`;
            revDots.forEach((dot, idx) => {
                if (idx === reviewIndex) {
                    dot.classList.add("active");
                } else {
                    dot.classList.remove("active");
                }
            });
        }

        function nextReview() {
            reviewIndex = (reviewIndex + 1) % totalReviews;
            updateReviews();
        }

        function goToReview(index) {
            reviewIndex = index;
            updateReviews();
            resetReviewAutoPlay();
        }

        function startReviewAutoPlay() {
            reviewInterval = setInterval(nextReview, 6000); // 6 seconds auto scroll
        }

        function resetReviewAutoPlay() {
            clearInterval(reviewInterval);
            startReviewAutoPlay();
        }

        startReviewAutoPlay();
    }

    // ==========================================
    // 5. AUTO-HIDE FLOATING MESSAGES
    // ==========================================
    const messageContainer = document.getElementById("message-container");
    if (messageContainer) {
        const alerts = messageContainer.querySelectorAll(".alert");
        alerts.forEach(alert => {
            setTimeout(() => {
                alert.style.opacity = 0;
                alert.style.transform = 'translateY(-10px)';
                setTimeout(() => alert.remove(), 400);
            }, 6000); // auto remove after 6 seconds
        });
    }

    // ==========================================
    // 5b. SCROLL TO TOP BUTTON VISIBILITY
    // ==========================================
    const scrollTopBtn = document.getElementById("scroll-to-top-btn");
    if (scrollTopBtn) {
        window.addEventListener("scroll", function() {
            if (window.scrollY > 300) {
                scrollTopBtn.style.display = "flex";
            } else {
                scrollTopBtn.style.display = "none";
            }
        });
    }
});

// ==========================================
// 6. GLOBAL CART / WISHLIST AJAX FUNCTIONS
// ==========================================

/**
 * Add a product to the cart via AJAX
 * @param {string} productId 
 * @param {number} quantity 
 */
function addToCart(productId, quantity = 1) {
    if (!window.CSRF_TOKEN) return;

    fetch("/api/cart/add/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": CSRF_TOKEN
        },
        body: JSON.stringify({ product_id: productId, quantity: quantity })
    })
    .then(res => {
        if (res.status === 401) {
             // User is not logged in. Django views redirect wrapper returns 401 JSON redirect url.
             window.location.href = '/login/?next=' + encodeURIComponent(window.location.pathname);
             return;
        }
        return res.json();
    })
    .then(data => {
        if (data) {
            if (data.status === "success") {
                // Update nav badge count
                const badge = document.getElementById("cart-badge");
                if (badge) badge.innerText = data.cart_count;
                
                // Reload page to display Django flash messages
                window.location.reload();
            } else {
                alert(data.message || "Could not add product to cart.");
            }
        }
    })
    .catch(err => {
         console.error("Cart AJAX error: ", err);
    });
}

/**
 * Toggle a product in the wishlist via AJAX
 * @param {string} productId 
 * @param {HTMLElement} btnElement 
 */
function toggleWishlist(productId, btnElement) {
    if (!window.CSRF_TOKEN) return;

    // Check if currently active (wishlisted)
    const isAct = btnElement.classList.contains("active");
    const apiUrl = isAct ? "/api/wishlist/remove/" : "/api/wishlist/add/";

    fetch(apiUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": CSRF_TOKEN
        },
        body: JSON.stringify({ product_id: productId })
    })
    .then(res => {
        if (res.status === 401) {
             // Redirect to login if anonymous
             window.location.href = '/login/?next=' + encodeURIComponent(window.location.pathname);
             return;
        }
        return res.json();
    })
    .then(data => {
        if (data) {
            if (data.status === "success" || data.status === "info") {
                // Toggle active class
                if (isAct) {
                     btnElement.classList.remove("active");
                } else {
                     btnElement.classList.add("active");
                }
                
                // Update nav wishlist count
                const badge = document.getElementById("wishlist-badge");
                if (badge) badge.innerText = data.wishlist_count;
                
                // Reload to sync django success notifications
                window.location.reload();
            } else {
                alert(data.message || "Failed to update wishlist.");
            }
        }
    })
    .catch(err => {
         console.error("Wishlist AJAX error: ", err);
    });
}
