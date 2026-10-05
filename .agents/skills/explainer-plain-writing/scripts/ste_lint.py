#!/usr/bin/env python3
"""Lint text against an "80% ASD-STE100" profile.

Checks: sentence length (procedural <= 20 words, descriptive <= 25), paragraph
length (<= 6 sentences), passive voice, progressive and perfect tenses, one
instruction per procedural sentence, noun clusters (advisory), and
approved-style word swaps.

Reads Markdown, plain text, HTML (sheets, pages), and storyboard JSON
(beats[].say). Standard library only, Python 3.8+.

Usage:
  ste_lint.py FILE [FILE ...]        # or "-" for stdin
  ste_lint.py --threshold 0.9 brief.md
  ste_lint.py --json storyboard.json

Exit codes: 0 = pass, 1 = below threshold, 2 = usage error.
"""

import argparse
import html.parser
import json
import re
import sys
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

MAX_PROCEDURAL = 20
MAX_DESCRIPTIVE = 25
MAX_PARAGRAPH = 6
MAX_NOUN_CLUSTER = 3
CODE = "CODE"

IMPERATIVES = set("""
add adjust apply ask attach avoid build call change check choose cite clean clear
click clone close commit compare configure confirm connect copy create cut delete
deploy describe disable do download drag draw drop edit enable enter export
extract fetch fill find fix follow get give go hand hold import include inspect
install keep kill label launch let lift link lint list load lock log look make
mark measure merge move name narrate note open paste pause pick pin place play
point prefer press print pull push put read rebase record reduce refresh
regenerate register release reload remove rename render repeat replace report
reset restart restore return review run save say scroll search select send set
ship show sign skip sort speak specify split start state stop store submit switch
take tell test tighten try turn type uninstall unlock update upgrade upload use
validate verify view wait watch write
""".split())

IRREGULAR_PARTICIPLES = set("""
been begun bent bound bought brought broken built burnt caught chosen come cut
dealt done drawn driven eaten fallen fed felt fought found forgotten frozen given
gone grown had heard held hidden hit hung hurt kept known laid led left lent let
lit lost made meant met overridden paid proven put quit read rebuilt rewritten
ridden risen run said seen sent set shaken shown shot shut sold spent split
spoken spun stolen struck stuck sworn taken taught thought thrown told torn
understood undone withdrawn woken won worn written
""".split())

NOT_PARTICIPLES = set("""
bed bred embed feed hundred indeed need red seed shed speed naked wicked sacred
rugged ragged kindred
""".split())

ING_NOT_PROGRESSIVE = set("""
anything ceiling during evening everything interesting morning nothing pending
sibling something thing existing following remaining matching corresponding
missing misleading outstanding willing amazing boring
""".split())

FUNCTION_WORDS = set("""
a an the this that these those it its it's they them their there here he she him
her his we us our you your i me my mine yours who whom whose which what when where
why how all any each every some no not none both either neither few many much more
most other such own same only also very too so than then just even still yet
and or but nor if because while although though unless until since as so before
after about above across against along among around at by down for from in into
like near of off on onto out over past per through to toward under up upon via
with within without am is are was were be been being has have had do does did
will would shall should can could may might must ought let lets never always
often sometimes again first last now later soon once ever
""".split())

COMMON_VERBS = set("""
appear appears become becomes cause causes come comes contain contains exist
exists fail fails go goes happen happens help helps lead leads live lives look
looks mean means need needs own owns remain remains seem seems stay stays work
works wins loses triggers fires passes matches
""".split())

# (pattern, suggestion). Patterns are matched case-insensitively on word boundaries.
WORD_SWAPS: List[Tuple[str, str]] = [
    (r"utili[sz](?:e|es|ed|ing|ation)", "use"),
    (r"commenc(?:e|es|ed|ing|ement)", "start"),
    (r"prior to", "before"),
    (r"in order to", "to"),
    (r"approximately|approx\.", "about"),
    (r"ensur(?:e|es|ed|ing)", "make sure"),
    (r"replenish(?:es|ed|ing)?", "fill"),
    (r"terminat(?:e|es|ed|ing)", "stop / end"),
    (r"initiat(?:e|es|ed|ing)", "start"),
    (r"facilitat(?:e|es|ed|ing)", "help / make easy"),
    (r"subsequently", "then / after"),
    (r"subsequent", "next / later"),
    (r"in the event (?:that|of)", "if"),
    (r"at (?:this|the present) (?:point in )?time", "now"),
    (r"due to the fact that", "because"),
    (r"owing to", "because of"),
    (r"a (?:large |small )?number of", "some / many / a count"),
    (r"sufficient", "enough"),
    (r"insufficient", "not enough"),
    (r"additional", "more"),
    (r"numerous", "many"),
    (r"demonstrat(?:e|es|ed|ing)", "show"),
    (r"indicat(?:e|es|ed|ing)", "show"),
    (r"modif(?:y|ies|ied|ying)", "change"),
    (r"obtain(?:s|ed|ing)?", "get"),
    (r"purchas(?:e|es|ed|ing)", "buy"),
    (r"assist(?:s|ed|ing)?", "help"),
    (r"endeavou?r(?:s|ed)?", "try"),
    (r"whilst", "while"),
    (r"e\.g\.", "for example"),
    (r"i\.e\.", "that is"),
    (r"etc\.", "give the full list"),
    (r"and/or", "A, B, or both"),
    (r"aforementioned", "this / that"),
    (r"thereby", "so"),
    (r"in addition to", "and / also"),
    (r"with (?:regard|respect) to|in regard to", "about"),
    (r"comprise(?:s|d)?", "has / contains"),
    (r"in conjunction with", "with"),
    (r"(?:has|have) the ability to|(?:is|are) able to", "can"),
    (r"make use of", "use"),
    (r"whether or not", "whether / if"),
    (r"in close proximity|proximity", "near"),
    (r"optimal", "best"),
    (r"methodology", "method"),
    (r"functionality", "function / feature"),
    (r"leverag(?:e|es|ed|ing)", "use"),
    (r"delv(?:e|es|ed|ing)", "look at / study"),
    (r"seamless(?:ly)?", "remove, or say what works"),
    (r"robust", "strong / reliable, or say how"),
    (r"cutting-edge|state-of-the-art", "remove, or name the feature"),
    (r"it is important to note(?: that)?|it's worth noting(?: that)?|please note(?: that)?",
     "remove"),
    (r"basically|essentially", "remove"),
]
WORD_SWAP_RES = [(re.compile(r"(?<![\w-])(?:%s)(?![\w-])" % p, re.I), s) for p, s in WORD_SWAPS]

BE = r"(?:am|is|are|was|were|be|been|being|get|gets|got|gotten|getting)"
ADV = r"(?:(?:not|also|then|now|only|always|never|often|usually|still|already|just|\w+ly)\s+)*"
PASSIVE_RE = re.compile(r"\b%s\s+%s(\w+)\b" % (BE, ADV), re.I)
PROGRESSIVE_RE = re.compile(r"\b(?:am|is|are|was|were|be|been)\s+%s(\w+ing)\b" % ADV, re.I)
PERFECT_RE = re.compile(r"\b(?:has|have|had|hasn't|haven't|hadn't)\s+%s(\w+)\b" % ADV, re.I)
CONDITION_RE = re.compile(
    r"^(?:if|when|before|after|until|while|once|unless|to|for|where|in|on|at)\b[^,]*,\s*", re.I)
SAFETY_RE = re.compile(r"^(?:warning|caution|note|important|tip)\s*:\s*", re.I)
PAREN_RE = re.compile(r"\s*\([^()]*\)")
QUOTE_RE = re.compile(r"\"[^\"]*\"|\u201c[^\u201d]*\u201d")
SEGMENT_SPLIT_RE = re.compile(r"[,;:()\[\]{}\"\u201c\u201d+=|\u2192\u2190\u00b7\u2022]|\s[-\u2013\u2014]\s|[\u2013\u2014]")
ABBREVIATIONS = ["e.g.", "i.e.", "etc.", "vs.", "approx.", "Fig.", "No.", "Mr.", "Ms.", "Dr.", "St."]
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])[\"')\]]*\s+(?=[\"'(\[*A-Z0-9])")
TOKEN_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9'\u2019_./-]*")


@dataclass
class Finding:
    rule: str
    line: int
    message: str
    excerpt: str
    advisory: bool = False


@dataclass
class Sentence:
    text: str
    line: int
    procedural: bool
    findings: List[Finding] = field(default_factory=list)


@dataclass
class Paragraph:
    lines: List[Tuple[int, str]]


def is_participle(word: str) -> bool:
    w = word.lower()
    if w in NOT_PARTICIPLES:
        return False
    return w in IRREGULAR_PARTICIPLES or (w.endswith("ed") and len(w) > 3)


def is_progressive(word: str) -> bool:
    w = word.lower()
    if w in ING_NOT_PROGRESSIVE:
        return False
    stem = w[:-3]
    return len(stem) >= 2 and bool(re.search(r"[aeiouy]", stem))


def words_of(text: str) -> List[str]:
    return [t.rstrip("./-") for t in TOKEN_RE.findall(text) if t.rstrip("./-")]


def is_procedural(text: str) -> bool:
    t = SAFETY_RE.sub("", PAREN_RE.sub("", text).strip().lstrip("*_\"'(["))
    low = t.lower()
    if re.match(r"^(?:do not|don't|never|always|make sure|be sure|please)\b", low):
        return True
    cond = CONDITION_RE.match(t)
    if cond:
        rest = t[cond.end():]
        first = (words_of(rest) or [""])[0].lower()
        return first in IMPERATIVES or rest.lower().startswith(("do not", "don't", "make sure"))
    first = (words_of(t) or [""])[0].lower()
    return first in IMPERATIVES


# ---------------------------------------------------------------- extraction

INLINE_CODE_RE = re.compile(r"`[^`]+`")
IMAGE_RE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]*\)")
URL_RE = re.compile(r"https?://\S+")
EMPH_RE = re.compile(r"(\*\*|__|\*)")
LIST_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+(?:\[[ xX]\]\s+)?")


def clean_inline(text: str) -> str:
    text = INLINE_CODE_RE.sub(CODE, text)
    text = IMAGE_RE.sub("", text)
    text = LINK_RE.sub(r"\1", text)
    text = URL_RE.sub("URL", text)
    text = EMPH_RE.sub("", text)
    text = text.replace("<br>", " ").replace("&nbsp;", " ")
    return text.strip()


def paragraphs_from_markdown(raw: str, include_tables: bool) -> List[Paragraph]:
    paras: List[Paragraph] = []
    current: List[Tuple[int, str]] = []
    in_fence = False
    in_comment = False
    lines = raw.splitlines()
    start = 0
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                start = i + 1
                break

    def flush():
        nonlocal current
        if current:
            paras.append(Paragraph(current))
        current = []

    for idx in range(start, len(lines)):
        lineno = idx + 1
        line = lines[idx]
        stripped = line.strip()
        if stripped.startswith(("```", "~~~")):
            in_fence = not in_fence
            flush()
            continue
        if in_fence:
            continue
        if in_comment:
            if "-->" in stripped:
                in_comment = False
            continue
        if stripped.startswith("<!--"):
            in_comment = "-->" not in stripped
            continue
        if not stripped or stripped.startswith("#") or re.match(r"^[-*_=]{3,}$", stripped):
            flush()
            continue
        if stripped.startswith("|"):
            flush()
            if include_tables and not re.match(r"^\|[\s:|-]+\|?$", stripped):
                for cell in stripped.strip("|").split("|"):
                    cell = clean_inline(cell)
                    if cell:
                        paras.append(Paragraph([(lineno, cell)]))
            continue
        stripped = stripped.lstrip("> ").strip()
        if LIST_RE.match(line):
            flush()
            stripped = LIST_RE.sub("", line).strip()
        text = clean_inline(stripped)
        if text:
            current.append((lineno, text))
    flush()
    return paras


class _HTMLText(html.parser.HTMLParser):
    BLOCK = set("""
    address article aside blockquote br caption dd details dialog div dl dt
    fieldset figcaption figure footer form h1 h2 h3 h4 h5 h6 header hr li main nav
    ol p section summary table tbody td tfoot th thead tr ul text tspan title
    button label option
    """.split())
    SKIP = {"script", "style", "pre", "noscript", "head"}

    VOID = {"br", "hr", "img", "input", "meta", "link", "wbr", "source", "col", "area", "base", "embed"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.paras: List[Paragraph] = []
        self.current: List[Tuple[int, str]] = []
        self.skip_depth = 0
        self.in_code = 0
        self.stack: List[Tuple[str, bool]] = []
        self.spaced = True

    def flush(self):
        text = "".join(t for _, t in self.current).strip()
        if text:
            self.paras.append(Paragraph([(self.current[0][0], text)]))
        self.current = []
        self.spaced = True

    def push(self, text):
        # Text in adjacent tags with no whitespace between them (flex labels,
        # badges) is a separate fragment, so join it with a segment break.
        sep = "" if not self.current else (" " if self.spaced else " | ")
        self.current.append((self.getpos()[0], sep + text))
        self.spaced = False

    def handle_starttag(self, tag, attrs):
        skip = tag in self.SKIP or dict(attrs).get("data-lint") == "skip"
        if tag not in self.VOID:
            self.stack.append((tag, skip))
        if skip:
            self.skip_depth += 1
        elif tag in ("code", "kbd"):
            self.in_code += 1
            if not self.skip_depth:
                self.push(CODE)
        if tag in self.BLOCK:
            self.flush()

    def handle_endtag(self, tag):
        while self.stack:
            open_tag, skip = self.stack.pop()
            if skip:
                self.skip_depth = max(0, self.skip_depth - 1)
            elif open_tag in ("code", "kbd"):
                self.in_code = max(0, self.in_code - 1)
            if open_tag == tag:
                break
        if tag in self.BLOCK:
            self.flush()

    def handle_data(self, data):
        if self.skip_depth or self.in_code:
            return
        if data[:1].isspace():
            self.spaced = True
        text = re.sub(r"\s+", " ", data).strip()
        if text:
            self.push(text)
        if data[-1:].isspace():
            self.spaced = True

    def close(self):
        super().close()
        self.flush()


def paragraphs_from_html(raw: str) -> List[Paragraph]:
    parser = _HTMLText()
    parser.feed(raw)
    parser.close()
    return parser.paras


def paragraphs_from_json(raw: str) -> List[Paragraph]:
    data = json.loads(raw)
    beats = data.get("beats", []) if isinstance(data, dict) else data
    paras = []
    raw_lines = raw.splitlines()
    for beat in beats:
        if not isinstance(beat, dict):
            continue
        text = beat.get("say") or beat.get("narration") or beat.get("text") or ""
        text = re.sub(r"\[[a-z ]+\]", "", text).strip()
        if not text:
            continue
        needle = json.dumps(text)[1:30]
        lineno = next((i + 1 for i, l in enumerate(raw_lines) if needle in l), 0)
        paras.append(Paragraph([(lineno, text)]))
    return paras


# ------------------------------------------------------------------ checking

def split_sentences(par: Paragraph) -> List[Tuple[int, str]]:
    joined = ""
    offsets: List[Tuple[int, int]] = []
    for lineno, text in par.lines:
        offsets.append((len(joined), lineno))
        joined += text + " "
    protected = joined
    for i, abbr in enumerate(ABBREVIATIONS):
        protected = protected.replace(abbr, abbr.replace(".", "\u2024"))
    out = []
    pos = 0
    for chunk in SENTENCE_SPLIT_RE.split(protected):
        idx = protected.find(chunk, pos)
        pos = idx + len(chunk)
        sentence = chunk.replace("\u2024", ".").strip()
        if not words_of(sentence):
            continue
        lineno = offsets[0][1]
        for off, ln in offsets:
            if off <= idx:
                lineno = ln
        out.append((lineno, sentence))
    return out


def excerpt(text: str, n: int = 70) -> str:
    return text if len(text) <= n else text[: n - 1] + "\u2026"


def check_sentence(s: Sentence, ignore: set) -> None:
    words = words_of(s.text)
    limit = MAX_PROCEDURAL if s.procedural else MAX_DESCRIPTIVE
    kind = "Procedural" if s.procedural else "Descriptive"

    def add(rule, message, advisory=False):
        if rule not in ignore:
            s.findings.append(Finding(rule, s.line, message, excerpt(s.text), advisory))

    if len(words) > limit:
        add("sentence-length", "%s sentence has %d words (max %d). Split it." % (kind, len(words), limit))

    used = QUOTE_RE.sub(" QUOTE ", s.text)
    for m in PASSIVE_RE.finditer(used):
        if is_participle(m.group(1)):
            where = " in a procedure" if s.procedural else ""
            add("passive", "Passive voice%s: \"%s\". Say who does the action." % (where, m.group(0)))
            break
    for m in PROGRESSIVE_RE.finditer(used):
        if is_progressive(m.group(1)):
            add("progressive", "Progressive tense: \"%s\". Use the simple present or past." % m.group(0))
            break
    for m in PERFECT_RE.finditer(used):
        if is_participle(m.group(1)):
            add("perfect", "Perfect tense: \"%s\". Use the simple past or present." % m.group(0))
            break

    if s.procedural:
        body = SAFETY_RE.sub("", PAREN_RE.sub("", used).strip())
        cond = CONDITION_RE.match(body)
        if cond:
            body = body[cond.end():]
        m = re.search(r"(?:,|;|\band\b|\bthen\b)\s+(?:then\s+)?(%s)\b" % "|".join(sorted(IMPERATIVES)),
                      body, re.I)
        if m:
            add("one-instruction", "Two instructions in one sentence (\"%s\"). Split into steps." % m.group(0).strip(", "))

    clusters = []
    for segment in SEGMENT_SPLIT_RE.split(s.text):
        run: List[str] = []
        for w in words_of(segment) + ["."]:
            lw = w.lower().strip("'\u2019")
            nounish = (w != "." and re.search(r"[a-z]", lw) and lw not in FUNCTION_WORDS
                       and lw not in COMMON_VERBS and not lw.endswith(("ly", "ed"))
                       and not (lw.endswith("s") and lw[:-1] in IMPERATIVES)
                       and not (lw.endswith("es") and lw[:-2] in IMPERATIVES)
                       and not (lw.endswith("ies") and lw[:-3] + "y" in IMPERATIVES))
            if nounish and not (not run and lw in IMPERATIVES):
                run.append(w)
            else:
                if len(run) > MAX_NOUN_CLUSTER:
                    clusters.append(" ".join(run))
                run = []
    for c in clusters:
        add("noun-cluster", "Possible noun cluster of %d words: \"%s\" (max %d). Use \"of\" or split."
            % (len(c.split()), c, MAX_NOUN_CLUSTER), advisory=True)

    seen = set()
    for rx, suggestion in WORD_SWAP_RES:
        for m in rx.finditer(used):
            key = m.group(0).lower()
            if key in seen:
                continue
            seen.add(key)
            add("word", "\"%s\" \u2192 %s." % (m.group(0), suggestion))


def lint_paragraphs(paras: List[Paragraph], ignore: set) -> Tuple[List[Sentence], List[Finding]]:
    sentences: List[Sentence] = []
    extra: List[Finding] = []
    for par in paras:
        sents = split_sentences(par)
        for i, (line, text) in enumerate(sents):
            s = Sentence(text=text, line=line, procedural=is_procedural(text))
            check_sentence(s, ignore)
            if i == MAX_PARAGRAPH and "paragraph-length" not in ignore:
                f = Finding("paragraph-length", line,
                            "Paragraph has %d sentences (max %d). Split it." % (len(sents), MAX_PARAGRAPH),
                            excerpt(text))
                extra.append(f)
            if i >= MAX_PARAGRAPH and "paragraph-length" not in ignore:
                s.findings.append(Finding("paragraph-length", line, "", excerpt(text)))
            sentences.append(s)
    return sentences, extra


def load(path: str, include_tables: bool) -> List[Paragraph]:
    raw = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()
    lower = path.lower()
    if lower.endswith((".html", ".htm", ".svg")):
        return paragraphs_from_html(raw)
    if lower.endswith(".json"):
        return paragraphs_from_json(raw)
    return paragraphs_from_markdown(raw, include_tables)


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Lint text against an 80% ASD-STE100 profile.")
    ap.add_argument("files", nargs="+", help="Files to lint (.md .txt .html .json), or - for stdin")
    ap.add_argument("--threshold", type=float, default=0.8,
                    help="Minimum share of clean sentences to pass (default 0.8)")
    ap.add_argument("--strict", action="store_true", help="Same as --threshold 1.0")
    ap.add_argument("--ignore", default="", help="Comma-separated rules to skip")
    ap.add_argument("--tables", action="store_true", help="Also lint Markdown table cells")
    ap.add_argument("--quiet", action="store_true", help="Print only the summary")
    ap.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    args = ap.parse_args(argv)
    threshold = 1.0 if args.strict else args.threshold
    ignore = {r.strip() for r in args.ignore.split(",") if r.strip()}

    results: Dict[str, dict] = {}
    overall_ok = True
    for path in args.files:
        try:
            paras = load(path, args.tables)
        except (OSError, ValueError) as exc:
            print("ste_lint: cannot read %s: %s" % (path, exc), file=sys.stderr)
            return 2
        sentences, extra = lint_paragraphs(paras, ignore)
        total = len(sentences)
        clean = sum(1 for s in sentences if not any(not f.advisory for f in s.findings))
        score = clean / total if total else 1.0
        ok = score >= threshold
        overall_ok &= ok
        findings = sorted(extra + [f for s in sentences for f in s.findings if f.message],
                          key=lambda f: (f.line, f.rule))
        results[path] = {"sentences": total, "clean": clean, "score": round(score, 3),
                         "pass": ok, "findings": [f.__dict__ for f in findings]}
        if args.json:
            continue
        name = "<stdin>" if path == "-" else path
        if not args.quiet:
            for f in findings:
                tag = f.rule + (" (advisory)" if f.advisory else "")
                print("%s:%d: [%s] %s\n    \"%s\"" % (name, f.line, tag, f.message, f.excerpt))
        print("%s: %d sentences, %d clean (%d%%) - %s (threshold %d%%)"
              % (name, total, clean, round(score * 100), "PASS" if ok else "FAIL", round(threshold * 100)))
    if args.json:
        print(json.dumps(results, indent=2))
    return 0 if overall_ok else 1


if __name__ == "__main__":
    sys.exit(main())
