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
    
    urls = ['fireworks.ai', 'vercel.com', 'cupidgpt.ai']
    qpss = [1, 10, 100, 1000]
    timeouts = [10, 60]
    durations = [5, 30, 60]

    # urls = ['fireworks.ai']
    # qpss = [1]
    # timeouts = [10, 60]
    # durations = [5]

    # List of all possible combinations of parameters
    params = [(url, qps, timeout, duration) for qps in qpss for timeout in timeouts for duration in durations for url in urls]

    results = []

    with open('results.csv', 'w') as f:
        f.write(','.join(['URL', 'QPS', 'Timeout', 'Duration', 'Actual QPS', 'Num Requests', 'Num Successful', 'Num Failed', 'Error Rate %', 'Average Latency (ms)', 'Max Latency (ms)', 'Min Latency (ms)', 'Error Count', 'Top Errors']) + '\n')
    
        for url, qps, timeout, duration in params:
            print(f"Testing URL: {url}, QPS: {qps}, Timeout: {timeout}, Duration: {duration}")
            benchmark = HTTPBenchmark(url, qps, timeout)
            benchmark.start_test(duration)
            results.append(benchmark.get_results())
            f.write(f"{','.join(map(str,results[-1]))}\n")
            # Sleep for 10 sec between tests
            time.sleep(10)
    
            

    