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

Research outputs • journals, conference papers, and thesis work
# Publications

A structured, searchable overview of my research across AI in healthcare, human-AI interaction, service-system optimization, simulation, and clinical analytics.

<div class="pub-summary-links">
  <a href="{{ pub_data.profiles.scholar_url }}">{{ pub_data.profiles.scholar_label }}</a>
  <a href="{{ pub_data.profiles.orcid_url }}">{{ pub_data.profiles.orcid_label }}</a>
  <a href="{{ '/files/Moustafa_Abdelwanis_CV.pdf' | relative_url }}">Download CV</a>
</div>

<div class="pub-metrics-grid">
  <div class="pub-metric-card">
    <div class="pub-metric-value">{{ pub_data.analytics.listed_outputs }}</div>
    <div class="pub-metric-label">Verified outputs listed on this page.</div>
  </div>
  <div class="pub-metric-card">
    <div class="pub-metric-value">{{ pub_data.analytics.journal_articles }}</div>
    <div class="pub-metric-label">Journal articles and review papers.</div>
  </div>
  <div class="pub-metric-card">
    <div class="pub-metric-value">{{ pub_data.analytics.conference_papers }}</div>
    <div class="pub-metric-label">Conference papers and proceedings contributions.</div>
  </div>
  <div class="pub-metric-card">
    <div class="pub-metric-value">{{ pub_data.analytics.theses }}</div>
    <div class="pub-metric-label">Thesis currently verified in public sources.</div>
  </div>
  {% if scholar %}
  <div class="pub-metric-card">
    <div class="pub-metric-value">{{ scholar.citations }}</div>
    <div class="pub-metric-label">Google Scholar citations ({{ scholar.last_checked }}).</div>
  </div>
  <div class="pub-metric-card">
    <div class="pub-metric-value">h{{ scholar.h_index }}</div>
    <div class="pub-metric-label">Google Scholar h-index; i10-index {{ scholar.i10_index }}.</div>
  </div>
  {% elsif pub_data.analytics.citations %}
  <div class="pub-metric-card">
    <div class="pub-metric-value">{{ pub_data.analytics.citations }}</div>
    <div class="pub-metric-label">Google Scholar citations ({{ pub_data.analytics.last_checked }}).</div>
  </div>
  <div class="pub-metric-card">
    <div class="pub-metric-value">h{{ pub_data.analytics.h_index }}</div>
    <div class="pub-metric-label">Google Scholar h-index; i10-index {{ pub_data.analytics.i10_index }}.</div>
  </div>
  {% endif %}
</div>

<p>Academic profiles: <a href="{{ pub_data.profiles.scholar_url }}">{{ pub_data.profiles.scholar_label }}</a> | <a href="{{ pub_data.profiles.orcid_url }}">{{ pub_data.profiles.orcid_label }}</a></p>

<p>{{ pub_data.analytics.note }}</p>

<div class="pub-browser">
  <div class="pub-filters">
    <div class="pub-filter-block">
      <div class="pub-filter-label">Type</div>
      <div class="pub-filter-chips">
        <button type="button" class="filter-chip is-active" data-filter-group="type" data-filter-value="all">All</button>
        <button type="button" class="filter-chip" data-filter-group="type" data-filter-value="journal">Journal Articles</button>
        <button type="button" class="filter-chip" data-filter-group="type" data-filter-value="conference">Conference Papers</button>
        <button type="button" class="filter-chip" data-filter-group="type" data-filter-value="thesis">Thesis</button>
      </div>
    </div>

    <div class="pub-filter-block">
      <div class="pub-filter-label">Theme</div>
      <div class="pub-filter-chips">
        <button type="button" class="filter-chip is-active" data-filter-group="theme" data-filter-value="all">All Themes</button>
        <button type="button" class="filter-chip" data-filter-group="theme" data-filter-value="ai-healthcare">AI in Healthcare</button>
        <button type="button" class="filter-chip" data-filter-group="theme" data-filter-value="human-ai">Human-AI Interaction</button>
        <button type="button" class="filter-chip" data-filter-group="theme" data-filter-value="operations-optimization">Operations &amp; Optimization</button>
        <button type="button" class="filter-chip" data-filter-group="theme" data-filter-value="clinical-analytics">Clinical Analytics</button>
        <button type="button" class="filter-chip" data-filter-group="theme" data-filter-value="reviews">Reviews</button>
      </div>
    </div>

    <div class="pub-filter-block">
      <label class="pub-filter-label" for="pub-search">Search</label>
      <input id="pub-search" type="search" placeholder="Search title, venue, authors, keywords, or themes" />
    </div>
  </div>

  <section class="pub-section" data-section="journal">
    <h2>Journal articles</h2>
    <p>Peer-reviewed journal articles and review papers across healthcare AI, human factors, clinical decision support, and operations research.</p>

    {% for item in journals %}
      {% capture search_blob %}{{ item.title }} {{ item.authors }} {{ item.venue }} {{ item.themes | join: ' ' }} {{ item.keywords | join: ' ' }}{% endcapture %}
      <article
        class="pub-record"
        data-type="{{ item.type_slug }}"
        data-themes="{{ item.theme_slugs | join: ' ' }}"
        data-search="{{ search_blob | strip | strip_newlines | replace: '"', '&quot;' | downcase }}">
        <div class="pub-record-meta">
          <span>{{ item.year }}</span>
          <span>{{ item.type_label }}</span>
          {% if item.citations %}<span>{{ item.citations }} Scholar citations</span>{% endif %}
        </div>

        {% if item.highlight %}<div class="pub-record-highlight">{{ item.highlight }}</div>{% endif %}
        <h3>{{ item.title }}</h3>
        <p class="pub-record-authors">{{ item.authors }}</p>
        <p class="pub-record-venue">{{ item.venue }}</p>
        <p>{{ item.description }}</p>
        {% if item.summary_note %}<p class="pub-record-note">{{ item.summary_note }}</p>{% endif %}

        {% if item.themes and item.themes.size > 0 %}
        <ul class="pub-tags">
          {% for theme in item.themes %}
          <li>{{ theme }}</li>
          {% endfor %}
        </ul>
        {% endif %}

        {% if item.links and item.links.size > 0 %}
        <p class="pub-record-links">
          {% for link in item.links %}
            <a href="{{ link.url }}">{{ link.label }}</a>{% unless forloop.last %} {% endunless %}
          {% endfor %}
        </p>
        {% endif %}
      </article>
    {% endfor %}
  </section>

  <section class="pub-section" data-section="conference">
    <h2>Conference papers</h2>
    <p>Proceedings papers spanning simulation, healthcare resilience, AI adoption, metaheuristics, and clinical machine learning.</p>

    {% for item in conferences %}
      {% capture search_blob %}{{ item.title }} {{ item.authors }} {{ item.venue }} {{ item.themes | join: ' ' }} {{ item.keywords | join: ' ' }}{% endcapture %}
      <article
        class="pub-record"
        data-type="{{ item.type_slug }}"
        data-themes="{{ item.theme_slugs | join: ' ' }}"
        data-search="{{ search_blob | strip | strip_newlines | replace: '"', '&quot;' | downcase }}">
        <div class="pub-record-meta">
          <span>{{ item.year }}</span>
          <span>{{ item.type_label }}</span>
          {% if item.citations %}<span>{{ item.citations }} Scholar citations</span>{% endif %}
        </div>

        {% if item.highlight %}<div class="pub-record-highlight">{{ item.highlight }}</div>{% endif %}
        <h3>{{ item.title }}</h3>
        <p class="pub-record-authors">{{ item.authors }}</p>
        <p class="pub-record-venue">{{ item.venue }}</p>
        <p>{{ item.description }}</p>
        {% if item.summary_note %}<p class="pub-record-note">{{ item.summary_note }}</p>{% endif %}

        {% if item.themes and item.themes.size > 0 %}
        <ul class="pub-tags">
          {% for theme in item.themes %}
          <li>{{ theme }}</li>
          {% endfor %}
        </ul>
        {% endif %}

        {% if item.links and item.links.size > 0 %}
        <p class="pub-record-links">
          {% for link in item.links %}
            <a href="{{ link.url }}">{{ link.label }}</a>{% unless forloop.last %} {% endunless %}
          {% endfor %}
        </p>
        {% endif %}
      </article>
    {% endfor %}
  </section>

  <section class="pub-section" data-section="thesis">
    <h2>Thesis</h2>
    <p>Long-form degree research that anchors the optimization and simulation stream of the publication record.</p>

    {% for item in theses %}
      {% capture search_blob %}{{ item.title }} {{ item.authors }} {{ item.venue }} {{ item.themes | join: ' ' }} {{ item.keywords | join: ' ' }}{% endcapture %}
      <article
        class="pub-record"
        data-type="{{ item.type_slug }}"
        data-themes="{{ item.theme_slugs | join: ' ' }}"
        data-search="{{ search_blob | strip | strip_newlines | replace: '"', '&quot;' | downcase }}">
        <div class="pub-record-meta">
          <span>{{ item.year }}</span>
          <span>{{ item.type_label }}</span>
        </div>

        {% if item.highlight %}<div class="pub-record-highlight">{{ item.highlight }}</div>{% endif %}
        <h3>{{ item.title }}</h3>
        <p class="pub-record-authors">{{ item.authors }}</p>
        <p class="pub-record-venue">{{ item.venue }}</p>
        <p>{{ item.description }}</p>
        {% if item.summary_note %}<p class="pub-record-note">{{ item.summary_note }}</p>{% endif %}

        {% if item.themes and item.themes.size > 0 %}
        <ul class="pub-tags">
          {% for theme in item.themes %}
          <li>{{ theme }}</li>
          {% endfor %}
        </ul>
        {% endif %}

        {% if item.links and item.links.size > 0 %}
        <p class="pub-record-links">
          {% for link in item.links %}
            <a href="{{ link.url }}">{{ link.label }}</a>{% unless forloop.last %} {% endunless %}
          {% endfor %}
        </p>
        {% endif %}
      </article>
    {% endfor %}
  </section>

  <div class="pub-empty-state" hidden>
    No publications match the current filters. Try clearing the search box or switching back to All Themes.
  </div>
</div>

<script src="{{ '/assets/js/publications.js' | relative_url }}"></script>
