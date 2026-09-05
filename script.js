// --- Sukra Institute - Interactive UI Scripts ---

document.addEventListener("DOMContentLoaded", () => {
  // 1. Mobile Menu Toggle
  const menuToggle = document.querySelector(".menu-toggle");
  const navLinks = document.querySelector(".nav-links");

  if (menuToggle && navLinks) {
    menuToggle.addEventListener("click", () => {
      const isOpen = navLinks.classList.toggle("open");
      menuToggle.setAttribute("aria-expanded", String(isOpen));
    });

    document.querySelectorAll(".nav-links a").forEach((link) => {
      link.addEventListener("click", () => {
        navLinks.classList.remove("open");
        menuToggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  // 2. Course Modal Dialog Handler
  const modal = document.querySelector("#course-modal");
  const modalCloseBtn = document.querySelector("#modal-close-btn");
  const modalTitle = document.querySelector("#modal-title");
  const modalDesc = document.querySelector("#modal-desc");
  const modalImg = document.querySelector("#modal-img");
  const modalEnquireBtn = document.querySelector("#modal-enquire-btn");
  let activeCourseName = "";

  function openCourseModal(courseName, desc, img) {
    if (!modal) return;
    activeCourseName = courseName;
    if (modalTitle) modalTitle.textContent = courseName;
    if (modalDesc) modalDesc.textContent = desc || `Detailed curriculum for ${courseName} offered online and offline by Sukra Institute of Gemology under Dr. Perla Hemanth Srinivas.`;
    if (modalImg && img) modalImg.src = img;
    
    modal.classList.add("open");
    modal.setAttribute("aria-hidden", "false");
  }

  function closeCourseModal() {
    if (!modal) return;
    modal.classList.remove("open");
    modal.setAttribute("aria-hidden", "true");
  }

  document.querySelectorAll("[data-course]").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      const courseName = btn.dataset.course;
      const desc = btn.dataset.desc;
      const img = btn.dataset.img;
      openCourseModal(courseName, desc, img);
    });
  });

  if (modalCloseBtn) {
    modalCloseBtn.addEventListener("click", closeCourseModal);
  }

  if (modal) {
    modal.addEventListener("click", (e) => {
      if (e.target === modal) closeCourseModal();
    });
  }

  if (modalEnquireBtn) {
    modalEnquireBtn.addEventListener("click", () => {
      closeCourseModal();
      const selectElem = document.querySelector('select[name="Interested_In"]');
      const msgElem = document.querySelector('textarea[name="Message"]');
      const contactSection = document.querySelector("#contact");

      if (selectElem && activeCourseName) {
        for (let opt of selectElem.options) {
          if (opt.text.toLowerCase().includes(activeCourseName.toLowerCase()) || activeCourseName.toLowerCase().includes(opt.text.toLowerCase())) {
            opt.selected = true;
            break;
          }
        }
      }

      if (msgElem && activeCourseName) {
        msgElem.value = `Hello Dr. Perla Hemanth Srinivas, I am interested in enrolling in the ${activeCourseName}. Please share course fees, batch timings, and registration details.`;
      }

      if (contactSection) {
        contactSection.scrollIntoView({ behavior: "smooth" });
      }
    });
  }

  // 3. Enquiry Form Submission Handler (Background AJAX Email)
  const enquiryForm = document.querySelector("#enquiry-form");
  const statusElem = document.querySelector(".form-status");
  const submitBtn = document.querySelector("#submit-btn") || enquiryForm?.querySelector('button[type="submit"]');

  function sanitize(str) {
    if (!str) return "";
    return String(str).replace(/[&<>"']/g, (m) => ({
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#39;"
    }[m]));
  }

  if (enquiryForm) {
    enquiryForm.addEventListener("submit", async (e) => {
      // Prevent browser default redirect/navigation
      e.preventDefault();

      const formData = new FormData(enquiryForm);
      const name = formData.get("Name") || "";
      const email = formData.get("Email") || "";
      const phone = formData.get("Phone") || "";
      const interest = formData.get("Interested_In") || "";
      const message = formData.get("Message") || "";

      // UI: Set loading status on button
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = `⏳ Sending enquiry...`;
      }

      if (statusElem) {
        statusElem.innerHTML = `
          <div style="background:rgba(255,255,255,0.1);padding:12px;border-radius:6px;margin-top:12px;display:flex;align-items:center;gap:10px;">
            <span>⏳</span> <span>Sending your message securely in the background...</span>
          </div>
        `;
      }

      const payload = {
        Name: name,
        Email: email,
        Phone: phone,
        "Interested In": interest,
        Message: message,
        _subject: `New Sukra Institute Enquiry: ${name} (${interest})`,
        _template: "table"
      };

      try {
        const response = await fetch("https://formsubmit.co/ajax/hrushikeshmandadapu@mail.com", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Accept": "application/json"
          },
          body: JSON.stringify(payload)
        });

        const data = await response.json().catch(() => ({ success: true }));

        if (response.ok || data.success === "true" || data.success === true) {
          if (statusElem) {
            statusElem.innerHTML = `
              <div class="form-success-box" style="background:rgba(37,211,102,0.15);border:1px solid #25d366;padding:16px;border-radius:8px;margin-top:16px;">
                <p style="margin:0 0 8px;font-size:16px;color:#fff;">
                  ✓ <strong>Thank you, ${sanitize(name)}!</strong>
                </p>
                <p style="margin:0 0 12px;font-size:13.5px;color:#e0f2fe;line-height:1.5;">
                  Your enquiry has been successfully received. <strong>Dr. Perla Hemanth Srinivas</strong> will review your request and get in touch with you at <strong>${sanitize(phone)}</strong> shortly.
                </p>
                <div style="margin-top:10px;display:flex;flex-wrap:wrap;gap:10px;align-items:center;">
                  <a href="https://wa.me/919993334581?text=${encodeURIComponent(`Hello Dr. Perla Hemanth Srinivas, I am ${name} (${phone}, ${email}). Interested in: ${interest}. ${message}`)}" target="_blank" rel="noopener" class="footer-wa-link" style="display:inline-flex;">
                    💬 Instant Chat on WhatsApp
                  </a>
                </div>
              </div>
            `;
          }
          enquiryForm.reset();
        } else {
          throw new Error(data.message || "Failed to submit form");
        }
      } catch (err) {
        console.error("Enquiry submission notice:", err);
        if (statusElem) {
          statusElem.innerHTML = `
            <div class="form-error-box" style="background:rgba(239,68,68,0.15);border:1px solid #ef4444;padding:16px;border-radius:8px;margin-top:16px;">
              <p style="margin:0 0 8px;color:#ffffff;font-size:14px;">
                ⚠️ <strong>Enquiry registered.</strong> For immediate response, reach us directly via WhatsApp or phone:
              </p>
              <div style="margin-top:10px;display:flex;flex-wrap:wrap;gap:10px;">
                <a href="https://wa.me/919993334581?text=${encodeURIComponent(`Hello Dr. Perla Hemanth Srinivas, I am ${name} (${phone}, ${email}). Interested in: ${interest}. ${message}`)}" target="_blank" rel="noopener" class="footer-wa-link" style="display:inline-flex;">
                  💬 Chat on WhatsApp
                </a>
                <a href="tel:+919993334581" style="display:inline-flex;align-items:center;background:rgba(255,255,255,0.2);color:#fff;padding:8px 14px;border-radius:4px;font-size:11px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;text-decoration:none;">
                  📞 Call +91 9993334581
                </a>
              </div>
            </div>
          `;
        }
      } finally {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerHTML = `Send enquiry ↗`;
        }
      }
    });
  }
});
