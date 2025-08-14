import asyncio
import inspect
from typing import Any

import pytest


def pytest_configure(config: pytest.Config) -> None:
    # Ensure the asyncio marker is recognized even without pytest-asyncio installed
    config.addinivalue_line("markers", "asyncio: mark test as asyncio")


@pytest.hookimpl(tryfirst=True)
def pytest_pyfunc_call(pyfuncitem: pytest.Function) -> bool | None:
    """
    Minimal async test runner to support `async def` tests without requiring
    the pytest-asyncio plugin. If the test function is a coroutine function,
    run it using asyncio.run and signal that the call was handled by returning True.
    """
    test_func: Any = pyfuncitem.obj
    if inspect.iscoroutinefunction(test_func):
        kwargs = {
            arg: pyfuncitem.funcargs[arg] for arg in pyfuncitem._fixtureinfo.argnames
        }
        asyncio.run(test_func(**kwargs))
        return True
    return None
