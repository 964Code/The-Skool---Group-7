from setuptools import setup, find_packages

print(find_packages())

setup(
    name="the_skool",
    version="0.0.1",
    description="""
    This package is used for creating a dashboard in taipy
    """,
    author="G7",
    author_email="uv ",
    ## This is like the requirements, will install packages if they are not installed.
    install_requires=["pandas", "taipy", "duckdb"],
    packages=find_packages(exclude=("test*", "explorations", "assets")),
)
