---
layout: single
title: "Research"
permalink: /research/
author_profile: true
---

{% assign profile = site.data.site_profile %}
{% assign grants = nil %}
{% if profile and profile.grants %}
  {% assign grants = profile.grants %}
{% endif %}

My research integrates operations management, simulation, machine learning, and human factors to address real-world challenges in healthcare and service systems. Across these themes, I focus on designing decision-support tools that are analytically rigorous, operationally realistic, and safe for end users.

## Research grants

{% if grants and grants.size > 0 %}
{% for grant in grants %}
### {{ grant.project_title }}

- **Role:** {{ grant.role }}
- **Grant scheme:** {{ grant.title }}
- **Sponsor:** {{ grant.sponsor }}
- **Funding:** {{ grant.amount }}
- **Focus:** {{ grant.summary }}

{% endfor %}
{% else %}
### Human-AI Collaboration in Medical Training: Balancing Learning Acceleration Against Automation Bias

- **Role:** Co-Investigator
- **Grant scheme:** International Research Grant
- **Sponsor:** GMU, UAE
- **Funding:** Approximately AED 90,000
- **Focus:** Funded project on how AI-supported medical training can accelerate learning while mitigating automation bias and preserving safe human judgment.
{% endif %}

## Core research themes

The topics below organize my research agenda across healthcare operations, AI adoption, human factors, and analytics. Together, they show how my work moves from funded projects and safety questions to methods development and applied decision support.

## 1. AI adoption in healthcare

I study the organizational, behavioral, and safety factors that influence the adoption of AI in healthcare settings. This includes healthcare providers' perceptions, implementation barriers, and the design of interventions that improve trust, safety, usability, and human oversight.

Representative topics:
- Healthcare AI adoption barriers
- Human-AI interaction
- Automation bias
- Patient safety and risk analysis
- Medical training and AI-enabled learning

## 2. Simulation-based optimization

I develop computationally efficient simulation-based optimization approaches for complex service systems, especially settings that involve multi-skilled staff, constrained inventories, and dynamic operational trade-offs.

Representative topics:
- Multi-skill, multi-server queues
- Skill assignment and cross-training
- Simulation for healthcare and service operations
- Variable neighborhood search
- Decision support for operational planning

## 3. Organ transplantation

I study the risks associated with kidney transplantation and investigate models for improving allocation decisions with attention to both utility and fairness.

Representative topics:
- Survival analysis
- Fairness between recipients
- Allocation priorities
- Optimization for transplantation systems

## 4. Healthcare data analytics and AI

I apply data-driven methods to support clinical assessment, risk prediction, and decision-making. My work explores classification pipelines, interpretable modeling, and practical healthcare analytics applications.

Representative topics:
- AI-enabled decision support
- Explainable AI
- Cardiac autonomic neuropathy assessment
- Depression severity detection
- Clinical risk modeling
