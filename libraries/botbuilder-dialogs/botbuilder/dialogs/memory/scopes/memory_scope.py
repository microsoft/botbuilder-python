# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from abc import ABC, abstractmethod


class MemoryScope(ABC):
    def __init__(self, name: str, include_in_snapshot: bool = True):
        # <summary>
        # Gets or sets name of the scope.
        # </summary>
        # <value>
        # Name of the scope.
        # </value>
        self.include_in_snapshot = include_in_snapshot
        # <summary>
        # Gets or sets a value indicating whether this memory should be included in snapshot.
        # </summary>
        # <value>
        # True or false.
        # </value>
        self.name = name

    # <summary>
    # Get the backing memory for this scope.
    # </summary>
    # <param name="dc">dc.</param>
    # <returns>memory for the scope.</returns>
    @abstractmethod
    def get_memory(
        self, dialog_context: "DialogContext"
    ) -> object:  # pylint: disable=unused-argument
        raise NotImplementedError()

    # <summary>
    # Changes the backing object for the memory scope.
    # </summary>
    # <param name="dc">dc.</param>
    # <param name="memory">memory.</param>
    @abstractmethod
    def set_memory(
        self, dialog_context: "DialogContext", memory: object
    ):  # pylint: disable=unused-argument
        raise NotImplementedError()

    # <summary>
    # Populates the state cache for this <see cref="BotState"/> from the storage layer.
    # </summary>
    # <param name="dialogContext">The dialog context object for this turn.</param>
    # <param name="force">Optional, <c>true</c> to overwrite any existing state cache
    # or <c>false</c> to load state from storage only if the cache doesn't already exist.</param>
    # <param name="cancellationToken">A cancellation token that can be used by other objects
    # or threads to receive notice of cancellation.</param>
    # <returns>A task that represents the work queued to execute.</returns>
    async def load(
        self, dialog_context: "DialogContext", force: bool = False
    ):  # pylint: disable=unused-argument
        return

    # <summary>
    # Writes the state cache for this <see cref="BotState"/> to the storage layer.
    # </summary>
    # <param name="dialogContext">The dialog context object for this turn.</param>
    # <param name="force">Optional, <c>true</c> to save the state cache to storage
    # or <c>false</c> to save state to storage only if a property in the cache has changed.</param>
    # <param name="cancellationToken">A cancellation token that can be used by other objects
    # or threads to receive notice of cancellation.</param>
    # <returns>A task that represents the work queued to execute.</returns>
    async def save_changes(
        self, dialog_context: "DialogContext", force: bool = False
    ):  # pylint: disable=unused-argument
        return

    # <summary>
    # Deletes any state in storage and the cache for this <see cref="BotState"/>.
    # </summary>
    # <param name="dialogContext">The dialog context object for this turn.</param>
    # <param name="cancellationToken">A cancellation token that can be used by other objects
    # or threads to receive notice of cancellation.</param>
    # <returns>A task that represents the work queued to execute.</returns>
    async def delete(
        self, dialog_context: "DialogContext"
    ):  # pylint: disable=unused-argument
        return
