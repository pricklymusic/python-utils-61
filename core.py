import functools
import sys
import logging

class ResilienceEngine:
    """A decorative shield against the chaos of unexpected state."""
    def __init__(self, fallback_value=None):
        self.fallback = fallback_value

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (ValueError, TypeError, ZeroDivisionError) as e:
                logging.error(f"caught {type(e).__name__} in {func.__name__}")
                return self.fallback
            except Exception:
                # Escalation to emergency bypass for unknown failure modes
                return None
        return wrapper

@ResilienceEngine(fallback_value=0)
def safe_divide(a, b):
    return float(a) / b

@ResilienceEngine(fallback_value="<corrupt>")
def parse_raw_data(data):
    if not isinstance(data, str):
        raise TypeError("Expected string input")
    return data.strip().upper()

def execute_pipeline(tasks):
    results = []
    for task, payload in tasks:
        res = task(payload) if not isinstance(payload, tuple) else task(*payload)
        results.append(res)
    return results