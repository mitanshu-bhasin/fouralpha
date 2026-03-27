import { db } from './firebase-config.js';
import { collection, addDoc, serverTimestamp } from "https://www.gstatic.com/firebasejs/11.4.0/firebase-firestore.js";

document.addEventListener("DOMContentLoaded", () => {
    const contactForm = document.getElementById("contact-form");
    const nameInput = document.getElementById("contact-name");
    const emailInput = document.getElementById("contact-email");
    const messageInput = document.getElementById("contact-message");
    const submitBtn = document.getElementById("contact-submit");
    const toast = document.getElementById("contact-toast");

    if (contactForm) {
        contactForm.addEventListener("submit", async (e) => {
            e.preventDefault();

            submitBtn.innerHTML = 'Transmitting... <i class="fas fa-spinner fa-spin ml-2"></i>';
            submitBtn.disabled = true;
            toast.classList.add("hidden");

            try {
                await addDoc(collection(db, "contacts"), {
                    name: nameInput.value.trim(),
                    email: emailInput.value.trim(),
                    message: messageInput.value.trim(),
                    timestamp: serverTimestamp(),
                    status: "unread"
                });

                // Success
                contactForm.reset();
                toast.innerHTML = '<i class="fas fa-check-circle mr-2"></i> Message transmitted successfully. We will respond shortly.';
                toast.className = "text-sm font-bold p-3 rounded bg-green-500/10 text-green-400 border border-green-500/30";
                toast.classList.remove("hidden");
            } catch (error) {
                console.error("Error adding document: ", error);
                toast.innerHTML = '<i class="fas fa-exclamation-triangle mr-2"></i> Transmission failed. Please contact us directly via email.';
                toast.className = "text-sm font-bold p-3 rounded bg-red-500/10 text-red-400 border border-red-500/30";
                toast.classList.remove("hidden");
            } finally {
                submitBtn.innerHTML = 'Initiate Transmission <i class="fas fa-paper-plane ml-2"></i>';
                submitBtn.disabled = false;
            }
        });
    }
});
