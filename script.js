document.addEventListener("DOMContentLoaded", () => {
    const e = document.getElementById("mobile-menu-button"),
        t = document.getElementById("mobile-menu"),
        n = e ? e.querySelector("i") : null,
        a = document.body;
    let i = document.getElementById("mobile-menu-backdrop");

    if (!i) {
        i = document.createElement("div");
        i.id = "mobile-menu-backdrop";
        i.className = "fixed inset-0 bg-black/60 backdrop-blur-sm z-40 hidden transition-opacity duration-300 opacity-0";
        i.setAttribute("aria-hidden", "true");
        document.body.appendChild(i);
    }

    if (e && t) {
        const toggleMenu = () => {
            const isClosed = t.classList.contains("translate-x-full");
            if (isClosed) {
                // Open menu
                t.classList.remove("hidden");
                i.classList.remove("hidden");
                // Force a reflow for the transition to trigger
                void t.offsetWidth;
                t.classList.remove("translate-x-full");
                i.classList.remove("opacity-0");
                i.classList.add("opacity-100");

                e.setAttribute("aria-expanded", "true");
                t.setAttribute("aria-hidden", "false");
                i.setAttribute("aria-hidden", "false");

                if (n) {
                    n.classList.remove("fa-bars");
                    n.classList.add("fa-times");
                }
                a.style.overflow = "hidden";
            } else {
                closeMenu();
            }
        };

        function closeMenu() {
            t.classList.add("translate-x-full");
            i.classList.remove("opacity-100");
            e.setAttribute("aria-expanded", "false");
            t.setAttribute("aria-hidden", "true");
            i.setAttribute("aria-hidden", "true");

            if (n) {
                n.classList.remove("fa-times");
                n.classList.add("fa-bars");
            }
            a.style.overflow = "";

            setTimeout(() => {
                if (t.classList.contains("translate-x-full")) {
                    t.classList.add("hidden");
                    i.classList.add("hidden");
                }
            }, 300);
        }

        e.addEventListener("click", toggleMenu);
        i.addEventListener("click", closeMenu);
        document.addEventListener("keydown", (event) => {
            if (event.key === "Escape" && !t.classList.contains("translate-x-full")) {
                closeMenu();
            }
        });

        // Handle menu links click
        t.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', closeMenu);
        });
    }

    const o = document.getElementById("logout-btn-desktop"),
        d = document.getElementById("logout-btn-mobile"),
        l = () => {
            window.signOutUser ? window.signOutUser() : window.location.href = "index.html"
        };
    o && o.addEventListener("click", l), d && d.addEventListener("click", l)
});

window.toggleMobileDropdown = function (e, t) {
    const n = document.getElementById(e),
        a = t.querySelector(".chevron-icon");
    if (n) {
        if (n.classList.contains("hidden")) {
            n.classList.remove("hidden");
            t.setAttribute("aria-expanded", "true");
            if (a) {
                a.classList.remove("fa-chevron-down");
                a.classList.add("fa-chevron-up");
            }
        } else {
            n.classList.add("hidden");
            t.setAttribute("aria-expanded", "false");
            if (a) {
                a.classList.remove("fa-chevron-up");
                a.classList.add("fa-chevron-down");
            }
        }
    }
};

window.selectSphere = function (e, t) {
    const n = document.getElementById("default-info"),
        a = document.getElementById("sphere-info"),
        i = document.getElementById("sphere-name"),
        s = document.getElementById("sphere-description");
    if (!a) return;
    n && n.classList.add("hidden"), a.classList.remove("hidden"), a.classList.add("animate-fade-in");
    let o = "";
    const d = t.toLowerCase();
    if (d.includes("self")) {
        o = "Optimize personal baseline, resolve internal friction, and align with your highest trajectory.";
        t = "Self";
    } else if (d.includes("family")) {
        o = "Structure generational potential, harmonize interpersonal dynamics, and build a unified core framework.";
        t = "Family";
    } else if (d.includes("org") || d.includes("organization")) {
        o = "Drive systemic efficiency, eliminate operational drag, and scale through behavioral excellence.";
        t = "Organization";
    } else if (d.includes("nation")) {
        o = "Enhance civic structures, fortify national resilience, and engineer societal progression.";
        t = "Nation";
    } else if (d.includes("globe")) {
        o = "Coordinate macro-level ecosystems, balance interconnected systems, and elevate humanity's baseline.";
        t = "Globe";
    }
    i && (i.innerText = t), s && (s.innerText = o), document.querySelectorAll(".audit-btn").forEach(e => {
        e.classList.remove("border-gold", "bg-white/10"), e.classList.add("border-white/10", "bg-white/5");
        const t = e.querySelector("i");
        t && (t.classList.remove("text-gold"), t.classList.add("text-gray-400"))
    }), e.classList.remove("border-white/10", "bg-white/5"), e.classList.add("border-gold", "bg-white/10");
    const l = e.querySelector("i");
    l && (l.classList.remove("text-gray-400"), l.classList.add("text-gold")), requestAnimationFrame(() => {
        const e = a.getBoundingClientRect().top + window.pageYOffset + -100;
        window.scrollTo({
            top: e,
            behavior: "smooth"
        })
    })
};

window.googleTranslateElementInit = function () {
    const config = {
        pageLanguage: "en",
        includedLanguages: "en,as,bn,brx,doi,gu,hi,kn,ks,gom,mai,ml,mni,mr,ne,or,pa,sa,sat,sd,ta,te,ur",
        layout: google.translate.TranslateElement.InlineLayout.SIMPLE,
        autoDisplay: false
    };

    // Support multiple translate elements on the same page
    const desktopEl = document.getElementById("google_translate_element");
    const mobileEl = document.getElementById("google_translate_element_mobile");

    if (desktopEl) {
        new google.translate.TranslateElement(config, "google_translate_element");
    }

    if (mobileEl) {
        // Use a slightly different approach for the second one if needed
        setTimeout(() => {
            new google.translate.TranslateElement(config, "google_translate_element_mobile");
        }, 100);
    }
};

window.addEventListener("load", () => {
    setTimeout(() => {
        const e = document.createElement("script");
        e.type = "text/javascript", e.async = !0, e.src = "https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit", document.head.appendChild(e)
    }, 1000) // Reduced from 3500 to 1000 for faster appearance
});