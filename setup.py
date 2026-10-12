"""Setup configuration for AI Live Translation Broadcast Solution"""

from setuptools import setup, find_packages

setup(
    name="ai-live-translation-broadcast",
    version="1.0.0",
    description="AI-powered live translation and lip sync for broadcasts",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "torch>=2.0.0",
        "transformers>=4.35.0",
        "fastapi>=0.104.0",
        "uvicorn[standard]>=0.27.0",
        "openai-whisper>=20240930",
        "elevenlabs>=1.0.0",
        "soundfile>=0.12.0",
        "accelerate>=0.25.0",
        "psutil>=5.9.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Multimedia :: Video",
        "Topic :: Software Development :: Libraries :: AI",
    ],
)