find_package(cpr REQUIRED)

set(CMAKE_CXX_STANDARD 20)

target_link_libraries(${PROJECT_NAME} PRIVATE cpr::cpr)
add_executable(trader trader.cc)
target_link_libraries(trader PRIVATE cpr::cpr)

# compile with -O3
set(CMAKE_CXX_FLAGS_RELEASE "-O3")