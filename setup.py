from setuptools import setup, Extension
from Cython.Build import cythonize
import sys
import numpy

cxx_flags = ["-O3", "-std=c++11"]
c_flags = ["-O3", "-std=c11"]
ld_flags: list[str] = []

if sys.platform == "darwin":
    cxx_flags.append("-DGGML_USE_ACCELERATE")
    c_flags.append("-DGGML_USE_ACCELERATE")
    ld_flags.extend(["-framework", "Accelerate"])
else:
    cxx_flags.extend(["-mavx", "-mavx2", "-mfma", "-mf16c"])
    c_flags.extend(["-mavx", "-mavx2", "-mfma", "-mf16c"])

external_modules = [
    Extension(
        name="ggml",
        sources=["./whisper.cpp/ggml.c"],
        extra_compile_args=c_flags,
        extra_link_args=ld_flags,
    ),
    Extension(
        name="whispercpp",
        sources=["./whisper.cpp/whisper.cpp"],
        extra_compile_args=cxx_flags,
        extra_link_args=ld_flags,
    ),
    *cythonize("whispercpp.pyx"),
]

setup(
    ext_modules=external_modules,
    include_dirs=["./whisper.cpp/", numpy.get_include()],
    zip_safe=False,
)
