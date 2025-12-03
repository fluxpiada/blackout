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

    let md = "";   // no heading
    for (const r of releases) {
      const date = r.published_at?.substring(0, 10) ?? "unknown";
      md += `<div style="text-align:center;"><em>${r.name} — ${date}</em></div>\n\n`;
     
    }
 // today's date in YYYY-MM-DD
      const today = new Date().toISOString().substring(0, 10);
      md += `<div style="text-align:center;"><em>Current edition — ${today}</em></div>\n`;


    
    fs.writeFileSync("manuscript/001_releases.md", md);
  });
});
