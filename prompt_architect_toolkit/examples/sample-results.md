# Sample A/B Test Results

This file shows example output from the A/B testing harness comparing two code review prompts.

## Configuration
- **Model:** gpt-4
- **Temperature:** 0.3
- **Runs per variant:** 2
- **Test Input:** A Python function with mixed-quality characteristics

```python
def process_user_data(users):
    result = []
    for u in users:
        tmp = {}
        tmp['name'] = u['name']
        tmp['email'] = u.get('email', 'unknown')
        # FIXME: this is slow
        tmp['orders'] = len([o for o in all_orders if o['user_id'] == u['id']])
        result.append(tmp)
    return result
```

## Variant A (Default Code Review Prompt)
- Avg latency: 8.3s | Avg tokens: 412
- Found: 1 critical issue (nested loop), 2 major issues (mutable default, missing type hints), 3 minor issues

## Variant B (Structured Code Review Prompt with Severity Levels)
- Avg latency: 9.1s | Avg tokens: 528
- Found: Same issues + 1 additional (performance: O(n*m) algorithm), with clearer severity breakdown

## Verdict
Variant B provides more thorough analysis with actionable severity levels, at a minimal latency cost.