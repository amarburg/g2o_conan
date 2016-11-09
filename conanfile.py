from conans import ConanFile, CMake
import os

class G2OConan(ConanFile):
  name = "g2o"
  version = "master"
  url = "https://github.com/amarburg/g2o_conan"
  settings = "os", "compiler", "build_type", "arch"
  options = {"shared": [True, False], "build_parallel": [True, False]}
  default_options = "shared=True", "build_parallel=True"

  def source(self):
    if os.path.isdir('g2o'):
      self.run('cd g2o && git pull origin master')
    else:
      self.run('git clone https://github.com/RainerKuemmerle/g2o.git')

  def build(self):
    cmake = CMake(self.settings)

    if self.options.shared:
      cmake_opts = "-DBUILD_SHARED_LIBS=True"

    if self.options.build_parallel:
      build_opts = "-- -j"

    self.run('cmake "%s/g2o" %s %s' % (self.conanfile_directory, cmake.command_line, cmake_opts ))
    self.run('cmake --build . %s %s' % (cmake.build_config, build_opts))


  def package(self):
    self.copy("*.h", src="g2o", dst="include")
    self.copy("config.h", src="g2o", dst="include/g2o")
    if self.options.shared:
      if self.settings.os == "Macos":
          self.copy(pattern="*.dylib", dst="lib", keep_path=False)
      else:
          self.copy(pattern="*.so*", dst="lib", src="lib", keep_path=False)
    else:
        self.copy(pattern="*.a", dst="lib", src="lib", keep_path=False)

  # def package_info(self):
  #     self.cpp_info.libs = ["videoio"]
