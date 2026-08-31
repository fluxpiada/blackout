---
title: "The Blackout: Weak Signals — Download"
description: "Download the ePub of The Blackout: Weak Signals."
author: "F. J. S. Remmelzwaal"
---

# The Blackout: Weak Signals
*by F. J. S. Remmelzwaal*

Use this page to download the latest ePub version of *The Blackout: Weak Signals* and browse archived releases.

---

### Downloads

- **[Download EPUB]({{ DOWNLOAD_URL }})**
- **[What changed?](https://github.com/fluxpiada/blackout/releases/latest)**
- **[Older Versions](https://github.com/fluxpiada/blackout/releases)**
- **[Join Discussion →](https://github.com/fluxpiada/blackout/discussions)**

---

### Metadata

| Field | Value |
|---|---|
| **Title** | *The Blackout: Weak Signals* |
| **Author** | F. J. S. Remmelzwaal |
| **Version** | loading… |
| **Published** | loading… |
<p><strong>Pages deploy:</strong> <span id="pages-run">loading…</span></p>

<script>
document.addEventListener('DOMContentLoaded', async () => {
  const repo = 'fluxpiada/blackout';     // your repo
  const workflow = 'pages.yml';           // .github/workflows/pages.yml
  const target = document.getElementById('pages-run');
  if (!target) return;

  try {
    const url = `https://api.github.com/repos/${repo}/actions/workflows/${encodeURIComponent(workflow)}/runs?per_page=5&branch=main&status=completed`;
    const res = await fetch(url);
    if (!res.ok) throw new Error('GitHub API error');
    const data = await res.json();

    // pick the most recent successful run on main
    const run = (data.workflow_runs || []).find(r => r.conclusion === 'success');
    if (!run) { target.textContent = 'no successful runs found'; return; }

    const dt = new Date(run.updated_at || run.run_started_at || run.created_at);
    target.textContent = dt.toISOString().replace('T',' ').replace(/\..+/, ' UTC');
    target.title = `Run #${run.run_number} • ${run.html_url}`;
  } catch (e) {
    console.warn(e);
    target.textContent = 'unavailable';
  }
});
</script>



© <span id="year"></span> F. J. S. Remmelzwaal. All rights reserved.

<script>
document.addEventListener('DOMContentLoaded', () => {
  const y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();
});
</script>
