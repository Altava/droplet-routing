(define (domain p8x8d8n-domain)

(:requirements :strips :typing :conditional-effects :negative-preconditions :disjunctive-preconditions :universal-preconditions)

(:types
    reagent coordinate percentage - object
    xcoord ycoord - coordinate
    x1 x2 x3 x4 - xcoord
    y1 y2 y3 y4 - ycoord
    hcl kcl bovine gelatin - reagent
    p0 p20 p40 p60 p80 p100 - percentage
)

(:predicates
    (reagent-type ?r - reagent ?x - xcoord ?y - ycoord)
    (occupied ?x - xcoord ?y - ycoord)
    (VICINITY ?xo - xcoord ?yo - ycoord ?xt - xcoord ?yt - ycoord)
    (NEIGHBOUR ?xo - xcoord ?yo - ycoord ?xt - xcoord ?yt - ycoord)
    (blocked ?x - xcoord ?y - ycoord)
    (small ?x - xcoord ?y - ycoord)
    (mix-percentage ?p - percentage ?x - xcoord ?y - ycoord)
    (NEXTPERCENTAGE ?p1 ?p2 - percentage)
    (moved-west ?x - xcoord ?y - ycoord)
    (moved-east ?x - xcoord ?y - ycoord)
    (moved-north ?x - xcoord ?y - ycoord)
    (moved-south ?x - xcoord ?y - ycoord)
    (moved-once ?x - xcoord ?y - ycoord)
    (moved-twice ?x - xcoord ?y - ycoord)
    (moved-three-times ?x - xcoord ?y - ycoord)
    (ISEAST ?x1 ?x2 - xcoord)
    (ISWEST ?x1 ?x2 - xcoord)
    (ISNORTH ?y1 ?y2 - ycoord)
    (ISSOUTH ?y1 ?y2 - ycoord)
)

(:action spawn_KCL
    :parameters ()
    :precondition (and
        (not (occupied x1 y3))
        (not (occupied x2 y3))
        (not (occupied x1 y4))
        (not (occupied x2 y4))
    )
    :effect (and
        (reagent-type kcl x1 y4)
        (occupied x1 y4)
        (mix-percentage p100 x1 y4)
        (small x1 y4)
    )
)

(:action dispose
    :parameters (?r - reagent)
    :precondition (and 
        (reagent-type ?r x3 y1)
    )
    :effect (and
        (not (reagent-type ?r x3 y1))
        (not (occupied x3 y1))
        (not (small x3 y1))
    )
)

(:action move_south
    :parameters (?r - reagent ?xo - xcoord ?yo ?yt - ycoord ?p1 - percentage)
    :precondition (and
        (reagent-type ?r ?xo ?yo)
        (mix-percentage ?p1 ?xo ?yo)
        (ISSOUTH ?yt ?yo)
        (not (blocked ?xo ?yt))
        (forall (?x - xcoord)
          (forall (?y - ycoord)
            (imply (and
                (not (and (= ?x ?xo) (= ?y ?yo)))
                (VICINITY ?x ?y ?xo ?yt)
            )
                (not (occupied ?x ?y))
            )
          )
        )
    )
    :effect (and
        (forall (?p2 - percentage)
            (when (and
                (moved-south ?xo ?yo)
                (moved-once ?xo ?yo)
                (mix-percentage ?p1 ?xo ?yo)
                (NEXTPERCENTAGE ?p1 ?p2)
            ) (and
                (not (moved-south ?xo ?yo))
                (not (moved-once ?xo ?yo))
                (not (mix-percentage ?p1 ?xo ?yo))
                (moved-twice ?xo ?yt)
                (moved-south ?xo ?yt)
                (mix-percentage ?p2 ?xo ?yt)
            )
            )
        )
        (when (and
            (moved-south ?xo ?yo)
            (moved-twice ?xo ?yo)
        ) (and
            (not (moved-south ?xo ?yo))
            (not (moved-twice ?xo ?yo))
            (not (mix-percentage ?p1 ?xo ?yo))
            (moved-south ?xo ?yt)
            (moved-once ?xo ?yt)
            (mix-percentage ?p1 ?xo ?yt)
        )
        )
        (when (and
            (not (moved-south ?xo ?yo))
        ) (and
            (not (moved-east ?xo ?yo))
            (not (moved-west ?xo ?yo))
            (not (moved-north ?xo ?yo))
            (not (moved-south ?xo ?yo))
            (not (moved-once ?xo ?yo))
            (not (moved-twice ?xo ?yo))
            (not (moved-three-times ?xo ?yo))
            (not (mix-percentage ?p1 ?xo ?yo))
            (moved-south ?xo ?yt)
            (moved-once ?xo ?yt)
            (mix-percentage ?p1 ?xo ?yt)
        )
        )
        (when (small ?xo ?yo) (and
            (not (small ?xo ?yo))
            (small ?xo ?yt)
        ))
        (not (reagent-type ?r ?xo ?yo))
        (reagent-type ?r ?xo ?yt)
        (not (occupied ?xo ?yo))
        (occupied ?xo ?yt)
    )
)

(:action split_x
    :parameters (?r - reagent ?xo ?xl ?xr - xcoord ?yo - ycoord)
    :precondition (and
        (reagent-type ?r ?xo ?yo)
        (mix-percentage p100 ?xo ?yo)
        (NEIGHBOUR ?xo ?yo ?xl ?yo)
        (NEIGHBOUR ?xo ?yo ?xr ?yo)
        (not (= ?xl ?xr))
        (not (small ?xo ?yo))
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
        (not (reagent-type ?r ?xo ?yo))
        (not (occupied ?xo ?yo))
        (small ?xl ?yo)
        (reagent-type ?r ?xl ?yo)
        (occupied ?xl ?yo)
        (small ?xr ?yo)
        (reagent-type ?r ?xr ?yo)
        (occupied ?xr ?yo)
    )
)

(:action split_y
    :parameters (?r - reagent ?xo - xcoord ?yo ?yt ?yb - ycoord)
    :precondition (and
        (reagent-type ?r ?xo ?yo)
        (mix-percentage p100 ?xo ?yo)
        (NEIGHBOUR ?xo ?yo ?xo ?yt)
        (NEIGHBOUR ?xo ?yo ?xo ?yb)
        (not (= ?yt ?yb))
        (not (small ?xo ?yo))
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
        (not (reagent-type ?r ?xo ?yo))
        (not (occupied ?xo ?yo))
        (small ?xo ?yt)
        (reagent-type ?r ?xo ?yt)
        (occupied ?xo ?yt)
        (small ?xo ?yb)
        (reagent-type ?r ?xo ?yb)
        (occupied ?xo ?yb)
    )
)

)