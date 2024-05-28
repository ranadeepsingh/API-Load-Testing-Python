## About
HTTP load-testing and benchmarking library for testing the performance of a given URL. The library generates requests at a given fixed QPS and reports latencies, error rates, and common errors.

**Output Example:**
```bash
docker run -it --name http-benchmark --rm http-benchmark python http_benchmark.py --url fireworks.ai --qps 100 --timeout 20 --duration 10
```
![Output Example Schreenshot](output_example.png)

## Setup

### Docker Compose Setup
1. Start Docker Desktop/Docker Daemon \
Optional: [Install Docker Desktop](https://www.docker.com/get-started/)
2. Self Sign SSL Certificate to test HTTPS
```bash
mkdir -p certs
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout certs/nginx.key -out certs/nginx.crt -subj "/CN=localhost"
```

3. Use Python heklper script to run benchmarking with N number of load-balanced docker containers
```bash
python scalabale_http_benchmark.py --nodes 4
```

*Alternatively*, you can use the run 
3. Build Docker Compose
```bash
docker-compose build
```
3. Run Docker Compose with default params
```bash
docker-compose up
```
4. Run Docker Compose with custom params
```bash
docker-compose run http-benchmark python http_benchmark.py --url fireworks.ai --qps 100 --timeout 20 --duration 10
```


### Individual Docker Setup
1. Start Docker Desktop/Docker Daemon \
Optional: [Install Docker Desktop](https://www.docker.com/get-started/)

2. Build Docker Image
```bash
docker build -t http-benchmark --rm .
```

3. Run Docker Image with default params
```bash
docker run -it --name http-benchmark --rm http-benchmark
```

4. Run Docker Image with custom params
```bash
docker run -it --name http-benchmark --rm http-benchmark python http_benchmark.py --url fireworks.ai --qps 100 --timeout 20 --duration 10
```

### Local Env Setup

1. Conda env setup
```bash
conda create -n http_testing python=3.11
conda activate http_testing
pip install -r requirements.txt
```

2. Usage
```bash
python http_benchmark.py --url fireworks.ai --qps 100 --timeout 20 --duration 10
```

## Usage Parameters
1. -u, --url: URL to test.
2. -q, --qps: Queries per second to send. Default 10
3. -t, --time: Timeout of HTTP/HTTPS request in seconds. Default 10
4. -d, --duration: Duration of the test in seconds. Default 10

## File Structure
1. `http_benchmark.py`: Main file to run the load testing and contains the HTTPBenchmark class
2. `Dockerfile`: Dockerfile to build the docker image
3. `docker-compose.yml`: Docker Compose file to run the benchmarking with multiple containers
4. `scalabale_http_benchmark.py`: Python helper script to run benchmarking with N number of load-balanced docker containers
5. `requirements.txt`: Python dependencies
6. `results.csv`: CSV file to store the results of the benchmarking

## Future Improvements
1. Add observability metrics support though Prometheus and Grafana
2. Add support for custom headers and body in the request
3. Write lower level code in C++/Go for better load testing performance


## By
- Author: Ranadeep Singh
- Email: ranadeep.dtu@gmail.com