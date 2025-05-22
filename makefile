lintfix:
	black .
	isort .
	autoflake --remove-all-unused-imports --remove-unused-variables --in-place -r .