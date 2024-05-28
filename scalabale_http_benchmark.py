"""
Python script to run N number of scalable HTTP benchmarks using
- Nginx
- docker-compose

"""

import sys
import os
import argparse

def generate_nginx_conf(n:int) -> None:
    """
    Generate Nginx configuration file for N number of worker nodes to be load balanced
    Inputs:
    - n (int): Number of worker nodes
    """
    servers = "\n".join([f"server benchmark:80;" for i in range(1, n+1)])
    with open('nginx.conf.template', 'r') as template_file:
        template = template_file.read()
    config = template.replace('{{servers}}', servers)
    with open('nginx.conf', 'w') as config_file:
        config_file.write(config)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Scalable HTTP benchmarks')
    parser.add_argument('--nodes', '-n', help='Number of worker nodes', required=True, type=int)

    args = parser.parse_args()
    generate_nginx_conf(args.nodes)

    # Run docker-compose build
    print("Building docker images...")
    os.system('docker-compose build')

    # Run docker-compose up
    print("Starting benchmarks...")
    os.system(f'docker-compose up --scale benchmark={args.nodes}')