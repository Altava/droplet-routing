(define (problem 3by3grid) (:domain grid)
(:objects 
    x1
    x2
    x3
    y1
    y2
    y3
    droplet1
    droplet2
)

(:init
    (droplet-at ?droplet1 ?x1 ?y1)
    (droplet-at ?droplet2 ?x3 ?y3)
    (occupied ?x1 ?y1)
    (occupied ?x3 ?y3)

    (NEIGHBOUR ?x1 ?y1 ?x1 ?y2)
    (NEIGHBOUR ?x1 ?y1 ?x2 ?y1)
    (NEIGHBOUR ?x1 ?y2 ?x1 ?y3)
    (NEIGHBOUR ?x1 ?y2 ?x1 ?y1)
    (NEIGHBOUR ?x1 ?y2 ?x2 ?y2)
    (NEIGHBOUR ?x1 ?y3 ?x1 ?y2)
    (NEIGHBOUR ?x1 ?y3 ?x2 ?y3)
    (NEIGHBOUR ?x2 ?y1 ?x2 ?y2)
    (NEIGHBOUR ?x2 ?y1 ?x3 ?y1)
    (NEIGHBOUR ?x2 ?y1 ?x1 ?y1)
    (NEIGHBOUR ?x2 ?y2 ?x2 ?y3)
    (NEIGHBOUR ?x2 ?y2 ?x2 ?y1)
    (NEIGHBOUR ?x2 ?y2 ?x3 ?y2)
    (NEIGHBOUR ?x2 ?y2 ?x1 ?y2)
    (NEIGHBOUR ?x2 ?y3 ?x2 ?y2)
    (NEIGHBOUR ?x2 ?y3 ?x3 ?y3)
    (NEIGHBOUR ?x2 ?y3 ?x1 ?y3)
    (NEIGHBOUR ?x3 ?y1 ?x3 ?y2)
    (NEIGHBOUR ?x3 ?y1 ?x2 ?y1)
    (NEIGHBOUR ?x3 ?y2 ?x3 ?y3)
    (NEIGHBOUR ?x3 ?y2 ?x3 ?y1)
    (NEIGHBOUR ?x3 ?y2 ?x2 ?y2)
    (NEIGHBOUR ?x3 ?y3 ?x3 ?y2)
    (NEIGHBOUR ?x3 ?y3 ?x2 ?y3)

Process finished with exit code 0


)

(:goal (and
    ;todo: put the goal condition here
))

;un-comment the following line if metric is needed
;(:metric minimize (???))
)
