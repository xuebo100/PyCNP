# PyCNP构建工具

此目录包含用于构建PyCNP原生扩展的脚本和工具。

## 文件说明

- `build_extensions.py`: 主要的构建脚本，用于编译C++扩展模块
- `build_wrapper.py`: 构建包装器，用于Poetry构建系统集成
- `extract_docstrings.py`: 从C++头文件提取文档字符串的工具
- `__init__.py`: Python包初始化文件

## 使用方法

### 直接构建
```bash
python buildtools/build_extensions.py
```

### 清理并重新构建
```bash
python buildtools/build_extensions.py --clean
```

### 调试构建
```bash
python buildtools/build_extensions.py --build_type debug --verbose
```

### 通过Poetry构建
```bash
poetry build
```

## 构建选项

- `--build_dir`: 指定构建目录（默认：build）
- `--build_type`: 构建类型（debug/debugoptimized/release，默认：release）
- `--clean`: 构建前清理
- `--verbose`: 详细输出
- `--use_pgo`: 启用配置文件引导优化
- `--additional`: 额外的Meson选项

## 依赖要求

- Python 3.8+
- Meson >= 1.0.0
- Ninja >= 1.11.1
- pybind11 >= 2.10.0
- C++20兼容的编译器
