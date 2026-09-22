name = "rhubarb"

version = "1.14.0.sse.1.0.0"

description = \
    """
    Rhubarb Lip Sync is a command-line tool that automatically creates 2D mouth
    animation from voice recordings. It analyses a WAVE or Ogg Vorbis file and
    emits timed mouth cues - shapes A-F, plus the optional extended shapes G, H
    and X.

    Consumed by sse_maya_lipsync. MIT licensed.
    """

authors = ["Daniel S. Wolf"]

with scope("config") as c:
    import os
    c.release_packages_path = os.environ["SSE_REZ_REPO_RELEASE_EXT"]

# NOTE: Boost headers only - the source does find_package(Boost 1.54 REQUIRED)
# and links Boost::headers. sphinxbase, pocketsphinx, vorbis, ogg, utfcpp,
# utf8proc and gtest are all vendored under rhubarb/lib and built statically, so
# there is nothing else to resolve.
requires = [
    "boost-1.82",
]

# NOTE: The root CMakeLists declares cmake_minimum_required(VERSION 3.24). The
# README's "CMake 3.10+" is out of date, and Rocky 9 has no system cmake.
private_build_requires = [
    "cmake-3.29+",
]

# No Python linkage and no DCC coupling, so one build serves every environment.
variants = []

build_system = "cmake"

uuid = "repository.rhubarb"


def pre_build_commands():

    info = {}
    with open("/etc/os-release", 'r') as f:
        for line in f.readlines():
            if line.startswith('#'):
                continue
            line_info = line.replace('\n', '').split('=')
            if len(line_info) != 2:
                continue
            info[line_info[0]] = line_info[1].replace('"', '')
    linux_distro = info.get("NAME", "centos")
    print("Using Linux distro: " + linux_distro)

    if linux_distro.lower().startswith("centos"):
        # C++17 needs a newer toolchain than CentOS 7 ships.
        command("source /opt/rh/devtoolset-6/enable")
    elif linux_distro.lower().startswith("rocky"):
        # Rocky 9 ships gcc 11.5, which covers C++17.
        pass


def commands():
    env.RHUBARB_ROOT = "{root}"

    # NOTE: rhubarb resolves its pocketSphinx model data from res/ relative to
    # the executable, so {root}/bin holds both `rhubarb` and `res/`. Never copy
    # the binary elsewhere on its own - it will fail at recognition time with an
    # error that does not mention the missing data.
    env.RHUBARB_EXECUTABLE = "{root}/bin/rhubarb"
    env.PATH.append("{root}/bin")
