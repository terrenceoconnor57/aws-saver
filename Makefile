.PHONY: install fmt lint typecheck test clean fix-colima clean_dist build_lambda_scan_ebs tf_init tf_plan tf_apply tf_destroy

install:
	pip install -e ".[dev]"

fmt:
	ruff format src tests
	ruff check --fix src tests

lint:
	ruff check src tests

typecheck:
	mypy src tests

test:
	pytest tests/ -v

test_ec2:
	pytest -k ec2_unattached -q

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

clean_dist:
	rm -rf dist/

build_lambda_scan_ebs: clean_dist
	@echo "Building Lambda artifact for scan_ec2_unattached_ebs..."
	@mkdir -p dist/build
	@cp -r src/lambdas/scan_ec2_unattached_ebs dist/build/
	@cp -r src/saverbot dist/build/
	@find dist/build -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find dist/build -type f -name "*.pyc" -delete 2>/dev/null || true
	@cd dist/build && zip -r ../scan_ec2_unattached_ebs.zip . -x "*.pyc" "*__pycache__*"
	@rm -rf dist/build
	@echo "✓ Created dist/scan_ec2_unattached_ebs.zip"

fix-colima:
	./fix-colima.sh

tf_init:
	cd infra/terraform && terraform init -input=false

tf_plan:
	cd infra/terraform && terraform plan -var-file=terraform.tfvars -input=false

tf_apply:
	cd infra/terraform && terraform apply -auto-approve -var-file=terraform.tfvars

tf_destroy:
	cd infra/terraform && terraform destroy -auto-approve -var-file=terraform.tfvars

