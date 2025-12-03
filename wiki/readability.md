# Readability stats version v1.11.28

| **Flesch** | **FK** | **Fog** | **Words** | **File**                      |
|------------|--------|---------|-----------|-------------------------------|
| 51.38      | 11.96  | 14.67   | 543       | 02_The_Copse.md               |
| 60.97      | 9.90   | 12.95   | 1242      | 11_Zoning_For_Success.md      |
| 61.24      | 9.73   | 12.35   | 1272      | 05_The_Party_Hangover.md      |
| 61.52      | 9.93   | 12.86   | 1226      | 08_Doras_Gear.md              |
| 61.52      | 9.27   | 12.11   | 1442      | 10_Phil.md                    |
| 62.54      | 8.17   | 11.59   | 877       | 03_The_Cove.md                |
| 63.55      | 8.97   | 12.24   | 1049      | 01_The_Mistakes.md            |
| 71.88      | 7.46   | 9.77    | 2007      | 09_The_Fjord.md               |
| 71.91      | 6.55   | 9.63    | 1738      | 04_The_Houtrakkers.md         |
| 74.25      | 6.15   | 9.62    | 509       | 07_Mr_Ate.md                  |
| 74.28      | 6.42   | 9.32    | 1944      | 06_The_Green_Suit.md          |

# 1. Your chapters fall into two clusters

## Cluster A — Harder, denser, more “literary”

Flesch 51–64
FK Grade ~9–12
Fog 11–15
These chapters lean heavier on:
longer sentences
more multisyllabic words
more complex phrasing or description
They read like adult contemporary/literary fiction with moments that edge toward academic density.

### Members:

02_The_Copse (hardest)
11_Zoning_for_Success
05_The_Party_Hangover
08_Doras_Gear
10_Phil
03_The_Cove
01_The_Mistakes
Interpretation:
These chapters demand more cognitive load. They likely have longer sentences, more internal reflection, more descriptive prose, or thematic/technical content.
Think: Richard Powers, early Margaret Atwood, Don DeLillo in terms of density.

## Cluster B — Breezier, more accessible, faster-moving

Flesch 71–75
FK Grade 6–7
Fog ~9–10
These chapters read much lighter:
shorter sentences
cleaner structure
fewer 3-syllable words
quicker pace

### Members:

06_The_Green_Suit
07_Mr_Ate
04_The_Houtrakkers
09_The_Fjord
Interpretation:
These are “easy onboarding” chapters — more dialogue, more action, or simpler scene construction.
Think: Le Carré at his more accessible moments, Naomi Alderman, Blake Crouch.
2. The overall picture of your manuscript
Your readability profile is coherent but varied:
No chapter plunges into academic territory (Flesch < 30).
No chapter drops into children’s literature territory (Flesch > 85).
The majority sits in the 60–75 Flesch band → classic mainstream fiction.
Your hardest chapter (The_Copse, Flesch 51) is still perfectly readable; it just demands attention.
Your easiest chapters are squarely in “airport novel” territory — which is good for pacing variety.
You are not wildly inconsistent. Your chapters are not schizophrenic in style. They just vary depending on content and intent.
## 3. What this means, narratively
You’ve got the classic pattern of a novel that oscillates between:
Atmospheric / interior / descriptive sections → harder readability
Dialogue-heavy / action / travel sections → easier readability
That's healthy.
Readers need the breathing rhythm.
If the “harder” chapters are placed early in the structure, they may slow the onboarding. If they’re mid-late, they deepen immersion.

# python go to
## More Python stuff for readability 
- pacing curves (readability vs story structure)
- sentence-length histograms
- complexity deltas between versions
- lexical diversity
- “which chapter most needs tightening” report

## instructions:
`pip install textstat pandas matplotlib seaborn numpy nltk`
For lexical diversity:
`python -m nltk.downloader punkt stopwords `


