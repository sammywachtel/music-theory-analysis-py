# PyPI Publishing Setup Guide

This guide explains how to set up automatic PyPI publishing for the harmonic-analysis library.

## 📋 Prerequisites

### 1. PyPI Account Setup

**Main PyPI (for stable releases):**
1. Go to [https://pypi.org/account/register/](https://pypi.org/account/register/)
2. Create an account with your email
3. Verify your email address

**Test PyPI (for testing releases):**
1. Go to [https://test.pypi.org/account/register/](https://test.pypi.org/account/register/)
2. Create a separate account (can use same email)
3. Verify your email address

### 2. Generate API Tokens

**For PyPI:**
1. Log into [https://pypi.org](https://pypi.org)
2. Go to Account Settings → API tokens
3. Click "Add API token"
4. Name: `harmonic-analysis-github-actions`
5. Scope: Select "Entire account" (for first publication) or "harmonic-analysis" project (after first upload)
6. **Copy the token immediately** (starts with `pypi-`)

**For Test PyPI:**
1. Log into [https://test.pypi.org](https://test.pypi.org)
2. Follow same steps as above
3. Name: `harmonic-analysis-github-test`
4. **Copy the token immediately** (starts with `pypi-`)

### 3. Configure GitHub Secrets

In your GitHub repository:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add these secrets:

**Secret Name:** `PYPI_API_TOKEN`  
**Value:** `pypi-AgE...` (the full token from PyPI)

**Secret Name:** `TEST_PYPI_API_TOKEN`  
**Value:** `pypi-AgE...` (the full token from Test PyPI)

## 🚀 How It Works

### Automatic Publishing Triggers

The workflow automatically publishes when:

1. **Version tags are pushed:**
   ```bash
   git tag v0.2.0
   git push origin v0.2.0
   ```

2. **GitHub releases are published:**
   - Create release through GitHub UI
   - Workflow triggers automatically

### Publishing Logic

- **Release Candidates/Beta/Alpha** → Test PyPI
  - Tags like `v0.2.0rc1`, `v1.0.0beta1`, `v2.0.0alpha1`
  - Install with: `pip install -i https://test.pypi.org/simple/ harmonic-analysis`

- **Stable Releases** → PyPI
  - Tags like `v0.2.0`, `v1.0.0`, `v2.1.3`
  - Install with: `pip install harmonic-analysis`

## 🔧 Manual Publishing (Backup Method)

If you need to publish manually:

```bash
# Build the package
python -m build

# Check the package
python -m twine check dist/*

# Upload to Test PyPI
python -m twine upload --repository testpypi dist/*

# Upload to PyPI
python -m twine upload dist/*
```

## 📝 First Time Setup Checklist

- [ ] Create PyPI account
- [ ] Create Test PyPI account  
- [ ] Generate PyPI API token
- [ ] Generate Test PyPI API token
- [ ] Add `PYPI_API_TOKEN` to GitHub secrets
- [ ] Add `TEST_PYPI_API_TOKEN` to GitHub secrets
- [ ] Test with a release candidate tag
- [ ] Verify package appears on Test PyPI
- [ ] Create stable release
- [ ] Verify package appears on PyPI

## 🎯 Testing the Setup

1. **Test with Release Candidate:**
   ```bash
   git tag v0.2.0rc2
   git push origin v0.2.0rc2
   ```
   - Should publish to Test PyPI
   - Check: https://test.pypi.org/project/harmonic-analysis/

2. **Test Installation:**
   ```bash
   pip install -i https://test.pypi.org/simple/ harmonic-analysis==0.2.0rc2
   ```

3. **Create Stable Release:**
   ```bash
   git tag v0.2.0
   git push origin v0.2.0
   ```
   - Should publish to PyPI
   - Check: https://pypi.org/project/harmonic-analysis/

## 🚨 Security Notes

- **Never commit API tokens** to the repository
- **Use repository secrets** for all sensitive data
- **Regenerate tokens** if they're ever exposed
- **Use scoped tokens** when possible (project-specific vs account-wide)

## 📞 Support

If you encounter issues:

1. **Check GitHub Actions logs** for detailed error messages
2. **Verify tokens** are correctly set in repository secrets
3. **Test manually** using `twine` commands above
4. **Check PyPI project permissions** if using scoped tokens

## 🎉 Success!

Once configured, every tagged release will automatically:
- ✅ Build the package
- ✅ Run quality checks
- ✅ Publish to appropriate PyPI (test or production)
- ✅ Make the package available via `pip install`

**Next release will be automatically available for pip installation!**