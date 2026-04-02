# 🎧 Model Card — VibeFinder 1.0

---

## 1. Model Name

**VibeFinder 1.0**

A content-based music recommender simulation built for an intro AI course. It scores songs against a user's taste profile and returns the best matches from a small catalog.

---

## 2. Goal / Task

The goal is to predict which songs a user is most likely to enjoy based on their preferences. Given four inputs — a favorite genre, a favorite mood, a target energy level, and whether they prefer acoustic or electronic sounds — the system finds the songs in the catalog that best match those preferences and ranks them from best to worst fit.

It does not learn from user behavior over time. It makes a one-shot recommendation based purely on a profile you hand it.

---

## 3. Data Used

- **Catalog size:** 18 songs
- **Features per song:** genre, mood, energy (0.0–1.0), tempo (BPM), valence, danceability, acousticness
- **Genres covered:** pop, rock, lofi, jazz, reggae, metal, blues, r&b, hip-hop, country, classical, ambient, synthwave, indie pop, electronic
- **Moods covered:** happy, chill, intense, relaxed, moody, focused, melancholic, romantic, energetic, aggressive, nostalgic, dreamy

**Limits:** The catalog is very small. Some genres have 2–3 songs; others have only 1. The data was hand-picked for a classroom demo, so it does not reflect real listening diversity. Songs with genres not in the catalog (e.g., k-pop, folk) cannot be recommended, and there is no song with energy below 0.28, which causes problems for users who prefer very quiet or ambient music.

---

## 4. Algorithm Summary

Each song gets a score by comparing its attributes to what the user asked for. The scoring has four parts:

1. **Genre match (+2.0 points):** If the song's genre matches the user's favorite, it gets the biggest bonus. Genre is the strongest signal of overall taste, so it carries the most weight.

2. **Mood match (+1.0 point):** If the song's mood matches the user's preferred mood, it gets a smaller bonus. Mood matters, but genre is considered more defining.

3. **Energy closeness (0 to 2.0 points):** This one always applies. The closer the song's energy level is to what the user wants, the more points it gets. A perfect energy match gives the full 2.0; a song that is very far off gets close to 0. The formula rewards closeness rather than just "higher is better."

4. **Acousticness bonus (+0.5 points):** If the user likes acoustic music and the song is mostly acoustic, or the user prefers electronic and the song is mostly electronic, it gets a small bonus.

After scoring every song, the system sorts all 18 by score from highest to lowest and returns the top 5. The maximum possible score is **5.50 points**.

---

## 5. Observed Behavior / Biases

**What works well:** For common genres with multiple catalog entries (pop, lofi, rock), the results feel genuinely correct. The Chill Lofi profile hit a perfect 5.50 on its top result. High-energy profiles consistently surfaced the right songs.

**Genre dominance bias:** Because genre is worth +2.0 and mood is only +1.0, the system can recommend the wrong emotional vibe as long as the genre matches. Testing a "metal fan who wants chill music" returned an aggressive metal song first — because the genre bonus overrode the mood mismatch. The system does not penalize contradictions; it only rewards matches.

**Small catalog cliff:** For rare genres with only one song, position #1 is excellent and positions 2–5 are nearly meaningless. The reggae profile's #1 song scored 5.34; second place dropped to 2.46. The scoring had nothing left to distinguish the remaining songs.

**Energy extremes don't work:** The lowest-energy song in the catalog has energy=0.28. A user targeting energy=0.0 can only score 1.44 on energy proximity because no song goes low enough to earn more. The formula breaks down at the edges of the preference range.

**Unknown genres produce weak results:** A k-pop user got a max score of 3.48 because the genre component never fired. The top results were driven by energy and mood alone, making the output feel random.

---

## 6. Evaluation Process

Seven user profiles were tested: three normal cases and four adversarial edge cases.

- **High-Energy Pop, Chill Lofi, Deep Intense Rock** — all produced intuitive results. Top songs matched expectations.
- **Metal/Chill conflict** — revealed genre dominance (aggressive song ranked #1 for a chill-seeking user).
- **Rare Genre (reggae)** — revealed catalog cliff (only 1 matching song, rest was noise).
- **Extreme Low Energy (0.0)** — revealed the energy floor problem.
- **Unknown Genre (k-pop)** — revealed what happens when no catalog songs match at all.

One weight experiment was run: genre weight halved to +1.0, energy weight doubled to max +4.0. The top-ranked song stayed the same for all profiles, but the score gap between good and bad matches collapsed. Songs with no genre match jumped from ~2.5 to ~4.5, making weak results look strong. The original weights were kept because they produce more clearly separated, readable rankings.

---

## 7. Intended Use and Non-Intended Use

**Intended use:**
- A classroom simulation to demonstrate how content-based filtering works
- Learning exercise for understanding scoring functions, feature weights, and recommendation bias
- Quick demo with a small, hand-curated catalog

**Not intended for:**
- Real users making actual music decisions — the catalog is too small and not diverse enough
- Replacing a real music app like Spotify or YouTube Music
- Users with tastes outside the 15 genres in the catalog
- Any context where fairness or representation of diverse music cultures matters — the catalog heavily reflects Western and English-language genres

---

## 8. Ideas for Improvement

1. **Expand and balance the catalog.** Go from 18 to at least 100 songs, with 3–5 songs per genre so every genre has meaningful coverage beyond position #1.

2. **Replace exact string matching with similarity groups.** Right now, "intense" and "energetic" are treated as completely different moods even though they feel very similar. A lookup table that groups related moods and genres would produce smoother results.

3. **Add a diversity rule to the ranking step.** The current system can return 5 songs that are almost identical. A simple rule like "don't return more than 2 songs from the same genre in the top 5" would make the output more interesting and useful.

---

## 9. Personal Reflection

**Biggest learning moment:** The weight experiment was the most surprising part. I expected halving genre and doubling energy to change which songs appeared at the top — but the top result stayed the same for all seven profiles. What actually changed was the gap between the best and worst results. When energy dominated, mediocre matches scored almost as high as perfect ones, making the whole ranking feel meaningless. That taught me that weights are not just about picking a winner — they're about creating readable separation between "great fit" and "not really."

**How AI tools helped, and when I had to double-check:** AI was genuinely useful for generating diverse song data, drafting the Mermaid flowchart, and suggesting adversarial test profiles I wouldn't have thought of on my own (like the conflicting metal/chill case and the extreme 0.0 energy profile). Where I had to pay close attention was making sure the generated CSV data had realistic values — the AI's numbers looked plausible but I checked that energy, acousticness, and tempo were internally consistent for each song (e.g., a "classical/melancholic" song shouldn't have energy=0.95). The code suggestions were accurate, but the explanations sometimes glossed over why one choice was better than another, so I made sure I understood `sorted()` vs `.sort()` rather than just copying the answer.

**What surprised me about simple algorithms feeling like recommendations:** The biggest surprise was how much the output *feels* intelligent even though the logic is just four additions. When Library Rain scored a perfect 5.50, it genuinely felt like the system understood what the Chill Lofi user wanted. But the metal/chill test immediately showed the illusion — the same formula that felt smart in one case made a tone-deaf recommendation in another. The system doesn't actually understand music or emotion at all. It just finds numerical closeness. The feeling of "good recommendation" is really just what happens when your test case fits neatly inside what the data covers.

**What I would try next:** The most interesting next step would be adding a small collaborative element — even just tracking which songs users skip versus replay across multiple sessions and using that to adjust weights dynamically. Right now the weights are fixed forever. A system that lowered the genre weight when genre matches keep getting skipped would be much more adaptive. I'd also want to test whether mixing two user profiles (e.g., a "group listening" mode that averages preferences) produces results that satisfy both people or satisfies neither.
