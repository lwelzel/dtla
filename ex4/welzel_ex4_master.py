# run this to have all code run
# the .png files have proper labeling etc so they are probably nicer to look at than the .fits

def main():
    print("   ---===### QUESTION 1 ###===---   \n\n")
    import welzel_ex4_q1
    print("\n\n   ---===### QUESTION 2 ###===---   \n\n")
    import welzel_ex4_q2
    print("\n\n   ---===### QUESTION 3 ###===---   \n\n")
    import welzel_ex4_q3
    print("\n\n   ---===### QUESTION 4 ###===---   \n\n")
    import welzel_ex4_q4
    print("\n\n   ---===###  FINISHED  ###===---   \n\n")


if __name__ == '__main__':
    import os
    print(os.getcwd())
    main()