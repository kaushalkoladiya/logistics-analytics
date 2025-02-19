import asyncio
import aiohttp
import time
from datetime import datetime, timedelta
from typing import List, Dict
import json
import logging


def get_logger():
    logger = logging.getLogger("load_testing")
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


logger = get_logger()


async def run_concurrent_requests(
    url: str, num_requests: int, params: Dict = None, method: str = "GET"
) -> Dict:
    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(num_requests):
            if method == "GET":
                tasks.append(asyncio.create_task(session.get(url, params=params)))
            elif method == "POST":
                tasks.append(asyncio.create_task(session.post(url, json=params)))

        start = time.time()
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        end = time.time()

        # Analyze responses in detail
        status_counts = {}
        error_details = []
        success_count = 0

        for resp in responses:
            if isinstance(resp, Exception):
                error_details.append(str(resp))
                continue

            status = resp.status
            status_counts[status] = status_counts.get(status, 0) + 1

            if 200 <= status < 300:
                success_count += 1

        return {
            "total_time": end - start,
            "avg_time": (end - start) / num_requests,
            "success_rate": success_count / num_requests,
            "total_requests": num_requests,
            "status_distribution": status_counts,
            "error_details": error_details[:5],  # First 5 errors for brevity
        }


async def main():
    base_url = "http://localhost:8000/api"
    concurrent_users = [1, 10, 50, 100]

    # Test date ranges
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    invalid_date = "2025-13-45"  # Invalid date format

    # Test endpoints with various scenarios
    endpoints = [
        # Dashboard endpoints
        {
            "name": "Dashboard Overview (Valid)",
            "url": f"{base_url}/dashboard",
            "params": {
                "start": start_date.strftime("%Y-%m-%d"),
                "end": end_date.strftime("%Y-%m-%d"),
                "interval_type": "week",
            },
        },
        {
            "name": "Dashboard Overview (Invalid Date)",
            "url": f"{base_url}/dashboard",
            "params": {
                "start": invalid_date,
                "end": end_date.strftime("%Y-%m-%d"),
                "interval_type": "week",
            },
        },
        # Cost endpoints
        {
            "name": "Cost Overview (Valid)",
            "url": f"{base_url}/costs/overview",
            "params": {
                "start": start_date.strftime("%Y-%m-%d"),
                "end": end_date.strftime("%Y-%m-%d"),
            },
        },
        {
            "name": "Cost Overview (Future Date)",
            "url": f"{base_url}/costs/overview",
            "params": {"start": "2025-01-01", "end": "2025-12-31"},
        },
        # Route endpoints
        {
            "name": "Route Reliability",
            "url": f"{base_url}/route/reliability",
            "params": {
                "start": start_date.strftime("%Y-%m-%d"),
                "end": end_date.strftime("%Y-%m-%d"),
                "page": 1,
                "page_size": 10,
            },
        },
        {
            "name": "Route Cost Value",
            "url": f"{base_url}/route/cost-value",
            "params": {
                "start": start_date.strftime("%Y-%m-%d"),
                "end": end_date.strftime("%Y-%m-%d"),
                "search": "New York",  # Test search functionality
            },
        },
        {
            "name": "Top Performing Routes",
            "url": f"{base_url}/route/top-performing",
            "params": {
                "start": start_date.strftime("%Y-%m-%d"),
                "end": end_date.strftime("%Y-%m-%d"),
                "limit": 5,
            },
        },
        # Shipment endpoints
        {
            "name": "Shipment Analytics",
            "url": f"{base_url}/shipments/analytics",
            "params": {
                "start": start_date.strftime("%Y-%m-%d"),
                "end": end_date.strftime("%Y-%m-%d"),
            },
        },
        {
            "name": "Route Performance (Invalid Sort)",
            "url": f"{base_url}/shipments/routes",
            "params": {
                "page": 1,
                "page_size": 10,
                "sort_by": "invalid_column",  # Test invalid sort column
                "sort_order": "desc",
            },
        },
        # Vehicle endpoints
        {
            "name": "Vehicle Metrics",
            "url": f"{base_url}/vehicles/metrics",
            "params": {
                "start": start_date.strftime("%Y-%m-%d"),
                "end": end_date.strftime("%Y-%m-%d"),
            },
        },
        {
            "name": "Vehicle Details (Valid)",
            "url": f"{base_url}/vehicles/V-004/details",
            "params": {
                "start": start_date.strftime("%Y-%m-%d"),
                "end": end_date.strftime("%Y-%m-%d"),
            },
        },
        {
            "name": "Vehicle Details (Invalid ID)",
            "url": f"{base_url}/vehicles/INVALID_ID/details",
            "params": {
                "start": start_date.strftime("%Y-%m-%d"),
                "end": end_date.strftime("%Y-%m-%d"),
            },
        },
        # Edge cases
        {
            "name": "Large Date Range",
            "url": f"{base_url}/dashboard",
            "params": {
                "start": "2020-01-01",
                "end": end_date.strftime("%Y-%m-%d"),
                "interval_type": "week",
            },
        },
        {
            "name": "Large Page Size",
            "url": f"{base_url}/route/reliability",
            "params": {
                "start": start_date.strftime("%Y-%m-%d"),
                "end": end_date.strftime("%Y-%m-%d"),
                "page": 1,
                "page_size": 1000,  # Test large page size
            },
        },
    ]

    results = []
    for endpoint in endpoints:
        logger.info(f"\nTesting {endpoint['name']}")
        for users in concurrent_users:
            logger.info(f"Concurrent users: {users}")
            result = await run_concurrent_requests(
                endpoint["url"], users, endpoint.get("params")
            )
            results.append(
                {"endpoint": endpoint["name"], "concurrent_users": users, **result}
            )

            # Add delay between tests to prevent rate limiting
            await asyncio.sleep(1)

    return results


def save_results(results: List[Dict]):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"load_test_results_{timestamp}.json"

    with open(filename, "w") as f:
        json.dump(results, f, indent=2)

    logger.info(f"\nDetailed results saved to {filename}")


def print_summary(results: List[Dict]):
    logger.info("\nLoad Test Summary:")
    logger.info("=" * 80)

    # Group by endpoint
    endpoint_results = {}
    for r in results:
        if r["endpoint"] not in endpoint_results:
            endpoint_results[r["endpoint"]] = []
        endpoint_results[r["endpoint"]].append(r)

    for endpoint, tests in endpoint_results.items():
        logger.info(f"\nEndpoint: {endpoint}")
        logger.info("-" * 40)

        for test in tests:
            logger.info(f"\nConcurrent Users: {test['concurrent_users']}")
            logger.info(f"Total Time: {test['total_time']:.2f}s")
            logger.info(f"Average Response Time: {test['avg_time']*1000:.2f}ms")
            logger.info(f"Success Rate: {test['success_rate']*100:.1f}%")

            if test["status_distribution"]:
                logger.info("Status Codes:")
                for status, count in test["status_distribution"].items():
                    logger.info(f"  {status}: {count}")

            if test["error_details"]:
                logger.info("Sample Errors:")
                for error in test["error_details"]:
                    logger.info(f"  {error}")


if __name__ == "__main__":
    results = asyncio.run(main())
    print_summary(results)
    save_results(results)
