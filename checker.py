import sys

def check(t, s1, s2):
    
    # Implement your code here.
    # Do not modify the main function.
    # You may define additional helper functions if needed.
    return '1'
    '''
    return '0' if you assume there is no bug triggered
    return '1' if you assume there is bug triggered
    '''

if __name__ == '__main__':

    t = sys.argv[1]
    inname1 = sys.argv[2]
    inname2 = sys.argv[3]
    outname = sys.argv[4]
    fin1 = open(inname1, "r")
    fin2 = open(inname2, "r")
    s1 = fin1.readlines()
    s2 = fin2.readlines()
    fin1.close()
    fin2.close()
    fout = open(outname, "w")
    fout.write(check(t, s1, s2))
    fout.close()