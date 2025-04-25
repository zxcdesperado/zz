import os

T = 100 # Reduce this value for debugging purposes.
def clear(directory):
    f = open(directory, "w")
    f.write("")
    f.close()

def compare(directory1, directory2):
    f1 = open(directory1, "r")
    f2 = open(directory2, "r")
    res = 0
    if(f1.readlines() != f2.readlines()):
        res = 1    
    f1.close()
    f2.close()
    return res

def test_diff(directory):
    tmp_score = 0
    simulators = os.listdir(directory)
    base_score = 20 // len(simulators)
    for simulator in simulators:
        simulator = os.path.join(directory, simulator)
        flag = 0
        for t in range(T):
            clear("1.in")
            os.system("python generator_diff.py " + str(t) + " 1.in")
            clear("1.out")
            clear("2.out")
            os.system("python simulator_correct.py 1.in 1.out")
            os.system("python " + simulator + " 1.in 2.out")
            flag |= compare("1.out", "2.out")
        if flag:
            tmp_score += base_score
    return tmp_score

def test_meta(directory):
    tmp_score = 0
    simulators = os.listdir(directory)
    base_score = 20 // len(simulators)
    for simulator in simulators:
        simulator = os.path.join(directory, simulator)
        flag = 0
        tpcount = 0
        fpcount = 0
        for t in range(T):
            clear("1.in")
            clear("2.in")

            is_p = 0
            os.system("python generator_meta.py " + str(t) + " 1.in 2.in")
            
            clear("1.out")
            clear("2.out")
            os.system("python " + simulator + " 1.in 1.out")
            os.system("python simulator_correct.py 1.in 2.out")
            is_p |= compare("1.out", "2.out")

            clear("1.out")
            clear("2.out")
            os.system("python " + simulator + " 2.in 1.out")
            os.system("python simulator_correct.py 2.in 2.out")
            is_p |= compare("1.out", "2.out")

            clear("1.out")
            clear("2.out")
            os.system("python " + simulator + " 1.in 1.out")
            os.system("python " + simulator + " 2.in 2.out")

            clear("res.out")
            os.system("python checker.py " + str(t) +" 1.out 2.out res.out")

            resf = open("res.out", "r")
            flag = resf.readline()
            try:
                flag = int(flag)
                if flag != 0 and flag != 1:
                    return 0
            except:
                return 0
            
            if flag == 1:
                if is_p:
                    tpcount += 1
                else:
                    fpcount += 1

        tmp_score += base_score * tpcount / max(tpcount + fpcount , 1)
    return tmp_score

if __name__ == '__main__':
    buggy_diff_score = test_diff("simulator_buggy")
    buggy_meta_score = test_meta("simulator_buggy")
    score = buggy_diff_score + buggy_meta_score
    print("total grade %d out of 40" % score)

    