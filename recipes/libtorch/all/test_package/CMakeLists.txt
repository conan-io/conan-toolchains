cmake_minimum_required(VERSION 3.15)
project(PackageTest CXX)

find_package(libtorch CONFIG REQUIRED)


#https://pytorch.org/cppdocs/installing.html

add_executable(example src/example.cpp)
target_link_libraries(example  "$<LINK_LIBRARY:WHOLE_ARCHIVE,torch_cpu>" "$<LINK_LIBRARY:WHOLE_ARCHIVE,c10>" libtorch::libtorch)
