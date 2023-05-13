# Simple Python subdomain generator
# Generate list of subdomain combinations

To generate the list of subdomain combinations the script uses an exist wordlist file of subdomains in a same folder.

The list of subdomains can be found here
```sh
https://github.com/rbsec/dnscan
```

-l parameter uses to generate all subdomain combinations up to the specified level.

## Requirements:

- Python 3
- tqdm

## Install requirements
```sh
pip3 install tdqm
```

## General usage options
```sh
  -d string
        Input domain
  -df string
        Input domain file, one domain per line
  -l int
        Subdomain level to generate (default 1)
  -o string
        Output file (stdout will be used when omitted)
  -r string
        Regex to filter words from wordlist file
  -silent
        Skip writing generated subdomains to stdout (faster) (default true)
  -t int
        Number of threads for every subdomain level (default 100)
  -w string
        Wordlist file
```

## Simple command to use
```sh
python3 subdomain_generator.py example.com wordlist.txt --regex '^[a-z]+$' --level 3 --workers 10 --output output.txt
```
