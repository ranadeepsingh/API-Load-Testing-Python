"""
Python scipt to tun HTTP latencies and error rates
Python: 3.11.9
Packages: requirements.txt

Author: Ranadeep Singh
Email: ranadeep.dtu@gmail.com
"""

from collections import Counter
import time

# To pass command line arguments
import argparse

# Send HTTP/HTTPS requests
import requests

# Async HTTP/HTTPS requests
import asyncio
import aiohttp



class HTTPBenchmark:
    """
    Class to perform HTTP benchmarks on a target URL
    """

    def __init__(self, url:str, qps: int=10, timeout: int=10) -> None:
        """
        Initialize the HTTPBenchmark object with the target URL and QPS
        Inputs:
        - url: The URL to test
        - qps: The number of requests per second to send. Default: 10
        - timeout: The timeout duration of each request in seconds. Default: 10
        """

        self.url = url
        # If url does not start with http:// or https://, add http://
        if not self.url.startswith('http://') and not self.url.startswith('https://'):
            self.url = 'http://' + self.url
        self.qps = qps 
        self.timeout = timeout
        # Tests to ensure the URL is valid
        self.__test_url__(url)
        # Asserts to ensure QPS and Timeout are positive integers
        assert qps > 0, "QPS must be a positive integer"
        assert timeout > 0, "Timeout must be a positive integer"
        
        self.__reset_results__()

    def __reset_results__(self) -> None:
        """
        Reset the results of the test
        """
        self.results =  {
                'start_time': None,
                'end_time': None,
                'total_requests': 0,
                'successful_requests': 0,
                'failed_requests': 0,
                'latencies': [],
                'error_code_count': {}, # Error code and their counts, if any
            }
        
    def __test_url__(self, url) -> None:
        """
        Test the URL to ensure it is valid
        """
        try:
            response = requests.head(url)
            response.raise_for_status()
        except Exception as e:
            raise f"Invalid URL: {str(e)}"

    def __str__(self) -> str:
        """
        Return a string representation of the test
        """
        return f"HTTP Benchmark: {self.url} @ {self.qps} qps"
    
    def __repr__(self) -> str:
        """
        Return a string representation of the test
        """
        return self.__str__()

    def pretty_print_results(self) -> None:
        """
        Pretty print the results of the test
        Print in tabular format:
        -------
        | Config: |
        -------
        |   URL: http://example.com |
        -------
        |   QPS: 10 |
        -------
        |   Timeout: 10 seconds |
        -------
        | Results: |
        -------
        |   Duration: 10 seconds |
        -------
        |   Achived QPS: 10.0 |
        -------
        |   Num Requests: 100 |
        -------
        |   Num Successful Requests: 90 |
        -------
        |   Num Failed Requests: 10 |
        -------
        |   % Successful Requests: 90.0 |
        -------
        |   Average Latency (ms): 100.0 |
        -------
        | Top 3 Error Codes: |
        -------
        |   404: 5 |
        -------
        |   Timeout: 3 |
        -------
        """
        
        ret_parts = [
            "Config:",
            f"  URL: {self.url}",
            f"  QPS: {self.qps}",
            f"  Timeout: {self.timeout} seconds",
            "Results:",
            f"  Duration: {round(self.results['end_time'] - self.results['start_time'],1)} seconds",
            f"  Achived QPS: {round(self.results['total_requests']/(self.results['end_time'] - self.results['start_time']),2)}",
            f"  Num Requests: {self.results['total_requests']}",
            f"  Num Successful Requests: {self.results['successful_requests']}",
            f"  Num Failed Requests: {self.results['failed_requests']}",
            f"  % Successful Requests: {round(self.results['successful_requests']/self.results['total_requests']*100,2) if self.results['total_requests'] else None}",
            f"  Average Latency (ms): {round(sum(self.results['latencies'])/len(self.results['latencies'])*1000,2) if self.results['latencies'] else None}"
        ]
        # Add optional error code count if present
        if self.results['error_code_count']:
            top_k = min(3, len(self.results['error_code_count']))
            ret_parts.append(f"Top Errors:")
            sorted_error_codes = sorted(self.results['error_code_count'].items(), key=lambda x: x[1], reverse=True)[:top_k]
            for code, count in sorted_error_codes:
                ret_parts.append(f"  {code}: {count}")

        # Use max_len of parts to format the output table's length
        max_len = max(len(part) for part in ret_parts)

        # Create table
        line_sep = '\n' + '-' * (max_len+4) + '\n'
        table_lines = [ '| ' + part + ' '*(max_len-len(part)+1) + '|' for part in ret_parts]

        table = line_sep + line_sep.join(table_lines) + line_sep

        print(table)

    async def send_request(self, session: aiohttp.ClientSession, url: str, timeout: int=10) -> tuple:
        """
        Asynchronously send an HTTP request to the target URL with a default timeout
        Inputs:
        - session: The aiohttp ClientSession object
        - url: The URL to send the request to
        - timeout: The timeout duration of the request in seconds. Default: 10
        """
        start_time = time.time()
        try:
            async with session.get(url, timeout=timeout) as response:
                await response.read()  # Ensure the whole response is fetched
                return time.time() - start_time, response.status
        # except Exception as e:
        #     return time.time() - start_time, str(e)  # Capture and return exception message
        except aiohttp.ClientResponseError as e:
            # This exception type includes cases where the HTTP request returns an error status (e.g., 404, 500)
            return time.time() - start_time, e.status
        except aiohttp.ClientError as e:
            # Generic client errors in aiohttp, handling without a status code
            return time.time() - start_time, f"ClientError: {str(e)}"
        except asyncio.TimeoutError:
            # Handle timeouts specifically
            return time.time() - start_time, "Timeout"
        except Exception as e:
            # Catch-all for any other exceptions that may occur
            return time.time() - start_time, f"Other: {str(e)}"

    async def load_test(self, duration: int) -> None:
        """
        Asynchronously load the test for the specified duration
        Inputs:
        - duration: The duration of the test in seconds
        """
        tasks = []
        total_requests = self.qps * duration
        interval = 1 / self.qps  # Interval to maintain requests per second

        async with aiohttp.ClientSession() as session:
            self.results['start_time'] = start_time = time.time()
            while time.time() - start_time <= duration:
                task = asyncio.create_task(self.send_request(session, self.url, self.timeout))
                tasks.append(task)
                await asyncio.sleep(interval)  # Wait for the next request slot
            self.results['end_time'] = time.time()

            results = await asyncio.gather(*tasks, return_exceptions=True)  # Wait for all tasks to complete

        # Update the results
        
        self.results['total_requests'] = len(results)
        self.results['successful_requests'] = sum(1 for _, status in results if status == 200)
        self.results['failed_requests'] = len(results) - self.results['successful_requests']
        self.results['latencies'] = [latency for latency, status in results if status == 200]
        self.results['error_code_count'] = Counter([status for _, status in results if status != 200])    

    def start_test(self, duration: int=10, verbose: bool=True) -> None:
        """
        Start the test for the specified duration
        Inputs:
        - duration: The duration of the test in seconds
        - verbose: Whether to print the results
        """
        # Asserts to ensure duration is a positive integers
        assert duration > 0, "Duration must be a positive integer"

        self.__reset_results__()
        asyncio.run(self.load_test(duration))

        # Print the results
        if verbose:
            self.pretty_print_results()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run HTTP benchmarks')
    parser.add_argument('--url', '-u', help='The URL to test', required=True, type=str)
    parser.add_argument('--qps', '-q', help='The number of requests per second to send', default=10, type=int)
    parser.add_argument('--timeout', '-t', help='The timeoput duration of per request in seconds', default=10, type=int)
    parser.add_argument('--duration', '-d', help='The duration of of the benchmarking test in seconds', default=10, type=int)
    args = parser.parse_args()

    benchmark = HTTPBenchmark(args.url, args.qps, args.timeout)
    benchmark.start_test(args.duration)