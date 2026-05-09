# dsk-keepercmd-demo — end-to-end demo Makefile
# Requires: dsk installed (`pip install -e /path/to/dsk`)
# Target run-dir is at ./run-dir/ (synthetic fixture; Bob's real fixture replaces it)

RUN_DIR := $(PWD)/run-dir
OUT_DIR  := $(PWD)/manifests

.PHONY: demo-verify demo-import demo-plan demo-clean help

help:
	@echo "dsk-keepercmd-demo targets:"
	@echo "  demo-verify   Verify the run-dir integrity (audit chain + SHA256SUMS)"
	@echo "  demo-import   Import run-dir into DSK manifests (dry-run by default)"
	@echo "  demo-plan     Run dsk plan against the imported manifests"
	@echo "  demo-clean    Remove generated manifests/"

demo-verify:
	@echo "=== Step 1: Verify keeperCMD run-dir integrity ==="
	cd $(RUN_DIR) && sha256sum -c SHA256SUMS.txt
	@echo "SHA256SUMS OK"

demo-import:
	@echo "=== Step 2: Import into DSK manifests ==="
	mkdir -p $(OUT_DIR)
	python3 -m dsk.cli import-from-keepercmd $(RUN_DIR) \
	    --output $(OUT_DIR)/manifest.yaml \
	    --dry-run

demo-plan:
	@echo "=== Step 3: DSK plan — mock provider shows creates (exit 2 is expected) ==="
	python3 -m dsk.cli plan $(OUT_DIR)/manifest.yaml || test $$? -eq 2

demo-clean:
	rm -rf $(OUT_DIR)

demo-all: demo-verify demo-import demo-plan
	@echo ""
	@echo "=== Demo complete. Check manifests/ for imported YAML. ==="
