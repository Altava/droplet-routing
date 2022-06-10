(define (problem grid3by3) (:domain grid)
(:objects 
    droplet1 droplet2 - droplet
)

(:init
    (droplet-at droplet1 x2 y2)
    (droplet-at droplet2 x4 y4)
    (occupied x2 y2)
    (occupied x4 y4)
)

(:goal (and
    (droplet-at droplet1 x2 y3)
    (droplet-at droplet2 x4 y4)
))
)
