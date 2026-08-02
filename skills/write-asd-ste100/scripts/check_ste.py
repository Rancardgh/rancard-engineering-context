#!/usr/bin/env python3
"""Check deterministic ASD-STE100 structure rules in text documents.

This checker does not validate the ASD-STE100 controlled dictionary.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


TEXT_SUFFIXES = {".md", ".markdown", ".rst", ".txt"}
SENTENCE_BOUNDARY = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9<`])")
WORD = re.compile(r"[A-Za-z0-9]+(?:[-/'_.][A-Za-z0-9]+)*")
INLINE_CODE = re.compile(r"`[^`]+`")
MARKDOWN_IMAGE = re.compile(r"!\[[^]]*]\([^)]+\)")
MARKDOWN_LINK = re.compile(r"\[([^]]+)]\([^)]+\)")
PARENTHETICAL = re.compile(r"\([^()]*\)")
QUOTED = re.compile(r'"[^"\n]+"|“[^”\n]+”')
NUMBER_UNIT = re.compile(
    r"\b\d+(?:[.,]\d+)?\s*(?:%|°[CF]?|ms|s|min|h|B|KB|MB|GB|TB|Hz|kHz|MHz|GHz|V|A|W|mm|cm|m|km|g|kg|psi)\b",
    re.IGNORECASE,
)
CONTRACTION = re.compile(
    r"\b(?:aren't|can't|couldn't|didn't|doesn't|don't|hadn't|hasn't|haven't|he's|I'd|I'll|I'm|isn't|it's|let's|mustn't|shan't|she's|shouldn't|that's|there's|they'd|they'll|they're|they've|wasn't|we'd|we'll|we're|we've|weren't|what's|where's|who's|won't|wouldn't|you'd|you'll|you're|you've)\b",
    re.IGNORECASE,
)
LATIN_ABBREVIATION = re.compile(r"\b(?:e\.g\.|i\.e\.|etc\.)", re.IGNORECASE)
FRONTMATTER = re.compile(r"\A---\s*\n(?P<body>.*?)\n---(?:\n|\Z)", re.DOTALL)
STE_MODE = re.compile(
    r"^ste_mode:\s*['\"]?(descriptive|procedural)['\"]?\s*$",
    re.IGNORECASE | re.MULTILINE,
)


@dataclass(frozen=True)
class Paragraph:
    line: int
    text: str


@dataclass(frozen=True)
class Finding:
    path: Path
    line: int
    code: str
    message: str

    def format(self) -> str:
        return f"{self.path}:{self.line}: {self.code} {self.message}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check deterministic ASD-STE100 structure rules."
    )
    parser.add_argument("paths", nargs="*", type=Path)
    parser.add_argument(
        "--changed-from",
        metavar="GIT_REF",
        help="Check supported files changed from this Git reference.",
    )
    parser.add_argument(
        "--mode",
        choices=("auto", "descriptive", "procedural"),
        default="auto",
        help="Use frontmatter mode, a 25-word limit, or a 20-word limit.",
    )
    return parser.parse_args()


def changed_paths(git_ref: str) -> list[Path]:
    result = subprocess.run(
        [
            "git",
            "diff",
            "--name-only",
            "--diff-filter=ACMR",
            "-z",
            git_ref,
            "--",
            "*.md",
            "*.markdown",
            "*.rst",
            "*.txt",
        ],
        check=True,
        stdout=subprocess.PIPE,
    )
    return [Path(value.decode()) for value in result.stdout.split(b"\0") if value]


def supported_paths(paths: list[Path]) -> list[Path]:
    result: list[Path] = []
    for path in paths:
        if path.is_dir():
            result.extend(
                candidate
                for candidate in path.rglob("*")
                if candidate.is_file() and candidate.suffix.lower() in TEXT_SUFFIXES
            )
        elif path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
            result.append(path)
    return sorted(set(result))


def prose_paragraphs(text: str) -> list[Paragraph]:
    paragraphs: list[Paragraph] = []
    current: list[str] = []
    start_line = 1
    in_fence = False
    in_frontmatter = False
    in_comment = False

    def flush() -> None:
        nonlocal current
        if current:
            paragraphs.append(Paragraph(start_line, " ".join(current)))
            current = []

    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        stripped = raw_line.strip()

        if line_number == 1 and stripped == "---":
            in_frontmatter = True
            continue
        if in_frontmatter:
            if stripped == "---":
                in_frontmatter = False
            continue

        if stripped.startswith("<!--"):
            flush()
            in_comment = "-->" not in stripped
            continue
        if in_comment:
            if "-->" in stripped:
                in_comment = False
            continue

        if stripped.startswith(("```", "~~~")):
            flush()
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        if not stripped:
            flush()
            continue
        if stripped.startswith(("#", ">", "|")):
            flush()
            continue
        if re.fullmatch(r"[-=]{3,}", stripped):
            flush()
            continue

        is_list_item = bool(re.match(r"^(?:[-+*]|\d+[.)])\s+", stripped))
        if is_list_item:
            flush()

        line = re.sub(r"^(?:[-+*]|\d+[.)])\s+", "", stripped)
        line = MARKDOWN_IMAGE.sub("", line)
        line = MARKDOWN_LINK.sub(r"\1", line)
        line = INLINE_CODE.sub("IDENTIFIER", line)

        if is_list_item:
            paragraphs.append(Paragraph(line_number, line))
            continue

        if not current:
            start_line = line_number
        current.append(line)

    flush()
    return paragraphs


def sentences(text: str) -> list[str]:
    parts = [part.strip() for part in SENTENCE_BOUNDARY.split(text) if part.strip()]
    return parts or [text]


def word_count(text: str) -> int:
    value = PARENTHETICAL.sub(" PARENTHETICAL ", text)
    value = QUOTED.sub(" QUOTED ", value)
    value = NUMBER_UNIT.sub(" MEASUREMENT ", value)
    return len(WORD.findall(value))


def document_mode(text: str, requested_mode: str) -> str:
    if requested_mode != "auto":
        return requested_mode

    frontmatter = FRONTMATTER.match(text)
    if frontmatter:
        match = STE_MODE.search(frontmatter.group("body"))
        if match:
            return match.group(1).lower()
    return "descriptive"


def inspect(path: Path, mode: str) -> list[Finding]:
    findings: list[Finding] = []
    text = path.read_text(encoding="utf-8")
    selected_mode = document_mode(text, mode)
    limit = 20 if selected_mode == "procedural" else 25

    for paragraph in prose_paragraphs(text):
        paragraph_sentences = sentences(paragraph.text)
        if len(paragraph_sentences) > 6:
            findings.append(
                Finding(
                    path,
                    paragraph.line,
                    "STE006",
                    f"paragraph has {len(paragraph_sentences)} sentences; maximum is 6",
                )
            )

        for sentence in paragraph_sentences:
            count = word_count(sentence)
            sentence_for_rules = QUOTED.sub("QUOTED", sentence)
            if count > limit:
                findings.append(
                    Finding(
                        path,
                        paragraph.line,
                        "STE001",
                        f"sentence has {count} words; maximum for {selected_mode} text is {limit}",
                    )
                )
            if ";" in sentence_for_rules:
                findings.append(
                    Finding(path, paragraph.line, "STE002", "do not use a semicolon")
                )
            match = CONTRACTION.search(sentence_for_rules)
            if match:
                findings.append(
                    Finding(
                        path,
                        paragraph.line,
                        "STE003",
                        f"replace the contraction {match.group(0)!r}",
                    )
                )
            match = LATIN_ABBREVIATION.search(sentence_for_rules)
            if match:
                findings.append(
                    Finding(
                        path,
                        paragraph.line,
                        "STE004",
                        f"replace the Latin abbreviation {match.group(0)!r}",
                    )
                )

    return findings


def main() -> int:
    args = parse_args()
    requested = list(args.paths)
    if args.changed_from:
        requested.extend(changed_paths(args.changed_from))
    if not requested and not args.changed_from:
        print("No paths were specified.", file=sys.stderr)
        return 2

    paths = supported_paths(requested)
    findings = [finding for path in paths for finding in inspect(path, args.mode)]

    for finding in findings:
        print(finding.format())

    print(
        f"Checked {len(paths)} file(s). "
        "This check does not validate the ASD-STE100 controlled dictionary."
    )
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
