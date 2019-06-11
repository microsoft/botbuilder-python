# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

class OAuthPromptSettings:
    def __init__(
        self,
        connection_name: str = None,
        title: str = None,
        text: str = None,
        timeout: int = None
    ):
        self._connection_name = connection_name
        self._title = title
        self._text = text
        self._timeout

    @property
    def connection_name(self) -> str:
        """
        Name of the OAuth connection being used.
        """
        return self._connection_name
    
    @connection_name.setter
    def connection_name(self, value: str) -> None:
        """
        Sets the name of the OAuth connection being used.
        """
        self._connection_name = value
    
    @property
    def title(self) -> str:
        """
        Title of the cards signin button.
        """
        return self._title
    
    @title.setter
    def title(self, value: str) -> None:
        """
        Sets the title of the cards signin button.
        """
        self._title = value
    
    @property
    def text(self) -> str:
        """
        (Optional) additional text included on the signin card.
        """
        return self._text
    
    @text.setter
    def text(self, value: str) -> None:
        """
        (Optional) Sets additional text to include on the signin card.
        """
        self._text = value
    
    @property
    def timeout(self) -> int:
        """
        (Optional) number of milliseconds the prompt will wait for the user to authenticate.

        Defaults to 900000 (15 minutes).
        """
    
    @timeout.setter
    def timeout(self, value: int) -> None:
        """
        (Optional) Sets the number of milliseconds the prompt will wait for the user to authenticate.

        Defaults to 900000 (15 minutes).

        Parameters
        ----------
        value
            Number in milliseconds prompt will wait fo ruser to authenticate.
        """
        if value:
            self._timeout = value
        else:
            self._timeout = 900000
