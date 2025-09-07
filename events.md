---
layout: page
title: Events
permalink: /events/
---

<h1>Events</h1>
{% if site.events %}
<ul style="list-style: disc; padding-left: 1.2em;">
  {% assign events = site.events | sort: 'date' | reverse %}
  {% for event in events %}
    <li style="margin-bottom: 1.5em;">
      <a href="{{ event.url | relative_url }}">{{ event.title }}</a>
      <span style="color: #888; font-size: 0.9em;">({{ event.date | date: '%Y-%m-%d' }})</span>
      <br>
      <span style="font-size: 0.95em;">{{ event.description }}</span>
    </li>
  {% endfor %}
</ul>
{% else %}
<p>No events found.</p>
{% endif %}
