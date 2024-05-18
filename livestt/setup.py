from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()


VERSION = '1.0.7'
DESCRIPTION = "Simple and easy to use realtime speech to text"
# Setting up
setup(
    name="livestt",
    version=VERSION,
    author="a3l6",
    author_email="<emen3998@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[
        "av==10.0.0",
        "certifi==2024.2.2",
        "charset-normalizer==3.3.2",
        "coloredlogs==15.0.1",
        "ctranslate2==3.24.0",
        "faster-whisper==0.10.0",
        "filelock==3.13.1",
        "flatbuffers==23.5.26",
        "fsspec==2024.2.0",
        "huggingface-hub==0.20.3",
        "humanfriendly==10.0",
        "idna==3.6",
        "Jinja2==3.1.3",
        "MarkupSafe==2.1.5",
        "mpmath==1.3.0",
        "networkx==3.2.1",
        "numpy==1.26.3",
        "nvidia-cublas-cu12==12.1.3.1",
        "nvidia-cuda-cupti-cu12==12.1.105",
        "nvidia-cuda-nvrtc-cu12==12.1.105",
        "nvidia-cuda-runtime-cu12==12.1.105",
        "nvidia-cudnn-cu12==8.9.2.26",
        "nvidia-cufft-cu12==11.0.2.54",
        "nvidia-curand-cu12==10.3.2.106",
        "nvidia-cusolver-cu12==11.4.5.107",
        "nvidia-cusparse-cu12==12.1.0.106",
        "nvidia-nccl-cu12==2.19.3",
        "nvidia-nvjitlink-cu12==12.3.101",
        "nvidia-nvtx-cu12==12.1.105",
        "onnxruntime==1.17.0",
        "packaging==23.2",
        "protobuf==4.25.2",
        "pvporcupine==3.0.2",
        "pvrecorder==1.2.2",
        "PyAudio==0.2.14",
        "python-dotenv==1.0.1",
        "PyYAML==6.0.1",
        "regex==2023.12.25",
        "requests==2.31.0",
        "safetensors==0.4.2",
        "sympy==1.12",
        "tokenizers==0.15.1",
        "torch==2.2.0",
        "tqdm==4.66.1",
        "transformers==4.37.2",
        "triton==2.2.0",
        "typing_extensions==4.9.0",
        "urllib3==2.2.0",
    ],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
