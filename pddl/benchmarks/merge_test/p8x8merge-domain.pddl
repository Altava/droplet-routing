(define (domain p8x8d8n-domain)

(:requirements :strips :typing :conditional-effects :negative-preconditions :disjunctive-preconditions :universal-preconditions)

(:types
    droplet coordinate - object
    xcoord ycoord - coordinate
    x1 x2 x3 x4 x5 x6 x7 x8 - xcoord
    y1 y2 y3 y4 y5 y6 y7 y8 - ycoord
)

(:predicates
    (droplet-at ?d - droplet ?x - xcoord ?y - ycoord)
    (occupied ?x - xcoord ?y - ycoord)
    (VICINITY ?xo - xcoord ?yo - ycoord ?xt - xcoord ?yt - ycoord)
    (NEIGHBOUR ?xo - xcoord ?yo - ycoord ?xt - xcoord ?yt - ycoord)
    (blocked ?x - xcoord ?y - ycoord)
    (MIX ?d1 ?d2 ?dt - droplet)
    (small ?d - droplet)
)

(:action spawn_HCL
    :parameters ()
    :precondition (and
        (not (occupied x1 y6))
        (not (occupied x1 y7))
        (not (occupied x1 y8))
        (not (occupied x2 y6))
        (not (occupied x2 y7))
        (not (occupied x2 y8))
    )
    :effect (and
        (droplet-at droplet11 x1 y7)
        (occupied x1 y7)
        (small droplet11)
    )
)

(:action spawn_KCL
    :parameters ()
    :precondition (and
        (not (occupied x1 y7))
        (not (occupied x2 y7))
        (not (occupied x3 y7))
        (not (occupied x1 y8))
        (not (occupied x2 y8))
        (not (occupied x3 y8))
    )
    :effect (and
        (droplet-at droplet12 x2 y8)
        (occupied x2 y8)
        (small droplet12)
    )
)

(:action spawn_Bovine
    :parameters ()
    :precondition (and
        (not (occupied x6 y7))
        (not (occupied x7 y7))
        (not (occupied x8 y7))
        (not (occupied x6 y8))
        (not (occupied x7 y8))
        (not (occupied x8 y8))
    )
    :effect (and
        (droplet-at droplet13 x7 y8)
        (occupied x7 y8)
        (small droplet13)
    )
)

(:action spawn_Gelatin
    :parameters ()
    :precondition (and
        (not (occupied x7 y6))
        (not (occupied x7 y7))
        (not (occupied x7 y8))
        (not (occupied x8 y6))
        (not (occupied x8 y7))
        (not (occupied x8 y8))
    )
    :effect (and
        (droplet-at droplet14 x8 y7)
        (occupied x8 y7)
        (small droplet14)
    )
)

(:action spawn_Primer
    :parameters ()
    :precondition (and
        (not (occupied x1 y1))
        (not (occupied x1 y2))
        (not (occupied x1 y3))
        (not (occupied x2 y1))
        (not (occupied x2 y2))
        (not (occupied x2 y3))
    )
    :effect (and
        (droplet-at droplet15 x1 y2)
        (occupied x1 y2)
        (small droplet15)
    )
)

(:action spawn_Beosynucleotide
    :parameters ()
    :precondition (and
        (not (occupied x1 y1))
        (not (occupied x2 y1))
        (not (occupied x3 y1))
        (not (occupied x1 y2))
        (not (occupied x2 y2))
        (not (occupied x3 y2))
    )
    :effect (and
        (droplet-at droplet16 x2 y1)
        (occupied x2 y1)
        (small droplet16)
    )
)

(:action spawn_AmpliTag
    :parameters ()
    :precondition (and
        (not (occupied x6 y1))
        (not (occupied x7 y1))
        (not (occupied x8 y1))
        (not (occupied x6 y2))
        (not (occupied x7 y2))
        (not (occupied x8 y2))
    )
    :effect (and
        (droplet-at droplet17 x7 y1)
        (occupied x7 y1)
        (small droplet17)
    )
)

(:action spawn_LamdaDNA
    :parameters ()
    :precondition (and
        (not (occupied x7 y1))
        (not (occupied x7 y2))
        (not (occupied x7 y3))
        (not (occupied x8 y1))
        (not (occupied x8 y2))
        (not (occupied x8 y3))
    )
    :effect (and
        (droplet-at droplet18 x8 y2)
        (occupied x8 y2)
        (small droplet18)
    )
)

(:action dispose
    :parameters (?d - droplet)
    :precondition (and 
        (droplet-at ?d x8 y4)
    )
    :effect (and
        (not (droplet-at ?d x8 y4))
        (not (occupied x8 y4))
    )
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

(:action merge_x
    :parameters (?d1 ?d2 ?d3 - droplet ?x1 ?x2 ?xt - xcoord ?yt - ycoord)
    :precondition (and
        (droplet-at ?d1 ?x1 ?yt)
        (droplet-at ?d2 ?x2 ?yt)
        (small ?d1)
        (small ?d2)
        (NEIGHBOUR ?x1 ?yt ?xt ?yt)
        (NEIGHBOUR ?x2 ?yt ?xt ?yt)
        (not (blocked ?xt ?yt))
        (MIX ?d1 ?d2 ?d3)
    )
    :effect (and
        (not (droplet-at ?d1 ?x1 ?yt))
        (not (droplet-at ?d2 ?x2 ?yt))
        (droplet-at ?d3 ?xt ?yt)
        (not (occupied ?x1 ?yt))
        (not (occupied ?x2 ?yt))
        (occupied ?xt ?yt)
    )
)

(:action merge_y
    :parameters (?d1 ?d2 ?d3 - droplet ?xt - xcoord ?y1 ?y2 ?yt - ycoord)
    :precondition (and
        (droplet-at ?d1 ?xt ?y1)
        (droplet-at ?d2 ?xt ?y2)
        (small ?d1)
        (small ?d2)
        (NEIGHBOUR ?xt ?y1 ?xt ?yt)
        (NEIGHBOUR ?xt ?y2 ?xt ?yt)
        (not (blocked ?xt ?yt))
        (MIX ?d1 ?d2 ?d3)
    )
    :effect (and
        (not (droplet-at ?d1 ?xt ?y1))
        (not (droplet-at ?d2 ?xt ?y2))
        (droplet-at ?d3 ?xt ?yt)
        (not (occupied ?xt ?y1))
        (not (occupied ?xt ?y2))
        (occupied ?xt ?yt)
    )
)

(:action split_x
    :parameters (?d - droplet ?xo ?xl ?xr - xcoord ?yo - ycoord)
    :precondition (and
        (droplet-at ?d ?xo ?yo)
        (NEIGHBOUR ?xo ?yo ?xl ?yo)
        (NEIGHBOUR ?xo ?yo ?xr ?yo)
        (not (= ?xl ?xr))
        (not (small ?d))
        (forall (?x - xcoord)
          (forall (?y - ycoord)
            (imply (and
                (not (and (= ?x ?xo) (= ?y ?yo)))
                (or
                    (VICINITY ?x ?y ?xl ?yo)
                    (VICINITY ?x ?y ?xr ?yo)
                )
            )
                (not (occupied ?x ?y))
            )
          )
        )
    )
    :effect (and
        (not (droplet-at ?d ?xo ?yo))
        (not (occupied ?xo ?yo))
        (small ?d)
        (droplet-at ?d ?xl ?yo)
        (occupied ?xl ?yo)
        (droplet-at ?d ?xr ?yo)
        (occupied ?xr ?yo)
    )
)

(:action split_y
    :parameters (?d - droplet ?xo - xcoord ?yo ?yt ?yb - ycoord)
    :precondition (and
        (droplet-at ?d ?xo ?yo)
        (NEIGHBOUR ?xo ?yo ?xo ?yt)
        (NEIGHBOUR ?xo ?yo ?xo ?yb)
        (not (= ?yt ?yb))
        (not (small ?d))
        (forall (?x - xcoord)
          (forall (?y - ycoord)
            (imply (and
                (not (and (= ?x ?xo) (= ?y ?yo)))
                (or
                    (VICINITY ?x ?y ?xo ?yt)
                    (VICINITY ?x ?y ?xo ?yb)
                )
            )
                (not (occupied ?x ?y))
            )
          )
        )
    )
    :effect (and
        (not (droplet-at ?d ?xo ?yo))
        (not (occupied ?xo ?yo))
        (small ?d)
        (droplet-at ?d ?xo ?yt)
        (occupied ?xo ?yt)
        (droplet-at ?d ?xo ?yb)
        (occupied ?xo ?yb)
    )
)


)