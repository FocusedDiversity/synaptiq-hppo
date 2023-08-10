import inspect
import textwrap

import pytest

from chatbae.response_generator import ResponseGenerator


@pytest.fixture
def g():
    return ResponseGenerator()


def test_splits_on_newlines(g):
    assert g.update("Hello") == None
    assert g.update("Hello, this is chatbae") == None
    assert g.update("Hello, this is chatbae\n") == 'Hello, this is chatbae\n'
    assert g.update("Hello, this is chatbae\nI like cats") == None
    assert g.update("Hello, this is chatbae\nI like cats\n") == 'I like cats\n'


def test_keeps_code_blocks(g):
    assert g.update("Hello, this is chatbae\n") == 'Hello, this is chatbae\n'
    assert g.update(inspect.cleandoc("""Hello, this is chatbae
    ```python
    print("Hello, this is chatbae")
    ```
    """)) == inspect.cleandoc("""```python
    print("Hello, this is chatbae")
    ```
    """)
