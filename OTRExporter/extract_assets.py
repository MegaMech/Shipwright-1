#!/usr/bin/env python3

import argparse, json, os, signal, time, sys, shutil, glob
from multiprocessing import Pool, cpu_count, Event, Manager, ProcessError
from enum import Enum
import shutil

romVer = "..\\soh\\baserom_non_mq.z64"
roms = [];
checksums = ["", "", ""];

class Checksums(Enum):
    OOT_NTSC_10 = "EC7011B7"
    OOT_NTSC_11 = "D43DA81F"
    OOT_NTSC_12 = "693BA2AE"
    OOT_PAL_10 = "B044B569"
    OOT_PAL_11 = "B2055FBD"
    OOT_NTSC_JP_GC_CE = "F7F52DB8"
    OOT_NTSC_JP_GC = "F611F4BA"
    OOT_NTSC_US_GC = "F3DD35BA"
    OOT_PAL_GC = "09465AC3"
    OOT_NTSC_JP_MQ = "F43B45BA"
    OOT_NTSC_US_MQ = "F034001A"
    OOT_PAL_MQ = "1D4136F3"
    OOT_PAL_GC_DBG1 = "871E1C92"
    OOT_PAL_GC_DBG2 = "87121EFE"
    OOT_PAL_GC_MQ_DBG = "917D18F6"
    OOT_IQUE_TW = "3D81FB3E"
    OOT_IQUE_CN = "B1E1E07B"
    OOT_UNKNOWN = "FFFFFFFF"
    
CompatibleChecksums = [
    Checksums.OOT_PAL_GC,
    Checksums.OOT_PAL_GC_DBG1
]

def BuildOTR(xmlPath, rom):
    shutil.copytree("assets", "Extract/assets")

    execStr = "x64\\Release\\ZAPD.exe" if sys.platform == "win32" else "../ZAPD/ZAPD.out"    
    execStr += " ed -i %s -b %s -fl CFG\\filelists -o placeholder -osf placeholder -gsf 1 -rconf CFG/Config.xml -se OTR" % (xmlPath, rom)

    print(execStr)
    exitValue = os.system(execStr)
    if exitValue != 0:
        print("\n")
        print("Error when building the OTR file...", file=os.sys.stderr)
        print("Aborting...", file=os.sys.stderr)
        print("\n")

def checkChecksum(rom):
    r = open(rom, "rb")
    r.seek(16)
    bytes = r.read(4).hex().upper()
    r.close()
    
    for checksum in Checksums:
        if (checksum.value == bytes):
            
            for compat in CompatibleChecksums:
                if (checksum.name == compat.name):
                    print("Compatible rom found!")   
                    return checksum
            print("Valid oot rom found. However, not compatible with SoH.")
            print("Compatible roms:")
            for compat in CompatibleChecksums:
                print(compat.name+" | 0x"+compat.value)
            sys.exit(1)
            
    print("Wrong rom! No valid checksum found")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="baserom asset extractor")
    parser.add_argument("-v", "--version", help="Sets game version.")
    args = parser.parse_args()
    
    romToUse = "";
    
    for file in glob.glob("*.z64"):
        roms.append(file)
        
    if not (roms):
        print("Error: No roms located, place one in the OTRExporter directory", file=os.sys.stderr)
        sys.exit(1)
        
    if (len(roms) > 1):
    
        print(str(len(roms))+" roms found, please select one by pressing 1-"+str(len(roms)))
        
        for list in range(len(roms)):
            print(roms[list])
            
        while(1):
            try:
                selection = int(input())
            except:
                print("Bad input. Try again with the number keys.")
                continue
                
            if (selection < 1 or selection > len(roms)):
                print("Bad input. Try again.")
                continue
            
            else: break
            
        romToUse = roms[selection - 1]
        
    else:
        romToUse = roms[0]
        
    validRom = checkChecksum(romToUse)
    
    match validRom.name:
        case Checksums.OOT_PAL_GC:
            xmlVer = "GC_NMQ_PAL_F"
        case Checksums.OOT_PAL_GC_DBG1:
            xmlVer = "GC_MQ_D"
        case _: # default case
            xmlVer = "GC_NMQ_D"

    if (os.path.exists("Extract")):
        shutil.rmtree("Extract")
    
    BuildOTR("..\\soh\\assets\\xml\\" + xmlVer + "\\", romToUse)

if __name__ == "__main__":
    main()
