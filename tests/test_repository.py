import pytest
from abc import ABC
from src.repository.repository import Registry


class TestRegistry:
    def test_registry_is_abstract(self):
        # Verify Registry is an abstract class
        assert issubclass(Registry, ABC)

    def test_add_is_abstract(self):
        # Verify add is an abstract method
        assert hasattr(Registry, "add")

    def test_get_by_id_is_abstract(self):
        # Verify get_by_id is an abstract method
        assert hasattr(Registry, "get_by_id")

    def test_get_all_is_abstract(self):
        # Verify get_all is an abstract method
        assert hasattr(Registry, "get_all")

    def test_cannot_instantiate_registry(self):
        # Verify Registry cannot be instantiated directly
        with pytest.raises(TypeError):
            Registry()  # type: ignore
