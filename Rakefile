
task :default => "debug:test"

@conan_opts = { shared: 'True', build_parallel: 'False' }
@conan_settings = {}
@conan_scopes = { build_tests: 'True' }
@conan_build = "missing"
load 'config.rb' if FileTest.readable? 'config.rb'

['Debug','Release'].each { |build_type|
  namespace build_type.downcase.to_sym do
    build_dir = ENV['BUILD_DIR'] || "build-#{build_type}"

    @conan_settings[:build_type] = build_type
    conan_opts = @conan_opts.each_pair.map { |key,val| "-o %s=%s" % [key,val] } +
                @conan_settings.each_pair.map { |key,val| "-s %s=%s" % [key,val] } +
                @conan_scopes.each_pair.map { |key,val| "--scope %s=%s" % [key,val] }

    task :build do
      FileUtils::mkdir build_dir unless FileTest::directory? build_dir
      sh "conan source ."
      chdir build_dir do
        sh "conan install %s .. --build=%s" % [conan_opts.join(' '), @conan_build]
        sh "conan build .."
      end
    end

    task :test => :build do
      #
    end
  end
}

namespace :conan do
  task :export do
    sh "conan export amarburg/testing"
  end

  task :upload do
    sh "conan upload g2o/master@amarburg/testing"
  end
end

namespace :dependencies do

  task :trusty do
    sh "sudo apt-get update"
    sh "sudo apt-get install -y cmake libeigen3-dev"
    sh "pip install conan"
  end

  task :osx do
    sh "brew update"
    # sh "brew tap homebrew/science"
    sh "brew install eigen"
    sh "pip install conan"
  end

  namespace :travis do
    task :linux => "dependencies:trusty"
    task :osx => "dependencies:osx" do
      ## Let's see what minimal configuration I can get away with
      mkdir "/Users/travis/.conan" unless FileTest::directory? ".conan"
      File.open("/Users/travis/.conan/conan.conf",'w') { |f|
        f.write <<CONAN_CONF_END
[storage]
path: ~/.conan/data

[proxies]

[settings_defaults]
arch=x86_64
build_type=Release
compiler=apple-clang
compiler.libcxx=libc++
compiler.version=7.3
os=Macos
CONAN_CONF_END
        }
        sh "cat $HOME/.conan/conan.conf"
      end
  end
end
