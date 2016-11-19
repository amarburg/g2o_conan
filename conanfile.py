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
    cmake_opts = ""
    build_opts = ""

    if self.options.shared:
      cmake_opts = "-DBUILD_SHARED_LIBS=True"

    if self.options.build_parallel:
      build_opts = "-- -j"

    self.run('cmake "%s/g2o" %s %s' % (self.conanfile_directory, cmake.command_line, cmake_opts ))
    self.run('cmake --build . %s %s' % (cmake.build_config, build_opts))


  def package(self):
    self.copy("*.h", src="g2o", dst="include")
    self.copy("*.hpp", src="g2o", dst="include")
    self.copy("config.h", src="g2o", dst="include/g2o")
    if self.options.shared:
      if self.settings.os == "Macos":
          self.copy(pattern="*.dylib", dst="lib", keep_path=False)
      else:
          self.copy(pattern="*.so*", dst="lib", src="lib", keep_path=False)
    else:
        self.copy(pattern="*.a", dst="lib", src="lib", keep_path=False)

  def package_info(self):
      self.cpp_info.libs = ["g2o_calibration_odom_laser", "g2o_solver_eigen", "g2o_cli" ,\
                      "g2o_solver_pcg", "g2o_core", "g2o_solver_slam2d_linear",\
                      "g2o_csparse_extension", "g2o_solver_structure_only",\
                       "g2o_ext_freeglut_minimal", "g2o_stuff", "g2o_hierarchical",\
                        "g2o_tutorial_slam2d", "g2o_incremental", "g2o_typesata",\
                         "g2o_interactive", "g2o_types_icp", "g2o_interface", "g2o_types_sba",\
                          "g2o_opengl_helper", "g2o_types_sclam2d", "g2o_parser", "g2o_types_sim3",\
                           "g2o_simulator", "g2o_types_slam2d_addons", "g2o_solver_cholmod",\
                            "g2o_types_slam2d", "g2o_solver_csparse", "g2o_types_slam3d_addons",\
                             "g2o_solverense", "g2o_types_slam3d"]
