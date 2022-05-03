# Building Ship of Harkinian

 1. Install [Python](https://www.python.org/ftp/python/3.10.2/python-3.10.2-amd64.exe)
 2. Install [Visual Studio 2022 Community Edition](https://visualstudio.microsoft.com/vs/community/)
 2b. In the Visual Studio Installer, install `MSVC v142 - VS 2019 C++`.
 4. Clone the Ship of Harkinian repository.
 5. Place one or more [compatible](#compatible-roms) roms in the `OTRExporter` directory with namings of your choice.
 6. Run `OTRExporter/OTRExporter.sln`.
 7. Switch the solution to `Release x64`.
 8. Build the solution. 
 9. Launching `OTRExporter/extract_assets.py` will generate an `oot.otr` archive file in `OTRExporter/oot.otr`.
 10. Run `soh/soh.sln`
 11. Switch the solution to `Release x86`.
 12. Build the solution.
 13. Copy the `OTRExporter/oot.otr` archive file to `soh/Release`.
 14. Launch `soh.exe`.

## Compatible Roms
```
OOT_PAL_GC      checksum 0x09465AC3
OOT_PAL_GC_DBG1 checksum 0x871E1C92 (debug non-master quest)
```

# OTRExporter Usage

The OTRExporter generates the `oot.otr` archive required to play Ship of Harkinian. The `extract_assets.py` script file runs the exporter.

This script may be activated using the following methods:
1) Double clicking after placing rom in the same directory as the script.
2) Drag and Dropping a rom onto the script
3) In terminal using `python3 extract_assets.py`
4) In terminal using `python3 extract_assets.py rom_name.z64`

If multiple roms are in the directory the user will be prompted which to use.
