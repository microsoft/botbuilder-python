from setuptools import setup, find_packages

setup(
    name='botbuilder-core',
    version='4.0.0-a0',
    url='https://www.github.com/Microsoft/botbuilder-python',
    long_description='Microsoft Bot Framework Bot Builder SDK for Python. Build intelligent bots that scale.',
    license='MIT',
    author='Microsoft',
    author_email='bf-reports@microsoft.com',
    description='Microsoft Bot Framework Bot Builder',
    packages=["botbuilder.core"],
    classifiers=[
        'Programming Language :: Python',
        'Intended Audience :: Bot Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ]
)
