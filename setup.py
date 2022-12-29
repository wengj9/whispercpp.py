from setuptools import setup, Extension
from Cython.Build import cythonize
import sys
import numpy
import os

cxx_flags = ["-O3", "-std=c++11", "-Wall", "-Wextra", "-Wpedantic"]
c_flags = ["-O3", "-std=c11", "-Wall", "-Wextra", "-Wpedantic"]
ld_flags: list[str] = []

# if sys.platform == "darwin":
#     cxx_flags.append("-DGGML_USE_ACCELERATE")
#     c_flags.append("-DGGML_USE_ACCELERATE")
#     ld_flags.extend(["-framework", "Accelerate"])
# else:
#     cxx_flags.extend(["-mavx", "-mavx2", "-mfma", "-mf16c"])
#     c_flags.extend(["-mavx", "-mavx2", "-mfma", "-mf16c"])

if sys.platform == "darwin":
    os.environ["CFLAGS"] = "-DGGML_USE_ACCELERATE -O3 -std=c11"
    os.environ["CXXFLAGS"] = "-DGGML_USE_ACCELERATE -O3 -std=c++11"
    os.environ["LDFLAGS"] = "-framework Accelerate"
else:
    os.environ["CFLAGS"] = "-mavx -mavx2 -mfma -mf16c -O3 -std=c11"
    os.environ["CXXFLAGS"] = "-mavx -mavx2 -mfma -mf16c -O3 -std=c++11"

external_libs = [
    (
        "ggml",
        {
            "sources": ["whisper.cpp/ggml.c"],
            "extra_compile_args": c_flags,
            "extra_link_flags": ld_flags,
        },
    ),
    (
        "whispercpp",
        {
            "sources": ["whisper.cpp/whisper.cpp"],
            "language": "c++",
        },
    ),
]

setup(
    ext_modules=cythonize("whispercpp.pyx"),
    libraries=external_libs,
    include_dirs=["whisper.cpp/", numpy.get_include()],
    zip_safe=False,
)
