#!/usr/bin/env python3
"""Prompt A/B Testing Harness

Compares two prompt variants head-to-head across multiple runs,
collecting structured results for analysis.

Usage:
  export OPENAI_API_KEY="sk-..."
  prompt-ab --prompt-a prompt-a.md --prompt-b prompt-b.md --input "Test input" --runs 3
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


def load_prompt(path):
    with open(path) as f:
        return f.read().strip()


def call_llm(system_prompt, user_input, model="gpt-4", temperature=0.7,
             max_tokens=2048, api_key=None, base_url=None):
    client_kwargs = {"api_key": api_key or os.environ.get("OPENAI_API_KEY")}
    if base_url:
        client_kwargs["base_url"] = base_url

    if OpenAI is None:
        raise ImportError(
            "openai package not installed. Run: pip install openai"
        )

    client = OpenAI(**client_kwargs)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input},
        ],
        temperature=temperature,
        max_tokens=max_tokens,
    )

    return response.choices[0].message.content


def run_ab_test(prompt_a, prompt_b, user_input, model, temperature=0.7,
                runs=3, max_tokens=2048, api_key=None, base_url=None):
    results = {
        "config": {
            "model": model,
            "temperature": temperature,
            "runs": runs,
            "max_tokens": max_tokens,
            "timestamp": datetime.utcnow().isoformat(),
        },
        "prompt_a": {"label": "A", "runs": []},
        "prompt_b": {"label": "B", "runs": []},
    }

    for i in range(runs):
        for label, prompt, target in [
            ("A", prompt_a, results["prompt_a"]),
            ("B", prompt_b, results["prompt_b"]),
        ]:
            start = time.time()
            try:
                output = call_llm(
                    prompt, user_input, model=model,
                    temperature=temperature, max_tokens=max_tokens,
                    api_key=api_key, base_url=base_url,
                )
                elapsed = time.time() - start
                target["runs"].append({
                    "run": i + 1,
                    "output": output,
                    "latency_s": round(elapsed, 2),
                    "tokens": len(output.split()),
                    "error": None,
                })
            except Exception as e:
                target["runs"].append({
                    "run": i + 1,
                    "output": None,
                    "latency_s": None,
                    "tokens": None,
                    "error": str(e),
                })

    return results


def format_report(results):
    lines = []
    lines.append("# A/B Test Results")
    lines.append("")
    lines.append(f"**Model:** {results['config']['model']}")
    lines.append(f"**Temperature:** {results['config']['temperature']}")
    lines.append(f"**Runs per variant:** {results['config']['runs']}")
    lines.append(f"**Timestamp:** {results['config']['timestamp']}")
    lines.append("")

    for variant_key in ["prompt_a", "prompt_b"]:
        v = results[variant_key]
        label = v["label"]
        success_runs = [r for r in v["runs"] if r["error"] is None]
        avg_latency = sum(r["latency_s"] for r in success_runs) / len(success_runs) if success_runs else 0
        avg_tokens = sum(r["tokens"] for r in success_runs) / len(success_runs) if success_runs else 0

        lines.append(f"## Variant {label}")
        lines.append(f"- **Successful runs:** {len(success_runs)}/{len(v['runs'])}")
        lines.append(f"- **Avg latency:** {avg_latency:.1f}s")
        lines.append(f"- **Avg output length:** {avg_tokens:.0f} tokens")
        lines.append("")

        for r in v["runs"]:
            lines.append(f"### Run {r['run']}")
            if r["error"]:
                lines.append(f"**Error:** {r['error']}")
            else:
                lines.append(f"**Latency:** {r['latency_s']}s | **Tokens:** {r['tokens']}")
                lines.append("")
                lines.append(r["output"][:500] +
                             ("..." if len(r["output"]) > 500 else ""))
            lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Prompt A/B Testing Harness — compare prompt variants scientifically"
    )
    parser.add_argument("--prompt-a", help="Path to prompt A file")
    parser.add_argument("--prompt-b", help="Path to prompt B file")
    parser.add_argument("--input", help="User input text")
    parser.add_argument("--model", default="gpt-4", help="Model name")
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--runs", type=int, default=3, help="Runs per variant")
    parser.add_argument("--max-tokens", type=int, default=2048)
    parser.add_argument("--config", help="YAML config file")
    parser.add_argument("--output", help="Save results to file (JSON)")
    parser.add_argument("--report", help="Save markdown report to file")
    parser.add_argument("--base-url", help="Custom API base URL")

    args = parser.parse_args()

    if args.config:
        if yaml is None:
            parser.error("YAML support requires pyyaml: pip install pyyaml")
        with open(args.config) as f:
            cfg = yaml.safe_load(f)
        prompt_a = load_prompt(cfg["prompt_a"])
        prompt_b = load_prompt(cfg["prompt_b"])
        user_input = cfg.get("input", args.input or "")
        model = cfg.get("model", args.model)
        temperature = cfg.get("temperature", args.temperature)
        runs = cfg.get("runs", args.runs)
        max_tokens = cfg.get("max_tokens", args.max_tokens)
        base_url = cfg.get("base_url", args.base_url)
    else:
        if not args.prompt_a or not args.prompt_b:
            parser.error("--prompt-a and --prompt-b are required without --config")
        prompt_a = load_prompt(args.prompt_a)
        prompt_b = load_prompt(args.prompt_b)
        user_input = args.input or ""
        model = args.model
        temperature = args.temperature
        runs = args.runs
        max_tokens = args.max_tokens
        base_url = args.base_url

    if not os.environ.get("OPENAI_API_KEY"):
        print("Warning: No API key found. Set OPENAI_API_KEY.", file=sys.stderr)

    print(f"Running A/B test: {runs} runs per variant")
    print(f"Model: {model} | Temperature: {temperature}")
    print()

    results = run_ab_test(
        prompt_a, prompt_b, user_input, model=model,
        temperature=temperature, runs=runs, max_tokens=max_tokens,
        base_url=base_url,
    )

    report = format_report(results)
    print(report)

    if args.output:
        with open(args.output, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to: {args.output}")

    if args.report:
        with open(args.report, "w") as f:
            f.write(report)
        print(f"\nReport saved to: {args.report}")


if __name__ == "__main__":
    main()
