from typing import Protocol, runtime_checkable


@runtime_checkable
class StoppingCriterion(Protocol):  # pragma: no cover
    """
    Protocol for algorithm stopping criteria.

    """

    def __call__(self, best_obj_value: float) -> bool:
        """
        Determines whether the algorithm should stop.

        Parameters
        ----------
        best_obj_value : float
            The best objective value found so far.

        Returns
        -------
        bool
            True if the stopping condition is met, False otherwise.
        """

    def get_name(self) -> str:
        """
        Returns the name of the stopping criterion.

        This can be used for logging or identification purposes.

        Returns
        -------
        str
            The name of the criterion as a string.
        """
        return self.__class__.__name__
