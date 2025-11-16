import os
import json
import time
import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache, wraps
from typing import Dict, List, Any, Callable, Optional
import logging

class PerformanceOptimizer:
    """Enterprise-grade performance optimization utilities for Level 3 AI system"""

    def __init__(self, max_workers: int = None):
        self.max_workers = max_workers or min(32, (os.cpu_count() or 1) * 4)
        self.executor = ThreadPoolExecutor(max_workers=self.max_workers, thread_name_prefix="level3_ai")
        self.cache = {}
        self.cache_ttl = 3600  # 1 hour default TTL
        self.logger = logging.getLogger(__name__)

        # Performance metrics
        self.metrics = {
            "cache_hits": 0,
            "cache_misses": 0,
            "parallel_tasks_completed": 0,
            "async_tasks_completed": 0,
            "errors_handled": 0
        }

    def cached(self, ttl: int = None):
        """Decorator for caching function results"""
        def decorator(func):
            cache_key_prefix = f"{func.__module__}.{func.__name__}"

            @wraps(func)
            def wrapper(*args, **kwargs):
                # Create cache key from function arguments
                cache_key = f"{cache_key_prefix}:{hash(str(args) + str(sorted(kwargs.items())))}"

                # Check cache
                if cache_key in self.cache:
                    cached_result, timestamp = self.cache[cache_key]
                    if time.time() - timestamp < (ttl or self.cache_ttl):
                        self.metrics["cache_hits"] += 1
                        return cached_result
                    else:
                        # Expired, remove from cache
                        del self.cache[cache_key]

                # Execute function
                result = func(*args, **kwargs)
                self.cache[cache_key] = (result, time.time())
                self.metrics["cache_misses"] += 1

                # Clean old cache entries periodically
                if len(self.cache) > 1000:
                    self._cleanup_cache()

                return result
            return wrapper
        return decorator

    def _cleanup_cache(self):
        """Clean up expired cache entries"""
        current_time = time.time()
        expired_keys = [
            key for key, (_, timestamp) in self.cache.items()
            if current_time - timestamp > self.cache_ttl
        ]
        for key in expired_keys:
            del self.cache[key]

    def parallel_execute(self, tasks: List[Callable], max_concurrent: int = None) -> List[Any]:
        """Execute tasks in parallel with error handling"""
        max_concurrent = max_concurrent or self.max_workers
        results = []

        with ThreadPoolExecutor(max_workers=max_concurrent, thread_name_prefix="level3_parallel") as executor:
            future_to_task = {executor.submit(task): i for i, task in enumerate(tasks)}

            for future in as_completed(future_to_task):
                task_index = future_to_task[future]
                try:
                    result = future.result(timeout=300)  # 5 minute timeout
                    results.append((task_index, result))
                    self.metrics["parallel_tasks_completed"] += 1
                except Exception as e:
                    self.logger.error(f"Parallel task {task_index} failed: {e}")
                    results.append((task_index, None))
                    self.metrics["errors_handled"] += 1

        # Sort results by original task order
        results.sort(key=lambda x: x[0])
        return [result for _, result in results]

    async def async_execute(self, tasks: List[Callable]) -> List[Any]:
        """Execute async tasks with proper error handling"""
        async def run_task(task):
            try:
                if asyncio.iscoroutinefunction(task):
                    result = await task()
                else:
                    result = await asyncio.get_event_loop().run_in_executor(self.executor, task)
                self.metrics["async_tasks_completed"] += 1
                return result
            except Exception as e:
                self.logger.error(f"Async task failed: {e}")
                self.metrics["errors_handled"] += 1
                return None

        results = await asyncio.gather(*[run_task(task) for task in tasks], return_exceptions=True)
        return results

    def batch_process(self, items: List[Any], batch_size: int, processor: Callable) -> List[Any]:
        """Process items in batches for memory efficiency"""
        results = []
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            batch_results = processor(batch)
            results.extend(batch_results)
        return results

    def circuit_breaker(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        """Circuit breaker decorator for external service calls"""
        def decorator(func):
            failures = 0
            last_failure_time = 0
            is_open = False

            @wraps(func)
            def wrapper(*args, **kwargs):
                nonlocal failures, last_failure_time, is_open

                current_time = time.time()

                # Check if circuit should be reset
                if is_open and (current_time - last_failure_time) > recovery_timeout:
                    is_open = False
                    failures = 0
                    self.logger.info(f"Circuit breaker reset for {func.__name__}")

                if is_open:
                    raise Exception(f"Circuit breaker open for {func.__name__}")

                try:
                    result = func(*args, **kwargs)
                    # Success - reset failure count
                    failures = 0
                    return result
                except Exception as e:
                    failures += 1
                    last_failure_time = current_time

                    if failures >= failure_threshold:
                        is_open = True
                        self.logger.warning(f"Circuit breaker opened for {func.__name__} after {failures} failures")

                    raise e

            return wrapper
        return decorator

    def rate_limiter(self, calls_per_minute: int = 60):
        """Rate limiter decorator"""
        def decorator(func):
            call_times = []
            lock = threading.Lock()

            @wraps(func)
            def wrapper(*args, **kwargs):
                with lock:
                    current_time = time.time()
                    # Remove old call times
                    call_times[:] = [t for t in call_times if current_time - t < 60]

                    if len(call_times) >= calls_per_minute:
                        sleep_time = 60 - (current_time - call_times[0])
                        if sleep_time > 0:
                            time.sleep(sleep_time)

                    call_times.append(time.time())
                    return func(*args, **kwargs)

            return wrapper
        return decorator

    def memory_efficient_processor(self, memory_limit_mb: int = 100):
        """Process data with memory usage monitoring"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                import psutil
                process = psutil.Process()

                memory_before = process.memory_info().rss / 1024 / 1024  # MB

                try:
                    result = func(*args, **kwargs)
                    memory_after = process.memory_info().rss / 1024 / 1024  # MB
                    memory_used = memory_after - memory_before

                    if memory_used > memory_limit_mb:
                        self.logger.warning(f"High memory usage in {func.__name__}: {memory_used:.2f} MB")

                    return result
                except Exception as e:
                    memory_after = process.memory_info().rss / 1024 / 1024  # MB
                    memory_used = memory_after - memory_before
                    self.logger.error(f"Error in {func.__name__} with {memory_used:.2f} MB memory usage: {e}")
                    raise e

            return wrapper
        return decorator

    def optimize_api_calls(self, api_calls: List[Dict]) -> Dict[str, Any]:
        """Optimize API calls by batching and deduplication"""
        # Group by endpoint
        endpoint_groups = {}
        for call in api_calls:
            endpoint = call.get("endpoint", "default")
            if endpoint not in endpoint_groups:
                endpoint_groups[endpoint] = []
            endpoint_groups[endpoint].append(call)

        # Deduplicate calls
        optimized_calls = []
        for endpoint, calls in endpoint_groups.items():
            seen_params = set()
            for call in calls:
                param_hash = hash(json.dumps(call.get("params", {}), sort_keys=True))
                if param_hash not in seen_params:
                    seen_params.add(param_hash)
                    optimized_calls.append(call)

        return {
            "original_calls": len(api_calls),
            "optimized_calls": len(optimized_calls),
            "savings_percent": ((len(api_calls) - len(optimized_calls)) / len(api_calls) * 100) if api_calls else 0,
            "calls": optimized_calls
        }

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance optimization metrics"""
        return {
            "cache_performance": {
                "total_requests": self.metrics["cache_hits"] + self.metrics["cache_misses"],
                "hit_rate": (self.metrics["cache_hits"] / max(1, self.metrics["cache_hits"] + self.metrics["cache_misses"])) * 100,
                "cache_size": len(self.cache)
            },
            "parallel_processing": {
                "tasks_completed": self.metrics["parallel_tasks_completed"],
                "max_workers": self.max_workers
            },
            "async_processing": {
                "tasks_completed": self.metrics["async_tasks_completed"]
            },
            "error_handling": {
                "errors_handled": self.metrics["errors_handled"]
            },
            "system_resources": self._get_system_resources()
        }

    def _get_system_resources(self) -> Dict[str, Any]:
        """Get current system resource usage"""
        try:
            import psutil
            return {
                "cpu_percent": psutil.cpu_percent(),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_percent": psutil.disk_usage('/').percent,
                "threads_active": threading.active_count()
            }
        except ImportError:
            return {"note": "psutil not available for resource monitoring"}

    def cleanup(self):
        """Clean up resources"""
        self.executor.shutdown(wait=True)
        self.cache.clear()
        self.logger.info("Performance optimizer cleaned up")

class ResourceManager:
    """Resource management for Level 3 AI operations"""

    def __init__(self):
        self.resources = {}
        self.locks = {}
        self.timeouts = {}

    def acquire_resource(self, resource_name: str, timeout: int = 30) -> bool:
        """Acquire a resource with timeout"""
        if resource_name not in self.locks:
            self.locks[resource_name] = threading.Lock()
            self.resources[resource_name] = False

        lock = self.locks[resource_name]
        acquired = lock.acquire(timeout=timeout)

        if acquired:
            self.resources[resource_name] = True
            self.timeouts[resource_name] = time.time() + 300  # 5 minute default timeout

        return acquired

    def release_resource(self, resource_name: str):
        """Release a resource"""
        if resource_name in self.locks:
            self.resources[resource_name] = False
            self.locks[resource_name].release()

    def cleanup_stale_resources(self):
        """Clean up resources that have timed out"""
        current_time = time.time()
        stale_resources = [
            name for name, timeout in self.timeouts.items()
            if current_time > timeout
        ]

        for resource in stale_resources:
            self.release_resource(resource)
            del self.timeouts[resource]

# Global instances for the Level 3 AI system
performance_optimizer = PerformanceOptimizer()
resource_manager = ResourceManager()