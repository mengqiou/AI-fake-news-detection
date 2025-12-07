# Backend Documentation

Comprehensive documentation for the AI fake news detection agent system.

## Documents

### `platform_verification.md`
**How the verification platform works**

- Architecture and workflow
- Example scenarios (claims found/not found)
- Integration with social media platforms
- Customizing the verification database
- Production implementation guide

**Read when:**
- Understanding the "given platform" concept
- Implementing platform integrations
- Connecting to real fact-checking APIs

---

### `testing_guide.md`
**Quick testing reference**

- Fast testing commands
- Expected results
- Troubleshooting guide
- Performance tips
- Cost estimation

**Read when:**
- Quick reference for testing
- Need fast troubleshooting
- First time testing

**Note:** For comprehensive testing docs, see `tests/README.md`

---

## Other Documentation Locations

- **Main README**: `/README.md` - Project overview and quick start
- **Config Guide**: `configs/README.md` - Configuration templates
- **Setup Guide**: `setup/README.md` - Setup and verification tests
- **Tests Guide**: `tests/README.md` - Integration testing (most comprehensive)
- **Utils Guide**: `app/utils/README.md` - Utility functions
- **Examples**: `examples/README.md` - Code examples

## Documentation Philosophy

- **README files**: Quick reference, how-to guides
- **Code docstrings**: API documentation, function-level
- **Examples**: Working code demonstrating concepts
- **Markdown docs** (`docs/`): Conceptual explanations, architecture

## Contributing Documentation

When adding new features:

1. **Update relevant README** - Add to appropriate section
2. **Add docstrings** - Document all public functions
3. **Create example** (optional) - If complex feature
4. **Update main README** - If significant feature

Keep docs close to code when possible (README in same directory).
