#!/usr/bin/env python3
"""hodie_zero_point.py — Find the zero-point lexeme of a document and search Perplexity.

The zero-point lexeme is the single term that anchors a document's meaning —
remove it and the document loses coherence. This script:
  1. Reads a document
  2. Scores terms by frequency × position weight × uniqueness
  3. Returns the top candidate (zero-point lexeme)
  4. Queries Perplexity for external enrichment
  5. Logs results to the HODIE session log

Usage:
  python3 .scripts/hodie_zero_point.py <document_path>
  python3 .scripts/hodie_zero_point.py <document_path> --no-perplexity
  python3 .scripts/hodie_zero_point.py <document_path> --top 3
"""

import argparse
import json
import math
import os
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    requests = None  # type: ignore[assignment]

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

HODIE_ROOT = Path(__file__).parent.parent
LOG_FILE = HODIE_ROOT / "_TODAY" / "daily" / "session.log"

STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "this", "that", "these", "those", "it", "its",
    "as", "if", "so", "we", "our", "you", "your", "i", "my", "me", "he",
    "she", "they", "them", "not", "no", "all", "any", "each", "more", "also",
    "can", "when", "where", "which", "who", "what", "how", "than", "then",
    "into", "through", "about", "between", "after", "before", "up", "down",
}

# ---------------------------------------------------------------------------
# Zero-point extraction
# ---------------------------------------------------------------------------

def extract_terms(text: str) -> list[str]:
    """Extract meaningful tokens from text."""
    # Lowercase, split on non-alphanumeric (keep hyphens within words)
    tokens = re.findall(r'\b[a-z][a-z0-9_-]{2,}\b', text.lower())
    return [t for t in tokens if t not in STOPWORDS and not t.isdigit()]


def _score_term(term: str, tf: float, total: int, count: int,
                header_terms: set, early_terms: set) -> float:
    """Compute weighted TF-IDF score for a single term."""
    score = tf * math.log(total / count + 1)
    if term in header_terms:
        score *= 3.0
    if term in early_terms:
        score *= 1.5
    return score


def score_terms(text: str, top_n: int = 5) -> list[tuple[str, float]]:
    """Score terms by frequency × title_boost × early_position_weight.

    Title/header terms score 3x — they're declared anchors.
    Terms in first 20% of document score 1.5x — authors front-load key concepts.
    Rare-but-present terms score higher than ubiquitous ones via TF-IDF-style dampening.
    """
    lines = text.split('\n')
    total_chars = len(text)

    header_terms: set[str] = set()
    for line in lines:
        if re.match(r'^#{1,3}\s+', line):
            header_terms.update(extract_terms(line))

    split_point = max(1, total_chars // 5)
    early_terms = set(extract_terms(text[:split_point]))

    freq = Counter(extract_terms(text))
    total = sum(freq.values()) or 1

    scores = {
        term: _score_term(term, count / total, total, count, header_terms, early_terms)
        for term, count in freq.items()
    }
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_n]


def find_zero_point(file_path: Path, top_n: int = 1) -> list[tuple[str, float]]:
    """Find the zero-point lexeme(s) of a document."""
    text = file_path.read_text(encoding='utf-8', errors='ignore')
    return score_terms(text, top_n=top_n)


# ---------------------------------------------------------------------------
# Perplexity search
# ---------------------------------------------------------------------------

def query_perplexity(lexeme: str, context: str = "") -> dict:
    """Query Perplexity API for the zero-point lexeme."""
    if requests is None:
        return {"error": "requests not installed — run: pip install requests"}

    api_key = os.environ.get("PERPLEXITY_API_KEY")
    if not api_key:
        return {"error": "PERPLEXITY_API_KEY not set in environment"}

    prompt = (
        f"Explain the concept '{lexeme}' in the context of: {context}" if context
        else f"Explain '{lexeme}': its origin, applications, and conceptual significance."
    )
    payload = {
        "model": "sonar",
        "messages": [
            {"role": "system", "content": "Be concise. Focus on conceptual significance and connections."},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": 400,
    }

    try:
        resp = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json=payload,
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        return {
            "lexeme": lexeme,
            "response": data["choices"][0]["message"]["content"],
            "citations": data.get("citations", []),
        }
    except (requests.RequestException, KeyError, ValueError) as e:
        return {"error": str(e)}


# ---------------------------------------------------------------------------
# Session logging
# ---------------------------------------------------------------------------

def log_to_session(entry: dict) -> None:
    """Append a structured entry to the HODIE session log."""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry) + '\n')


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _print_perplexity_result(zero_lexeme: str, context: str) -> dict:
    """Query Perplexity and print the result; return the perplexity payload."""
    print(f"\n▶ Querying Perplexity for: '{zero_lexeme}'")
    print("─" * 50)
    perp = query_perplexity(zero_lexeme, context=context)
    if "error" in perp:
        print(f"  Perplexity error: {perp['error']}")
    else:
        print(f"\n{perp['response']}\n")
        for c in perp.get("citations", []):
            print(f"  - {c}")
    return perp


def main():
    parser = argparse.ArgumentParser(description="Find zero-point lexeme and search Perplexity")
    parser.add_argument("document", help="Path to document file")
    parser.add_argument("--top", type=int, default=1, help="Number of top lexemes to return (default: 1)")
    parser.add_argument("--no-perplexity", action="store_true", help="Skip Perplexity search")
    parser.add_argument("--context", default="", help="Optional context string for Perplexity query")
    args = parser.parse_args()

    doc_path = Path(args.document)
    if not doc_path.exists():
        print(f"ERROR: File not found: {doc_path}", file=sys.stderr)
        sys.exit(1)

    print(f"\n▶ Zero-point analysis: {doc_path.name}")
    print("─" * 50)

    ranked = find_zero_point(doc_path, top_n=args.top)
    for rank, (lexeme, score) in enumerate(ranked, 1):
        print(f"  #{rank}: '{lexeme}'  (score: {score:.4f})")

    zero_lexeme = ranked[0][0] if ranked else None
    result: dict = {
        "timestamp": datetime.now().isoformat(),
        "operation": "zero_point",
        "document": str(doc_path),
        "ranked_lexemes": ranked,
        "zero_point": zero_lexeme,
    }

    if zero_lexeme and not args.no_perplexity:
        result["perplexity"] = _print_perplexity_result(zero_lexeme, args.context)

    log_to_session(result)
    print(f"\n✓ Logged to {LOG_FILE}")


if __name__ == "__main__":
    main()
