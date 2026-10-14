name = "rhubarb"

# NOTE: version = <maya_release>.sse.<sse_patch>
version = "1.14.0.sse.1.0.0"

description = \
    """
    rez wrapper for Rhubarb Lip Sync. Thi is a command-line tool that automatically creates 2D mouth
    animation from voice recordings. It analyses a WAVE or Ogg Vorbis file and
    emits timed mouth cues - shapes A-F, plus the optional extended shapes G, H
    and X.

    Consumed by sse_maya_lipsync. MIT licensed.
    """

with scope("config") as c:
    import os
    c.release_packages_path = os.environ["SSE_REZ_REPO_RELEASE_EXT"]

requires = [
]

private_build_requires = [
]

variants = [
]

build_command = "rez python {root}/rez_build.py"
uuid = "repository.maya"


def commands():

    # NOTE: REZ package versions can have ".sse." to separate the external
    # version from the internal modification version.
    split_versions = str(version).split(".sse.")
    external_version = split_versions[0]
    internal_version = None
    if len(split_versions) == 2:
        internal_version = split_versions[1]

    env.REZ_RHUBARB_ROOT = "{root}"

    rez_softwares = "/mnt/rez/usd_pipe_rocky/softwares/binaries"
    installation_root = rez_softwares + "/Rhubarb-Lip-Sync/" + external_version

    env.RHUBARB_ROOT = installation_root

    # NOTE: rhubarb resolves its pocketSphinx model data from res/ relative to
    # the executable, so {root}/bin holds both `rhubarb` and `res/`. Never copy
    # the binary elsewhere on its own - it will fail at recognition time with an
    # error that does not mention the missing data.
    env.RHUBARB_EXECUTABLE = installation_root + "/rhubarb"
    env.PATH.append("{root}")
