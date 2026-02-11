# Anonymity Checklist

Before uploading to anonymous repository, verify:

## ✅ Files Checked

- [x] `README.md` - Author: "Anonymous Authors" ✓
- [x] `LICENSE` - Copyright: "Anonymous Authors" ✓
- [x] `setup.py` - Author/Email: Anonymous ✓
- [x] `.gitignore` - Excludes personal data ✓
- [x] All code files - No personal names in comments ✓
- [x] All code files - No institutional references ✓

## ⚠️ Additional Checks Required

### 1. Remove Git History (if any)
```bash
rm -rf .git
git init
git add .
git commit -m "Initial anonymous submission"
```

### 2. Check for Embedded Metadata
```bash
# Search for potential author names (replace with your actual name patterns)
grep -r "your_name" .
grep -r "your_university" .
grep -r "your_email" .
```

### 3. Clean API Keys
```bash
# Ensure no API keys in code
grep -r "sk-" . --exclude-dir=venv
grep -r "api_key" . --exclude-dir=venv
```

### 4. Remove Cached Data
```bash
find . -name "__pycache__" -type d -exec rm -rf {} +
find . -name "*.pyc" -delete
```

## 📋 Upload Checklist

Before uploading to anonymous.4open.science or similar:

- [ ] Run anonymity checks above
- [ ] Test that `pip install -e .` works
- [ ] Verify `run_experiment.py` runs without errors (even with placeholders)
- [ ] Check all file paths are relative (no absolute paths with usernames)
- [ ] Confirm README accurately describes what's included vs. simplified
- [ ] Double-check LICENSE year and "Anonymous" attribution
- [ ] Remove any experimental outputs (CSV, JSON results)
- [ ] Verify no `.env` files with real API keys

## 🔒 What's Protected

Remind yourself what's intentionally simplified/omitted:

1. **Complete PCC prompts** - Structure shown, exact wording in paper
2. **PDS case formatting** - Framework shown, specific techniques in paper
3. **M-layer 9-bucket descriptions** - Simplified to 3-level in code
4. **Hyperparameter tuning logs** - Final values in paper, tuning process private
5. **Analysis scripts** - Not included (post-acceptance release)

## ✅ Final Verification

Run this command to double-check no sensitive info:
```bash
grep -rni "TODO\|FIXME\|XXX\|HACK" public_release/ --exclude-dir=venv
```

If any TODOs reference specific people/places, remove them.

---

**Ready for upload when all boxes checked!**
