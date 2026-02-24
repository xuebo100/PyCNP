# PyCNP Build Tools

This directory contains scripts and tools for building PyCNP native extensions.

## File Descriptions

- `build_extensions.py`: Main build script for compiling C++ extension modules
- `build_wrapper.py`: Build wrapper for Poetry build system integration
- `extract_docstrings.py`: Tool for extracting docstrings from C++ headers
- `__init__.py`: Python package initialization file

## Usage

### Direct Build
```bash
python buildtools/build_extensions.py
```

### Clean and Rebuild
```bash
python buildtools/build_extensions.py --clean
```

### Debug Build
```bash
python buildtools/build_extensions.py --build_type debug --verbose
```

### Build via Poetry
```bash
poetry build
```

## Build Options

- `--build_dir`: Specify build directory (default: build)
- `--build_type`: Build type (debug/debugoptimized/release, default: release)
- `--clean`: Clean before building
- `--verbose`: Verbose output
- `--use_pgo`: Enable Profile Guided Optimization
- `--additional`: Additional Meson options

## Requirements

- Python 3.8+
- Meson >= 1.0.0
- Ninja >= 1.11.1
- pybind11 >= 2.10.0
- C++20 compatible compiler
