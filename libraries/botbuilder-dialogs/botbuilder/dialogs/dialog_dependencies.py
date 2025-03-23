from typing import Iterable, Protocol, runtime_checkable

from .dialog import Dialog


@runtime_checkable
class DialogDependencies(Protocol):
    """Protocol for dialogs that have dependencies on other dialogs.

    If implemented, when the dialog is added to a DialogSet  all of its dependencies will be added as well.
    """

    def get_dependencies(self) -> Iterable[Dialog]:
        """Returns an iterable of the dialogs that this dialog depends on.

        :return: The dialog dependencies."""
