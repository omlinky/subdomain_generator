import argparse
import re
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm


lock = threading.Lock()


def main():
    parser = argparse.ArgumentParser(description='Generate subdomains for a domain')
    parser.add_argument('domain', type=str, help='The domain name or file containing domain names')
    parser.add_argument('wordlist', type=str, help='The file containing the wordlist')
    parser.add_argument('--regex', type=str, help='The regex string to filter the wordlist')
    parser.add_argument('--level', type=int, default=3, help='The level of recursion to use')
    parser.add_argument('--workers', type=int, default=10, help='The number of workers to use')
    parser.add_argument('--output', type=str, default='output.txt', help='The output file')
    args = parser.parse_args()

    domains = get_domains(args.domain)
    words = get_words(args.wordlist, args.regex)
    subdomains = set()

    for domain in domains:
        for i in range(args.level):
            for word in words:
                subdomain = word + '.' + domain
                subdomains.add(subdomain)
                for j in range(i):
                    subdomain = word + '.' + subdomain
                    subdomains.add(subdomain)

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = [executor.submit(process_subdomain, subdomain, args.output) for subdomain in subdomains]

        for _ in tqdm(as_completed(futures), total=len(futures), desc='Generating subdomains', unit=' subdomain'):
            pass


def process_subdomain(subdomain, output_file):
    with lock, open(output_file, 'a') as f:
        f.write(subdomain + '\n')


def get_domains(domain):
    if not is_file(domain):
        return [domain]

    with open(domain, 'r') as f:
        return [line.strip() for line in f.readlines() if line.strip()]


def get_words(wordlist, regex=None):
    with open(wordlist, 'r') as f:
        words = {line.strip() for line in f.readlines()}

    if regex is not None:
        pattern = re.compile(regex)
        return {word for word in words if pattern.match(word)}

    return words


def is_file(path):
    return '.' in path and path.rsplit('.', 1)[1].lower() in ['txt', 'csv']


if __name__ == '__main__':
    main()
