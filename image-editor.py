import copy



#Invert Colors
def invert(img_matrix):
    '''
This function serves to reverse the colors within an image. It achieves this by subtracting each color component from 255.

Input is expected in the form of a 3D matrix, representing a .bmp image.
Each element of this matrix corresponds to a row of pixels in the image.
Within each row, elements represent individual pixels.
Pixels are defined as lists containing three numerical values, each ranging from 0 to 255, and following the order [red, green, blue].
Return Value:

The function outputs a 3D matrix of identical dimensions to the input.
However, the colors of each pixel in this output are inverted, offering a transformed image.


    '''

    m1 = len(img_matrix)
    m2 = len(img_matrix[0])
    m3 = len(img_matrix[0][0])
    for i in range(m1):
        for j in range(m2):
            for k in range(m3):
                img_matrix[i][j][k] = 255 - img_matrix[i][j][k]
    return img_matrix
  


# High Contrast
def high_contrast(img_matrix):
    '''
    
      For every pixel, sets each color component to 0 (if the original
      value was 127 or less), or 255 (if the original value was >= 128).
    
    '''
    m1 = len(img_matrix)
    m2 = len(img_matrix[0])
    m3 = len(img_matrix[0][0])

    for i in range(m1):
      for k in range(m2):
        for z in range(m3):
          if img_matrix[i][k][z] > 127:
            img_matrix[i][k][z] = 255
          else:
            img_matrix[i][k][z] = 0
    return img_matrix   

# Rotate Quadrants
def rotate_quadrants(img_matrix):
  
    '''
    Purpose:
      Split the image into four equally sized quadrants, and rotate
      them clockwise to form the output image.
    Input Parameter(s):
      (see invert) - plus, it can be assumed the img_matrix will have
      an even number of rows and columns.
    Return Value:
      A 3D matrix of the same dimensions, where each pixel has been moved
      to the corresponding location.  
    '''
    new_matrix = copy.deepcopy(img_matrix)
    height = len(img_matrix)
    width = len(img_matrix[0])
    height1 = height // 2
    width1 = width //2
    for i in range(height1):
      for j in range(width1):
        new_matrix[i][j] = img_matrix[int(i + height/2)][j]
        new_matrix[int(i + height/2)][j] = img_matrix[int(i + height/2)][int(j + width/2)]
        new_matrix[int(i + height/2)][int(j + width/2)] = img_matrix[i][int(j+width/2)]
        new_matrix[i][int(j+width/2)] = img_matrix[i][j]
    return new_matrix   
                

#App Specific Filter
def custom_filter(img_matrix):

    '''
 
      Creates a gradient by increasing a pixel's shade if it is on an odd position and setting every even position to 0.
    '''
    shade = 100

    m1 = len(img_matrix)
    m2 = len(img_matrix[0])
    m3 = len(img_matrix[0][0])

    for i in range(m1):
      for k in range(m2):
        for z in range(m3):
          if img_matrix[i][k][z] % 2 == 0:
            img_matrix[i][k][z] = 0
          if img_matrix[i][k][z] % 2 != 0:
               img_matrix[i][k][z] = shade
               shade += 1     
    return img_matrix  


# Swapping red and blue components
def swap_red_blue(img_matrix):
    '''
 
      Swaps the red and blue components in an image
   
    '''
    height = len(img_matrix)  #Height = # of rows, i.e. length of matrix
    width = len(img_matrix[0]) #Width = # of columns, i.e. length of one row
    for y in range(height):
        for x in range(width):
            # img_matrix[y][x] is a 3-element list representing the
            # [red, green, blue] values for the pixel at coordinates (x, y)
            old_red = img_matrix[y][x][0]
            old_blue = img_matrix[y][x][2]
            img_matrix[y][x][0] = old_blue
            img_matrix[y][x][2] = old_red
    return img_matrix


# Blur the image
def blur(img_matrix):
    '''

      Blurs an image by applying a 3x3 pixel filter
  
    '''
    height = len(img_matrix)
    width = len(img_matrix[0])
    #Make a deep copy of the matrix to use as our output matrix.
    #This is just a convenient way to get an output matrix of the same
    #dimensions as the original.
    new_matrix = copy.deepcopy(img_matrix)

    #Loops through every pixel we need to compute via (x, y) coordinates
    for y in range(height):
        for x in range(width):

            #To compute each pixel, for each of the three color components
            #take the average of that component for the surrounding 9 pixels
            new_pixel = [0, 0, 0]
            for j in range(-1,2):  #Loop through y-1, y, y+1
                for i in range(-1,2):  #Loop through x-1, x, x+1
                    for color in range(3):
                        #If x+i or y+j is out of bounds, ignore it
                        if 0 <= x+i < width and 0 <= y+j < height:
                            new_pixel[color] += img_matrix[y+j][x+i][color]/9

            #Averaging might result in a float, so truncate down to nearest int
            for color in range(3):
                new_pixel[color] = int(new_pixel[color])

            #Replace pixel in output matrix
            new_matrix[y][x] = new_pixel
    return new_matrix



#--------------------------------------------------
# 
# .bmp file manipulation functions.  
#--------------------------------------------------

def big_end_to_int(ls):
    '''
    Byte conversion helper 
    Purpose:
      Compute the integer represented by a sequence of bytes
    Input Parameter(s):
      A list of bytes (integers between 0 and 255), in big-endian order
    Return Value:
      Integer value that the bytes represent
    '''
    total = 0
    for ele in ls[::-1]:
        total *= 256
        total += ele
    return total

def transform_image(fname,operation):
    '''
    .bmp conversion function
    Purpose:
      Turns a .bmp file into a matrix of pixel values, performs an operation
      on it, and then converts it back into a new .bmp file
    Input Parameter(s):
      fname, a string representing a file name in the current directory
      operation, a string representing the operation to be performed on the
      image. 
    Return Value:
      None
    '''
    #Open file in read bytes mode, get bytes specifying width/height
    fp = open(fname,'rb')
    data = list(fp.read())
    old_data = list(data)
    width = big_end_to_int(data[18:22])
    height = big_end_to_int(data[22:26])

    #Data starts at byte 54.  Create matrix of pixels, where each
    #pixel is a 3 element list [red,green,blue].
    #Starts in lower left corner of image.
    i = 54
    matrix = []
    for y in range(height):
        row = []
        for x in range(width):
            pixel = [data[i+2],data[i+1],data[i]]
            i += 3
            row.append(pixel)
        matrix.append(row)
        #Row size must be divisible by 4, otherwise padding occurs
        i += (2-i)%4
    fp.close()

    #Perform operation on the pixel matrix
    if operation == 'invert':
        new_matrix = invert(matrix[::-1])
    elif operation == 'high_contrast':
        new_matrix = high_contrast(matrix[::-1])
    elif operation == 'custom_filter':
        new_matrix = custom_filter(matrix[::-1])
    elif operation == 'rotate_quadrants':
        new_matrix = rotate_quadrants(matrix[::-1])
    elif operation == 'blur':
        new_matrix = blur(matrix[::-1])
    elif operation == 'swap_red_blue':
        new_matrix = swap_red_blue(matrix[::-1])
    else:
        return
    new_matrix = new_matrix[::-1]
    #Write back to new .bmp file.
    #New file name is operation+fname
    i = 54
    for y in range(height):
        for x in range(width):
            pixel = tuple(new_matrix[y][x])
            data[i+2],data[i+1],data[i] = pixel
            i += 3
        i += (2-i)%4
    fp = open(operation+"_"+fname,'wb')
    fp.write(bytearray(data))
    fp.close()


