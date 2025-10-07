---
layout: page
title: Tactics
permalink: /tactics/
---

<h1>Anti-Democratic Tactics</h1>
{% if site.tactics %}
<ul style="list-style: disc; padding-left: 1.2em;">
  {% assign items = site.tactics | sort: 'date' | reverse %}
  {% for tactic in items %}
    <li style="margin-bottom: 1.2em;">
      <a href="{{ tactic.url | relative_url }}" style="font-weight:600; font-size:1.05em;">{{ tactic.title }}</a>
      <div style="color:#666; font-size:0.95em;">{{ tactic.description }}</div>
    </li>
  {% endfor %}
</ul>
{% else %}
<p>No tactics found.</p>
{% endif %}
