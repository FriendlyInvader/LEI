# Task


## 1. Install packages

~~~bash
pip install -r requirements.txt
~~~

## 2. Run tests

~~~bash
python -m pytest
~~~

## 3. The tests reprresents tasks

### 3.1 Task 1. Fetches LEI Issuers from the given GLEIF API endpoint, handling pagination

Please refer to **test_fetch_page** test in **test\LEIReader_test.py**

~~~python
def test_fetch_page():
	# GIVEN
	reader = LEIReader()                        # LINE 0
	result = reader.fetch_page(page=1, size=5)  # LINE 1
	assert len(result["data"]) == 5
~~~

**Line 0** creates LEI reader with default API endpoint, see **LEIReader.DEFAULT_ROOT** constant in **src\LEIReader.py** file for default GLEIF API endpoint. Please pass alternative GLEIF API endpoint as the first parameter of constructor of **LEIReader** class.

**Line 1** fetches issuers handling page number and page size.

### 3.2 Task 2. Parses the JSON and extracts, for each issuer

Please refer to **test_fetch_page** test in **test\LEIReader_test.py**

~~~python
def test_fetch_page():
	# GIVEN
	reader = LEIReader()                        # LINE 0
	result = reader.fetch_page(page=1, size=5)  # LINE 1
	assert len(result["data"]) == 5
~~~

**Line 1** delivers list of issuers. Each issuer has **code**, **name**, and **country_code** properties. Please look at **src\issuer.py** code.

### 3.3 Task 3. Implements a caching mechanism so that repeated requests for the same page number + size do not re-fetch from the API if done within a certain time window

Please refer to **test_extract_issuers_with_the_same_page_and_size** test in **test\LEIReader_test.py**

~~~python
def test_extract_issuers_with_the_same_page_and_size():
	# GIVEN
	reader = LEIReader(window=10.0)
	# WHEN - first call should be slow
	start = time.perf_counter()
	result = reader.extract_issuers(1, 7)   # LINE 0
	end = time.perf_counter()
	x1 = end-start
	assert isinstance(result, list)
	assert len(result) == 7
	# AND - second call should be faster due to caching
	start = time.perf_counter()
	result = reader.extract_issuers(1, 7)   # LINE 1
	end = time.perf_counter()
	# THEN
	x2 = end-start
	assert x2 < x1/10                       # LINE 1.1
	# WHEN
	time.sleep(7) # wait for cache to expire # LINE 2.1
	start = time.perf_counter()
	result = reader.extract_issuers(1, 7)   # LINE 2
	end = time.perf_counter()
	x3 = end-start
	# THEN - third call should be similar to the first call
	assert x2 < x3/10
~~~

**Line 0** requests page 1 size 7.

**Line 1** requests page 1 size 7. The result should be fetched from cache. See **LINE 1.1**.

**Line 2** requests page 1 size 7. But the cache of the page should be invalidated and requested again from API. see **LINE 2.1**

Additionally see **test_extract_issuers_with_diffrent_page_and_size** test in **test\LEIReader_test.py**

### 3.4 Task 4. Supports (or is architected so it could support) concurrent fetching of multiple pages in parallel. For example, being able to fetch pages 1, 2, 3 at the same time

Please refer to **test_extract_issuers_concurrent** test in **test\LEIReader_test.py**

~~~python
def test_extract_issuers_concurrent():
	# GIVEN
	reader = LEIReader(window=10.0)
	# WHEN
	result = reader.extract_issuers_concurrent([(1, 7), (2, 8)])    # LINE 0
	# THEN
	assert len(result) == 15
~~~

**Line 0** requests two pages (1,7) and (2,8) concurently.
