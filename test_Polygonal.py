#
# Mario h.c.t.
# Testing if function to test point in polygon works properly
#

import Polygonal

fence = [(50.863862, 4.67886),(50.863613,  4.678992),(50.863613, 4.678625),(50.863789, 4.678523),(50.863862, 4.678861)]


def test_point_in_poly():
    pointX = 46.27007
    pointY = 5.188
    fence = [(46.270088180220725, 5.184173583984375),
             (46.322274857040256, 5.33111572265625),
             (46.323223245368716, 5.42449951171875),
             (46.283376780187226, 5.447845458984375),
             (46.249199583637726, 5.384674072265625)]

    assert Polygonal.point_in_poly(pointX, pointY, fence) == True

def test_point_outside():
    pointX = 50.863777
    pointY = 4.679216

    assert Polygonal.point_in_poly(pointX, pointY, fence) == False

def test_cm_to_dd_basic():
    cm = 11.132
    assert abs(0.000001 - Polygonal.centimetersToDecimalDegrees(cm)) < 0.0000001

def test_cm_to_dd_big1():
    cm = 111.32
    assert abs(0.00001 - Polygonal.centimetersToDecimalDegrees(cm)) < 0.0000001

def test_from_flight1():
    lat=50.863831
    lon=4.6788333
    assert Polygonal.point_in_poly(lat, lon, fence) == True

#     lat=50.863831
#     lon=4.6788333,alt=8.48999977112,is_relative=False
# 8.35429392742e-06

# def test_random_coordinate():
#     r = 50.000003
#     import random
#     random.seed(10)
#     (x,y) = Polygonal.random_coordinate(1)
#
#     assert (x,y) == (1,1)


def test_points_in_poly():
    fence = [(50.863862, 4.678861),(50.863613,  4.678992),(50.863613, 4.678625),(50.863809, 4.678590),(50.863862, 4.678861)]
    assert Polygonal.points_in_poly(Polygonal.random_coordinates((0,0), 0.000001, 100), fence) == False

def test_points_in_poly():
    fence = [(50.863862, 4.678861),(50.863613,  4.678992),(50.863613, 4.678625),(50.863809, 4.678590),(50.863862, 4.678861)]
    assert Polygonal.points_in_poly(Polygonal.random_coordinates((50.863743, 4.678677), 0.000001, 100), fence) == True

def test_points_in_poly():
    fence = [(50.863862, 4.678861),(50.863613,  4.678992),(50.863613, 4.678625),(50.863809, 4.678590),(50.863862, 4.678861)]
    assert Polygonal.points_in_poly(Polygonal.random_coordinates((50.863743, 4.678677), 0.000110, 200), fence) == False


def test_random_coordinate():
    r = 1

    x = "x <- c("
    y = "y <- c("

    for i in range(1,2000):
        p = Polygonal.random_coordinate(r)
        x += str(p[0]) + ",\n"
        y += str(p[1]) + ",\n"

    x = x[0:len(x)-2] + ");"
    y = y[0:len(y)-2] + ");"


    f = open("circle.txt", 'w')
    f.write(x)
    f.write(y)
    f.close()


def test_random_coordinate_3d():
    r = 1

    x = "x <- c("
    y = "y <- c("
    z = "z <- c("

    for i in range(1,2000):
        p = Polygonal.random_coordinate_3d(r)
        x += str(p[0]) + ",\n"
        y += str(p[1]) + ",\n"
        z += str(p[2]) + ",\n"

    x = x[0:len(x)-2] + ");"
    y = y[0:len(y)-2] + ");"
    z = z[0:len(y)-2] + ");"

    graph = "par(pty='s');plot3d(x,y,z,pch='.');"

    f = open("sphere.r", 'w')
    f.write(x)
    f.write(y)
    f.write(z)
    f.write(graph)
    f.close()


#
# I am running this test visually in RStudio
# TODO fix it and check probabilities here
#
def test_bla():
    center = (50.863862, 4.678861)
    r = 0.000001
    n = 400
    points = Polygonal.random_coordinates(center, r, n)
    x_vector = 'x <- c('
    y_vector = 'y <- c('
    for x,y in points:
        x_vector += str(x) + ",\n"
        y_vector += str(y) + ",\n"

    print x_vector
    print y_vector

#test_bla()
