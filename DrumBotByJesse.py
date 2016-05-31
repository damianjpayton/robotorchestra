# DrumBot by Jesse Zaman
import explorerhat
from time import sleep
import threading

# status is set to true to play. When false, the sticks don't move
status = False
speed = 100

# IGNORE, This is just to test whether text of form '0.3' can be converted into number 0.3
def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False


# Drumsticks have to move to make sound, so we first have to 'raise' the stick before we strike the drum
# to ensure that we hit the drum each time, we only 'raise' the stick a bit, and go forward way to much.
# e.g. if you look to the code: we go backwards only for 0.05 seconds, then go forwards for 0.15 seconds to hit the drum

# Drum 1
def drumOne():
	explorerhat.motor.one.forward(100)
	sleep(0.05)
	explorerhat.motor.one.stop()
	explorerhat.motor.one.backward(100)
	sleep(0.15)
	explorerhat.motor.one.stop()
	
# Drum 2
def drumTwo():
	explorerhat.motor.two.backward(100)
	sleep(0.05)
	explorerhat.motor.two.stop()
	explorerhat.motor.two.forward(100)
	sleep(0.15)
	explorerhat.motor.two.stop()

# Make in instrument play for a certain BPM. <instrument> has to be the function drumOne or DrumTwo
# e.g. bpm (drumOne, 132)
# This function is not entirely correct. Each drumswing takes 0.2 seconds, which is not taken into account
# Had no time to fix this
def bpm(instrument, bpm):
        global status
        status = True
        while status:
            instrument()
            sleep((60 / bpm) - 0.1)

# Used by playPatternEndlessly to make a drum play a certain beat pattern
def analysePattern(string, instrument):
	array = string.split('/')
	
	def processMove(arrayOfMoves):
		if arrayOfMoves != []:
			currentMove = arrayOfMoves[0]
			if currentMove == '*':
				instrument()
			elif isfloat(currentMove):
				sleep(float(currentMove))
			else:
				print ("Skipping unknown instruction")
			arrayOfMoves.pop(0)
			processMove(arrayOfMoves)

	processMove(array) 

# Make a certain instrument play a certain pattern
# Patterns have to be of shape '*/1/*/0.5'
# Where * = Drumbeat
#       / = just to indicate the seperation to the next move
#       0.5 = time to wait between beats
def playPatternEndlessly(pattern, instrument):
    while status:
        analysePattern(pattern, instrument)
        #analysePattern('*/0.05/*', drumTwo)

# Instruments when pressing button 1    
def buttonOne(channel, event):
    global status
    status = not status
    t= threading.Thread(target=playPatternEndlessly, args=('0.2/*',drumTwo))
    t.start()
    t= threading.Thread(target=playPatternEndlessly, args=('*/0.2',drumOne))
    t.start()

#instrument by pressing button 2
def buttonTwo(channel, event):
    global status
    status = not status
    t= threading.Thread(target=playPatternEndlessly, args=('*/0.2',drumTwo))
    t.start()
    t= threading.Thread(target=playPatternEndlessly, args=('*/0.4/*/*/0.4',drumOne))
    t.start()

#instrument by pressing button 2
def buttonThree(channel, event):
    global status
    status = not status
    t= threading.Thread(target=playPatternEndlessly, args=('*/0.2',drumTwo))
    t.start()
    t= threading.Thread(target=playPatternEndlessly, args=('*/0.4/*/0.4/*/*',drumOne))
    t.start()

#instrument by pressing button 2
def buttonFour(channel, event):
    global status
    status = not status
    t= threading.Thread(target=playPatternEndlessly, args=('*/0.2/*/*/0.2',drumTwo))
    t.start()
    t= threading.Thread(target=playPatternEndlessly, args=('*/0.4/*/*',drumOne))
    t.start()


explorerhat.touch.one.pressed(buttonOne)
explorerhat.touch.two.pressed(buttonTwo)
explorerhat.touch.three.pressed(buttonThree)
explorerhat.touch.four.pressed(buttonFour)



                            
