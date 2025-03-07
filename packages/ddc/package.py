# Copyright (C) The DDC development team, see COPYRIGHT.md file
#
# SPDX-License-Identifier: MIT

from spack.package import *


class Ddc(CMakePackage):
    """DDC is the discrete domain computation library."""

    homepage = "https://github.com/CExA-project/ddc"
    git = "https://github.com/CExA-project/ddc.git"
    url = "https://github.com/CExA-project/ddc/archive/refs/tags/v0.4.2.tar.gz"

    maintainers("tpadioleau")

    license("MIT", checked_by="tpadioleau")

    test_requires_compiler = True

    version("main", branch="main")
    version(
        "0.5.2",
        sha256="0d4ae8714012d05a87de4515d959d3fc2ac8a856d28b2bb21ae22ecfd1a75b8b",
        extension="tar.gz",
    )
    version(
        "0.5.1",
        sha256="ee7abaac1111879875e2996fda8dc2a9e4cd0a8f8c71b0515cb185060e385b21",
        extension="tar.gz",
        deprecated=True,
    )
    version(
        "0.5.0",
        sha256="48ea5b4942188a16225f6affb03d703a1b1f7ed1b17fc1edf16945522301d039",
        extension="tar.gz",
        deprecated=True,
    )
    version(
        "0.4.2",
        sha256="ed29177cc11ef72f868e6f70cad60d04531454493135348f418090b4b4f4bfb9",
        extension="tar.gz",
        deprecated=True,
    )

    variant("fft", default=True, description="Build DDC kernels for FFT")
    variant("pdi", default=True, description="Build DDC PDI wrapper")
    variant("splines", default=True, description="Build DDC kernels for splines")

    depends_on("cxx", type="build")

    depends_on("cmake@3.22:3", type="build")
    depends_on("ginkgo@1.8:1", when="+splines")
    depends_on("kokkos@4.4.1:4")
    depends_on(
        "kokkos +cuda_constexpr +cuda_lambda +cuda_relocatable_device_code", when="^kokkos +cuda"
    )
    depends_on("kokkos +hip_relocatable_device_code", when="^kokkos +rocm")
    depends_on("kokkos-fft@0.2.1 +host", when="+fft")
    depends_on("kokkos-kernels@4.5.1:4", when="+splines")
    depends_on("lapack", when="+splines")
    depends_on("pdi@1.6:1", when="+pdi")

    conflicts("kokkos@4.5.0", msg="The embedded mdspan in Kokkos is not compatible with DDC.")

    def cmake_args(self):
        args = [
            self.define("DDC_BUILD_BENCHMARKS", "OFF"),
            self.define("DDC_BUILD_DEPRECATED_CODE", "OFF"),
            self.define("DDC_BUILD_DOCUMENTATION", "OFF"),
            self.define("DDC_BUILD_DOUBLE_PRECISION", "ON"),
            self.define("DDC_BUILD_EXAMPLES", "OFF"),
            self.define("DDC_BUILD_TESTS", "OFF"),
            self.define("DDC_Kokkos_DEPENDENCY_POLICY", "INSTALLED"),
            self.define_from_variant("DDC_BUILD_KERNELS_FFT", "fft"),
            self.define_from_variant("DDC_BUILD_KERNELS_SPLINES", "splines"),
            self.define_from_variant("DDC_BUILD_PDI_WRAPPER", "pdi"),
            self.define("CMAKE_CXX_COMPILER", self.spec["kokkos"].kokkos_cxx),
        ]
        if "+fft" in self.spec:
            args.append(self.define("DDC_KokkosFFT_DEPENDENCY_POLICY", "INSTALLED"))
        if "+splines" in self.spec:
            args.append(self.define("DDC_KokkosKernels_DEPENDENCY_POLICY", "INSTALLED"))

        return args
