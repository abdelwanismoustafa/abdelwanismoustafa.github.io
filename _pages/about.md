---
layout: archive
title: ""
permalink: /
author_profile: true
redirect_from:
  - /about/
---

{% assign pub_data = site.data.publications %}
{% assign profile = site.data.site_profile %}
{% assign featured = pub_data.selected_outputs %}
{% if featured == nil or featured.size == 0 %}
  {% assign featured = pub_data.outputs | slice: 0, 4 %}
{% endif %}
{% assign awards_count = 3 %}
{% if profile and profile.awards %}
  {% assign awards_count = profile.awards | size %}
{% endif %}
{% assign scholar = nil %}
{% if profile and profile.scholar_metrics %}
  {% assign scholar = profile.scholar_metrics %}
{% endif %}

<section class="page__hero--custom">
  <div class="hero-badge">Engineering Systems and Management • Khalifa University</div>
  <h1 class="hero-title">Moustafa Abdelwanis</h1>
  <p class="hero-subtitle">Ph.D. candidate researching operations management, AI in healthcare, human-AI interaction, simulation, and optimization, with a focus on safe and practically deployable decision support for healthcare and service systems.</p>
  <div class="hero-actions">
    <a class="btn btn--primary" href="/publications/">View Publications</a>
    <a class="btn btn--inverse" href="/files/Moustafa_Abdelwanis_CV.pdf">Download CV</a>
    <a class="btn btn--inverse" href="https://scholar.google.com/citations?hl=en&user=VwCuh7MAAAAJ&view_op=list_works">Google Scholar</a>
    <a class="btn btn--inverse" href="mailto:moustafa.abdelwanis@ku.ac.ae">Email</a>
  </div>
</section>

<section class="quick-stats">
  <div class="stat-card">
    <span class="stat-number">{{ pub_data.analytics.listed_outputs }}</span>
    <div class="stat-title">Research outputs</div>
    <div class="stat-label">{{ pub_data.analytics.journal_articles }} journal articles, {{ pub_data.analytics.conference_papers }} conference papers, and {{ pub_data.analytics.theses }} thesis currently featured on the publications page.</div>
  </div>
  <div class="stat-card">
    <span class="stat-number">{{ pub_data.analytics.journal_articles }}</span>
    <div class="stat-title">Journal articles</div>
    <div class="stat-label">Recent work in Safety Science, Computers &amp; Operations Research, Computers in Biology and Medicine, Journal of Heuristics, and Scientific Reports.</div>
  </div>
  <div class="stat-card">
    <span class="stat-number">{{ pub_data.analytics.conference_papers }}</span>
    <div class="stat-title">Conference papers</div>
    <div class="stat-label">Proceedings contributions across WSC, CIE, ICVNS, and Computing in Cardiology.</div>
  </div>
  <div class="stat-card">
    <span class="stat-number">{{ awards_count }}</span>
    <div class="stat-title">Awards and distinctions</div>
    <div class="stat-label">Including CIE 50 Best Paper, GSRC Best Paper, and Outstanding Graduate Student at Khalifa University.</div>
  </div>
</section>

{% if scholar %}
<p class="stats-note">Current analytics shown on the site: {{ scholar.citations }} Google Scholar citations, h-index {{ scholar.h_index }}, and i10-index {{ scholar.i10_index }}.</p>
{% elsif pub_data.analytics.citations %}
<p class="stats-note">Current analytics shown on the site: {{ pub_data.analytics.citations }} Google Scholar citations, h-index {{ pub_data.analytics.h_index }}, and i10-index {{ pub_data.analytics.i10_index }}.</p>
{% endif %}

<section class="section-block">
  <h2 class="section-title">Research focus</h2>
  <p class="section-intro">My work sits at the intersection of operations management, AI in healthcare, human factors, and analytics. I am interested in how intelligent systems can improve healthcare and service operations while remaining safe, human-centered, and operationally realistic.</p>

  <div class="research-grid">
    <article class="theme-card">
      <div class="card-label">AI in healthcare</div>
      <h3>Adoption, trust, and automation risk</h3>
      <p>I study how healthcare professionals adopt AI tools, what shapes trust and usability, and how risks such as automation bias can be identified and mitigated in practice.</p>
      <ul class="tag-list">
        <li class="tag">Human-AI interaction</li>
        <li class="tag">Automation bias</li>
        <li class="tag">Healthcare safety</li>
      </ul>
    </article>

    <article class="theme-card">
      <div class="card-label">Operations research</div>
      <h3>Simulation and optimization for service systems</h3>
      <p>I develop simulation-based optimization methods for multi-server, inventory-constrained, and cross-trained service systems, with applications in healthcare and operations management.</p>
      <ul class="tag-list">
        <li class="tag">Simulation modeling</li>
        <li class="tag">Optimization</li>
        <li class="tag">Service operations</li>
      </ul>
    </article>

    <article class="theme-card">
      <div class="card-label">Clinical analytics</div>
      <h3>Data-driven decision support</h3>
      <p>I apply machine learning and analytics to support clinical assessment and risk prediction, including work on cardiac autonomic neuropathy and depression severity detection.</p>
      <ul class="tag-list">
        <li class="tag">Machine learning</li>
        <li class="tag">Clinical decision support</li>
        <li class="tag">Healthcare analytics</li>
      </ul>
    </article>
  </div>
</section>

<section class="section-block">
  <h2 class="section-title">Current profile</h2>
  <p class="section-intro">A concise overview of my current academic position, research orientation, and recognition.</p>

  <div class="profile-grid">
    <article class="snapshot-card">
      <div class="card-label">Academic snapshot</div>
      <h3>Position and research setting</h3>
      <ul class="point-list">
        <li>Ph.D. candidate in Engineering Systems and Management at Khalifa University.</li>
        <li>Graduate Research and Teaching Assistant since 2021.</li>
        <li>Research spanning operations management, AI in healthcare, human-AI interaction, simulation, and optimization.</li>
        <li>Methods toolkit including simulation modeling, optimization, variable neighborhood search, Bowtie analysis, structural equation modeling, Python, R, and AnyLogic.</li>
      </ul>
    </article>

    <article class="snapshot-card">
      <div class="card-label">Recognition</div>
      <h3>Awards and distinction</h3>
      <ul class="point-list">
        {% if profile and profile.awards %}
          {% for award in profile.awards %}
          <li>{{ award.title }}</li>
          {% endfor %}
        {% else %}
          <li>Best Paper Award, 50th International Conference on Computers and Industrial Engineering (CIE 50), 2023.</li>
          <li>Best Paper Award, Graduate Student Research Competition (GSRC), American University in Sharjah, 2024.</li>
          <li>Outstanding Graduate Student, Graduate Students Research Awards, Khalifa University, 2024.</li>
        {% endif %}
      </ul>
    </article>
  </div>
</section>

<section class="section-block">
  <h2 class="section-title">Selected publications</h2>
  <p class="section-intro">These featured papers are manually curated from the publication records used on this site. Update <code>_data/publications.yml</code> when you want to change the homepage highlights.</p>

  <div class="publication-list">
    {% for item in featured %}
    <article class="pub-card">
      <div class="pub-meta">
        <span class="pub-year">{{ item.year }}</span>
        <span class="pub-venue">{{ item.venue }}</span>
      </div>
      <h3 class="pub-title">{{ item.title }}</h3>
      <p class="pub-summary">{{ item.description }}</p>
      <div class="pub-links">
        {% for link in item.links %}
        <a href="{{ link.url }}">{{ link.label }}</a>
        {% endfor %}
      </div>
    </article>
    {% endfor %}
  </div>
</section>

<section class="contact-strip">
  <div>
    <h3>Open to research collaboration and academic exchange</h3>
    <p>Use the links below to reach out, browse the full publication list, or download the current CV.</p>
  </div>
  <div class="contact-actions">
    <a class="btn btn--primary" href="/publications/">Publications</a>
    <a class="btn btn--inverse" href="mailto:moustafa.abdelwanis@ku.ac.ae">Contact</a>
    <a class="btn btn--inverse" href="https://scholar.google.com/citations?hl=en&user=VwCuh7MAAAAJ&view_op=list_works">Scholar profile</a>
  </div>
</section>
