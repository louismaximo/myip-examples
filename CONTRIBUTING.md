# Contributing to MyIP.foo Examples

Thank you for your interest in contributing! We welcome contributions from the community.

## How to Contribute

### Adding New Examples

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/add-rust-example
   ```
3. **Add your example**
   - Create a new file in the appropriate directory (`examples/python/`, `examples/bash/`, etc.)
   - Include comments explaining what the code does
   - Ensure code follows language best practices
   - Test your example to ensure it works
4. **Update README.md** if needed
5. **Commit your changes**
   ```bash
   git commit -m "Add Rust async example for IP lookup"
   ```
6. **Push to your fork**
   ```bash
   git push origin feature/add-rust-example
   ```
7. **Open a Pull Request**

### Example Guidelines

**Good examples:**
- ✅ Clear, well-commented code
- ✅ Follow language conventions and best practices
- ✅ Include error handling where appropriate
- ✅ Demonstrate a specific use case
- ✅ Work with the latest stable language version

**Avoid:**
- ❌ Overly complex or unreadable code
- ❌ Including personal credentials or API keys
- ❌ Examples that violate myip.foo's Terms of Service

### Code Style

- **Python:** Follow PEP 8
- **JavaScript:** Use ES6+ syntax
- **Bash:** Follow Google Shell Style Guide
- **Go:** Use `go fmt`
- **Rust:** Use `rustfmt`

### Reporting Issues

Found a bug or have a suggestion? [Open an issue](https://github.com/virtualox/myip-examples/issues) with:
- Clear title and description
- Steps to reproduce (if bug)
- Expected vs actual behavior
- Environment details (OS, language version)

### Questions?

Not sure if your contribution fits? Open an issue and ask! We're happy to help.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
