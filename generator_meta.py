import sys

def generator(t):

    # Implement your code here.
    # Do not modify the main function.
    # You may define additional helper functions if needed.
    
    return "2 2", "3 3" 

if __name__ == '__main__':

    t = sys.argv[1]
    outname1 = sys.argv[2]
    outname2 = sys.argv[3]
    fout1 = open(outname1, "w")
    fout2 = open(outname2, "w")
    s1, s2 = generator(t)
    fout1.write(s1)
    fout2.write(s2)
    fout1.close()
    fout2.close()