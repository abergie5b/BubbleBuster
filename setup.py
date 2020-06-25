from cx_Freeze import setup, Executable

setup(
    executables=[Executable("main.py")],
    options=dict(build_exe=dict(include_files=['resources/']))
    )

