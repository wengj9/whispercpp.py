from setuptools import setup, Extension
from Cython.Build import cythonize
import sys
import numpy
import os

cxx_flags = ["-O3", "-std=c++17", "-Wall", "-Wextra", "-Wpedantic"]
ld_flags: list[str] = []

if sys.platform == "darwin":
    cxx_flags.append("-DGGML_USE_ACCELERATE")
    ld_flags.extend(["-framework", "Accelerate"])

    os.environ['CFLAGS']   = '-DGGML_USE_ACCELERATE -O3 -std=c11'
    os.environ['LDFLAGS']  = '-framework Accelerate'
else:
    cxx_flags.extend(["-mavx", "-mavx2", "-mfma", "-mf16c"])
    
    os.environ['CFLAGS']   = '-mavx -mavx2 -mfma -mf16c -O3 -std=c11'

cythonize("whispercpp.pyx")

external_modules = [
    Extension(
        name="whispercpp.pyx",
        sources=["whispercpp.cpp", "whisper.cpp/whisper.cpp"],
        extra_compile_args=cxx_flags,
        extra_link_args=ld_flags,
    ),
]

static_libs = [
    ("ggml", {"sources": ["whisper.cpp/ggml.c"]}),
]

setup(
    ext_modules=external_modules,
    libraries=static_libs,
    include_dirs=["whisper.cpp/", numpy.get_include()],
    zip_safe=False,
)
