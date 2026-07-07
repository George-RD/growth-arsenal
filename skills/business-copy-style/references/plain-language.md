# Plain Language Rules

Target: Flesch-Kincaid Grade Level ≤ 6.

## Sentence Rules

- Average sentence length ≤ 15 words.
- One idea per sentence.
- Active voice, not passive.
- Concrete nouns, not abstractions.

## Word Rules

- No jargon without a one-line plain-English translation.
- Use "you" and "we" when talking to the reader.
- Use verbs, not nominalizations.
- Cut filler: "in order to", "due to the fact that", "at this point in time".

## Flesch-Kincaid Grade Level Formula

Compute with any scratch cell:

```
Grade = 0.39 * (words / sentences) + 11.8 * (syllables / words) - 15.59
```

### Syllable Counting Heuristic

1. Count vowel groups in a word. A vowel group is one or more consecutive vowels (a, e, i, o, u, y).
2. Each word has at least one syllable.
3. Silent "e" at the end of a word does not add a syllable unless it changes the vowel sound.
4. Treat numbers as spoken (e.g., "5" = one syllable, "100" = two syllables).

### Example

> "We help busy owners get more leads without working nights."

- Words: 10
- Sentences: 1
- Syllables: We(1) help(1) bus-y(2) own-ers(2) get(1) more(1) leads(1) with-out(2) work-ing(2) nights(1) = 14
- Grade = 0.39 * 10 + 11.8 * 1.4 - 15.59 = 3.9 + 16.52 - 15.59 = 4.83

## Exceptions

- Proper nouns and brand names count toward words but do not need translation.
- Technical terms in a technical document may exceed grade 6 if the audience is specialists; still translate once.
