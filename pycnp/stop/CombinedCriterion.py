from typing import List, Optional, Union

from .StoppingCriterion import StoppingCriterion


class CombinedCriterion(StoppingCriterion):
    """
    A stopping criterion that combines multiple criteria with OR logic.

    The algorithm stops when ANY of the provided criteria is met.
    This is useful for combining different types of stopping conditions,
    such as optimal value and maximum runtime.

    Example
    -------
    .. code-block:: python

        # Stop when either optimal value is reached OR max time is exceeded
        combined = CombinedCriterion([
            OptimalValue(target_value=5012, minimize=True),
            MaxRuntime(3600)  # 1 hour backup
        ])
    """

    def __init__(self, criteria: List[StoppingCriterion]):
        """
        Initializes the CombinedCriterion.

        Parameters
        ----------
        criteria : List[StoppingCriterion]
            List of stopping criteria to combine.

        Raises
        ------
        ValueError
            If criteria list is empty or contains invalid items.
        """
        if not criteria:
            raise ValueError("At least one stopping criterion must be provided.")

        for criterion in criteria:
            if not hasattr(criterion, "__call__") or not hasattr(criterion, "get_name"):
                raise ValueError(
                    "All criteria must implement StoppingCriterion protocol."
                )

        self.criteria = criteria
        self._triggered_criterion: Optional[StoppingCriterion] = None

    def __call__(self, best_obj_value: float) -> bool:
        """
        Checks if any of the combined criteria is met.

        Parameters
        ----------
        best_obj_value : float
            The current best objective value.

        Returns
        -------
        bool
            True if any criterion is met, False otherwise.
        """
        for criterion in self.criteria:
            if criterion(best_obj_value):
                self._triggered_criterion = criterion
                return True
        return False

    def get_name(self) -> str:
        """
        Returns the name of the combined criterion.

        Returns
        -------
        str
            A string describing the combined criteria.
        """
        names = [criterion.get_name() for criterion in self.criteria]
        return f"Combined({' OR '.join(names)})"

    def get_triggered_criterion(self) -> Union[StoppingCriterion, None]:
        """
        Returns the criterion that triggered the stop.

        Returns
        -------
        Union[StoppingCriterion, None]
            The stopping criterion that was triggered, or None if not stopped yet.
        """
        return self._triggered_criterion
