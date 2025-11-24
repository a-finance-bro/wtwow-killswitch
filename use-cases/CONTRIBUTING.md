# Contributing Use Cases

Thank you for your interest in contributing to WTWOW Universal KillSwitch!

## How to Add a New Sequence

### 1. Choose the Right Directory
- **macOS-only sequences**: `use-cases/macos/`
- **Windows-only sequences**: `use-cases/windows/`
- **Linux-only sequences**: `use-cases/linux/`
- **Cross-platform sequences**: `use-cases/cross-platform/`

### 2. File Naming Convention
Use descriptive names with underscores:
- Good: `example_send_email.md`, `example_clear_clipboard.md`
- Bad: `mysequence.md`, `seq1.md`

### 3. File Format
Each use-case file should be a Markdown file with:

```markdown
# Title: Brief Description

Brief explanation of what this sequence does and why it's useful.

## Installation

Explain how to add this to sequences.py

## Code

\```python
def my_custom_sequence():
    """Docstring explaining the function."""
    # Your code here
    pass

# Add to SEQUENCES dictionary:
# "My Custom Sequence": my_custom_sequence
\```

## Dependencies (if any)

List any additional pip packages or system dependencies.

## Notes

Any important warnings, limitations, or usage tips.
```

### 4. Safety Guidelines
- **DO NOT** submit sequences that:
  - Destroy user data without explicit warning
  - Contain malicious code
  - Violate privacy or security best practices
  
- **DO** submit sequences that:
  - Are well-documented
  - Handle errors gracefully
  - Include appropriate warnings for destructive actions

### 5. Testing
- Test your sequence on your target platform
- Ensure it doesn't interfere with system stability
- Verify it works when the USB is actually removed

### 6. Pull Request
- Fork the repository
- Add your sequence file to the appropriate directory
- Submit a PR with a clear description
- Tag it appropriately (e.g., `use-case`, `macos`, `windows`, etc.)

## Examples
See the existing examples in each directory for reference.

## Questions?
Open an issue on GitHub if you need help!
