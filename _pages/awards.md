---
layout: single
title: "Awards and Recognition"
permalink: /awards/
author_profile: true
---

{% assign profile = site.data.site_profile %}
{% assign grants = nil %}
{% if profile and profile.grants %}
  {% assign grants = profile.grants %}
{% endif %}

## Awards

{% if profile and profile.awards %}
{% for award in profile.awards %}
- **{{ award.title }}**
{% endfor %}
{% else %}
- **Best Paper Award**, 50th International Conference on Computers and Industrial Engineering (CIE 50), 2023.
- **Best Paper Award**, Graduate Student Research Competition (GSRC), American University in Sharjah, 2024.
- **Outstanding Graduate Student**, Graduate Students Research Awards, Khalifa University, 2024.
{% endif %}

## Research grants

{% if grants and grants.size > 0 %}
{% for grant in grants %}
### {{ grant.project_title }}

- **Role:** {{ grant.role }}
- **Grant scheme:** {{ grant.title }}
- **Sponsor:** {{ grant.sponsor }}
- **Funding:** {{ grant.amount }}
- **Summary:** {{ grant.summary }}

{% endfor %}
{% else %}
### Human-AI Collaboration in Medical Training: Balancing Learning Acceleration Against Automation Bias

- **Role:** Co-Investigator
- **Grant scheme:** International Research Grant
- **Sponsor:** GMU, UAE
- **Funding:** Approximately AED 90,000
- **Summary:** Funded project on how AI-supported medical training can accelerate learning while mitigating automation bias and preserving safe human judgment.
{% endif %}

## Conference participation

- Winter Simulation Conference (WSC), 2024
- Computers and Industrial Engineering (CIE 50), 2023
- International Conference on Variable Neighborhood Search (ICVNS), 2022

## Peer reviewer

- Computers &amp; Industrial Engineering
- Healthcare Analytics
- Computers in Human Behavior Reports
- Current Research in Translational Medicine
- Internet Interventions
