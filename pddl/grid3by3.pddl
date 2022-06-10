(define (problem grid3by3) (:domain grid_3x3)

(:objects
    droplet1 droplet2 - droplet
)

(:init
    (droplet-at droplet1 x1 y1)
    (occupied x1 y1)
    (droplet-at droplet2 x3 y3)
    (occupied x3 y3)
)
(:goal (and
    (droplet-at droplet1 x3 y3)
    (droplet-at droplet2 x1 y1)
))
)
