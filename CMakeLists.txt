cmake_minimum_required(VERSION 3.24)

include(appInfo.cmake)

project(${appName})

# Build and install main executable
add_subdirectory(rhubarb)

##############################################################
# REZ
# The extras are not built here.
#   * extras/EsotericSoftwareSpine needs a JDK, which this build
#     environment deliberately does not carry.
#   * The After Effects and Magix Vegas extras are Windows-only
#     authoring-tool scripts and are dead weight in a Linux rez
#     package.
# Only the `rhubarb` CLI is packaged; sse_maya_lipsync drives it.
##############################################################
# add_subdirectory("extras/AdobeAfterEffects")
# add_subdirectory("extras/MagixVegas")
# add_subdirectory("extras/EsotericSoftwareSpine")

# Install misc. files
install(
	FILES README.adoc LICENSE.md CHANGELOG.md
	DESTINATION .
)

# Configure CPack
function(get_short_system_name variable)
	if ("${CMAKE_SYSTEM_NAME}" STREQUAL "Darwin")
		set(${variable} "macOS" PARENT_SCOPE)
	else()
		set(${variable} "${CMAKE_SYSTEM_NAME}" PARENT_SCOPE)
	endif()
endfunction()

set(CPACK_PACKAGE_NAME ${appName})
string(REPLACE " " "-" CPACK_PACKAGE_NAME "${CPACK_PACKAGE_NAME}")
get_short_system_name(CPACK_SYSTEM_NAME)
set(CPACK_PACKAGE_VERSION_MAJOR ${appVersionMajor})
set(CPACK_PACKAGE_VERSION_MINOR ${appVersionMinor})
set(CPACK_PACKAGE_VERSION_PATCH ${appVersionPatch})
set(CPACK_PACKAGE_VERSION ${appVersion})
set(CPACK_PACKAGE_FILE_NAME "${CPACK_PACKAGE_NAME}-${CPACK_PACKAGE_VERSION}-${CPACK_SYSTEM_NAME}")
set(CPACK_GENERATOR ZIP)

# Run CPack
include(CPack)
