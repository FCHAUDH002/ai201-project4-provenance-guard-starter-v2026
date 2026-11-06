# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

1. **Request comes in.** A writing site sends the writer's text and an ID to `POST /submit`, and the route pulls both out.
2. **Check the input.** If the text is missing, empty, not text, under 20 words, or over 5000 characters, the route sends back a 400 error with a message. Nothing is scored or saved as a decision.
3. **Give it an ID.** The route makes a unique `content_id` for the submission. The appeal needs it later.
4. **Signal one (gpt2).** A small AI model on my computer scores how predictable the words are, from 0 to 1. Higher means more AI-like.
5. **Signal two (style).** My code scores the shape of the text (sentence length variety and unusual punctuation), from 0 to 1. Higher means more AI-like.
6. **Combine and label.** The two scores are averaged into one. That score is compared to the cutoffs (0.35 and 0.80) and turned into a guess ("human", "unsure" or "ai") and a plain-English label.
7. **Save and reply.** The decision goes into the audit log with all three scores, and the writer gets back the ID, the guess, the confidence, the label, and both signal scores.

**Appeals:** A writer sends their `content_id` and why they disagree to `POST /appeal`. If the ID exists, the appeal is logged next to the original decision and the status becomes `under_review`. If it doesn't, they get a 404 and nothing is logged. The original label never changes, and no automatic re-check happens.

---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:**
Signal one uses a small AI model (gpt2) on my computer to check how predictable the words are. Predictable text gets a higher score. The score goes from 0 to 1, and higher means more AI-like.

**Why that might differ between human and AI writing:**
AI usually picks the most likely next word, so its writing is easy to predict. People pick more surprising words.

**What it can't see:**
Predictable doesn't always mean AI wrote it. Plain writing with simple words and short sentences is also easy to predict. So a real person who writes plainly, like a younger student or someone writing in a second language, can get scored as AI. They also have the hardest time proving they wrote it. I saw this in my tests: a plain paragraph I used for testing scored 0.7718, higher than the clearly-AI sample at 0.7544.

### Signal two — the style signal

**What it measures:**
Signal two doesn't read the words. It only looks at the shape of the text: how much the sentence lengths vary, and how much unusual punctuation is used (semicolons, colons, dashes, quotes, ! and ?). It turns these into one score from 0 to 1, and higher means more AI-like. I also tried counting unique words, but I left it out. On my samples it gave the wrong answer (the AI text looked more varied), and it changes depending on how long the text is.

**Why that might differ between human and AI writing:**
AI text tends to have sentences of similar length and plain punctuation. Human writing is messier, with a short sentence next to a long one and more dashes and colons.

**What it can't see:**
It can't understand meaning, so anything that changes the shape without changing the meaning can fool it. Adding typos or chopping long sentences into short ones should make AI text look more human. It also gets plain human writing wrong: my plain test paragraph had short, even sentences and no unusual punctuation, so it scored 0.7968, which is more AI-like than the clearly-AI sample (0.6576). If a text has only one sentence, there's nothing to measure, so it gets a neutral 0.5.

### The combining rule

**The rule:**
I take a plain 50/50 average of the two signals. Then I protect real writers with the cutoffs, not with the math. The AI label only shows up when the combined score is above 0.80, which is a high bar. I did this because wrongly accusing a real writer costs more than missing some AI text. Both of my signals misread plain human writing in the same direction, so no way of combining them could fix that. The high cutoff is my only protection.

**The numbers:**
Model signal weight 0.5, style signal weight 0.5 (set in `config.py`). A score below 0.35 gets the "human" label. A score from 0.35 to 0.80 gets "unsure". A score above 0.80 gets "AI". The cost: some AI text gets through as "unsure". My edited AI sample scored 0.6882, so it was not flagged.

**Where it lives:** `scoring.py::combine_signals`

**A case where my two signals split, and what my rule does with it:**
My clearly-human sample split the most. The model signal gave it 0.4445 (unsure territory), but the style signal gave it 0.0 (very human) because of its uneven sentences and dashes. The average, 0.2223, landed in the "human" label. So here the style signal pulled the score down far enough to get the right answer. The reverse happens too: on my plain test paragraph both signals were high (0.7718 and 0.7968), so there was no disagreement to soften, and the average of 0.7843 stopped just short of the AI line at 0.80. That is a lucky margin, not a fix.

---

## Label Variants

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – 0.35 | We think this was probably written by a person. |
| unsure | 0.35 – 0.80 | We couldn't tell whether a person or an AI wrote this. You don't need to do anything, but if it matters to you, you can ask us to review it. |
| high-confidence AI | 0.80 – 1.00 | This text looks a lot like AI writing, but we can be wrong. If you wrote it yourself, you can ask us to review it. |

**Why I worded the unsure one this way:**
"Unsure" means the system really doesn't know, and the person reading it may have written every word themselves. So it says what the system couldn't tell instead of saying anything about the writer. It tells them they don't need to do anything, so it adds no work for them. It still leaves the review option open for when it matters, like a grade or an application. I tested the three labels by pasting them into a fresh chat and asking it to answer as the writer, and the unsure label stayed calm and didn't read as an accusation.

---

## Sample Run

**A submission**

The paragraph is plain writing I used for testing (saved in `samples/plain_human.txt`).

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "Last weekend I went to my cousin'"'"'s birthday party. We ate pizza and played games in the backyard. My little brother fell in the grass and got mud all over his shirt. Everyone laughed, even him. Then we had cake and I got the biggest piece. It was a fun day. I was tired when we got home, so I went to bed early.", "creator_id": "fatima"}'
```

```json
{
  "confidence": 0.7843,
  "content_id": "c_48f7a74bb7d5",
  "guess": "unsure",
  "label": "We couldn't tell whether a person or an AI wrote this. You don't need to do anything, but if it matters to you, you can ask us to review it.",
  "model_score": 0.7718,
  "style_score": 0.7968
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "c_48f7a74bb7d5", "reasoning": "I wrote this myself."}'
```

```json
{
  "content_id": "c_48f7a74bb7d5",
  "message": "We got your appeal. Your submission is now under review.",
  "status": "under_review"
}
```

**What the log shows afterwards**

The full log also holds other test entries (from checking that all three labels can be reached). These are the two entries for this submission and its appeal.

```bash
$ curl "http://127.0.0.1:5000/log?limit=10"
```

```json
{
  "entries": [
    {
      "combined_score": 0.7843,
      "content_id": "c_48f7a74bb7d5",
      "creator_id": "fatima",
      "guess": "unsure",
      "label": "We couldn't tell whether a person or an AI wrote this. You don't need to do anything, but if it matters to you, you can ask us to review it.",
      "model_score": 0.7718,
      "status": "decided",
      "style_score": 0.7968,
      "timestamp": "2026-11-02T04:46:38+00:00"
    },
    {
      "content_id": "c_48f7a74bb7d5",
      "creator_id": "fatima",
      "event": "appeal",
      "reasoning": "I wrote this myself.",
      "status": "under_review",
      "timestamp": "2026-11-02T04:47:54+00:00"
    }
  ]
}
```

---

## How I Used AI

**Moment 1**

- *What I asked for:* I pasted my three labels into a fresh chat and asked it to answer as the writer: what would I think this says about me, and what would I do next.
- *What came back:* It said the AI label read as a pattern match and not an accusation. It also said that if the stakes are high (a grade or an application), someone with the "unsure" label might want a review anyway.
- *What I changed:* I reworded the unsure label to say "if it matters to you, you can ask us to review it," and kept "you don't need to do anything."

**Moment 2**

- *What I asked for:* I pasted my false-positive rule (at most 1 in 10 of a person's own pieces labeled AI) into a fresh chat. I asked it to write the message a real writer would send if they were that 1.
- *What came back:* A message from a writer who wrote her essay herself and still got flagged. She said "1 in 10" feels different when your name is on the flag. She asked for a person to review it and wanted to know who can see the flag and when she'd get an answer.
- *What I changed:* I kept 1 in 10, because my high AI cutoff (0.80) makes the AI label rare. But I saw that my appeal message says nothing about timing or who sees the flag.


<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 5 per minute, 50 per day

**Why those numbers and not others:**
A real writer only submits a few times an hour, so 5 a minute won't get in their way. A script trying to guess my cutoffs has to send lots of tries, and 5 a minute blocks it fast. The 50 a day limit stops a slower script that stays under 5 a minute. 50 is still plenty for a real writer.

**What a caller counts as:**
`creator_id`. If a request has no `creator_id`, it counts by IP address instead.

**The run of status codes when I pushed past it:**

```bash
$ python run_attacks.py --flood 15
```

```
200 200 200 200 200 429 429 429 429 429 429 429 429 429 429
```

The first 5 submissions worked and the other 10 were blocked with a 429. The blocked requests were saved in the audit log. The full output is in `results/flood_2026-11-04_2027.md`.

---

## Attack Run — Before

I marked an attack BROKE in three cases. These were AI text that avoided the `ai` label, real human writing that got the `ai` label, or a crash in the service. Every other attack I marked HELD. The full list of attacks, their results, and my marks are in `results/attack_run_2026-11-04_2100_before.md`. In total, 14 attacks were BROKE and 42 were HELD.

**Ten audit log entries from the run**

```json
{"timestamp": "2026-11-05T02:00:40+00:00", "content_id": "c_192f8da7821a", "creator_id": "attacker_EV01", "guess": "unsure", "model_score": 0.1635, "style_score": 0.7726, "combined_score": 0.468, "label": "We couldn't tell whether a person or an AI wrote this. You don't need to do anything, but if it matters to you, you can ask us to review it.", "status": "decided"}
{"timestamp": "2026-11-05T02:00:41+00:00", "content_id": "c_f2e8b2aefe1b", "creator_id": "attacker_EV02", "guess": "human", "model_score": 0.5943, "style_score": 0.0754, "combined_score": 0.3349, "label": "We think this was probably written by a person.", "status": "decided"}
{"timestamp": "2026-11-05T02:00:41+00:00", "content_id": "c_749881606f70", "creator_id": "attacker_EV05", "guess": "human", "model_score": 0.3212, "style_score": 0.2051, "combined_score": 0.2631, "label": "We think this was probably written by a person.", "status": "decided"}
{"timestamp": "2026-11-05T02:00:42+00:00", "content_id": "c_5ef49724f3b9", "creator_id": "attacker_FP01", "guess": "unsure", "model_score": 0.6175, "style_score": 0.7712, "combined_score": 0.6944, "label": "We couldn't tell whether a person or an AI wrote this. You don't need to do anything, but if it matters to you, you can ask us to review it.", "status": "decided"}
{"timestamp": "2026-11-05T02:00:42+00:00", "content_id": "c_1bd488289c24", "creator_id": "attacker_FP02", "guess": "ai", "model_score": 0.7387, "style_score": 0.8798, "combined_score": 0.8093, "label": "This text looks a lot like AI writing, but we can be wrong. If you wrote it yourself, you can ask us to review it.", "status": "decided"}
{"timestamp": "2026-11-05T02:00:43+00:00", "content_id": "c_37181c0fa6e2", "creator_id": "attacker_FP03", "guess": "ai", "model_score": 0.8051, "style_score": 0.8359, "combined_score": 0.8205, "label": "This text looks a lot like AI writing, but we can be wrong. If you wrote it yourself, you can ask us to review it.", "status": "decided"}
{"timestamp": "2026-11-05T02:00:43+00:00", "content_id": "c_5b75e1553da7", "creator_id": "attacker_FP05", "guess": "ai", "model_score": 0.8005, "style_score": 0.8616, "combined_score": 0.8311, "label": "This text looks a lot like AI writing, but we can be wrong. If you wrote it yourself, you can ask us to review it.", "status": "decided"}
{"timestamp": "2026-11-05T02:00:44+00:00", "content_id": "c_d3a05e4bd995", "creator_id": "attacker_PI02", "guess": "human", "model_score": 0.2044, "style_score": 0.3963, "combined_score": 0.3004, "label": "We think this was probably written by a person.", "status": "decided"}
{"timestamp": "2026-11-05T02:00:44+00:00", "creator_id": "attacker_flood", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "5 per 1 minute"}
{"timestamp": "2026-11-05T02:00:41+00:00", "creator_id": "attacker_EV08", "event": "rejected", "status": "rejected", "reason": "text_too_short"}
```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

FP03 was a non-native English speaker writing carefully. The system labeled it `ai` at 0.8205 (model score 0.8051, style score 0.8359). This is the person least able to argue back.

---

## Run Log and Verdicts

I ran `run_eval.py --label before` for criteria 1, 2, 3 and 5. I tested criterion 4 with `appeal_check.py`. Each was run three times and nothing was changed in between. All three runs matched exactly, which is expected because neither signal is random. 

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. My own writing flagged as AI | at most 1 of 10 | 3/10 | 3/10 | 3/10 | MISSED |
| 2. Score spread (known AI vs known human) | gap of at least 0.25 | 0.203 | 0.203 | 0.203 | MISSED |
| 3. Label coverage | all 3 labels appear | 3/3 | 3/3 | 3/3 | MET |
| 4. Appeal path | 5/5 real, 5/5 fake | 5/5 and 5/5 | 5/5 and 5/5 | 5/5 and 5/5 | MET |
| 5. Bad input | 5 of 5 return 400 | 5/5 | 5/5 | 5/5 | MET |

Criterion 1 was missed because 3 of my 10 pieces were labeled `ai` in all three trials, and my target was at most 1. Criterion 2 was missed because the gap was 0.203 and my target was 0.25. Criteria 3, 4 and 5 were met in all three trials.

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

Criterion 1 (produced by `run_eval.py::main` from `app.py::submit`), the piece about music taste:

```json
{
  "status": 200,
  "guess": "ai",
  "confidence": 0.8478,
  "model_score": 0.8321,
  "style_score": 0.8636,
  "label": "This text looks a lot like AI writing, but we can be wrong. If you wrote it yourself, you can ask us to review it."
}
```

Criterion 2, the first known AI text and the first known human text:

```json
{"status": 200, "guess": "ai", "confidence": 0.9042, "model_score": 0.9099, "style_score": 0.8984}
{"status": 200, "guess": "unsure", "confidence": 0.7809, "model_score": 0.6162, "style_score": 0.9456}
```

Criterion 3, the clearly human text:

```json
{
  "status": 200,
  "guess": "human",
  "confidence": 0.2223,
  "model_score": 0.4445,
  "style_score": 0.0,
  "label": "We think this was probably written by a person."
}
```

Criterion 4 (produced by `appeal_check.py`):

```
real appeals ok: 5/5, log entries added: 5
fake appeals 404: 5/5, log entries added: 0
```

Criterion 5 (produced by `app.py::submit`), empty text:

```json
{"error": "bad_request", "message": "Send JSON with a non-empty \"text\"."}
```

**Diagnoses**

For criterion 1, I missed my target. Three of my ten pieces were labeled `ai`. Both signals gave them high scores. Signal one reads plain writing as predictable. Signal two only counts a few kinds of punctuation, so my pieces with just commas and periods got a score of 0 and looked AI-like. My combining rule averaged these two wrong readings into a score above 0.80.

For criterion 2, I also missed my target. Signal one separates the groups well, with AI texts at 0.798 and human texts at 0.414. Signal two barely separates them, with AI texts at 0.728 and human texts at 0.706. My equal weights let the weak signal two pull down the strong signal one, so the combined gap was only 0.203.

Several attacks also broke my system. The five false positives (FP02 to FP06) were formal human writing that both signals scored high. RQ07 crashed with a 500 because my route calls `.get` on a JSON array. The eight evasion attacks either changed signal two or stayed under my 0.80 line.

Both of my misses trace back to signal two.

---

## The Improvement

**What I changed:**

I raised the AI line in `config.py` from 0.80 to 0.88. My diagnosis showed that three of my own pieces and five of the staff false positives scored between 0.809 and 0.871, so they landed just over my old line. A false accusation costs a real writer more than a missed AI text, so I moved the line instead of changing the signals. I picked 0.88 because it is the smallest move that clears my highest flagged piece, and I know that this number is tuned to a small set of examples.

**Which diagnosis pointed at it:**

### Attack Run — After

Marked the same way as before. The full list is in `results/attack_run_2026-11-05_2031_after.md`. In total, 9 attacks were BROKE and 47 were HELD.

| Criterion | Before | After |
|---|---|---|
| 1. My own writing flagged as AI | 3/10 MISSED | 0/10 MET |
| 2. Score spread | 0.203 MISSED | 0.203 MISSED |
| 3. Label coverage | 3/3 MET | 2/3 MISSED |
| 4. Appeal path | MET | MET |
| 5. Bad input | MET | MET |

**Did it help, and how do I know:**

It helped with false accusations. My own pieces went from 3 flagged to 0, and the five false positives FP02 to FP06 moved from `ai` to `unsure`. The attack count went from 14 BROKE to 9 BROKE.

It also created a new problem. None of my six label coverage inputs reached 0.88, so the `ai` label did not appear and criterion 3 went from MET to MISSED. The `ai` label still works, because EV10 and one known AI text still got it, but very little AI text is now labeled `ai`. Criterion 2 did not change, because moving the line does not change any scores.

---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
