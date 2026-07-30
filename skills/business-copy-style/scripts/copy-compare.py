#!/usr/bin/env python3
"""Compare copy signals without choosing a qualitative winner."""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from dataclasses import asdict, dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
from copy_structure import (  # noqa: E402
    COMPARISON_FIELDS as STRUCTURAL_COMPARISON_FIELDS,
    StructuralMetrics,
    analyse as analyse_structure,
)

TIER_1 = {
    "delve", "landscape", "tapestry", "paradigm", "leverage", "harness",
    "navigate", "realm", "embark", "journey", "myriad", "plethora",
    "multifaceted", "revolutionize", "synergy", "ecosystem", "resonate",
    "streamline",
}
TIER_2 = {
    "robust", "seamless", "cutting-edge", "innovative", "comprehensive",
    "pivotal", "nuanced", "compelling", "transformative", "bolster",
    "underscore", "foster", "imperative", "intricate", "overarching",
    "unprecedented", "groundbreaking", "elevate", "empower", "unlock",
    "spearhead",
}
WORD_RE = re.compile(r"[A-Za-z]+(?:[-'][A-Za-z]+)*|\d+(?:[.,]\d+)*")
BLOCK_TAGS = {
    "address", "article", "aside", "blockquote", "br", "dd", "div", "dl",
    "dt", "fieldset", "figcaption", "figure", "footer", "form", "h1", "h2",
    "h3", "h4", "h5", "h6", "header", "hr", "li", "main", "nav", "ol",
    "p", "pre", "section", "summary", "table", "tbody", "td", "tfoot", "th",
    "thead", "tr", "ul",
}
IGNORED_TAGS = {"script", "style", "svg", "noscript"}
NONTERMINAL_DOT = "\u2024"
ABBREVIATION_RE = re.compile(
    r"\b(?:e\.g|i\.e|mr|mrs|ms|dr|prof|sr|jr|vs|etc|no|fig|st)\.", re.I
)
INITIALISM_RE = re.compile(r"\b(?:[A-Za-z]\.){2,}")
URL_OR_EMAIL_RE = re.compile(
    r"https?://\S+|www\.\S+|\b[\w.+-]+@[\w.-]+\.\w+\b", re.I
)
TERMINAL_RE = re.compile(r"[.!?]+(?:[\"'”’\)\]]*)?(?=\s|$)")


class VisibleTextParser(HTMLParser):
    """Extract visible HTML text while preserving block boundaries."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._ignored_depth = 0
        self.parts: list[str] = []

    def _boundary(self) -> None:
        if self.parts and not self.parts[-1].endswith("\n"):
            self.parts.append("\n")

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag in IGNORED_TAGS:
            self._ignored_depth += 1
        elif not self._ignored_depth and tag in BLOCK_TAGS:
            self._boundary()

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if not self._ignored_depth and tag.lower() in BLOCK_TAGS:
            self._boundary()

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in IGNORED_TAGS and self._ignored_depth:
            self._ignored_depth -= 1
        elif not self._ignored_depth and tag in BLOCK_TAGS:
            self._boundary()

    def handle_data(self, data: str) -> None:
        if not self._ignored_depth:
            self.parts.append(data)

    def text(self) -> str:
        return "\n".join(
            line for raw in "".join(self.parts).splitlines()
            if (line := re.sub(r"[ \t]+", " ", raw).strip())
        )


@dataclass(frozen=True)
class Metrics(StructuralMetrics):
    words: int
    sentences: int
    average_words_per_sentence: float
    flesch_kincaid_grade: float
    em_dashes: int
    en_dashes: int
    double_hyphens: int
    tier_1_count: int
    tier_1_terms: list[str]
    tier_2_count: int
    tier_2_terms: list[str]
    hard_gate_pass: bool
    hard_gate_failures: list[str]


def visible_text(raw: str, suffix: str = "") -> str:
    if suffix.lower() in {".html", ".htm"} or re.search(
        r"<\s*(?:html|body|main|section|article|div|p|h[1-6])\b", raw, re.I
    ):
        parser = VisibleTextParser()
        parser.feed(raw)
        parser.close()
        return parser.text()
    return html.unescape(raw)


def read_copy(path: str | Path) -> str:
    source = Path(path)
    try:
        return visible_text(source.read_text(encoding="utf-8"), source.suffix)
    except FileNotFoundError as exc:
        raise ValueError(f"No such file: {source}") from exc


def syllables(word: str) -> int:
    cleaned = re.sub(r"[^a-z]", "", word.lower())
    if not cleaned:
        return 1
    count = len(re.findall(r"[aeiouy]+", cleaned))
    if cleaned.endswith("e") and not cleaned.endswith("le") and count > 1:
        count -= 1
    return max(1, count)


def base_forms(word: str) -> Iterable[str]:
    word = word.lower()
    yield word
    if word.endswith("ies") and len(word) > 3:
        yield word[:-3] + "y"
    for suffix in ("ing", "ed", "es", "s", "d"):
        if word.endswith(suffix) and len(word) > len(suffix) + 2:
            stem = word[: -len(suffix)]
            yield stem
            if suffix in {"ing", "ed"}:
                yield stem + "e"


def matched_terms(words: list[str], vocabulary: set[str]) -> list[str]:
    matched: list[str] = []
    for word in words:
        for form in base_forms(word):
            if form in vocabulary:
                matched.append(form)
                break
    return matched


def protect_nonterminal_dots(text: str) -> str:
    def protect(match: re.Match[str]) -> str:
        token, trailing = match.group(0), ""
        while token and token[-1] in ".!?":
            trailing = token[-1] + trailing
            token = token[:-1]
        return token.replace(".", NONTERMINAL_DOT) + trailing

    text = URL_OR_EMAIL_RE.sub(protect, text)
    text = re.sub(r"(?<=\d)\.(?=\d)", NONTERMINAL_DOT, text)
    text = ABBREVIATION_RE.sub(lambda match: match.group(0).replace(".", NONTERMINAL_DOT), text)
    return INITIALISM_RE.sub(
        lambda match: match.group(0).replace(".", NONTERMINAL_DOT), text
    )


def split_sentences(text: str) -> list[str]:
    protected = protect_nonterminal_dots(text)
    matches = list(TERMINAL_RE.finditer(protected))
    if not matches:
        return [protected.strip().replace(NONTERMINAL_DOT, ".")] if protected.strip() else []
    sentences, start = [], 0
    for match in matches:
        if sentence := protected[start : match.end()].strip():
            sentences.append(sentence.replace(NONTERMINAL_DOT, "."))
        start = match.end()
    return sentences


def sentence_count(text: str) -> int:
    return max(1, len(split_sentences(text)))


def analyse(
    text: str,
    *,
    max_grade: float = 6,
    max_emdash: int = 0,
    max_sentence: float = 15,
    similar_length_tolerance: int = 2,
    similar_run_min: int = 3,
    max_paragraph_words: int = 120,
    max_paragraph_sentences: int = 6,
) -> Metrics:
    normalized = re.sub(r"\s+", " ", text).strip()
    words_raw = WORD_RE.findall(normalized)
    words = [word.lower() for word in words_raw]
    sentence_texts = split_sentences(normalized)
    sentences = max(1, len(sentence_texts))
    word_count = max(1, len(words))
    average = word_count / sentences
    grade = max(
        0.0,
        0.39 * average
        + 11.8 * ((sum(syllables(word) for word in words_raw) or 1) / word_count)
        - 15.59,
    )
    tier_1, tier_2 = matched_terms(words, TIER_1), matched_terms(words, TIER_2)
    structure = analyse_structure(
        text,
        sentence_texts,
        word_count=word_count,
        sentence_counter=sentence_count,
        similar_length_tolerance=similar_length_tolerance,
        similar_run_min=similar_run_min,
        max_paragraph_words=max_paragraph_words,
        max_paragraph_sentences=max_paragraph_sentences,
    )
    em_dashes = normalized.count("—")
    failures: list[str] = []
    if grade > max_grade + 0.05:
        failures.append(f"grade {grade:.1f} > {max_grade:g}")
    if em_dashes > max_emdash:
        failures.append(f"em dashes {em_dashes} > {max_emdash}")
    if tier_1:
        failures.append(f"Tier-1 vocabulary {len(tier_1)} > 0")
    if average > max_sentence + 0.05:
        failures.append(f"average sentence {average:.1f} > {max_sentence:g} words")

    return Metrics(
        **asdict(structure),
        words=len(words),
        sentences=sentences,
        average_words_per_sentence=round(average, 1),
        flesch_kincaid_grade=round(grade, 1),
        em_dashes=em_dashes,
        en_dashes=normalized.count("–"),
        double_hyphens=len(re.findall(r"\s--\s", normalized)),
        tier_1_count=len(tier_1),
        tier_1_terms=sorted(set(tier_1)),
        tier_2_count=len(tier_2),
        tier_2_terms=sorted(set(tier_2)),
        hard_gate_pass=not failures,
        hard_gate_failures=failures,
    )


COMPARISON_FIELDS = (
    "words", "sentences", "average_words_per_sentence", "flesch_kincaid_grade",
    "em_dashes", "tier_1_count", "tier_2_count", *STRUCTURAL_COMPARISON_FIELDS,
)


def comparison(baseline: Metrics, candidate: Metrics) -> dict[str, float | int]:
    deltas: dict[str, float | int] = {}
    for field in COMPARISON_FIELDS:
        delta = getattr(candidate, field) - getattr(baseline, field)
        deltas[field] = round(delta, 1) if isinstance(delta, float) else delta
    return deltas


def result(
    baseline_text: str,
    candidate_text: str,
    *,
    baseline_label: str,
    candidate_label: str,
    max_grade: float,
    max_emdash: int,
    max_sentence: float,
    similar_length_tolerance: int = 2,
    similar_run_min: int = 3,
    max_paragraph_words: int = 120,
    max_paragraph_sentences: int = 6,
) -> dict[str, object]:
    settings = {
        "max_grade": max_grade,
        "max_emdash": max_emdash,
        "max_sentence": max_sentence,
        "similar_length_tolerance": similar_length_tolerance,
        "similar_run_min": similar_run_min,
        "max_paragraph_words": max_paragraph_words,
        "max_paragraph_sentences": max_paragraph_sentences,
    }
    baseline, candidate = analyse(baseline_text, **settings), analyse(candidate_text, **settings)
    return {
        "baseline": {"label": baseline_label, **asdict(baseline)},
        "candidate": {"label": candidate_label, **asdict(candidate)},
        "candidate_minus_baseline": comparison(baseline, candidate),
        "thresholds": {
            "hard_gates": {
                "max_grade": max_grade,
                "max_emdash": max_emdash,
                "max_sentence": max_sentence,
                "tier_1_count": 0,
            },
            "structural_advisories": {
                "similar_length_tolerance": similar_length_tolerance,
                "similar_run_min": similar_run_min,
                "max_paragraph_words": max_paragraph_words,
                "max_paragraph_sentences": max_paragraph_sentences,
            },
        },
        "winner": None,
        "decision_required": (
            "Deterministic signals do not choose the winner. Run the blind paired "
            "qualitative rubric; keep the baseline, candidate, or a re-evaluated "
            "hybrid based on audience fit and product truth."
        ),
    }


def text_report(payload: dict[str, object]) -> str:
    rows: list[str] = []
    for key in ("baseline", "candidate"):
        item = payload[key]
        assert isinstance(item, dict)
        rows.append(
            f"{item['label']}: grade {item['flesch_kincaid_grade']} | "
            f"avg sentence {item['average_words_per_sentence']} | "
            f"em dashes {item['em_dashes']} | Tier-1 {item['tier_1_count']} | "
            f"hard gate {'PASS' if item['hard_gate_pass'] else 'FAIL'}"
        )
        rows.extend(f"  - {failure}" for failure in item["hard_gate_failures"])
        rows.extend([
            "  Advisory (structural; never gates):",
            "    repetition: "
            f"duplicate sentences {item['duplicate_sentence_instances']} | "
            f"repeated starters {item['repeated_two_word_starter_instances']} | "
            f"repeated 4-word phrases {item['repeated_four_word_phrase_instances']} "
            f"({item['repeated_four_word_phrases_per_1000_words']}/1k words)",
            "    rhythm/load: "
            f"sentence stdev {item['sentence_length_stdev']} | "
            f"similar-length runs {item['similar_sentence_length_run_count']} | "
            f"overloaded paragraphs {item['overloaded_paragraph_count']}",
            "    voice/scaffolds: "
            f"first-person starts {item['first_person_sentence_start_rate']}% | "
            f"contrast {item['contrast_scaffold_count']} | meta phrases {item['meta_phrase_count']}",
        ])
    rows.extend([
        "", "Candidate minus baseline:",
        json.dumps(payload["candidate_minus_baseline"], ensure_ascii=False, sort_keys=True),
        "", str(payload["decision_required"]),
    ])
    return "\n".join(rows)


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(
        description="Compare deterministic copy signals without choosing a winner"
    )
    command.add_argument("--baseline", required=True)
    command.add_argument("--candidate", required=True)
    command.add_argument("--baseline-label", default="Baseline")
    command.add_argument("--candidate-label", default="Candidate")
    command.add_argument("--max-grade", type=float, default=6)
    command.add_argument("--max-emdash", type=int, default=0)
    command.add_argument("--max-sentence", type=float, default=15)
    command.add_argument("--similar-length-tolerance", type=int, default=2)
    command.add_argument("--similar-run-min", type=int, default=3)
    command.add_argument("--max-paragraph-words", type=int, default=120)
    command.add_argument("--max-paragraph-sentences", type=int, default=6)
    command.add_argument("--format", choices=["text", "json"], default="text")
    return command


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        payload = result(
            read_copy(args.baseline),
            read_copy(args.candidate),
            baseline_label=args.baseline_label,
            candidate_label=args.candidate_label,
            max_grade=args.max_grade,
            max_emdash=args.max_emdash,
            max_sentence=args.max_sentence,
            similar_length_tolerance=args.similar_length_tolerance,
            similar_run_min=args.similar_run_min,
            max_paragraph_words=args.max_paragraph_words,
            max_paragraph_sentences=args.max_paragraph_sentences,
        )
    except ValueError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}), file=sys.stderr)
        return 2
    print(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)
        if args.format == "json" else text_report(payload)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
