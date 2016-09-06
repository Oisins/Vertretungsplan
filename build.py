# -*- coding: utf-8 -*-
from cx_Freeze import setup, Executable


include_files = ["config.py", "upload.py", "config.json"]
buildOptions = dict(
    include_files=include_files
)

executables = [
    Executable(
        script='VertretungPlan.py',
        targetName='VertretungsPlan.exe',
        base="Win32GUI"  # THIS ONE IS IMPORTANT FOR GUI APPLICATION
    )
]

setup(
    name="VertretungsPlan",
    version="1.0",
    description="Vertretungsplan uploader",
    options=dict(build_exe=buildOptions),
    executables=executables
)