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
    cmake_opts = "-DG2O_USE_OPENGL=False -DG2O_BUILD_APPS=False -DG2O_BUILD_EXAMPLES=False"
    build_opts = ""

    if self.options.shared:
      cmake_opts += " -DBUILD_SHARED_LIBS=True"

    if self.options.build_parallel:
      build_opts = "-- -j4"

    self.run('cmake "%s/g2o" %s %s' % (self.conanfile_directory, cmake.command_line, cmake_opts ))
    self.run('cmake --build . %s %s' % (cmake.build_config, build_opts))


  def package(self):
    self.copy("*.h", src="g2o", dst="include")
    self.copy("*.hpp", src="g2o", dst="include")
    self.copy("config.h", src="g2o", dst="include/g2o")
    if self.options.shared:
      if self.settings.os == "Macos":
          self.copy(pattern="*.dylib", dst="lib", src="g2o/lib", keep_path=False)
      else:
          self.copy(pattern="*.so*", dst="lib", src="g2o/lib", keep_path=False)
    else:
        self.copy(pattern="lib*.a", dst="lib", src="lib", keep_path=False)

  def package_info(self):
    ## I'm sure there's a much more compact python-ism for this (I could write the one-liner in Ruby...)
    libs = ["g2o_solver_eigen", \
                  "g2o_solver_pcg", "g2o_core", "g2o_solver_slam2d_linear",\
                  "g2o_csparse_extension", "g2o_solver_structure_only",\
                   "g2o_stuff", "g2o_types_data",\
                     "g2o_types_icp", "g2o_types_sba",\
                      "g2o_types_sclam2d", "g2o_types_sim3",\
                        "g2o_types_slam2d_addons", "g2o_solver_cholmod",\
                        "g2o_types_slam2d", "g2o_solver_csparse", "g2o_types_slam3d_addons",\
                         "g2o_solver_dense", "g2o_types_slam3d"]


    if self.settings.build_type == 'Debug':
     self.cpp_info.libs = [ name+"_d" for name in libs ]
    else:
      self.cpp_info.libs = libs
