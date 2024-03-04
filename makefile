clean: 
	find . | grep -E "(__pycache__|\.pyc$$)" | xargs rm -rf

test-domain-dataset:
	echo "Testing Datasets Domain" && \
		poetry run pytest src/common/domains/datasets

test-domains:
	test-domain-dataset

test:
	poetry run pytest

