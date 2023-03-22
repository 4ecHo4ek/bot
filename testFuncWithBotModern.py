import modules as mod


        
def mainFunc(fileName: str) -> None:
    data, err =mod.common.readFile(fileName)
    if err:
        print(data)
        exit
    print(data)




if __name__ == "__main__":
    if len (mod.sys.argv) > 1:
        mainFunc(str(mod.sys.argv[1]))
    else:
        print ("give values file")






# # def func(value: type) -> type:
# #     ...
# #     return(value, err)




