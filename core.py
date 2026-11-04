import functools
import types
from typing import Callable, Any, List


class CorePipeline:
    """High-performance processing pipeline with dynamic bytecode synthesis."""

    __slots__ = ("_stages", "_fused_kernel", "_fast_path")

    def __init__(self, *stages: Callable[[Any], Any]):
        self._stages: List[Callable[[Any], Any]] = list(stages)
        self._fused_kernel: Callable[[Any], Any] | None = None
        self._fast_path = None
        if stages:
            self._fuse_stages()

    def add_stage(self, func: Callable[[Any], Any]) -> "CorePipeline":
        self._stages.append(func)
        self._fused_kernel = None
        return self

    def _fuse_stages() -> None:
        if not self._stages:
            self._fused_kernel = lambda x: x
            return

        ns = {f"_f{i}": fn for i, fn in enumerate(self._stages)}
        expr = "val"
        for i in range(len(self._stages)):
            expr = f"_f{i}({expr})"

        code_str = f"def _kernel(val):\n    return {expr}\n"
        compiled = compile(code_str, "<fused_kernel>", "exec")
        kernel_ns = {}
        exec(compiled, ns, kernel_ns)
        self._fused_kernel = kernel_ns["_kernel"]

    def run(self, payload: Any) -> Any:
        if self._fused_kernel is None:
            self._fuse_stages()
        return self._fused_kernel(payload)

    def run_batch(self, items: List[Any]) -> List[Any]:
        kernel = self._fused_kernel
        if kernel is None:
            self._fuse_stages()
            kernel = self._fused_kernel

        return [kernel(item) for item in items]
