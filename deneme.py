import re
import numpy

def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

#print(findWholeWord('seek')('those who seek shall find'))

a = numpy.asarray([ [1,2,3], [4,5,6], [7,8,9] ])
#numpy.savetxt("foo.csv", a, delimiter=",")


a = "Bağlar Cad. Cad Cd cd cd. Ethem Köslü Sok. No13 Seyranbağları /  ANKARA"
kom = re.split('.  |\ ', a)
print(kom)

out = map(lambda x:x.lower(), kom)

print ("Cad." in list(out))