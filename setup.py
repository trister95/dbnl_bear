from setuptools import setup, find_packages

setup(
    name='dbnl_bear',
    version='0.1',
    packages=find_packages(),  # Automatically finds all sub-packages like subfolder1, subfolder2
    install_requires=["os", "lxml.etree", "tqdm", "glob", "re", "asyncio",
                      "dotenv", "langchain_core", "langchain_openai", "tqdm.asyncio",
                      "typing", "langchain_text_splitters", "docx", "fuzzywuzzy"],  # Add dependencies if necessary
    description='A Python package to use an AI assitant for historical analysis',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Arjan van Dalfsen',
    author_email='j.a.vandalfsen@uu.nl',
    url='https://github.com/trister95/dbnl_bear',  # Optional
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
