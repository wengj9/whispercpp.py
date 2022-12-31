from setuptools import setup, Extension
from Cython.Build import cythonize
import sys
import numpy
import os

cxx_flags = ["-O3", "-std=c++17", "-Wall", "-Wextra", "-Wpedantic", "-pthread", "-g3", "-ggdb"]
c_flags = ["-O3", "-std=c11", "-Wall", "-Wextra", "-Wpedantic", "-pthread", "-g3", "-ggdb"]
ld_flags: list[str] = []

if sys.platform == "darwin":
    cxx_flags.append("-DGGML_USE_ACCELERATE")
    ld_flags.extend(["-framework", "Accelerate"])

    c_flags.append("-DGGML_USE_ACCELERATE")
else:
    cxx_flags.extend(["-mavx", "-mavx2", "-mfma", "-mf16c", "-D_POSIX_SOURCE", "-D_GNU_SOURCE"])
    c_flags.extend(["-mavx", "-mavx2", "-mfma", "-mf16c", "-D_POSIX_SOURCE", "-D_GNU_SOURCE"])

os.environ["LDFLAGS"] = " ".join(ld_flags)
os.environ["CFLAGS"] = " ".join(c_flags)

module = Extension(
    name="whispercpp",
    sources=["whispercpp.pyx", "whisper.cpp/whisper.cpp"],
    extra_compile_args=cxx_flags,
    extra_link_args=ld_flags,
    libraries=["pthread"],
)

static_libs = [
    ("ggml", {"sources": ["whisper.cpp/ggml.c"]}),
]

setup(
    ext_modules=cythonize(module, gdb_debug=True),
    libraries=static_libs,
    include_dirs=["whisper.cpp/", numpy.get_include()],
    zip_safe=False,
)
