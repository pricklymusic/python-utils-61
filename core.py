import time
from functools import wraps, lru_cache
from typing import Callable, Any, List

class AdaptiveMemoizer:
    """Performance optimizer that dynamically enables caching based on execution latency."""
    
    def __init__(self, sample_size: int = 10, latency_threshold_ms: float = 0.5):
        self.sample_size = sample_size
        self.threshold = latency_threshold_ms / 1000.0

    def __call__(self, func: Callable) -> Callable:
        cached_variant = lru_cache(maxsize=2048)(func)
        samples: List[float] = []
        
        @wraps(func)
        def adaptive_wrapper(*args: Any, **kwargs: Any) -> Any:
            if getattr(adaptive_wrapper, "_is_hot", False):
                return cached_variant(*args, **kwargs)

            if len(samples) < self.sample_size:
                start = time.perf_counter()
                res = func(*args, **kwargs)
                samples.append(time.perf_counter() - start)
                return res

            avg_latency = sum(samples) / len(samples)
            if avg_latency > self.threshold:
                setattr(adaptive_wrapper, "_is_hot", True)
                return cached_variant(*args, **kwargs)
            
            return func(*args, **kwargs)

        def clear_stats():
            samples.clear()
            setattr(adaptive_wrapper, "_is_hot", False)
            cached_variant.cache_clear()

        adaptive_wrapper.clear_stats = clear_stats
        adaptive_wrapper._is_hot = False
        return adaptive_wrapper


def batch_process_optimized(items: List[Any], processor_func: Callable) -> List[Any]:
    """High-throughput batch utility leveraging adaptive execution path optimization."""
    memoized = AdaptiveMemoizer(sample_size=5, latency_threshold_ms=0.1)(processor_func)
    return [memoized(item) for item in items]
