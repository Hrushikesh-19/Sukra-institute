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

  // 3. Enquiry Form Submission Handler
  const enquiryForm = document.querySelector("#enquiry-form");
  const statusElem = document.querySelector(".form-status");

  if (enquiryForm) {
    enquiryForm.addEventListener("submit", (e) => {
      const formData = new FormData(enquiryForm);
      const name = formData.get("Name") || "";
      const phone = formData.get("Phone") || "";
      const interest = formData.get("Interested_In") || "";
      const message = formData.get("Message") || "";

      if (statusElem) {
        statusElem.innerHTML = `
          <div style="background:rgba(255,255,255,0.15);padding:14px;border-radius:6px;margin-top:15px;border:1px solid #fff;">
            ✓ Thank you, <strong>${name}</strong>! Your enquiry has been registered.<br>
            <span style="font-size:13px;opacity:0.9;">Dr. Perla Hemanth Srinivas will contact you shortly.</span>
            <div style="margin-top:12px;">
              <a href="https://wa.me/919993334581?text=${encodeURIComponent(`Hello Dr. Perla Hemanth Srinivas, I am ${name} (${phone}). Interested in: ${interest}. ${message}`)}" target="_blank" rel="noopener" class="button button-small whatsapp-button" style="display:inline-flex;">
                💬 Send via WhatsApp Now
              </a>
            </div>
          </div>
        `;
      }
    });
  }
});
