'''
Test file for Project 1, Part1: TCP client/server
Jack Robertson
Selected functions tested
'''
from server import reverse

def testReverse(inStr, expected):
    '''
    Fxn: testReverse()
    Does: testst reverse(), server.py
    Params:
    * inStr: input string, 'a dog', 'A dog'
    * expected: expected result, 'god a', 'god A'
    returns: success 1/fail -1
    '''
    result = reverse(inStr)    
    print('Res:', result)

    if result == expected:
        return 1
    else:
        return -1



def main():
    res = testReverse('dog', 'GOD')
    res1 = testReverse('a dog', 'GOD A')
    res2 = testReverse('a dOg', 'GoD A')
    res3 = testReverse('a dOg 1', '1 GoD A')
    print(res, res1, res2, res3)



main()

