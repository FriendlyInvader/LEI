
import time
from src.LEIReader import LEIReader

def test_fetch_page():
	# GIVEN
	reader = LEIReader()
	# WHEN
	result = reader.fetch_page(page=1, size=5)
	# THEN
	assert isinstance(result, dict)
	assert "data" in result
	assert isinstance(result["data"], list)
	assert len(result["data"]) == 5
	# for item in result["data"]:
	# 	print(item)
	# assert False, "X"

def test_fetch_cache():
	# GIVEN
	reader = LEIReader()
	# WHEN
	result = reader.fetch_cache(page=1, size=5)
	# THEN
	assert isinstance(result, dict)
	assert "data" in result
	assert isinstance(result["data"], list)
	assert len(result["data"]) == 5
	# for item in result["data"]:
	# 	print(item)
	# assert False, "X"

def test_extract_issuers_with_the_same_page_and_size():
	# GIVEN
	reader = LEIReader(window=10.0)
	# WHEN - first call should be slow
	start = time.perf_counter()
	result = reader.extract_issuers(1, 7)
	end = time.perf_counter()
	x1 = end-start
	assert isinstance(result, list)
	assert len(result) == 7
	# AND - second call should be faster due to caching
	start = time.perf_counter()
	result = reader.extract_issuers(1, 7)
	end = time.perf_counter()
	# THEN
	x2 = end-start
	assert x2 < x1/10
	# WHEN
	time.sleep(7) # wait for cache to expire
	start = time.perf_counter()
	result = reader.extract_issuers(1, 7)
	end = time.perf_counter()
	x3 = end-start
	# THEN - third call should be similar to the first call
	assert x2 < x3/10
	
def test_extract_issuers_with_diffrent_page_and_size():
	# GIVEN
	reader = LEIReader(window=10.0)
	# WHEN - first call should be slow
	start = time.perf_counter()
	result = reader.extract_issuers(1, 7)
	end = time.perf_counter()
	x1 = end-start
	assert isinstance(result, list)
	assert len(result) == 7
	# AND - second call should be faster due to caching
	start = time.perf_counter()
	result = reader.extract_issuers(2, 8)
	end = time.perf_counter()
	# THEN
	assert len(result) == 8
	x2 = end-start
	assert (x2 - x1) < 4 # both calls should not be cached

def test_extract_issuers_concurrent():
	# GIVEN
	reader = LEIReader(window=10.0)
	# WHEN
	result = reader.extract_issuers_concurrent([(1, 7), (2, 8)])
	# THEN
	assert len(result) == 15
	# for r in result:
	# 	print(r)
	# assert False, len(result)

