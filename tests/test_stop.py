import pytest

from pycnp.stop import (
    CombinedCriterion,
    MaxIterations,
    MaxRuntime,
    NoImprovement,
)


class TestMaxIterations:
    """Tests for MaxIterations stopping criterion."""

    def test_init_valid(self):
        """Test initialization with valid max_iterations."""
        criterion = MaxIterations(100)
        assert criterion.max_iterations == 100
        assert criterion.iterations == 0

    def test_init_invalid_negative(self):
        """Test that negative max_iterations raises ValueError."""
        with pytest.raises(ValueError):
            MaxIterations(-1)

    def test_init_invalid_zero(self):
        """Test that zero max_iterations raises ValueError."""
        with pytest.raises(ValueError):
            MaxIterations(0)

    def test_init_invalid_float(self):
        """Test that float max_iterations raises ValueError."""
        with pytest.raises(ValueError):
            MaxIterations(10.5)

    def test_init_invalid_string(self):
        """Test that string max_iterations raises ValueError."""
        with pytest.raises(ValueError):
            MaxIterations("100")

    def test_call_increments_counter(self):
        """Test that __call__ increments the iteration counter."""
        criterion = MaxIterations(5)
        assert criterion(100.0) is False
        assert criterion.iterations == 1
        assert criterion(100.0) is False
        assert criterion.iterations == 2

    def test_call_stops_at_limit(self):
        """Test that __call__ returns True when limit is reached."""
        criterion = MaxIterations(3)
        assert criterion(100.0) is False
        assert criterion(100.0) is False
        assert criterion(100.0) is True

    def test_get_name(self):
        """Test that get_name returns correct name."""
        assert MaxIterations(10).get_name() == "MaxIterations"


class TestMaxRuntime:
    """Tests for MaxRuntime stopping criterion."""

    def test_init_valid(self):
        """Test initialization with valid runtime."""
        criterion = MaxRuntime(60.0)
        assert criterion.max_runtime == 60.0

    def test_init_valid_int(self):
        """Test initialization with integer runtime."""
        criterion = MaxRuntime(60)
        assert criterion.max_runtime == 60

    def test_init_invalid_negative(self):
        """Test that negative runtime raises ValueError."""
        with pytest.raises(ValueError):
            MaxRuntime(-1.0)

    def test_init_invalid_zero(self):
        """Test that zero runtime raises ValueError."""
        with pytest.raises(ValueError):
            MaxRuntime(0.0)

    def test_init_invalid_string(self):
        """Test that string runtime raises ValueError."""
        with pytest.raises(ValueError):
            MaxRuntime("60")

    def test_call_before_timeout(self):
        """Test that __call__ returns False before timeout."""
        criterion = MaxRuntime(10.0)  # 10 seconds
        # Immediate call should return False
        assert criterion(100.0) is False

    def test_get_name(self):
        """Test that get_name returns correct name."""
        assert MaxRuntime(60).get_name() == "MaxRuntime"


class TestNoImprovement:
    """Tests for NoImprovement stopping criterion."""

    def test_init_valid(self):
        """Test initialization with valid max_idle_iterations."""
        criterion = NoImprovement(20)
        assert criterion.max_idle_iterations == 20
        assert criterion.idle_iterations == 0

    def test_init_invalid_negative(self):
        """Test that negative max_idle_iterations raises ValueError."""
        with pytest.raises(ValueError):
            NoImprovement(-1)

    def test_init_invalid_zero(self):
        """Test that zero max_idle_iterations raises ValueError."""
        with pytest.raises(ValueError):
            NoImprovement(0)

    def test_init_invalid_float(self):
        """Test that float max_idle_iterations raises ValueError."""
        with pytest.raises(ValueError):
            NoImprovement(10.5)

    def test_call_with_improvement(self):
        """Test __call__ when there is improvement."""
        criterion = NoImprovement(3)
        # Improvement resets counter
        assert criterion(100.0) is False
        assert criterion(99.0) is False  # Improvement!
        assert criterion.idle_iterations == 0

    def test_call_without_improvement(self):
        """Test __call__ when there is no improvement."""
        criterion = NoImprovement(3)
        assert criterion(100.0) is False
        assert criterion(100.0) is False
        assert criterion(100.0) is False
        assert criterion(100.0) is True  # 3 idle iterations reached

    def test_get_name(self):
        """Test that get_name returns correct name."""
        assert NoImprovement(10).get_name() == "NoImprovement"


class TestCombinedCriterion:
    """Tests for CombinedCriterion stopping criterion."""

    def test_init_single_criterion(self):
        """Test initialization with single criterion."""
        max_iter = MaxIterations(100)
        combined = CombinedCriterion([max_iter])
        assert len(combined.criteria) == 1

    def test_init_multiple_criteria(self):
        """Test initialization with multiple criteria."""
        max_iter = MaxIterations(100)
        max_time = MaxRuntime(60)
        combined = CombinedCriterion([max_iter, max_time])
        assert len(combined.criteria) == 2

    def test_init_empty_raises_error(self):
        """Test that empty criteria list raises ValueError."""
        with pytest.raises(ValueError):
            CombinedCriterion([])

    def test_init_invalid_criterion_raises_error(self):
        """Test that invalid criterion raises ValueError."""
        with pytest.raises(ValueError):
            CombinedCriterion([None])  # type: ignore

    def test_call_stops_on_first_criterion(self):
        """Test that __call__ returns True when first criterion is met."""
        max_iter = MaxIterations(1)
        max_time = MaxRuntime(3600)
        combined = CombinedCriterion([max_iter, max_time])

        combined(100.0)  # First iteration - max_iter becomes 1
        combined(100.0)  # Second iteration - max_iter stops
        assert combined(100.0) is True  # MaxIterations reached

    def test_get_triggered_criterion(self):
        """Test get_triggered_criterion returns correct criterion."""
        max_iter = MaxIterations(1)
        max_time = MaxRuntime(3600)
        combined = CombinedCriterion([max_iter, max_time])

        # First call: max_iter iterations becomes 1 (>= 1), so it triggers
        combined(100.0)
        assert combined.get_triggered_criterion() is max_iter

    def test_get_name(self):
        """Test that get_name returns combined name."""
        max_iter = MaxIterations(100)
        max_time = MaxRuntime(60)
        combined = CombinedCriterion([max_iter, max_time])
        name = combined.get_name()
        assert "MaxIterations" in name
        assert "MaxRuntime" in name
        assert "OR" in name

    def test_get_name_empty_criteria(self):
        """Test get_name with empty criteria list (edge case)."""
        # Note: Empty list raises ValueError in __init__, so we don't test this
        pass
