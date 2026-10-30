# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---

## 1. False positives on my own writing

Of the 10 pieces I wrote myself, listed in `scenarios.py` under "my own writing", at most 1 comes back with `guess` equal to "ai", in every one of 3 trials. At least 3 of the 10 are plain writing, meaning their average sentence length is 15 words or fewer.

**Why this target:** Calling a real person's work AI hurts them a lot more than missing some AI text. Plain writing is the kind most likely to get wrongly flagged, so I test it on purpose. I allow 1 instead of 0 because the model's scores can change a little between runs. More than 1 would mean something is actually wrong.

---

## 2. Score spread

The average `confidence` of the 5 texts in `scenarios.py` under "known AI" is at least 0.25 higher than the average `confidence` of the 5 texts under "known human", in every one of 3 trials. "Known AI" texts are ones I generated with an AI tool. "Known human" texts are ones I or a classmate wrote without AI.

**Why this target:** If AI and human text get similar scores, the system can't tell them apart. A 0.25 gap shows the two groups are clearly separating. This checks the groups as a whole. Criteria 1 and 3 check single texts.

---

## 3. Label coverage

Out of the 6 inputs in `scenarios.py` under "label coverage", `guess` comes back as "human", "unsure", and "ai" at least once each, in every one of 3 trials.

**Why this target:** If a label can never show up, my score ranges have a gap. All three labels need to actually work.

---

## 4. The appeal path

5 out of 5 appeals on real content_ids return status "under_review" and add exactly one appeal entry to the log. 5 out of 5 appeals with a fake content_id return 404 and add nothing to the log.

**Why this target:** An appeal is the only way a wrongly accused writer can push back. If it fails without telling them, they think they were heard when they weren't. So it has to work every time.

---

## 5. Bad input

Each of 5 bad requests returns a 400 with a non-empty `message` field: text missing, text null, text empty, text under 20 words, and text over 5000 characters. 0 of them return a 500, and none create a log entry with status "decided".

**Why this target:** Bad input should never crash the service. A clear error tells the writer what to fix, and it keeps junk out of my log.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
