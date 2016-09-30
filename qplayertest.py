from qplayer import QPlayer

# Test highestQvalue() method
qplay = QPlayer()
qplay.addState((1,-1,0), {0:1.0, 1:0.5, 2:0.1})

print qplay.highestQValue((1,-1,0))

qplay.reverseTableStates()
qplay.prettyprintTable()