"""Advisory structural signals for copy review.

These counts organise evidence. They do not detect authorship, fail copy, or choose
between variants.
"""
from __future__ import annotations

import re
import statistics
from collections import Counter
from dataclasses import dataclass
from typing import Mapping, Sequence

WORD_RE = re.compile(r"[A-Za-z]+(?:[-'][A-Za-z]+)*|\d+(?:[.,]\d+)*")
STOPWORDS = frozenset(
    """
    a about after again against all am an and any are as at be because been before
    being below between both but by can could did do does doing down during each
    few for from further had has have having he her here hers herself him himself
    his how i if in into is it its itself just me more most my myself no nor not
    of off on once only or other our ours ourselves out over own same she should
    so some such than that the their theirs them themselves then there these they
    this those through to too under until up very was we were what when where
    which while who whom why will with would you your yours yourself yourselves
    """.split()
)
FIRST_PERSON_STARTERS = {
    "i", "i'm", "i've", "i'd", "i'll", "my", "mine",
    "we", "we're", "we've", "we'd", "we'll", "our", "ours",
}
CONTRAST_SCAFFOLDS: Mapping[str, re.Pattern[str]] = {
    "not just": re.compile(r"\bnot\s+just\b", re.I),
    "not only": re.compile(r"\bnot\s+only\b", re.I),
    "more than just": re.compile(r"\bmore\s+than\s+just\b", re.I),
    "i'm not": re.compile(r"\bi(?:'m|\s+am)\s+not\b", re.I),
    "this isn't": re.compile(r"\bthis\s+is(?:n't|\s+not)\b", re.I),
    "we don't just": re.compile(r"\bwe\s+do(?:n't|\s+not)\s+just\b", re.I),
}
META_PHRASES: Mapping[str, re.Pattern[str]] = {
    "what this means": re.compile(r"\bwhat\s+this\s+means\b", re.I),
    "the takeaway": re.compile(r"\bthe\s+takeaway\b", re.I),
    "in this section": re.compile(r"\bin\s+this\s+section\b", re.I),
    "on this page": re.compile(r"\bon\s+this\s+page\b", re.I),
    "as you can see": re.compile(r"\bas\s+you\s+can\s+see\b", re.I),
    "let's break": re.compile(r"\blet(?:'s|\s+us)\s+break\b", re.I),
    "here's what": re.compile(r"\bhere(?:'s|\s+is)\s+what\b", re.I),
    "below you'll": re.compile(r"\bbelow\s+you(?:'ll|\s+will)\b", re.I),
}


@dataclass(frozen=True)
class StructuralMetrics:
    duplicate_sentence_instances: int
    duplicate_sentence_examples: list[str]
    repeated_two_word_starter_instances: int
    repeated_two_word_starter_examples: list[str]
    sentence_length_stdev: float
    similar_sentence_length_run_count: int
    longest_similar_sentence_length_run: int
    repeated_four_word_phrase_instances: int
    repeated_four_word_phrases_per_1000_words: float
    repeated_four_word_phrase_examples: list[str]
    overloaded_paragraph_count: int
    longest_paragraph_words: int
    longest_paragraph_sentences: int
    first_person_sentence_start_count: int
    first_person_sentence_start_rate: float
    contrast_scaffold_count: int
    contrast_scaffold_examples: list[str]
    meta_phrase_count: int
    meta_phrase_examples: list[str]


COMPARISON_FIELDS = (
    "duplicate_sentence_instances",
    "repeated_two_word_starter_instances",
    "sentence_length_stdev",
    "similar_sentence_length_run_count",
    "longest_similar_sentence_length_run",
    "repeated_four_word_phrase_instances",
    "repeated_four_word_phrases_per_1000_words",
    "overloaded_paragraph_count",
    "longest_paragraph_words",
    "longest_paragraph_sentences",
    "first_person_sentence_start_count",
    "first_person_sentence_start_rate",
    "contrast_scaffold_count",
    "meta_phrase_count",
)


def words(text: str) -> list[str]:
    """Return lowercase lexical tokens with curly apostrophes normalised."""

    return [token.lower() for token in WORD_RE.findall(text.replace("’", "'"))]


def repeated_instances(counter: Counter[str]) -> int:
    return sum(count - 1 for count in counter.values() if count > 1)


def examples(counter: Counter[str], limit: int = 5) -> list[str]:
    repeated = ((value, count) for value, count in counter.items() if count > 1)
    return [
        f"{value} ({count}x)"
        for value, count in sorted(repeated, key=lambda item: (-item[1], item[0]))[:limit]
    ]


def similar_runs(lengths: Sequence[int], tolerance: int, minimum: int) -> tuple[int, int]:
    """Count non-overlapping runs whose min/max lengths stay within tolerance."""

    if not lengths:
        return 0, 0
    count = longest = 0
    run = [lengths[0]]
    for length in lengths[1:]:
        candidate = [*run, length]
        if max(candidate) - min(candidate) <= tolerance:
            run.append(length)
            continue
        if len(run) >= minimum:
            count += 1
            longest = max(longest, len(run))
        run = [length]
    if len(run) >= minimum:
        count += 1
        longest = max(longest, len(run))
    return count, longest


def phrase_counts(
    text: str, patterns: Mapping[str, re.Pattern[str]]
) -> tuple[int, list[str]]:
    counts = Counter(
        {name: len(pattern.findall(text.replace("’", "'"))) for name, pattern in patterns.items()}
    )
    return sum(counts.values()), [
        f"{name} ({count}x)"
        for name, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
        if count
    ]


def paragraphs(text: str) -> list[str]:
    return [
        re.sub(r"[ \t]*\n[ \t]*", " ", paragraph).strip()
        for paragraph in re.split(r"\n\s*\n+", text.strip())
        if paragraph.strip()
    ]


def analyse(
    text: str,
    sentence_texts: Sequence[str],
    *,
    word_count: int,
    sentence_counter,
    similar_length_tolerance: int = 2,
    similar_run_min: int = 3,
    max_paragraph_words: int = 120,
    max_paragraph_sentences: int = 6,
) -> StructuralMetrics:
    """Calculate advisory repetition, rhythm, load, voice and scaffold counts."""

    sentence_words = [tokens for sentence in sentence_texts if (tokens := words(sentence))]
    lengths = [len(sentence) for sentence in sentence_words]
    duplicates = Counter(" ".join(sentence) for sentence in sentence_words)
    starters = Counter(" ".join(sentence[:2]) for sentence in sentence_words if len(sentence) >= 2)
    run_count, longest_run = similar_runs(
        lengths, max(0, similar_length_tolerance), max(2, similar_run_min)
    )

    fourgrams: Counter[str] = Counter()
    for sentence in sentence_words:
        for index in range(max(0, len(sentence) - 3)):
            window = sentence[index : index + 4]
            if sum(token not in STOPWORDS for token in window) >= 2:
                fourgrams[" ".join(window)] += 1
    fourgram_instances = repeated_instances(fourgrams)

    loads = [(len(words(paragraph)), sentence_counter(paragraph)) for paragraph in paragraphs(text)]
    overloaded = sum(
        paragraph_words > max_paragraph_words
        or paragraph_sentences > max_paragraph_sentences
        for paragraph_words, paragraph_sentences in loads
    )
    first_person = sum(sentence[0] in FIRST_PERSON_STARTERS for sentence in sentence_words)
    contrast_count, contrast_examples = phrase_counts(text, CONTRAST_SCAFFOLDS)
    meta_count, meta_examples = phrase_counts(text, META_PHRASES)

    return StructuralMetrics(
        duplicate_sentence_instances=repeated_instances(duplicates),
        duplicate_sentence_examples=examples(duplicates),
        repeated_two_word_starter_instances=repeated_instances(starters),
        repeated_two_word_starter_examples=examples(starters),
        sentence_length_stdev=round(statistics.pstdev(lengths), 1) if len(lengths) > 1 else 0.0,
        similar_sentence_length_run_count=run_count,
        longest_similar_sentence_length_run=longest_run,
        repeated_four_word_phrase_instances=fourgram_instances,
        repeated_four_word_phrases_per_1000_words=round(
            fourgram_instances * 1000 / max(1, word_count), 1
        ),
        repeated_four_word_phrase_examples=examples(fourgrams),
        overloaded_paragraph_count=overloaded,
        longest_paragraph_words=max((load[0] for load in loads), default=0),
        longest_paragraph_sentences=max((load[1] for load in loads), default=0),
        first_person_sentence_start_count=first_person,
        first_person_sentence_start_rate=round(
            first_person * 100 / len(sentence_words), 1
        ) if sentence_words else 0.0,
        contrast_scaffold_count=contrast_count,
        contrast_scaffold_examples=contrast_examples,
        meta_phrase_count=meta_count,
        meta_phrase_examples=meta_examples,
    )
