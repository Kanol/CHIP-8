from CPU import CPU
import sys
import tkinter


if __name__ == "__main__":
    try:
        if sys.argv[1] == "--help":
            print("CHIP-8 Emulator.\nUsage: CHIP_8.py PATH_TO_GAME [PIXEL SIZE]")
            exit()
    except IndexError:
        exit()
    cpu = CPU(tkinter)
    cpu.main()
