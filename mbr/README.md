# minimum bounding box - python
Minimum bounding box operations in python

# example
```py
box1 = MBR(0, 0, 0, 0)
box1.expand_include_xy(2, 2)
print box1  # POLYGON ((0 0, 0 2, 2 2, 2 0, 0 0))

box2 = MBR(0, 0, 2, 2)
print box2.equals(box1) # True
print box1.height       # 2
print box1.width        # 2
print box1.area         # 4
print box1.center       # (1.0, 1.0)

#let p = point(1.7, 1.5)
p = 1.7, 1.5
print box2.intersects_point(p) #True

box3 = MBR(1.7, 1.5, 3.0, 1.9)
box4 = MBR(2.5, 3, 4.0, 5.0)

#intersects & intersection 
print box2.intersects(box3) # True
iters, bln = box2.intersection(box3)
# mbr, intersects
# MBR (1.7, 1.5, 2.0, 1.9), True

print box2.intersects(box4) # False
inter, bln = box2.intersection(box4)
# MBR(nan, nan, nan, nan), False

print box1.distance(box4) #1.118

```
## methods 
```python
    as_poly_array(self)      # ((x, y),..., (x, y)) 
    is_point(self)           # bool  -> (height,width) == (0,0)
    clone(self)              # MBR(minx, miny, maxx, maxy)
    as_tuple(self)           # (minx, miny, maxx, maxy)
    equals(self, other)      # bool
    translate(self, dx, dy)  # bool
    intersection(self, other)# MBR, bool
    intersects_bounds(self, q1, q2)           # bool, q1 and q2 -> (x, y)
    contains(self, other)                     # bool
    contains_xy(self, x, y)                   # bool
    completely_contains_xy(self, x, y)        # bool
    completely_contains_mbr(self, other)      # bool
    disjoint(self, other)                     # bool
    intersects(self, other)                   # bool
    intersects_point(self, pt)                # bool, pt -> (x, y)
    expand_include_mbr(self, other)           # bool
    expand_by_delta(self, dx, dy)             # self
    expand_include_xy(self, x_coord, y_coord) # self 
    distance(self, other)                     # float 
    distance_square(self, other)              # float 
```

## properties
```python
    llur    # float
    width   # float
    height  # float
    area    # float
    center  # (float, float)
```

# lic
MIT