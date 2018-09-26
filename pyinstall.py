import  os
if __name__ == '__main__':
    from PyInstaller.__main__ import run
    opts=['main.py','-w','-F','--icon=ai.ico']
    run(opts)
