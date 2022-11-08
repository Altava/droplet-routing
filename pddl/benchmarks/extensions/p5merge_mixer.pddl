(define (problem p5merge_mixer) (:domain p5merge_mixer-domain)

(:objects
    hcl kcl bovine gelatin firstmix1 firstmix2 secondmix1 - reagent
    xcoord ycoord - coordinate
    x1 x2 x3 x4 x5 x6 x7 x8 - xcoord
    y1 y2 y3 y4 y5 y6 y7 y8 - ycoord
)

(:init
    (MIX hcl kcl firstmix1)
    (MIX bovine gelatin firstmix2)
    (MIX firstmix1 firstmix2 secondmix1)
    (ISEAST x2 x1)
    (ISEAST x3 x2)
    (ISEAST x4 x3)
    (ISEAST x5 x4)
    (ISEAST x6 x5)
    (ISEAST x7 x6)
    (ISEAST x8 x7)
    (ISWEST x1 x2)
    (ISWEST x2 x3)
    (ISWEST x3 x4)
    (ISWEST x4 x5)
    (ISWEST x5 x6)
    (ISWEST x6 x7)
    (ISWEST x7 x8)
    (ISNORTH y2 y1)
    (ISNORTH y3 y2)
    (ISNORTH y4 y3)
    (ISNORTH y5 y4)
    (ISNORTH y6 y5)
    (ISNORTH y7 y6)
    (ISNORTH y8 y7)
    (ISSOUTH y1 y2)
    (ISSOUTH y2 y3)
    (ISSOUTH y3 y4)
    (ISSOUTH y4 y5)
    (ISSOUTH y5 y6)
    (ISSOUTH y6 y7)
    (ISSOUTH y7 y8)
    (VICINITY x1 y1 x1 y2)
    (VICINITY x1 y1 x2 y2)
    (VICINITY x1 y1 x2 y1)
    (VICINITY x1 y2 x1 y3)
    (VICINITY x1 y2 x2 y3)
    (VICINITY x1 y2 x1 y1)
    (VICINITY x1 y2 x2 y2)
    (VICINITY x1 y2 x2 y1)
    (VICINITY x1 y3 x1 y4)
    (VICINITY x1 y3 x2 y4)
    (VICINITY x1 y3 x1 y2)
    (VICINITY x1 y3 x2 y3)
    (VICINITY x1 y3 x2 y2)
    (VICINITY x1 y4 x1 y5)
    (VICINITY x1 y4 x2 y5)
    (VICINITY x1 y4 x1 y3)
    (VICINITY x1 y4 x2 y4)
    (VICINITY x1 y4 x2 y3)
    (VICINITY x1 y5 x1 y6)
    (VICINITY x1 y5 x2 y6)
    (VICINITY x1 y5 x1 y4)
    (VICINITY x1 y5 x2 y5)
    (VICINITY x1 y5 x2 y4)
    (VICINITY x1 y6 x1 y7)
    (VICINITY x1 y6 x2 y7)
    (VICINITY x1 y6 x1 y5)
    (VICINITY x1 y6 x2 y6)
    (VICINITY x1 y6 x2 y5)
    (VICINITY x1 y7 x1 y8)
    (VICINITY x1 y7 x2 y8)
    (VICINITY x1 y7 x1 y6)
    (VICINITY x1 y7 x2 y7)
    (VICINITY x1 y7 x2 y6)
    (VICINITY x1 y8 x1 y7)
    (VICINITY x1 y8 x2 y8)
    (VICINITY x1 y8 x2 y7)
    (VICINITY x2 y1 x2 y2)
    (VICINITY x2 y1 x3 y2)
    (VICINITY x2 y1 x3 y1)
    (VICINITY x2 y1 x1 y1)
    (VICINITY x2 y1 x1 y2)
    (VICINITY x2 y2 x2 y3)
    (VICINITY x2 y2 x3 y3)
    (VICINITY x2 y2 x2 y1)
    (VICINITY x2 y2 x1 y1)
    (VICINITY x2 y2 x3 y2)
    (VICINITY x2 y2 x3 y1)
    (VICINITY x2 y2 x1 y2)
    (VICINITY x2 y2 x1 y3)
    (VICINITY x2 y3 x2 y4)
    (VICINITY x2 y3 x3 y4)
    (VICINITY x2 y3 x2 y2)
    (VICINITY x2 y3 x1 y2)
    (VICINITY x2 y3 x3 y3)
    (VICINITY x2 y3 x3 y2)
    (VICINITY x2 y3 x1 y3)
    (VICINITY x2 y3 x1 y4)
    (VICINITY x2 y4 x2 y5)
    (VICINITY x2 y4 x3 y5)
    (VICINITY x2 y4 x2 y3)
    (VICINITY x2 y4 x1 y3)
    (VICINITY x2 y4 x3 y4)
    (VICINITY x2 y4 x3 y3)
    (VICINITY x2 y4 x1 y4)
    (VICINITY x2 y4 x1 y5)
    (VICINITY x2 y5 x2 y6)
    (VICINITY x2 y5 x3 y6)
    (VICINITY x2 y5 x2 y4)
    (VICINITY x2 y5 x1 y4)
    (VICINITY x2 y5 x3 y5)
    (VICINITY x2 y5 x3 y4)
    (VICINITY x2 y5 x1 y5)
    (VICINITY x2 y5 x1 y6)
    (VICINITY x2 y6 x2 y7)
    (VICINITY x2 y6 x3 y7)
    (VICINITY x2 y6 x2 y5)
    (VICINITY x2 y6 x1 y5)
    (VICINITY x2 y6 x3 y6)
    (VICINITY x2 y6 x3 y5)
    (VICINITY x2 y6 x1 y6)
    (VICINITY x2 y6 x1 y7)
    (VICINITY x2 y7 x2 y8)
    (VICINITY x2 y7 x3 y8)
    (VICINITY x2 y7 x2 y6)
    (VICINITY x2 y7 x1 y6)
    (VICINITY x2 y7 x3 y7)
    (VICINITY x2 y7 x3 y6)
    (VICINITY x2 y7 x1 y7)
    (VICINITY x2 y7 x1 y8)
    (VICINITY x2 y8 x2 y7)
    (VICINITY x2 y8 x1 y7)
    (VICINITY x2 y8 x3 y8)
    (VICINITY x2 y8 x3 y7)
    (VICINITY x2 y8 x1 y8)
    (VICINITY x3 y1 x3 y2)
    (VICINITY x3 y1 x4 y2)
    (VICINITY x3 y1 x4 y1)
    (VICINITY x3 y1 x2 y1)
    (VICINITY x3 y1 x2 y2)
    (VICINITY x3 y2 x3 y3)
    (VICINITY x3 y2 x4 y3)
    (VICINITY x3 y2 x3 y1)
    (VICINITY x3 y2 x2 y1)
    (VICINITY x3 y2 x4 y2)
    (VICINITY x3 y2 x4 y1)
    (VICINITY x3 y2 x2 y2)
    (VICINITY x3 y2 x2 y3)
    (VICINITY x3 y3 x3 y4)
    (VICINITY x3 y3 x4 y4)
    (VICINITY x3 y3 x3 y2)
    (VICINITY x3 y3 x2 y2)
    (VICINITY x3 y3 x4 y3)
    (VICINITY x3 y3 x4 y2)
    (VICINITY x3 y3 x2 y3)
    (VICINITY x3 y3 x2 y4)
    (VICINITY x3 y4 x3 y5)
    (VICINITY x3 y4 x4 y5)
    (VICINITY x3 y4 x3 y3)
    (VICINITY x3 y4 x2 y3)
    (VICINITY x3 y4 x4 y4)
    (VICINITY x3 y4 x4 y3)
    (VICINITY x3 y4 x2 y4)
    (VICINITY x3 y4 x2 y5)
    (VICINITY x3 y5 x3 y6)
    (VICINITY x3 y5 x4 y6)
    (VICINITY x3 y5 x3 y4)
    (VICINITY x3 y5 x2 y4)
    (VICINITY x3 y5 x4 y5)
    (VICINITY x3 y5 x4 y4)
    (VICINITY x3 y5 x2 y5)
    (VICINITY x3 y5 x2 y6)
    (VICINITY x3 y6 x3 y7)
    (VICINITY x3 y6 x4 y7)
    (VICINITY x3 y6 x3 y5)
    (VICINITY x3 y6 x2 y5)
    (VICINITY x3 y6 x4 y6)
    (VICINITY x3 y6 x4 y5)
    (VICINITY x3 y6 x2 y6)
    (VICINITY x3 y6 x2 y7)
    (VICINITY x3 y7 x3 y8)
    (VICINITY x3 y7 x4 y8)
    (VICINITY x3 y7 x3 y6)
    (VICINITY x3 y7 x2 y6)
    (VICINITY x3 y7 x4 y7)
    (VICINITY x3 y7 x4 y6)
    (VICINITY x3 y7 x2 y7)
    (VICINITY x3 y7 x2 y8)
    (VICINITY x3 y8 x3 y7)
    (VICINITY x3 y8 x2 y7)
    (VICINITY x3 y8 x4 y8)
    (VICINITY x3 y8 x4 y7)
    (VICINITY x3 y8 x2 y8)
    (VICINITY x4 y1 x4 y2)
    (VICINITY x4 y1 x5 y2)
    (VICINITY x4 y1 x5 y1)
    (VICINITY x4 y1 x3 y1)
    (VICINITY x4 y1 x3 y2)
    (VICINITY x4 y2 x4 y3)
    (VICINITY x4 y2 x5 y3)
    (VICINITY x4 y2 x4 y1)
    (VICINITY x4 y2 x3 y1)
    (VICINITY x4 y2 x5 y2)
    (VICINITY x4 y2 x5 y1)
    (VICINITY x4 y2 x3 y2)
    (VICINITY x4 y2 x3 y3)
    (VICINITY x4 y3 x4 y4)
    (VICINITY x4 y3 x5 y4)
    (VICINITY x4 y3 x4 y2)
    (VICINITY x4 y3 x3 y2)
    (VICINITY x4 y3 x5 y3)
    (VICINITY x4 y3 x5 y2)
    (VICINITY x4 y3 x3 y3)
    (VICINITY x4 y3 x3 y4)
    (VICINITY x4 y4 x4 y5)
    (VICINITY x4 y4 x5 y5)
    (VICINITY x4 y4 x4 y3)
    (VICINITY x4 y4 x3 y3)
    (VICINITY x4 y4 x5 y4)
    (VICINITY x4 y4 x5 y3)
    (VICINITY x4 y4 x3 y4)
    (VICINITY x4 y4 x3 y5)
    (VICINITY x4 y5 x4 y6)
    (VICINITY x4 y5 x5 y6)
    (VICINITY x4 y5 x4 y4)
    (VICINITY x4 y5 x3 y4)
    (VICINITY x4 y5 x5 y5)
    (VICINITY x4 y5 x5 y4)
    (VICINITY x4 y5 x3 y5)
    (VICINITY x4 y5 x3 y6)
    (VICINITY x4 y6 x4 y7)
    (VICINITY x4 y6 x5 y7)
    (VICINITY x4 y6 x4 y5)
    (VICINITY x4 y6 x3 y5)
    (VICINITY x4 y6 x5 y6)
    (VICINITY x4 y6 x5 y5)
    (VICINITY x4 y6 x3 y6)
    (VICINITY x4 y6 x3 y7)
    (VICINITY x4 y7 x4 y8)
    (VICINITY x4 y7 x5 y8)
    (VICINITY x4 y7 x4 y6)
    (VICINITY x4 y7 x3 y6)
    (VICINITY x4 y7 x5 y7)
    (VICINITY x4 y7 x5 y6)
    (VICINITY x4 y7 x3 y7)
    (VICINITY x4 y7 x3 y8)
    (VICINITY x4 y8 x4 y7)
    (VICINITY x4 y8 x3 y7)
    (VICINITY x4 y8 x5 y8)
    (VICINITY x4 y8 x5 y7)
    (VICINITY x4 y8 x3 y8)
    (VICINITY x5 y1 x5 y2)
    (VICINITY x5 y1 x6 y2)
    (VICINITY x5 y1 x6 y1)
    (VICINITY x5 y1 x4 y1)
    (VICINITY x5 y1 x4 y2)
    (VICINITY x5 y2 x5 y3)
    (VICINITY x5 y2 x6 y3)
    (VICINITY x5 y2 x5 y1)
    (VICINITY x5 y2 x4 y1)
    (VICINITY x5 y2 x6 y2)
    (VICINITY x5 y2 x6 y1)
    (VICINITY x5 y2 x4 y2)
    (VICINITY x5 y2 x4 y3)
    (VICINITY x5 y3 x5 y4)
    (VICINITY x5 y3 x6 y4)
    (VICINITY x5 y3 x5 y2)
    (VICINITY x5 y3 x4 y2)
    (VICINITY x5 y3 x6 y3)
    (VICINITY x5 y3 x6 y2)
    (VICINITY x5 y3 x4 y3)
    (VICINITY x5 y3 x4 y4)
    (VICINITY x5 y4 x5 y5)
    (VICINITY x5 y4 x6 y5)
    (VICINITY x5 y4 x5 y3)
    (VICINITY x5 y4 x4 y3)
    (VICINITY x5 y4 x6 y4)
    (VICINITY x5 y4 x6 y3)
    (VICINITY x5 y4 x4 y4)
    (VICINITY x5 y4 x4 y5)
    (VICINITY x5 y5 x5 y6)
    (VICINITY x5 y5 x6 y6)
    (VICINITY x5 y5 x5 y4)
    (VICINITY x5 y5 x4 y4)
    (VICINITY x5 y5 x6 y5)
    (VICINITY x5 y5 x6 y4)
    (VICINITY x5 y5 x4 y5)
    (VICINITY x5 y5 x4 y6)
    (VICINITY x5 y6 x5 y7)
    (VICINITY x5 y6 x6 y7)
    (VICINITY x5 y6 x5 y5)
    (VICINITY x5 y6 x4 y5)
    (VICINITY x5 y6 x6 y6)
    (VICINITY x5 y6 x6 y5)
    (VICINITY x5 y6 x4 y6)
    (VICINITY x5 y6 x4 y7)
    (VICINITY x5 y7 x5 y8)
    (VICINITY x5 y7 x6 y8)
    (VICINITY x5 y7 x5 y6)
    (VICINITY x5 y7 x4 y6)
    (VICINITY x5 y7 x6 y7)
    (VICINITY x5 y7 x6 y6)
    (VICINITY x5 y7 x4 y7)
    (VICINITY x5 y7 x4 y8)
    (VICINITY x5 y8 x5 y7)
    (VICINITY x5 y8 x4 y7)
    (VICINITY x5 y8 x6 y8)
    (VICINITY x5 y8 x6 y7)
    (VICINITY x5 y8 x4 y8)
    (VICINITY x6 y1 x6 y2)
    (VICINITY x6 y1 x7 y2)
    (VICINITY x6 y1 x7 y1)
    (VICINITY x6 y1 x5 y1)
    (VICINITY x6 y1 x5 y2)
    (VICINITY x6 y2 x6 y3)
    (VICINITY x6 y2 x7 y3)
    (VICINITY x6 y2 x6 y1)
    (VICINITY x6 y2 x5 y1)
    (VICINITY x6 y2 x7 y2)
    (VICINITY x6 y2 x7 y1)
    (VICINITY x6 y2 x5 y2)
    (VICINITY x6 y2 x5 y3)
    (VICINITY x6 y3 x6 y4)
    (VICINITY x6 y3 x7 y4)
    (VICINITY x6 y3 x6 y2)
    (VICINITY x6 y3 x5 y2)
    (VICINITY x6 y3 x7 y3)
    (VICINITY x6 y3 x7 y2)
    (VICINITY x6 y3 x5 y3)
    (VICINITY x6 y3 x5 y4)
    (VICINITY x6 y4 x6 y5)
    (VICINITY x6 y4 x7 y5)
    (VICINITY x6 y4 x6 y3)
    (VICINITY x6 y4 x5 y3)
    (VICINITY x6 y4 x7 y4)
    (VICINITY x6 y4 x7 y3)
    (VICINITY x6 y4 x5 y4)
    (VICINITY x6 y4 x5 y5)
    (VICINITY x6 y5 x6 y6)
    (VICINITY x6 y5 x7 y6)
    (VICINITY x6 y5 x6 y4)
    (VICINITY x6 y5 x5 y4)
    (VICINITY x6 y5 x7 y5)
    (VICINITY x6 y5 x7 y4)
    (VICINITY x6 y5 x5 y5)
    (VICINITY x6 y5 x5 y6)
    (VICINITY x6 y6 x6 y7)
    (VICINITY x6 y6 x7 y7)
    (VICINITY x6 y6 x6 y5)
    (VICINITY x6 y6 x5 y5)
    (VICINITY x6 y6 x7 y6)
    (VICINITY x6 y6 x7 y5)
    (VICINITY x6 y6 x5 y6)
    (VICINITY x6 y6 x5 y7)
    (VICINITY x6 y7 x6 y8)
    (VICINITY x6 y7 x7 y8)
    (VICINITY x6 y7 x6 y6)
    (VICINITY x6 y7 x5 y6)
    (VICINITY x6 y7 x7 y7)
    (VICINITY x6 y7 x7 y6)
    (VICINITY x6 y7 x5 y7)
    (VICINITY x6 y7 x5 y8)
    (VICINITY x6 y8 x6 y7)
    (VICINITY x6 y8 x5 y7)
    (VICINITY x6 y8 x7 y8)
    (VICINITY x6 y8 x7 y7)
    (VICINITY x6 y8 x5 y8)
    (VICINITY x7 y1 x7 y2)
    (VICINITY x7 y1 x8 y2)
    (VICINITY x7 y1 x8 y1)
    (VICINITY x7 y1 x6 y1)
    (VICINITY x7 y1 x6 y2)
    (VICINITY x7 y2 x7 y3)
    (VICINITY x7 y2 x8 y3)
    (VICINITY x7 y2 x7 y1)
    (VICINITY x7 y2 x6 y1)
    (VICINITY x7 y2 x8 y2)
    (VICINITY x7 y2 x8 y1)
    (VICINITY x7 y2 x6 y2)
    (VICINITY x7 y2 x6 y3)
    (VICINITY x7 y3 x7 y4)
    (VICINITY x7 y3 x8 y4)
    (VICINITY x7 y3 x7 y2)
    (VICINITY x7 y3 x6 y2)
    (VICINITY x7 y3 x8 y3)
    (VICINITY x7 y3 x8 y2)
    (VICINITY x7 y3 x6 y3)
    (VICINITY x7 y3 x6 y4)
    (VICINITY x7 y4 x7 y5)
    (VICINITY x7 y4 x8 y5)
    (VICINITY x7 y4 x7 y3)
    (VICINITY x7 y4 x6 y3)
    (VICINITY x7 y4 x8 y4)
    (VICINITY x7 y4 x8 y3)
    (VICINITY x7 y4 x6 y4)
    (VICINITY x7 y4 x6 y5)
    (VICINITY x7 y5 x7 y6)
    (VICINITY x7 y5 x8 y6)
    (VICINITY x7 y5 x7 y4)
    (VICINITY x7 y5 x6 y4)
    (VICINITY x7 y5 x8 y5)
    (VICINITY x7 y5 x8 y4)
    (VICINITY x7 y5 x6 y5)
    (VICINITY x7 y5 x6 y6)
    (VICINITY x7 y6 x7 y7)
    (VICINITY x7 y6 x8 y7)
    (VICINITY x7 y6 x7 y5)
    (VICINITY x7 y6 x6 y5)
    (VICINITY x7 y6 x8 y6)
    (VICINITY x7 y6 x8 y5)
    (VICINITY x7 y6 x6 y6)
    (VICINITY x7 y6 x6 y7)
    (VICINITY x7 y7 x7 y8)
    (VICINITY x7 y7 x8 y8)
    (VICINITY x7 y7 x7 y6)
    (VICINITY x7 y7 x6 y6)
    (VICINITY x7 y7 x8 y7)
    (VICINITY x7 y7 x8 y6)
    (VICINITY x7 y7 x6 y7)
    (VICINITY x7 y7 x6 y8)
    (VICINITY x7 y8 x7 y7)
    (VICINITY x7 y8 x6 y7)
    (VICINITY x7 y8 x8 y8)
    (VICINITY x7 y8 x8 y7)
    (VICINITY x7 y8 x6 y8)
    (VICINITY x8 y1 x8 y2)
    (VICINITY x8 y1 x7 y1)
    (VICINITY x8 y1 x7 y2)
    (VICINITY x8 y2 x8 y3)
    (VICINITY x8 y2 x8 y1)
    (VICINITY x8 y2 x7 y1)
    (VICINITY x8 y2 x7 y2)
    (VICINITY x8 y2 x7 y3)
    (VICINITY x8 y3 x8 y4)
    (VICINITY x8 y3 x8 y2)
    (VICINITY x8 y3 x7 y2)
    (VICINITY x8 y3 x7 y3)
    (VICINITY x8 y3 x7 y4)
    (VICINITY x8 y4 x8 y5)
    (VICINITY x8 y4 x8 y3)
    (VICINITY x8 y4 x7 y3)
    (VICINITY x8 y4 x7 y4)
    (VICINITY x8 y4 x7 y5)
    (VICINITY x8 y5 x8 y6)
    (VICINITY x8 y5 x8 y4)
    (VICINITY x8 y5 x7 y4)
    (VICINITY x8 y5 x7 y5)
    (VICINITY x8 y5 x7 y6)
    (VICINITY x8 y6 x8 y7)
    (VICINITY x8 y6 x8 y5)
    (VICINITY x8 y6 x7 y5)
    (VICINITY x8 y6 x7 y6)
    (VICINITY x8 y6 x7 y7)
    (VICINITY x8 y7 x8 y8)
    (VICINITY x8 y7 x8 y6)
    (VICINITY x8 y7 x7 y6)
    (VICINITY x8 y7 x7 y7)
    (VICINITY x8 y7 x7 y8)
    (VICINITY x8 y8 x8 y7)
    (VICINITY x8 y8 x7 y7)
    (VICINITY x8 y8 x7 y8)
)

(:goal (and
    (reagent-type secondmix1 x8 y1)
    (small x8 y1)
))

)
