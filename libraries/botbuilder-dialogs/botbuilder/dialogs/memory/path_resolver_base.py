from abc import ABC, abstractmethod


class PathResolverBase(ABC):
    @abstractmethod
    def transform_path(self, path: str):
        raise NotImplementedError()
