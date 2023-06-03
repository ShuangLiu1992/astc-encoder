from conan import ConanFile
import conan.tools.files
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout
import os


class ASTCENCODERConan(ConanFile):
    name = "astc_encoder"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    def generate(self):
        tc = CMakeToolchain(self)
        tc.presets_prefix = f"{self.settings.os}_{self.settings.build_type}_{self.settings.arch}"
        tc.variables["CLI"] = False
        if self.options.shared:
            tc.preprocessor_definitions["ASTCENC_DYNAMIC_LIBRARY"] = 1
        if self.settings.os == "Emscripten":
            tc.variables["ISA_NONE"] = True
        tc.generate()

    def export_sources(self):
        conan.tools.files.copy(self, "*", self.recipe_folder, self.export_sources_folder)

    def layout(self):
        cmake_layout(self)
    
    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        cmake.install()

    def package(self):
        lib_folder = os.path.join(self.package_folder, "lib")
        inc_folder = os.path.join(self.package_folder, "include")
        src_folder = os.path.join(self.build_folder, "Source")
        conan.tools.files.copy(self, "*astcenc-*-static.dll", src_folder, lib_folder, keep_path=False)
        conan.tools.files.copy(self, "*astcenc-*-static.lib", src_folder, lib_folder, keep_path=False)
        conan.tools.files.copy(self, "*astcenc-*-static.a", src_folder, lib_folder, keep_path=False)
        conan.tools.files.copy(self, "*astcenc-*-static.dylib", src_folder, lib_folder, keep_path=False)
        conan.tools.files.copy(self, "astcenc.h", os.path.join(self.folders.base_source, "Source"),
                               inc_folder)

    def package_info(self):
        self.cpp_info.libs = conan.tools.files.collect_libs(self)
