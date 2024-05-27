"""
Test HTTPBenchmark class
Python: 3.11.9
Packages: requirements.txt

Author: Ranadeep Singh
Email: ranadeep.dtu@gmail.com
"""

# import pandas as pd

from http_benchmark import HTTPBenchmark
import time

if __name__ == "__main__":
    
    urls = ['fireworks.ai', 'google.com', 'cupidgpt.ai']
    qpss = [1, 10, 100, 1000]
    timeouts = [10, 60]
    durations = [5, 10, 30]

    # List of all possible combinations of parameters
    params = [(url, qps, timeout, duration) for url in urls for qps in qpss for timeout in timeouts for duration in durations]

    results = ['URL', 'QPS', 'Timeout', 'Duration', 'Total Requests', 'Successful Requests', 'Failed Requests', '% Successful Requests', 'Average Latency (ms)', 'Error Code Count', 'Top Errors']
    
    for url, qps, timeout, duration in params:
        print(f"Testing URL: {url}, QPS: {qps}, Timeout: {timeout}, Duration: {duration}")
        benchmark = HTTPBenchmark(url, qps, timeout)
        benchmark.start_test(duration)
        results.append(benchmark.get_results())
        
    # Save results to a CSV file
    with open('results.csv', 'w') as f:
        for result in results:
            f.write(f"{result}\n")

    