import { app } from "./firebase-config.js";
import {
    getAuth,
    signInWithEmailAndPassword,
    createUserWithEmailAndPassword,
    GoogleAuthProvider,
    signInWithPopup,
    onAuthStateChanged,
    signOut,
    updateProfile,
    sendPasswordResetEmail
} from "https://www.gstatic.com/firebasejs/11.4.0/firebase-auth.js";
import { doc, setDoc, getDoc } from "https://www.gstatic.com/firebasejs/11.4.0/firebase-firestore.js";
import { db } from "./firebase-config.js";

const auth = getAuth(app);
const googleProvider = new GoogleAuthProvider();
googleProvider.setCustomParameters({
    client_id: "108392062510-7b0qvbj5e25lpbhu7routid0da8in2vl.apps.googleusercontent.com",
    prompt: "select_account"
});

const loginForm = document.getElementById("login-form");
const signupForm = document.getElementById("signup-form");
const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");
const nameInput = document.getElementById("name");
const errorMsg = document.getElementById("error-message");
const googleLoginBtn = document.getElementById("google-login");
const forgotPasswordLink = document.getElementById("forgot-password-link");

function showFeedback(message, type = "error") {
    if (!errorMsg) return;
    errorMsg.textContent = message;
    if (type === "success") {
        errorMsg.classList.remove("bg-red-900/50", "border-red-500", "text-red-200");
        errorMsg.classList.add("bg-green-900/50", "border-green-500", "text-green-200");
    } else {
        errorMsg.classList.remove("bg-green-900/50", "border-green-500", "text-green-200");
        errorMsg.classList.add("bg-red-900/50", "border-red-500", "text-red-200");
    }
    errorMsg.classList.remove("hidden");
    setTimeout(() => {
        errorMsg.classList.add("hidden");
    }, 5000);
}

// Login
if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const email = emailInput.value;
        const password = passwordInput.value;
        try {
            const userCredential = await signInWithEmailAndPassword(auth, email, password);
            const user = userCredential.user;
            const userSnap = await getDoc(doc(db, "users", user.uid));
            if (userSnap.exists() && userSnap.data().status === "suspended") {
                await signOut(auth);
                throw new Error("Your account has been suspended by an administrator.");
            }
            localStorage.setItem("fourAlphaUser", JSON.stringify({ email: user.email, uid: user.uid }));
            window.location.href = "dashboard.html";
        } catch (error) {
            if (error.code === "auth/invalid-credential" || error.code === "auth/wrong-password") {
                showFeedback("Invalid login. If you signed up via Google, please use 'Continue with Google'.");
            } else {
                showFeedback(error.message);
            }
        }
    });
}

// Signup
if (signupForm) {
    signupForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const name = nameInput.value;
        const email = emailInput.value;
        const password = passwordInput.value;
        const dobInput = document.getElementById("dob");
        const dob = dobInput ? dobInput.value : null;
        try {
            const userCredential = await createUserWithEmailAndPassword(auth, email, password);
            const user = userCredential.user;
            await updateProfile(user, { displayName: name });
            await setDoc(doc(db, "users", user.uid), {
                name: name,
                email: email,
                dob: dob,
                status: "active",
                certifications: {
                    whiteBelt: { completed: false },
                    yellowBelt: { completed: false },
                    greenBelt: { completed: false },
                    blackBelt: { completed: false }
                }
            });
            localStorage.setItem("fourAlphaUser", JSON.stringify({ email: user.email, uid: user.uid }));
            window.location.href = "dashboard.html";
        } catch (error) {
            if (error.code === "auth/email-already-in-use") {
                showFeedback("Email already in use. Please Login or use 'Continue with Google'.");
            } else {
                showFeedback(error.message);
            }
        }
    });
}

// Google Login
if (googleLoginBtn) {
    googleLoginBtn.addEventListener("click", async () => {
        try {
            const result = await signInWithPopup(auth, googleProvider);
            localStorage.setItem("fourAlphaUser", JSON.stringify({ email: result.user.email, uid: result.user.uid }));
            window.location.href = "dashboard.html";
        } catch (error) {
            if (error.code === "auth/account-exists-with-different-credential") {
                showFeedback("Account already exists. Please login using your Email and Password.");
            } else {
                showFeedback(error.message);
            }
        }
    });
}

// Forgot Password
if (forgotPasswordLink) {
    forgotPasswordLink.addEventListener("click", async (e) => {
        e.preventDefault();
        const email = emailInput?.value;
        if (email) {
            forgotPasswordLink.textContent = "Sending...";
            forgotPasswordLink.classList.add("opacity-50", "pointer-events-none");
            try {
                await sendPasswordResetEmail(auth, email);
                showFeedback("Password reset email sent. Please check your inbox.", "success");
            } catch (error) {
                if (error.code === "auth/invalid-email") {
                    showFeedback("Invalid email format.");
                } else {
                    showFeedback(error.message);
                }
            } finally {
                forgotPasswordLink.textContent = "Forgot Password?";
                forgotPasswordLink.classList.remove("opacity-50", "pointer-events-none");
            }
        } else {
            showFeedback("Please enter your email address to reset your password.");
        }
    });
}

// Progression Logic
const BELT_HIERARCHY = [
    { id: "whiteBelt", path: "white-belt", name: "White Belt" },
    { id: "yellowBelt", path: "yellow-belt", name: "Yellow Belt" },
    { id: "greenBelt", path: "green-belt", name: "Green Belt" },
    { id: "blackBelt", path: "black-belt", name: "Black Belt" },
    { id: "masterBlackBelt", path: "masters.html", name: "Master Black Belt" }
];

function checkProgression(userAuth, userData) {
    const path = window.location.pathname;
    const certs = userData.certifications || {};

    // Find if current page is a belt page
    for (let i = 1; i < BELT_HIERARCHY.length; i++) {
        const currentBelt = BELT_HIERARCHY[i];
        const prevBelt = BELT_HIERARCHY[i - 1];

        // Check if path matches current belt (either as directory /belt/ or file belt.html)
        const isCurrentPage = path.includes(`/${currentBelt.path}/`) || path.endsWith(currentBelt.path);

        if (isCurrentPage) {
            if (!certs[prevBelt.id]?.completed) {
                alert(`Progression Protocol: You must complete the ${prevBelt.name} assessment before accessing the ${currentBelt.name} module.`);
                const prefix = (path.includes("/education-policy/") || path.includes("-belt/")) ? "../" : "";
                // If nested deeper in education policy
                const deeperPrefix = path.includes("/education-policy/global/") || path.includes("/education-policy/national/") ? "../../" : prefix;

                const redirectPath = prevBelt.path.endsWith(".html") ? prevBelt.path : `${prevBelt.path}/index.html`;
                window.location.href = `${deeperPrefix}${redirectPath}`;
                return false;
            }
        }
    }
    return true;
}

function updateProgressionUI(userData) {
    const certs = userData.certifications || {};
    const links = document.querySelectorAll("a");

    links.forEach(link => {
        const href = link.getAttribute("href");
        if (!href) return;

        for (let i = 1; i < BELT_HIERARCHY.length; i++) {
            const currentBelt = BELT_HIERARCHY[i];
            const prevBelt = BELT_HIERARCHY[i - 1];

            if (href.includes(currentBelt.path)) {
                if (!certs[prevBelt.id]?.completed) {
                    // Lock this link
                    link.classList.add("locked-belt-link");
                    link.style.opacity = "0.5";
                    link.style.cursor = "not-allowed";
                    if (!link.querySelector(".fa-lock")) {
                        link.innerHTML += ' <i class="fas fa-lock ml-2 text-[10px] opacity-70"></i>';
                    }
                    link.onclick = (e) => {
                        e.preventDefault();
                        alert(`Progression Protocol: You must complete the ${prevBelt.name} assessment first.`);
                    };
                }
            }
        }
    });
}

onAuthStateChanged(auth, async (user) => {
    const path = window.location.pathname;
    const isLoginPage = path.includes("login.html");
    const isSignupPage = path.includes("signup.html");

    if (user) {
        // Fetch user data for progression
        const userSnap = await getDoc(doc(db, "users", user.uid));
        const userData = userSnap.exists() ? userSnap.data() : { certifications: {} };

        if (!checkProgression(user, userData)) return;
        updateProgressionUI(userData);

        if (isLoginPage || isSignupPage) {
            const isBeltPath = path.includes("/green-belt/") || path.includes("/white-belt/") || path.includes("/yellow-belt/") || path.includes("/black-belt/") || path.includes("/education-policy/");
            let redirectPrefix = "";
            if (path.includes("/education-policy/global/") || path.includes("/education-policy/national/")) {
                redirectPrefix = "../../";
            } else if (isBeltPath) {
                redirectPrefix = "../";
            }
            window.location.href = redirectPrefix + "dashboard.html";
            return;
        }
    } else {
        // Locked pages check (Add pages that require login)
        const lockedPaths = ["dashboard.html", "yellow-belt/", "green-belt/", "black-belt/", "masters.html"];
        if (lockedPaths.some(p => path.includes(p))) {
            const prefix = (path.includes("-belt/") || path.includes("/education-policy/")) ? "../" : "";
            window.location.href = prefix + "login.html";
        }
    }

    // Update Navigation UI (Dashboard / Profile links)
    const links = document.querySelectorAll("a");
    const isBeltPath = path.includes("/green-belt/") || path.includes("/white-belt/") || path.includes("/yellow-belt/") || path.includes("/black-belt/") || path.includes("/education-policy/");
    const isNestedPolicy = path.includes("/education-policy/global/") || path.includes("/education-policy/national/");
    let prefix = "";
    if (isNestedPolicy) prefix = "../../";
    else if (isBeltPath) prefix = "../";

    links.forEach(link => {
        const text = link.innerText.toUpperCase().trim();
        const isDashboardBtn = link.classList.contains("dashboard-btn");
        const isMyProfile = text === "MY PROFILE" || text.includes("MY PROFILE");
        const isLoginSignUp = text.includes("LOGIN / SIGN UP") || text.includes("LOG IN / SIGN UP") || text.includes("MY DASHBOARD / LOGIN");

        if (isDashboardBtn || isMyProfile || isLoginSignUp) {
            if (user) {
                link.innerHTML = 'MY DASHBOARD <i class="fas fa-chart-line ml-1"></i>';
                link.href = prefix + "dashboard.html";

                // Add Logout button if not present
                if (!link.nextElementSibling?.classList.contains("logout-btn") && !isBeltPath && !isNestedPolicy) {
                    const logoutBtn = document.createElement("button");
                    logoutBtn.classList.add("logout-btn", "text-xs", "text-gray-400", "hover:text-red-400", "ml-3");
                    logoutBtn.textContent = "Logout";
                    logoutBtn.onclick = (e) => {
                        e.preventDefault();
                        localStorage.removeItem("fourAlphaUser");
                        signOut(auth).then(() => {
                            window.location.href = prefix + "index.html";
                        });
                    };
                    link.parentNode.insertBefore(logoutBtn, link.nextSibling);
                }
            } else {
                if (isMyProfile || isDashboardBtn || isLoginSignUp) {
                    link.innerHTML = 'LOGIN / SIGN UP <i class="fas fa-sign-in-alt ml-1"></i>';
                    link.href = prefix + "login.html";
                }
                if (link.nextElementSibling?.classList.contains("logout-btn")) {
                    link.nextElementSibling.remove();
                }
            }
        }
    });
});