import test01

def main():
    test01.print_input("This works, yay!!!")

if __name__ == '__main__':
    with open("myDict.json") as readFile:
        # converts json into dictionary
        main()