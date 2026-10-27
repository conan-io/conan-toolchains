include_guard()

# Find ccache executable
find_program(CCACHE_PROGRAM NAMES ccache)

if(CCACHE_PROGRAM)
    message(STATUS "ccache found: ${CCACHE_PROGRAM}, enabling via CMake launcher and environment.")
    if (CMAKE_GENERATOR MATCHES "Visual Studio")
        # Copy original ccache.exe and rename to cl.exe, this way intermediate cmd file is not needed
        file(COPY_FILE ${CCACHE_PROGRAM} ${CMAKE_BINARY_DIR}/cl.exe ONLY_IF_DIFFERENT)

        # Set Visual Studio global variables:
        # - Use above cl.exe (ccache.exe) as a compiler 
        # - Enable parallel compilation
        list(APPEND CMAKE_VS_GLOBALS
            "CLToolExe=cl.exe"
            "CLToolPath=${CMAKE_BINARY_DIR}"
            "UseMultiToolTask=true"
            "UseStructuredOutput=false"
        )
    elseif(CMAKE_GENERATOR MATCHES "Ninja" OR CMAKE_GENERATOR MATCHES "Unix Makefiles")
        message(STATUS "Using ccache as compiler launcher for Ninja or Makefiles.")
        set(CMAKE_CXX_COMPILER_LAUNCHER ${CCACHE_PROGRAM} CACHE FILEPATH "CXX compiler cache used" FORCE)
        set(CMAKE_C_COMPILER_LAUNCHER ${CCACHE_PROGRAM} CACHE FILEPATH "C compiler cache used" FORCE)
    else()
        message(WARNING "Unsupported generator for ccache integration: ${CMAKE_GENERATOR}. ccache will not be used.")
    endif()
else()
    message(WARNING "ccache not found. Not enabling ccache integration.")
endif()
