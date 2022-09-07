(define (domain p3x3d3-domain)

(:requirements :strips :typing :conditional-effects :negative-preconditions :disjunctive-preconditions :universal-preconditions)

(:types
    droplet coordinate - object
    xcoord ycoord - coordinate
    x1 x2 x3 - xcoord
    y1 y2 y3 - ycoord
)

(:predicates
    (droplet-at ?d - droplet ?x - xcoord ?y - ycoord)
    (occupied ?x - xcoord ?y - ycoord)
    (VICINITY ?xo - xcoord ?yo - ycoord ?xt - xcoord ?yt - ycoord)
    (NEIGHBOUR ?xo - xcoord ?yo - ycoord ?xt - xcoord ?yt - ycoord)
    (blocked ?x - xcoord ?y - ycoord)
    (MIX ?d1 ?d2 ?dt - droplet)
)

(:functions
    (mix_completion ?d - droplet)
)

(:action move
    :parameters (?d - droplet ?xo ?xt - xcoord ?yo ?yt - ycoord)
    :precondition (and
        (droplet-at ?d ?xo ?yo)
        (NEIGHBOUR ?xo ?yo ?xt ?yt)
        (not (blocked ?xt ?yt))
        (forall (?x - xcoord)
          (forall (?y - ycoord)
            (imply (and
                (not (and (= ?x ?xo) (= ?y ?yo)))
                (VICINITY ?x ?y ?xt ?yt)
            )
                (not (occupied ?x ?y))
            )
          )
        )
    )
    :effect (and
        (not (droplet-at ?d ?xo ?yo))
        (droplet-at ?d ?xt ?yt)
        (not (occupied ?xo ?yo))
        (occupied ?xt ?yt)
    )
)

(:action merge
    :parameters (?d1 ?d2 ?d3 - droplet ?x1 ?x2 ?xt - xcoord ?y1 ?y2 ?yt - ycoord)
    :precondition (and
        (droplet-at ?d1 ?x1 ?y1)
        (droplet-at ?d2 ?x2 ?y2)
        (NEIGHBOUR ?x1 ?y1 ?xt ?yt)
        (NEIGHBOUR ?x2 ?y2 ?xt ?yt)
        (not (blocked ?xt ?yt))
        (MIX ?d1 ?d2 ?d3)
    )
    :effect (and 
        (not (droplet-at ?d1 ?x1 ?y1))
        (not (droplet-at ?d2 ?x2 ?y2))
        (droplet-at ?d3 ?xt ?yt)
        (not (occupied ?x1 ?y1))
        (not (occupied ?x2 ?y2))
        (occupied ?xt ?yt)
    )
)

)