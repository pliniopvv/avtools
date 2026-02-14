from setuptools import setup, find_packages

setup(
    name="avtools",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests",
        "yt-dlp",
        "whisper",
        "av",
        "moviepy==1.0.3"
    ],
    entry_points={
        "console_scripts": [
            "avtools=avtools.app:main"
        ]
    }
)
