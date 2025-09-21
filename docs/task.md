# Assignment: LEI Issuer Fetcher & Cache Service (Python)

## Task
Write a Python application/service that:
1. Fetches LEI Issuers from the given GLEIF API endpoint, handling pagination.
2. Parses the JSON and extracts, for each issuer, at least these fields:

* LEI code
* Issuer name
* Country of the issuer
* Any other field you find relevant

3. Implements a caching mechanism so that repeated requests for the same page
number + size do not re-fetch from the API if done within a certain time window.
4. Supports (or is architected so it could support) concurrent fetching of multiple
pages in parallel. For example, being able to fetch pages 1, 2, 3 at the same time.

## Constraints
- Create a public Github repository and share it.
- Create a Readme.md that documents how to run and test the application.
- Include any assumptions made in the design in the Readme.md

## [API Reference](https://api.gleif.org/api/v1/lei-issuers?page%5Bnumber%5D=1&page%5Bsize%5D=10) This is a paginated endpoint returning LEI Issuer data (10 items per page, page 1 in this
example).
