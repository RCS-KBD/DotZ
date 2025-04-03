# Contributing Guidelines

## Development Workflow

### 1. Testing Protocol
- All changes must be tested locally before committing
- Testing sequence:
  1. Run game to verify basic functionality
  2. Test the specific feature/change that was modified
  3. Test related features to ensure no regressions
  4. Run all automated tests
- Document test results in commit messages

### Testing Rules and Procedures

#### 1. Test Structure
- All tests must be placed in the `tests/` directory
- Test files should be named `test_*.py`
- Each test file should focus on a specific component or feature
- Tests should be independent and not rely on each other

#### 2. Test Categories
1. **Unit Tests**
   - Test individual components in isolation
   - Mock external dependencies
   - Focus on specific functionality
   - Example: `test_utils.py`, `test_config.py`

2. **State Tests**
   - Test game state transitions
   - Verify state initialization
   - Check state event handling
   - Example: `test_game_states.py`

3. **Functionality Tests**
   - Test complete feature workflows
   - Verify component interactions
   - Test user input handling
   - Example: `test_game_state_functionality.py`

#### 3. Test Requirements
- Each test must have a clear purpose and description
- Use descriptive test names that explain the test's purpose
- Include setup and teardown when necessary
- Clean up resources after tests (e.g., pygame.quit())
- Handle test isolation properly

#### 4. Running Tests
```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_game_states.py -v

# Run specific test
pytest tests/test_game_states.py::test_state_transitions -v
```

#### 5. Test Coverage Requirements
- All new features must include tests
- Critical game mechanics must have comprehensive tests
- State transitions must be fully tested
- Input handling must be verified
- Asset loading must be validated

#### 6. Mocking Guidelines
- Use pytest's monkeypatch for mocking
- Mock external dependencies (pygame, file system)
- Create realistic test data
- Document mock behavior

#### 7. Test Maintenance
- Keep tests up to date with code changes
- Remove obsolete tests
- Update tests when features change
- Document test dependencies

### 2. Code Preservation
- Never delete existing working code without explicit confirmation
- Use comments to temporarily disable code rather than deleting when testing alternatives
- Keep original function signatures and parameters intact
- Document any API changes before implementation

### 3. Python/Pygame Best Practices
- Follow PEP 8 style guidelines
- Use type hints for all functions and methods
- Maintain existing class structure patterns
- Keep Pygame-specific code in appropriate modules

## Example Commit Message
```
feat(enemy): Add new movement pattern

- Added oscillating movement to enemy ships
- Tested:
  * Basic game functionality ✓
  * New movement pattern ✓
  * Collision detection with new pattern ✓
  * No impact on existing features ✓
```

## Code Style Example
```python
def update_movement(self, delta_time: float) -> None:
    """Update enemy movement pattern.
    
    Args:
        delta_time: Time since last frame in seconds
    """
    # Implementation
    pass
``` 