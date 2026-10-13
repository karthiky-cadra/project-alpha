# ratelimit-lite

A tiny, dependency-free token-bucket rate limiter for Python.

## Install

```bash
pip install -e .
```

## Usage

```python
from ratelimit_lite import TokenBucket

bucket = TokenBucket(capacity=5, refill_per_sec=1)
if bucket.allow():
    print("request allowed")
```

## Design notes

- Token bucket with lazy refill (no background threads).
- Injectable clock so tests are deterministic.
- Thread-safe via a single lock.

## Tests

```bash
pip install pytest
pytest -q
```
