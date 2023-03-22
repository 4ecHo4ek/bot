import modules as mod


def readFile(fileName: str) -> tuple[str, int]:
    err = 0
    answer = ""
    
    if mod.os.path.exists(fileName):
        try:
            file = open(fileName,'r')
            answer = file.read()
            file.close()
        except:
            answer = f"could read fild {fileName}\n"
            err = 1
    else:
        answer = f"could not fild {fileName}\n"
        err = 1
    return(answer, err)







