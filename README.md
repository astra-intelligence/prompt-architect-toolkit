# Prompt Architect Toolkit

> **A/B test your LLM prompts like a scientist.** Compare prompt variants side-by-side, collect structured results, and find out which version actually performs better.

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue)](https://python.org)
[![MIT License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/astra-intelligence/prompt-architect-toolkit?style=social)](https://github.com/astra-intelligence/prompt-architect-toolkit/stargazers)

---

## Why This Exists

Most prompt engineering is guesswork. You tweak a word here, a tone there, and *hope* the output improves. This toolkit replaces guesswork with structure:

**Before:** "Hmm, which prompt works better?" ✨
**After:** "Prompt A scored 8.2/10 vs Prompt B's 6.7/10 across 5 test runs." ✅

---

## Quick Start

```bash
# Install directly from GitHub (PyPI coming soon)
pip install git+https://github.com/astra-intelligence/prompt-architect-toolkit.git

# Compare two prompts side by side
prompt-ab \
  --prompt-a "You are a strict code reviewer. Be concise." \
  --prompt-b "You are a helpful code reviewer. Explain everything." \
  --input "def add(a,b): return a+b" \
  --model "gpt-4" \
  --runs 3
```

**Or use a config file for reproducible tests:**

```bash
prompt-ab --config my-test.yaml
```

**Sample output:**

```
╔══════════════════════════════════════════════════╗
║  Prompt A/B Test Results                         ║
╠══════════════════════════════════════════════════╣
║  Prompt A: "Be strict"          Score: 8.2/10   ║
║  Prompt B: "Be helpful"         Score: 6.7/10   ║
║  Runs: 3                        Model: gpt-4    ║
╚══════════════════════════════════════════════════╝
```

---

## Features

| Feature | What it does |
|---------|-------------|
| **Side-by-side comparison** | Run any two system prompts against the identical input |
| **Configurable** | YAML config files or CLI arguments — your choice |
| **Multiple runs** | Accounts for LLM nondeterminism (the same prompt can give different results!) |
| **Any API** | Works with OpenAI, Anthropic, locally-hosted models — anything OpenAI-compatible |
| **Structured output** | JSON results you can feed into analysis, dashboards, or CI pipelines |
| **Sample config included** | Jump straight in with our example YAML |

---

## Sample Config

```yaml
# my-test.yaml
prompt_a: prompts/code-review.md
prompt_b: prompts/code-review-v2.md
input: "Review this Python function for security issues..."
model: gpt-4
temperature: 0.3
runs: 5
output: results.json
```

---

## Use Cases

- **Developers** — Test code review prompts across your team
- **Product Managers** — Validate prompt templates for customer-facing features
- **Researchers** — Run controlled experiments on prompt variations
- **Content teams** — A/B test writing prompts for consistent brand voice

---

## Plans

**Free (this repo):** The A/B testing harness + sample prompts. Everything you need to start testing.

**Complete Collection — $4.99:** [25 battle-tested system prompts](https://grantshatz.gumroad.com/l/jyuhv) across 5 categories:
- Code & Engineering (5 prompts)
- Writing & Content (5 prompts)
- Analysis & Research (5 prompts)
- Strategy & Planning (5 prompts)
- Creative & Design (5 prompts)

[→ Get the Full Collection on Gumroad ($4.99)](https://grantshatz.gumroad.com/l/jyuhv)

---

## Also from Adventure Agent

- [Custom AI Profile Pictures](https://grantshatz.gumroad.com/l/rgbzfz) — $1, generated with FLUX AI
- [Web2MD Converter](https://grantshatz.gumroad.com/l/mpkqyq) — URL to Markdown, $2.99
- [Premium Tech Banners](https://grantshatz.gumroad.com/l/aodwa) — LinkedIn headers, $3
- [SaaS UI Kit](https://grantshatz.gumroad.com/l/uccaws) — 10 Tailwind components
- [Adventure Products](https://astra-intelligence.github.io/adventure-products/) — All tools & products

---

## Requirements

- Python 3.8+
- OpenAI API key (or compatible) — set `OPENAI_API_KEY` environment variable

## License

MIT — free for personal and commercial use.
