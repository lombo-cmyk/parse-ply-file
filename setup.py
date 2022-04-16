import setuptools

setuptools.setup(
    name="parse_ply_file",
    version="0.0.1",
    author="Lukasz Kania",
    author_email="lukasz.kania.cc@gmail.com",
    url="https://github.com/lombo-cmyk/parse-ply-file",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=['pandas', 'openpyxl'],
    python_requires=">=3.8",
)
