```markdown
# hodie Development Patterns

> Auto-generated skill from repository analysis

## Overview
This skill teaches you the core development patterns and conventions used in the `hodie` Python repository. You'll learn how to structure files, write imports and exports, and follow commit and testing practices. This guide is ideal for contributors seeking to maintain consistency and quality in the codebase.

## Coding Conventions

### File Naming
- Use **snake_case** for all file names.
  - Example: `user_profile.py`, `data_loader.py`

### Import Style
- Use **relative imports** within the package.
  - Example:
    ```python
    from .utils import parse_date
    from .models import User
    ```

### Export Style
- Use **named exports** by explicitly listing exported symbols in `__all__`.
  - Example:
    ```python
    __all__ = ["User", "parse_date"]
    ```

### Commit Patterns
- Commit messages are **freeform** (no enforced prefixes).
- Average commit message length: **64 characters**.
  - Example:  
    ```
    Add support for parsing multiple date formats in utils
    ```

## Workflows

### Adding a New Module
**Trigger:** When you need to add a new feature or utility.
**Command:** `/add-module`

1. Create a new Python file using snake_case (e.g., `feature_x.py`).
2. Implement your functionality.
3. Use relative imports for any internal dependencies.
4. Add named exports via `__all__` if needed.
5. Write or update tests as appropriate.

### Refactoring Existing Code
**Trigger:** When improving or restructuring code.
**Command:** `/refactor`

1. Identify the target module(s).
2. Rename files to snake_case if not already.
3. Update imports to use relative style.
4. Ensure all exports are named via `__all__`.
5. Run tests to confirm correctness.

### Writing Tests
**Trigger:** When adding new code or fixing bugs.
**Command:** `/write-test`

1. Create a test file (pattern: `*.test.ts`).
2. Write tests for new or modified functionality.
3. Run tests to verify behavior.

## Testing Patterns

- **Testing framework:** Unknown (not detected).
- **Test file pattern:** Files are named with the `.test.ts` suffix (suggesting TypeScript or a hybrid setup).
- **Best practice:** For Python code, ensure tests are present and follow the repository's conventions, even if the framework is not specified.
- **Example:**
  ```typescript
  // sample.test.ts
  import { myFunction } from './my_module';

  test('should return correct value', () => {
    expect(myFunction()).toBe('expected');
  });
  ```

## Commands
| Command      | Purpose                                      |
|--------------|----------------------------------------------|
| /add-module  | Add a new module following conventions       |
| /refactor    | Refactor code to match style and structure   |
| /write-test  | Write or update tests for your code changes  |
```
