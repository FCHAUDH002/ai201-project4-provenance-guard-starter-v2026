# Milestone 1 notes

## Path of a submission
1. Request comes in at /submit with text and creator_id.
2. Check the input. Bad input gets a 400 and nothing is scored or logged as a decision.
3. Make a content_id (the receipt number the appeal needs).
4. Signal one (gpt2) scores how predictable the text is, 0 to 1.
5. Signal two (style) scores sentence length, word variety, and punctuation, 0 to 1.
6. Combine into one score, then turn it into a guess and a label.
7. Save to the audit log and reply.

## Blind spots
- Signal one measures how predictable the words are, so it can't tell AI text apart from a real person who writes plainly, like a younger student or someone writing in a second language.
- Signal two measures sentence length, word variety, and punctuation, so it can't tell a person's natural writing from AI text roughed up with typos or chopped-up sentences.

## False positive trace
A real student submits a plain paragraph they wrote. Both signals score it as predictable, the combined score lands above the AI line, and the label says AI. They read it as an accusation. All they can do is appeal, so the appeal has to always get recorded.

## Labels (draft)
- Human: "We think this was probably written by a person."
- Unsure: "We couldn't tell whether a person or an AI wrote this. You don't need to do anything, but if it matters to you, you can ask us to review it."
- AI: "This text looks a lot like AI writing, but we can be wrong. If you wrote it yourself, you can ask us to review it."

## /submit
In: text (string), creator_id (string)
Out: content_id, guess ("ai"/"human"/"unsure"), confidence (combined score 0-1), label, model_score, style_score
Errors (400): text missing, null, not a string, empty, too short, or over 5000 characters. The message tells them why.

## /appeal
In: content_id (string), reasoning (string)
Out: content_id, status "under_review", message "We got your appeal. Your submission is now under review."
Error (404): unknown content_id. "We couldn't find that submission. Please check the ID and try again." Nothing gets logged.
The label stays the same. A person looks at it later.
