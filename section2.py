# Section 2

def get_array(n): # create array

    # initializing the array with zeros
    arrayNxN = [[0] * n for _ in range(n)]
    init_number = 1
    steps = 1
    directions = [[0,1],[1,0],[0,-1],[-1,0]] # right, down, left, up
    dir = 0
    current_direction = directions[dir]

    # define initial coordinates
    if n % 2 == 0:
        x = y = n // 2 - 1
    else:
        x = y = n // 2

    # main loop
    temp = 0
    current_step = 0
    for i in range(n*n):
            arrayNxN[x][y] = init_number # put a number in our current location x y
            init_number += 1
            current_step += 1
            # do a step in a current direction
            x += current_direction[0]
            y += current_direction[1]

            if current_step == steps: # change the direction
                temp += 1
                current_step = 0
                if dir == 3:
                    dir = 0
                else:
                    dir += 1
                current_direction = directions[dir]

            if temp == 2: # add number of steps every 2 changed directions
                temp = 0
                steps += 1

    return arrayNxN

def diagonals_sum(array):
    d1 = d2 = 0

    # primary diagonal sum(d1)
    for i in range(len(array)):
         d1 += array[i][i]
              
    # secondary diagonal sum(d2)
    for i in range(len(array)):
         d2 += array[i][len(array) - 1 - i]
   

    return d1, d2
     

# Main

#----------------------------------------------
# Test part 1
n = int(input("Enter the N(NxN array): "))
array = get_array(n)
# display the array
for row in array:
     print(row)
#----------------------------------------------

#----------------------------------------------
# Test part 2
d1, d2 = diagonals_sum(array)
print("Primary diagonal elements sum: " + str(d1))
print("Secondary diagonal elements sum: " + str(d2))
#----------------------------------------------