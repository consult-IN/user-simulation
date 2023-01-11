import glob
import os
from random import randint

def ppgPrint(pathname):
    #Pfad wird in file gespeichert
    file = glob.glob(pathname + "/**/*"+ searchedFileFormat, recursive=True)
    c = 0

    #Wenn keine Dateien des typs searchedFileFormat gefunden werden, wird ein verzeichnis darüber geschaut
    while len(file) == 0:
        pathname = ""
        for i in pfadname[0:len(pfadname) - c]:
            pathname += i + "\\"
        c = c+1
        file = glob.glob(pathname + "/**/*" + searchedFileFormat,recursive=True)

    #Es wird ein zufälliges Element der liste ausgegeben
    i = randint(1, len(file))
    print(file[i])

    #def jpgPrint(pfad):
    #    textfiles = glob.glob(pfad + "/**/*.jpg", recursive=True)
    #    if len(textfiles) < 1:
    #        jpgPrint("C:\\Users\\")
    #    else:
    #        i = randint(1, len(textfiles))
    #        print(textfiles[i])


if __name__ == '__main__':
    user = os.getlogin()
    path = ""
    searchedFileFormat = ".jpg"

    pfadname = ("C:", "Users", user, "Desktop")
    for i in pfadname:
        path += i + "\\"
    ppgPrint(path)
