---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
---

{% assign pub_data = site.data.publications %}
{% assign profile = site.data.site_profile %}
{% assign journals = pub_data.outputs | where: "type_slug", "journal" %}
{% assign conferences = pub_data.outputs | where: "type_slug", "conference" %}
{% assign theses = pub_data.outputs | where: "type_slug", "thesis" %}
{% assign scholar = nil %}
{% if profile and profile.scholar_metrics %}
  {% assign scholar = profile.scholar_metrics %}
{% endif %}

<section class="page__hero--custom page__hero--compact">
  <div class="hero-badge">Research outputs • journals, conference papers, and thesis work</div>
  <h1 class="hero-title">Publications</h1>
  <p class="hero-subtitle">A structured, searchable overview of my research across AI in healthcare, human-AI interaction, service-system optimization, simulation, and clinical analytics.</p>
  <div class="hero-actions">
    <a class="btn btn--primary" href="{{ pub_data.profiles.scholar_url }}">{{ pub_data.profiles.scholar_label }}</a>
    <a class="btn btn--inverse" href="{{ pub_data.profiles.orcid_url }}">{{ pub_data.profiles.orcid_label }}</a>
    <a class="btn btn--inverse" href="/files/Moustafa_Abdelwanis_CV.pdf">Download CV</a>
  </div>
</section>

<section class="quick-stats quick-stats--publications">
  <div class="stat-card">
    <span class="stat-number">{{ pub_data.analytics.listed_outputs }}</span>
    <div class="stat-label">Verified outputs listed on this page.</div>
  </div>
  <div class="stat-card">
    <span class="stat-number">{{ pub_data.analytics.journal_articles }}</span>
    <div class="stat-label">Journal articles and review papers.</div>
  </div>
  <div class="stat-card">
    <span class="stat-number">{{ pub_data.analytics.conference_papers }}</span>
    <div class="stat-label">Conference papers and proceedings contributions.</div>
  </div>
  <div class="stat-card">
    <span class="stat-number">{{ pub_data.analytics.theses }}</span>
    <div class="stat-label">Thesis currently verified in public sources.</div>
  </div>
  {% if scholar %}
  <div class="stat-card">
    <span class="stat-number">{{ scholar.citations }}</span>
    <div class="stat-label">Google Scholar citations ({{ scholar.last_checked }}).</div>
  </div>
  <div class="stat-card">
    <span class="stat-number">h{{ scholar.h_index }}</span>
    <div class="stat-label">Google Scholar h-index; i10-index {{ scholar.i10_index }}.</div>
  </div>
  {% elsif pub_data.analytics.citations %}
  <div class="stat-card">
    <span class="stat-number">{{ pub_data.analytics.citations }}</span>
    <div class="stat-label">Google Scholar citations ({{ pub_data.analytics.last_checked }}).</div>
  </div>
  <div class="stat-card">
    <span class="stat-number">h{{ pub_data.analytics.h_index }}</span>
    <div class="stat-label">Google Scholar h-index; i10-index {{ pub_data.analytics.i10_index }}.</div>
  </div>
  {% endif %}
</section>

<section class="section-block pub-browser">
  <div class="profiles-line">
    Academic profiles:
    <a href="{{ pub_data.profiles.scholar_url }}">{{ pub_data.profiles.scholar_label }}</a>
    <span class="profiles-separator">|</span>
    <a href="{{ pub_data.profiles.orcid_url }}">{{ pub_data.profiles.orcid_label }}</a>
  </div>

  <p class="pub-note-banner">{{ pub_data.analytics.note }}</p>

  <section class="section-block pub-section" data-section="journal">
    <div class="section-heading-stack">
      <h2 class="section-title">Journal articles</h2>
      <p class="section-intro">Peer-reviewed journal articles and review papers across healthcare AI, human factors, clinical decision support, and operations research.</p>
    </div>
    <div class="publication-list publication-list--detailed">
      {% for item in journals %}
      {% capture search_blob %}{{ item.title }} {{ item.authors }} {{ item.venue }} {{ item.themes | join: ' ' }} {{ item.keywords | join: ' ' }}{% endcapture %}
      <article class="pub-card pub-card--detailed pub-record" data-type="{{ item.type_slug }}" data-themes="{{ item.theme_slugs | join: ' ' }}" data-search="{{ search_blob | strip_newlines | downcase | escape }}">
        <div class="pub-topline">
          <div class="pub-meta">
            <span class="pub-year">{{ item.year }}</span>
            <span class="pub-venue">{{ item.type_label }}</span>
            {% if item.citations %}<span class="pub-citations">{{ item.citations }} Scholar citations</span>{% endif %}
          </div>
          {% if item.highlight %}<span class="pub-highlight">{{ item.highlight }}</span>{% endif %}
        </div>
        <h3 class="pub-title">{{ item.title }}</h3>
        <p class="pub-authors">{{ item.authors }}</p>
        <p class="pub-venue-line">{{ item.venue }}</p>
        <p class="pub-summary">{{ item.description }}</p>
        {% if item.summary_note %}<p class="pub-summary-note">{{ item.summary_note }}</p>{% endif %}
        <ul class="tag-list">
          {% for theme in item.themes %}<li class="tag">{{ theme }}</li>{% endfor %}
        </ul>
        <div class="pub-links">
          {% for link in item.links %}<a href="{{ link.url }}">{{ link.label }}</a>{% endfor %}
        </div>
      </article>
      {% endfor %}
    </div>
  </section>

  <section class="section-block pub-section" data-section="conference">
    <div class="section-heading-stack">
      <h2 class="section-title">Conference papers</h2>
      <p class="section-intro">Proceedings papers spanning simulation, healthcare resilience, AI adoption, metaheuristics, and clinical machine learning.</p>
    </div>
    <div class="publication-list publication-list--detailed">
      {% for item in conferences %}
      {% capture search_blob %}{{ item.title }} {{ item.authors }} {{ item.venue }} {{ item.themes | join: ' ' }} {{ item.keywords | join: ' ' }}{% endcapture %}
      <article class="pub-card pub-card--detailed pub-record" data-type="{{ item.type_slug }}" data-themes="{{ item.theme_slugs | join: ' ' }}" data-search="{{ search_blob | strip_newlines | downcase | escape }}">
        <div class="pub-topline">
          <div class="pub-meta">
            <span class="pub-year">{{ item.year }}</span>
            <span class="pub-venue">{{ item.type_label }}</span>
            {% if item.citations %}<span class="pub-citations">{{ item.citations }} Scholar citations</span>{% endif %}
          </div>
          {% if item.highlight %}<span class="pub-highlight">{{ item.highlight }}</span>{% endif %}
        </div>
        <h3 class="pub-title">{{ item.title }}</h3>
        <p class="pub-authors">{{ item.authors }}</p>
        <p class="pub-venue-line">{{ item.venue }}</p>
        <p class="pub-summary">{{ item.description }}</p>
        {% if item.summary_note %}<p class="pub-summary-note">{{ item.summary_note }}</p>{% endif %}
        <ul class="tag-list">
          {% for theme in item.themes %}<li class="tag">{{ theme }}</li>{% endfor %}
        </ul>
        <div class="pub-links">
          {% for link in item.links %}<a href="{{ link.url }}">{{ link.label }}</a>{% endfor %}
        </div>
      </article>
      {% endfor %}
    </div>
  </section>

  <section class="section-block pub-section" data-section="thesis">
    <div class="section-heading-stack">
      <h2 class="section-title">Thesis</h2>
      <p class="section-intro">Long-form degree research that anchors the optimization and simulation stream of the publication record.</p>
    </div>
    <div class="publication-list publication-list--detailed">
      {% for item in theses %}
      {% capture search_blob %}{{ item.title }} {{ item.authors }} {{ item.venue }} {{ item.themes | join: ' ' }} {{ item.keywords | join: ' ' }}{% endcapture %}
      <article class="pub-card pub-card--detailed pub-record" data-type="{{ item.type_slug }}" data-themes="{{ item.theme_slugs | join: ' ' }}" data-search="{{ search_blob | strip_newlines | downcase | escape }}">
        <div class="pub-topline">
          <div class="pub-meta">
            <span class="pub-year">{{ item.year }}</span>
            <span class="pub-venue">{{ item.type_label }}</span>
          </div>
          {% if item.highlight %}<span class="pub-highlight">{{ item.highlight }}</span>{% endif %}
        </div>
        <h3 class="pub-title">{{ item.title }}</h3>
        <p class="pub-authors">{{ item.authors }}</p>
        <p class="pub-venue-line">{{ item.venue }}</p>
        <p class="pub-summary">{{ item.description }}</p>
        {% if item.summary_note %}<p class="pub-summary-note">{{ item.summary_note }}</p>{% endif %}
        <ul class="tag-list">
          {% for theme in item.themes %}<li class="tag">{{ theme }}</li>{% endfor %}
        </ul>
        <div class="pub-links">
          {% for link in item.links %}<a href="{{ link.url }}">{{ link.label }}</a>{% endfor %}
        </div>
      </article>
      {% endfor %}
    </div>
  </section>

  <div class="pub-empty-state" hidden>
    <strong>No publications match the current filters.</strong>
    <span>Try clearing the search box or switching back to All Themes.</span>
  </div>
</section>

<script src="{{ '/assets/js/publications.js' | relative_url }}"></script>
