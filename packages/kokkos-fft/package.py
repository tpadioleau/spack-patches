# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class KokkosFft(CMakePackage):
    """FFFT interfaces for Kokkos C++ Performance Portability Programming EcoSystem"""

    homepage = "https://github.com/kokkos/kokkos-fft"
    url = "https://github.com/kokkos/kokkos-fft/archive/refs/tags/v0.2.1.tar.gz"

    maintainers("cedricchevalier19", "tpadioleau", "yasahi-hpc")

    license("Apache-2.0 WITH LLVM-exception OR MIT", checked_by="cedricchevalier19")

    version("0.2.1", sha256="e2df27211fc7042d8ed45a0f41583e748c69cbb7edb948aaebaa8a9d8c10c637")
    version("0.2.0", sha256="9067d3c1af1f3ca60b6e0a6ad483de49466617803bf7d397a5703244da4abf6d")
    version("0.1.0", sha256="8bc57c887ce6807da27af1eab1a642ba17def1669a928ac73dbe4efc6ca880af")

    depends_on("cxx", type="build")

    depends_on("kokkos@4.4.00: +complex_align")

    variant("host", default=False, description="Enable host fft, i.e. fftw")
    variant("unit_test", default=False, description="Enable Unit Tests")

    depends_on("cuda", when="^kokkos +cuda")

    # FIXME: deal with rocfft
    depends_on("hipfft", when="^kokkos +rocm")

    # FIXME: take the correct configuration for fftw:
    #   - +openmp if ^kokkos+openmp ~gpu || +host ^kokkos+openmp
    #   - ~openmp if ^kokkos+openmp ~gpu || +host ^kokkos+openmp
    #   - "+threads": not available as a variant in spack
    depends_on("fftw~mpi precision=float,double", when="^kokkos ~cuda ~rocm ~sycl")
    depends_on("fftw +openmp", when="^kokkos +openmp")
    depends_on("fftw~mpi precision=float,double", when="+host")

    depends_on("intel-oneapi-mkl", when="^kokkos +sycl")

    # FIXME: how to handle other kokkos backends: hpx, openmp target, openacc

    depends_on("googletest", when="+unit_test")

    def cmake_args(self):
        args = [
            self.define("KokkosFFT_ENABLE_INTERNAL_KOKKOS", False),
            self.define_from_variant("KokkosFFT_ENABLE_HOST_AND_DEVICE", "host"),
            self.define("KokkosFFT_ENABLE_TESTS", "unit_test"),
            self.define("KokkosFFT_ENABLE_DOCS", False),
            self.define("KokkosFFT_ENABLE_BENCHMARK", False),
            self.define("KokkosFFT_ENABLE_EXAMPLES", False),
            self.define("CMAKE_CXX_COMPILER", self["kokkos"].kokkos_cxx),
        ]

        return args
