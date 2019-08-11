if __name__ == "__main__":
    import os
    import json
    import subprocess

    #MonteCarloAgent
    mapping_method = {'1': 'RLAgent', '2': 'MonteCarloAgent'}
    mapping_succ = {'1': 0, '2': 0}
    pre_cmd = "python -m connectfour.game --player-one {0} --player-two {1} --no-graphics --fast --auto-close"\
        .format(mapping_method['1'], mapping_method['2'])
    round = 100
    os.system("rm -rf *.log")
    process_list = []
    for i in range(round):
        print("start round: {}".format(i+1))
        cmd = "numactl --physcpubind {} {} 2>&1 | tee run_{}.log".format(i, pre_cmd, i)
        print("cmd is {}".format(cmd))
        process_list.append(subprocess.Popen(cmd, shell=True))
    for p in process_list:
        p.wait()
    none_count = 0
    for i in range(round):
        with open("run_{}.log".format(i)) as f:
            lines = f.readlines()
            print(str(json.loads(lines[0].strip("\n"))['winner_id']))
            try:
                mapping_succ[str(json.loads(lines[0].strip("\n"))['winner_id'])] += 1
            except:
                none_count += 1
    round = round - none_count
    print("win rate of method {0} is: {1}%".format(mapping_method['1'], float(mapping_succ['1'])/round*100))
    print("win rate of method {0} is: {1}%".format(mapping_method['2'], float(mapping_succ['2'])/round*100))


