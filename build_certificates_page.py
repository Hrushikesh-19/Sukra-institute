import json
import re

with open('certificates_data.json', 'r', encoding='utf-8') as f:
    certs = json.load(f)

print(f"Loaded {len(certs)} certificates.")

# Calculate filter counts
count_all = len(certs)
count_navaratna = sum(1 for c in certs if 'NAVARATNA' in c['course'].upper())
count_jyothisha = sum(1 for c in certs if 'JYOTHISHA' in c['course'].upper() or 'ASTROLOGY' in c['course'].upper())
count_numerology = sum(1 for c in certs if 'NUMEROLOGY' in c['course'].upper())
count_batch19 = sum(1 for c in certs if str(c['batch']).strip() == '19')
count_batch18 = sum(1 for c in certs if str(c['batch']).strip() == '18')

# Generate cards HTML
cards_html = []
for idx, c in enumerate(certs):
    file_path = c['file']
    name = c['name']
    slno = c['slno']
    batch = c['batch']
    course = c['course']
    date = c['date']
    place = c['place']
    
    # Classify categories
    cat_tags = []
    if 'NAVARATNA' in course.upper():
        cat_tags.append('navaratna')
    if 'JYOTHISHA' in course.upper() or 'ASTROLOGY' in course.upper():
        cat_tags.append('jyothisha')
    if 'NUMEROLOGY' in course.upper():
        cat_tags.append('numerology')
    if str(batch).strip() == '19':
        cat_tags.append('batch19')
    elif str(batch).strip() == '18':
        cat_tags.append('batch18')
        
    cat_attr = ' '.join(cat_tags)
    
    # Friendly course name
    course_display = course
    if 'NAVARATNA' in course.upper():
        course_display = 'Navaratna Course'
    elif 'JYOTHISHA' in course.upper():
        course_display = 'Jyothisha Vignanam (Astrology)'
    elif 'NUMEROLOGY' in course.upper():
        course_display = 'Numerology Course'
        
    safe_download_name = f"Certificate_{name.replace(' ', '_').replace('.', '_')}_{batch}.jpg"
    
    card = f"""      <!-- Certificate {idx+1}: {name} -->
      <article class="cert-card" data-category="{cat_attr}" data-name="{name}" data-slno="{slno}" data-batch="{batch}" data-course="{course_display}">
        <div class="cert-img-wrap" onclick="openCertLightbox({idx})">
          <img src="{file_path}" alt="Certificate of Completion - {name}" class="cert-thumb" loading="lazy">
          <div class="cert-hover-overlay">
            <span class="view-cert-btn">🔍 Click to View Certificate</span>
          </div>
          {f'<span class="cert-sl-badge">Sl.No: {slno}</span>' if slno else ''}
        </div>
        <div class="cert-info-body">
          <div class="cert-batch-tag">Batch {batch} · {course_display}</div>
          <h3 class="student-name">{name}</h3>
          <p class="cert-desc">
            Successfully completed theoretical &amp; practical requirements for the <strong>{course_display}</strong> at Sukra Institute.
          </p>
          <div class="cert-meta-row">
            <div><span>Date:</span> <strong>{date}</strong></div>
            <div><span>Place:</span> <strong>{place}</strong></div>
          </div>
          <div class="cert-meta-instructor">
            <span>Issued by:</span> <strong>Dr. Perla Hemanth Srinivas</strong>
          </div>
          <div class="cert-card-actions">
            <button type="button" class="button button-small cert-modal-btn" onclick="openCertLightbox({idx})">🔍 Full View</button>
            <a href="{file_path}" target="_blank" class="cert-download-link" download="{safe_download_name}">📥 Download</a>
          </div>
        </div>
      </article>"""
    cards_html.append(card)

cards_joined = '\n\n'.join(cards_html)
json_embedded = json.dumps(certs, ensure_ascii=False)

html_content = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="description" content="Verified Course Completion Certificates & Graduates of Sukra Institute of Gemology under Dr. Perla Hemanth Srinivas. MSME & ISO Certified.">
  <title>Student Certificates | Sukra Institute of Gemology</title>
  <link rel="icon" type="image/png" href="logo.png">
  <meta property="og:title" content="Student Certificates | Sukra Institute of Gemology">
  <meta property="og:description" content="Verified course completion certificates and graduates of Sukra Institute of Gemology.">
  <meta property="og:image" content="logo.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Playfair+Display:ital,wght@0,500;0,600;0,700;1,500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css">
</head>
<body class="certificates-page">

<!-- SITE HEADER -->
<header class="site-header">
  <a class="brand" href="index.html#home">
    <img src="logo.png" alt="Sukra Institute Logo" class="brand-logo">
    <span>
      <strong>SUKRA</strong>
      <small>INSTITUTE OF GEMOLOGY</small>
    </span>
  </a>
  <button class="menu-toggle" aria-label="Open navigation menu" aria-expanded="false">☰</button>
  <nav class="nav-links">
    <a href="index.html#home">Home</a>
    <a href="index.html#about">About</a>
    <a href="index.html#courses">Courses</a>
    <a href="certificates.html" class="active-nav">Certificates</a>
    <a href="index.html#why-sukra">Why Sukra</a>
    <a href="index.html#gemstones">Gemstones</a>
    <a href="index.html#consultation">Consultation</a>
    <a href="index.html#jewellery">Jewellery</a>
    <a href="index.html#contact">Contact</a>
    <a class="button button-small" href="index.html#contact">Enquire now ↗</a>
  </nav>
</header>

<main>
  <!-- CERTIFICATES HERO BANNER -->
  <section class="cert-hero">
    <div class="cert-hero-content">
      <div class="cert-badge-pill">
        <span>🎓</span> Verified Academic Credentials &amp; Certifications
      </div>
      <h1>Student <em>Certificates</em><br>&amp; Course Completions</h1>
      <p class="cert-hero-lead">
        Honoring our <strong>{count_all} certified graduates</strong> who have successfully fulfilled the theoretical and laboratory practical training requirements under <strong>Dr. Perla Hemanth Srinivas</strong> at Sukra Institute of Gemology.
      </p>
      
      <div class="cert-trust-badges">
        <div class="trust-pill">
          <span class="pill-icon">🏛️</span>
          <div>
            <strong>MSME Registered</strong>
            <small>UDYAM-AP-22-0047511</small>
          </div>
        </div>
        <div class="trust-pill">
          <span class="pill-icon">💎</span>
          <div>
            <strong>ISO Certified</strong>
            <small>Quality &amp; Research</small>
          </div>
        </div>
        <div class="trust-pill">
          <span class="pill-icon">📜</span>
          <div>
            <strong>Smarthhagama Trust</strong>
            <small>Gurukula Vedha Vidhyapeetam</small>
          </div>
        </div>
        <div class="trust-pill">
          <span class="pill-icon">📍</span>
          <div>
            <strong>Pedakurapadu</strong>
            <small>Palnadu District, AP</small>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- CONTROLS & FILTER SECTION -->
  <section class="cert-gallery-section">
    <div class="cert-gallery-header">
      <div class="gallery-title-group">
        <p class="section-kicker">Certified Graduates</p>
        <h2>Hall of <em>Excellence.</em></h2>
        <p class="muted">Explore certificates issued to our students across Batch 18 &amp; Batch 19. Filter by course or search by student name.</p>
      </div>
      
      <div class="cert-search-box">
        <span class="search-icon">🔍</span>
        <input type="text" id="cert-search-input" placeholder="Search by student name, serial no, course..." aria-label="Search certificates">
      </div>
    </div>

    <!-- Filter Buttons -->
    <div class="cert-filters">
      <button class="filter-btn active" data-filter="all">All Certificates ({count_all})</button>
      <button class="filter-btn" data-filter="navaratna">Navaratna Course ({count_navaratna})</button>
      <button class="filter-btn" data-filter="jyothisha">Jyothisha Vignanam ({count_jyothisha})</button>
      <button class="filter-btn" data-filter="numerology">Numerology Course ({count_numerology})</button>
      <button class="filter-btn" data-filter="batch19">Batch 19 ({count_batch19})</button>
      <button class="filter-btn" data-filter="batch18">Batch 18 ({count_batch18})</button>
    </div>

    <div class="cert-results-counter" id="cert-counter" style="margin-bottom: 20px; font-size: 13px; color: var(--muted); font-weight: 500;">
      Showing <strong>{count_all}</strong> certificates
    </div>

    <!-- CERTIFICATES GRID -->
    <div class="cert-grid" id="cert-grid">
{cards_joined}
    </div>

    <!-- No results message -->
    <div id="no-cert-msg" class="no-results-box" style="display:none; text-align: center; padding: 60px 20px; background: var(--cream); border-radius: 8px; border: 1px dashed var(--line);">
      <p style="font-size: 1.2rem; color: var(--navy); margin-bottom: 8px;">🔍 No certificates found</p>
      <p style="color: var(--muted);">No student certificate matched your search or filter. Try a different name, serial number, or batch.</p>
    </div>
  </section>

  <!-- CTA ENROLL IN COURSES -->
  <section class="section dark-section cert-enroll-cta">
    <div class="cert-cta-inner">
      <p class="section-kicker">Start Your Journey</p>
      <h2>Earn Your <em>Certification</em> with Us.</h2>
      <p class="muted cert-cta-copy">
        Join our next batch in Gemology, Navaratna &amp; Diamonds, Astrology, Numerology or Vastu Shastra. Learn with hands-on laboratory practicals and earn an officially recognized certification.
      </p>
      <div class="cert-cta-buttons">
        <a href="index.html#courses" class="button">Explore All Courses ↗</a>
        <a href="index.html#contact" class="button button-outline">Enquire for Next Batch ↗</a>
        <a href="https://wa.me/919993334581" target="_blank" rel="noopener" class="button whatsapp-btn">💬 Chat with Dr. Perla Hemanth Srinivas</a>
      </div>
    </div>
  </section>
</main>

<!-- FOOTER -->
<footer class="site-footer">
  <div class="footer-top">
    <div class="footer-col footer-brand-col">
      <a class="brand" href="index.html#home">
        <img src="logo.png" alt="Sukra Institute Logo" class="brand-logo">
        <span>
          <strong>SUKRA</strong>
          <small>INSTITUTE OF GEMOLOGY</small>
        </span>
      </a>
      <p>Professional education and expert guidance by <strong>Dr. Perla Hemanth Srinivas</strong> in Gemology, Diamonds, Astrology, Numerology, Vastu and holistic remedies.</p>
    </div>

    <div class="footer-col footer-address-col">
      <h4>Locations &amp; Address</h4>
      <address class="footer-address">
        <p class="address-main">
          <span class="addr-icon">📍</span>
          <strong>Sukra Institute of Gemology</strong>
          <span>Under Direction of Dr. Perla Hemanth Srinivas</span>
          <span>Serving South India &amp; Online Worldwide</span>
        </p>
        <div class="address-regions">
          <span class="region-pill">Andhra Pradesh</span>
          <span class="region-pill">Telangana</span>
          <span class="region-pill">Karnataka</span>
        </div>
        <p class="address-note">Offline classroom batches &amp; consultations across AP, TS, KA. Live online interactive batches globally.</p>
      </address>
    </div>

    <div class="footer-col footer-links-col">
      <h4>Quick Links</h4>
      <ul class="footer-nav">
        <li><a href="index.html#about">Meet Founder</a></li>
        <li><a href="index.html#courses">Gemology &amp; Diamond Courses</a></li>
        <li><a href="certificates.html">Student Certificates</a></li>
        <li><a href="index.html#gemstones">Certified Gemstones</a></li>
        <li><a href="index.html#consultation">Personal Consultation</a></li>
        <li><a href="index.html#jewellery">Custom Jewellery</a></li>
      </ul>
    </div>

    <div class="footer-col footer-contact-col">
      <h4>Contact &amp; Timings</h4>
      <div class="footer-contact-details">
        <p class="contact-subhead">Direct Helplines &amp; Email</p>
        <p class="phone-row"><a href="tel:+919993334581">📞 +91 9993334581</a></p>
        <p class="phone-row"><a href="tel:+919346160217">📞 +91 9346160217</a></p>
        <p class="email-row"><a href="mailto:hrushikeshmandadapu@mail.com">✉️ hrushikeshmandadapu@mail.com</a></p>
        <div class="wa-container">
          <a href="https://wa.me/919993334581" target="_blank" rel="noopener" class="footer-wa-link">💬 Chat on WhatsApp</a>
        </div>
        <div class="timing-info">
          <p><strong>🕒 Timings:</strong> 10:00 AM – 10:00 PM (Everyday)</p>
          <p><span>Contact for Appointment</span> · Both Online &amp; Offline Available</p>
        </div>
      </div>
    </div>
  </div>

  <div class="footer-bottom">
    <span>© 2026 Sukra Institute of Gemology. All rights reserved.</span>
    <span>Founder &amp; Principal: <strong>Dr. Perla Hemanth Srinivas</strong> (<a href="tel:+919993334581">📞 +91 9993334581</a> / <a href="mailto:hrushikeshmandadapu@mail.com">✉️ hrushikeshmandadapu@mail.com</a>)</span>
    <a href="index.html#home">Back to Home ↑</a>
  </div>
</footer>

<!-- LIGHTBOX MODAL -->
<div class="cert-lightbox" id="cert-lightbox" role="dialog" aria-modal="true" aria-hidden="true">
  <div class="lightbox-overlay" onclick="closeCertLightbox()"></div>
  <div class="lightbox-dialog">
    <button class="lightbox-close" onclick="closeCertLightbox()" aria-label="Close certificate lightbox">✕</button>
    
    <div class="lightbox-nav-controls">
      <button class="lightbox-arrow lightbox-prev" onclick="changeLightboxCert(-1)" aria-label="Previous Certificate">❮</button>
      <button class="lightbox-arrow lightbox-next" onclick="changeLightboxCert(1)" aria-label="Next Certificate">❯</button>
    </div>

    <div class="lightbox-image-wrapper">
      <img src="" alt="Full Certificate View" id="lightbox-img" class="lightbox-cert-img">
    </div>

    <div class="lightbox-caption">
      <div>
        <h4 id="lightbox-student-name">Student Name</h4>
        <p id="lightbox-details">Batch Details · Date · Place</p>
      </div>
      <div class="lightbox-actions">
        <a href="" id="lightbox-download-btn" class="button button-small" download>📥 Download High-Res</a>
        <button type="button" class="button button-small button-outline" onclick="closeCertLightbox()">Close</button>
      </div>
    </div>
  </div>
</div>

<!-- SCRIPTS -->
<script src="script.js"></script>
<script>
  const certificatesData = {json_embedded};

  let currentCertIndex = 0;
  const lightbox = document.getElementById("cert-lightbox");
  const lightboxImg = document.getElementById("lightbox-img");
  const lightboxStudentName = document.getElementById("lightbox-student-name");
  const lightboxDetails = document.getElementById("lightbox-details");
  const lightboxDownloadBtn = document.getElementById("lightbox-download-btn");
  const counterEl = document.getElementById("cert-counter");

  function openCertLightbox(index) {{
    if (index < 0 || index >= certificatesData.length) return;
    currentCertIndex = index;
    const cert = certificatesData[index];
    lightboxImg.src = cert.file;
    lightboxImg.alt = `Certificate - ${{cert.name}}`;
    lightboxStudentName.textContent = cert.slno ? `${{cert.name}} (Sl.No: ${{cert.slno}})` : cert.name;
    lightboxDetails.textContent = `Batch ${{cert.batch}} · ${{cert.course}} · Completed: ${{cert.date}} (${{cert.place}})`;
    lightboxDownloadBtn.href = cert.file;
    lightboxDownloadBtn.download = `Certificate_${{cert.name.replace(/\\s+/g, '_')}}_Batch${{cert.batch}}.jpg`;
    
    lightbox.classList.add("open");
    lightbox.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
  }}

  function closeCertLightbox() {{
    if (!lightbox) return;
    lightbox.classList.remove("open");
    lightbox.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
  }}

  function changeLightboxCert(step) {{
    let nextIndex = currentCertIndex + step;
    if (nextIndex < 0) nextIndex = certificatesData.length - 1;
    if (nextIndex >= certificatesData.length) nextIndex = 0;
    openCertLightbox(nextIndex);
  }}

  // Keyboard navigation
  document.addEventListener("keydown", (e) => {{
    if (lightbox && lightbox.classList.contains("open")) {{
      if (e.key === "Escape") closeCertLightbox();
      if (e.key === "ArrowLeft") changeLightboxCert(-1);
      if (e.key === "ArrowRight") changeLightboxCert(1);
    }}
  }});

  // Search & Filters
  const searchInput = document.getElementById("cert-search-input");
  const filterBtns = document.querySelectorAll(".filter-btn");
  const certCards = document.querySelectorAll(".cert-card");
  const noCertMsg = document.getElementById("no-cert-msg");

  function applyFilter() {{
    const query = searchInput.value.toLowerCase().trim();
    const activeBtn = document.querySelector(".filter-btn.active");
    const activeFilter = activeBtn ? activeBtn.dataset.filter : "all";
    let visibleCount = 0;

    certCards.forEach((card) => {{
      const name = (card.dataset.name || "").toLowerCase();
      const slno = (card.dataset.slno || "").toLowerCase();
      const batch = (card.dataset.batch || "").toLowerCase();
      const course = (card.dataset.course || "").toLowerCase();
      const category = (card.dataset.category || "").toLowerCase();

      const matchesSearch = !query || 
                            name.includes(query) || 
                            slno.includes(query) || 
                            batch.includes(query) || 
                            course.includes(query);
      const matchesFilter = activeFilter === "all" || category.includes(activeFilter);

      if (matchesSearch && matchesFilter) {{
        card.style.display = "flex";
        visibleCount++;
      }} else {{
        card.style.display = "none";
      }}
    }});

    if (counterEl) {{
      counterEl.innerHTML = `Showing <strong>${{visibleCount}}</strong> of <strong>${{certCards.length}}</strong> certificates`;
    }}

    if (noCertMsg) {{
      noCertMsg.style.display = visibleCount === 0 ? "block" : "none";
    }}
  }}

  if (searchInput) {{
    searchInput.addEventListener("input", applyFilter);
  }}

  filterBtns.forEach((btn) => {{
    btn.addEventListener("click", () => {{
      filterBtns.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      applyFilter();
    }});
  }});
</script>
</body>
</html>
"""

with open('certificates.html', 'w', encoding='utf-8') as out:
    out.write(html_content)

print(f"Generated certificates.html successfully with {len(certs)} certificates.")
