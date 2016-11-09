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
      self.cpp_info.libs = ["g2o_calibration_odom_laser_d", "g2o_solver_eigen_d", "g2o_cli_d" ,\
                      "g2o_solver_pcg_d", "g2o_core_d", "g2o_solver_slam2d_linear_d",\
                      "g2o_csparse_extension_d", "g2o_solver_structure_only_d",\
                       "g2o_ext_freeglut_minimal_d", "g2o_stuff_d", "g2o_hierarchical_d",\
                        "g2o_tutorial_slam2d_d", "g2o_incremental_d", "g2o_types_data_d",\
                         "g2o_interactive_d", "g2o_types_icp_d", "g2o_interface_d", "g2o_types_sba_d",\
                          "g2o_opengl_helper_d", "g2o_types_sclam2d_d", "g2o_parser_d", "g2o_types_sim3_d",\
                           "g2o_simulator_d", "g2o_types_slam2d_addons_d", "g2o_solver_cholmod_d",\
                            "g2o_types_slam2d_d", "g2o_solver_csparse_d", "g2o_types_slam3d_addons_d",\
                             "libg2o_solver_dense_d", "libg2o_types_slam3d_d"]
