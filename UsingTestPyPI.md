# Using TestPyPI to consume rc builds
The BotBuilder SDK rc build feed is found on [TestPyPI](https://test.pypi.org/). 

The daily builds will be available soon through the mentioned feed as well.


# Configure TestPyPI

You can tell pip to download packages from TestPyPI instead of PyPI by specifying the --index-url flag (in the example below, replace 'botbuilder-core' for the name of the library you want to install)

```bash
$ pip install --index-url https://test.pypi.org/simple/ botbuilder-core
```
If you want to allow pip to also pull other packages from PyPI you can specify --extra-index-url to point to PyPI.
This is useful when the package you’re testing has dependencies:

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ botbuilder-core
```
