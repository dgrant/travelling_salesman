from numpy import sqrt
import random, Image, ImageDraw, ImageFont
import logging
from numpy import zeros, e

reload(logging)
logging.basicConfig(format='%(asctime)s - %(levelname)-6s - %(name)-10s:\n%(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
logger = logging.getLogger('myLogger')
logger.setLevel(logging.DEBUG)

def cartesian_matrixDict(coords):
    '''create a distance matrix for the city coords
      that uses straight line distance'''
    matrix={}
    for i,(x1,y1) in enumerate(coords):
        for j,(x2,y2) in enumerate(coords):
            dx,dy=x1-x2,y1-y2
            dist=sqrt(dx*dx + dy*dy)
            matrix[i,j]=dist
    return matrix

def cartesian_matrixList(coords):
    '''create a distance matrix for the city coords
      that uses straight line distance'''
    matrix=[[0]*len(coords) for x in xrange(len(coords))]
    for i,(x1,y1) in enumerate(coords):
        for j,(x2,y2) in enumerate(coords):
            dx,dy = x1-x2, y1-y2
            dist = sqrt(dx*dx + dy*dy)
            matrix[i][j] = dist
    return matrix

def cartesian_matrixNumPy(coords):
    '''create a distance matrix for the city coords
      that uses straight line distance'''
    matrix=zeros((len(coords), len(coords)), int)
    for i,(x1,y1) in enumerate(coords):
        for j,(x2,y2) in enumerate(coords):
            dx,dy = x1-x2, y1-y2
            dist = sqrt(dx*dx + dy*dy)
            matrix[i,j] = dist
    return matrix

cartesian_matrix = cartesian_matrixNumPy

def read_coords(coord_file):
    coords=[]
    for line in coord_file:
        x,y=line.strip().split(',')
        coords.append((float(x),float(y)))
    return coords

def tour_lengthDict(matrix, tour):
    total = 0
    num_cities = len(tour)
    for i in range(num_cities):
        j = (i+1) % num_cities
        city_i = tour[i]
        city_j = tour[j]
        total += matrix[city_i, city_j]
    return total

def tour_lengthList(matrix, tour):
    total = 0
    num_cities = len(tour)
    for i in range(num_cities):
        j = (i+1) % num_cities
        city_i = tour[i]
        city_j = tour[j]
        total += matrix[city_i][city_j]
    return total

def tour_lengthNumPy(matrix, tour):
    return matrix[tour,tour[1:]+tour[:1]].sum()

tour_length = tour_lengthNumPy

def all_pairs(size,shuffle=random.shuffle):
    r1=range(size)
    r2=range(size)
    if shuffle:
        shuffle(r1)
        shuffle(r2)
    for i in r1:
        for j in r2:
            yield (i,j)

def swapped_cities(tour):
    '''generator to create all possible variations
      where two cities have been swapped'''
    for i,j in all_pairs(len(tour)):
        if i < j:
            copy=tour[:]
            copy[i],copy[j]=tour[j],tour[i]
            yield copy

def reversed_sections(tour):
    '''generator to return all possible variations
      where the section between two cities are swapped'''
    for i,j in all_pairs(len(tour)):
        if i != j:
            copy=tour[:]
            if i < j:
                copy[i:j+1]=reversed(tour[i:j+1])
            else:
                copy[i+1:]=reversed(tour[:j])
                copy[:j]=reversed(tour[i+1:])
            if copy != tour: # no point returning the same tour
                yield copy
    
def random_reversed_section(tour):
    i = random.randint(0,len(tour)-1)
    j = random.randint(0,len(tour)-1)
    copy=tour[:]
    if i < j:
        copy[i:j+1]=reversed(tour[i:j+1])
    else:
        copy[i+1:]=reversed(tour[:j])
        copy[:j]=reversed(tour[i+1:])
    return copy

def write_tour_to_img(coords,tour,img_file):
    padding=20
    # shift all coords in a bit
    coords=[(x+padding,y+padding) for (x,y) in coords]
    maxx,maxy=0,0
    for x,y in coords:
        maxx=max(x,maxx)
        maxy=max(y,maxy)
    maxx+=padding
    maxy+=padding
    img=Image.new("RGB",(int(maxx),int(maxy)),color=(255,255,255))

    font=ImageFont.load_default()
    d=ImageDraw.Draw(img);
    num_cities=len(tour)
    for i in range(num_cities):
        j=(i+1)%num_cities
        city_i=tour[i]
        city_j=tour[j]
        x1,y1=coords[city_i]
        x2,y2=coords[city_j]
        d.line((int(x1),int(y1),int(x2),int(y2)),fill=(0,0,0))
        d.text((int(x1)+7,int(y1)-5),str(i),font=font,fill=(32,32,32))

    #for x,y in coords:
     #   x,y=int(x),int(y)
      #  d.ellipse((x-5,y-5,x+5,y+5),outline=(0,0,0),fill=(196,196,196))
    del d
    img.save(img_file, "PNG")

def randomCoords(num, max):
    coords = set()
    while len(coords) < num:
        coords.add((random.randint(0, max-1), random.randint(0, max-1)))
    return coords

#def solve_greedy(coords):
    #matrix = cartesian_matrix(coords)
    #tour = range(len(coords))
    #tourLength = tour_length(matrix, tour)
    #someImprovement = True
    #logger.debug("starting tour="+str(tour))
    #logger.debug("starting tour length="+str(tourLength))
    #while someImprovement:
        #someImprovement = False
        #bestPermLength = 1e99
        #bestPerm = []
        ##find the best permutation among all permutations
        #for perm in reversed_sections(tour):
            #permLength = tour_length(matrix, perm)
            #if permLength < bestPermLength:
                #bestPerm = perm
                #bestPermLength = permLength
        ##if the best permutation is better than the current tour, replace it
        #if bestPermLength < tourLength:
            #tourLength = bestPermLength
            #tour = bestPerm
            #logger.debug("better tour="+str(tour))
            #logger.debug("better tour length="+str(tourLength))
            #someImprovement = True
    #return tour

def random_tour(tour_length):
    tour = range(tour_length)
    random.shuffle(tour)
    return tour

def solve_greedySimple(coords, maxIters):
    matrix = cartesian_matrix(coords)
    bestTour = random_tour(len(coords))
    bestLength = tour_length(matrix, bestTour)
    someImprovement = True
    logger.debug("starting tour="+str(bestTour))
    logger.debug("starting tour length="+str(bestLength))
    numIters = 0
    while someImprovement and numIters < maxIters:
        someImprovement = False
        #go to the first improved permutation
        for perm in reversed_sections(bestTour):
            permLength = tour_length(matrix, perm)
            #if the best permutation is better than the current tour, replace it
            if permLength < bestLength:
                bestLength = permLength
                bestTour = perm
                logger.debug("better tour="+str(bestTour))
                logger.debug("better tour length="+str(bestLength))         
                someImprovement = True
                break
        numIters += 1
    return bestTour

def solve_annealing(coords, maxIters, maxCostDiff):
    Temp = maxCostDiff/3.0
    matrix = cartesian_matrix(coords)

    currTour = random_tour(len(coords))
    currLength = tour_length(matrix, currTour)

    bestLength = 1e99
    someImprovement = True
    logger.debug("starting tour="+str(currTour))
    logger.debug("starting tour length="+str(currLength))
    numIters = 0
    while numIters < maxIters:
        perm = random_reversed_section(currTour)
        permLength = tour_length(matrix, perm)
        #decide whether to accept this move
        try:
            probability = e**((permLength - currLength)/Temp)
        except OverflowError:
            probability = 0
        logger.debug("probability="+str(probability))
        if permLength < currLength or probability > random.random():
            currtour = perm
            currLength = permLength
            logger.debug("new current tour="+str(currTour))
            logger.debug("new current tour length="+str(currLength))
        #if the best permutation is better than the best ever tour, replace it
        if permLength < bestLength:
            bestLength = permLength
            bestTour = perm
            logger.debug("new best tour="+str(bestTour))
            logger.debug("new best tour length="+str(bestLength))         
        numIters += 1
        Temp -= maxCostDiff/float(maxIters)
    return bestTour

#misc reading from file type stuff
#cities = ['0,0','100,0','100,100']
#coords = read_coords(cities)


#print "swapped cities"
#for x in swapped_cities(tour):
    #print x

#tour = range(10)
#random.seed(100)
#coords = [x for x in randomCoords(10, 1000)]
#print "reversed sections"
#for x in reversed_sections(tour):
    #print x

#random.seed(100)
coords = [x for x in randomCoords(10, 1000)]
tour = solve_annealing(coords, 100000, 1000*1.414)

write_tour_to_img(coords, tour, 'out.png')
