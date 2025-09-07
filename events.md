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
  <a href="{{ event.url | relative_url }}" style="font-size: 1.25em; font-weight: bold;">{{ event.title }}</a>
      <span style="color: #888; font-size: 0.9em;">({{ event.date | date: '%Y-%m-%d' }})</span>
      <br>
      <span style="font-size: 0.95em;">{{ event.description }}</span>
      {% if event.principles_violated and event.principles_violated.size > 0 %}
        <div style="margin-top: 0.5em; display: flex; flex-wrap: wrap; gap: 0.5em; align-items: center;">
          {% for principle_slug in event.principles_violated %}
            {% assign principle = site.principles | where: "slug", principle_slug | first %}
            {% if principle %}
              <a href="{{ principle.url | relative_url }}" style="background: #e6f0fa; color: #005a9c; padding: 0.2em 0.7em; border-radius: 1em; font-size: 0.95em; text-decoration: none;">{{ principle.title }}</a>
            {% else %}
              <span style="background: #eee; color: #888; padding: 0.2em 0.7em; border-radius: 1em; font-size: 0.95em;">{{ principle_slug }}</span>
            {% endif %}
          {% endfor %}
        </div>
      {% endif %}
    </li>
  {% endfor %}
</ul>
{% else %}
<p>No events found.</p>
{% endif %}
