from scipy import stats
speed = [99,86,87,88,111,86,103,87,94,78,77,85,86]
x = stats.mode(speed)

print(x)
# ModeResult(mode=array([86]), count=array([3]))
# The mode() method returns a ModeResult object that contains the mode number (86), and count (how many times the mode number appeared (3)).