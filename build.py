from conan.packager import ConanMultiPackager

if __name__ == "__main__":
    builder = ConanMultiPackager()
    builder.add_common_builds(dll_with_static_runtime=True, pure_c=True)
    builder.run()
