import numpy as np


def userInput():
    try:
        (r, c) =(int(i) for i in input(f"\nPlease enter number of processes followed by number of resource types: \t").split())
        alloc = np.zeros((r,c))
        max = np.zeros((r,c))
        
        print(f"\nNow enter coefficients for each row of the Allocation Matrix separated by spaces.")
        for i in range(r):
            alloc[i] = np.array([int(i) for i in input(f"Enter row number {i+1}: \t").split()])
        
        print(f"\nNow enter coefficients for each row of the Maximum Matrix separated by spaces.")
        for i in range(r):
            max[i] = np.array([int(i) for i in input(f"Enter row number {i+1}: \t").split()])

        isSafe = input(f"\nEnter 'Yes' to ask about safe state (press enter if not.) \t")
        if isSafe.lower == "yes":
            pass
        avail = np.array([int(i) for i in input(f"Now enter the values of the available resources: \t\t").split()])
        
        isRequest = input(f"\nEnter 'Yes' to add additional inquiries (press enter if there aren't any.) \t")
        if isRequest.lower() == "yes":
            print(f"Enter process no. then ; then the resource values separated by a space: \t")
            requestId, requestTemp = input(f"For example 1 ; 0 4 2 0 means request (0, 4, 2, 0) arrives from process P1. \t").split(';')
            requestID = int(requestId)
            requestVal = np.array([int(i) for i in requestTemp.split()])
        
        else:    requestID, requestVal = -1, -1

    except:
        print("incorrect values entered try again.")    

    return alloc, max, avail, requestID, requestVal


def safety(alloc, need, avail):
    n,m = alloc.shape
    work = avail
    finish = np.zeros(n)
    sequence = []
    
    while 1:
        retry = 0
        for i in range(n):
            compare = need[i] <= work
            if finish[i] == 0 and compare.all():
                work = work + alloc[i]
                finish[i] = 1
                sequence.append(i)
                retry = 1
        if not retry:   break
    
    for i in finish:
        if not i:   return 0, 0
    return 1, sequence


def request(alloc, need, avail, requestVal, requestID ):
    while 1:
        compare1 = requestVal > need[requestID]
        if compare1.all():  return -1, 0
        
        compare2 = requestVal > avail
        if compare2.all():  pass

        avail = avail - requestVal
        alloc[requestID] = alloc[requestID] + requestVal
        need[requestID] = need[requestID] - requestVal
        
        answer, sequence = safety(alloc, need, avail)
        if answer:
            alloc[requestID] = requestVal
            return answer, sequence


alloc, max, avail, requestID, requestVal = userInput()
need = max - alloc
answer, sequence = safety(alloc, need, avail)

print(f"\n Need matrix = \n", need)
if requestID > -1 and answer:
    answer, sequence = request(alloc, need, avail, requestID, requestVal)
    out = "Error, process exceeded maximum claim." if answer == -1 else "Yes request can be granted with safe state, Safe state "
    if sequence:   out += "<P" + str(requestID) + "req, " + "".join((["P" + str(i) + ", " for i in sequence])).rstrip() + ">."
    print(out)
else:
    out = "Yes, safe state" if answer else "No, unsafe state."
    print(out)
    if sequence:   print("<" + "".join((["P" + str(i) + ", " for i in sequence])).rstrip() + ">.")
