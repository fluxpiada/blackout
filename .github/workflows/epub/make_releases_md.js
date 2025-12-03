#!/usr/bin/env node
const fs = require("fs");
const https = require("https");

const owner = "fluxpiada";
const repo = "blackout";

https.get(`https://api.github.com/repos/${owner}/${repo}/releases`, {
  headers: { "User-Agent": "node" }
}, res => {
  let data = "";
  res.on("data", chunk => data += chunk);
  res.on("end", () => {
    const releases = JSON.parse(data);

    let md = "# Release History\n\n";
    for (const r of releases) {
      const date = r.published_at?.substring(0, 10) ?? "unknown";
      md += `- **${r.tag_name}** — ${date}\n`;
    }

    // place file inside manuscript folder
    fs.writeFileSync("manuscript/releases.md", md);
  });
});
