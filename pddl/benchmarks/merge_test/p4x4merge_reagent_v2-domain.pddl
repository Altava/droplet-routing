(define (domain p8x8d8n-domain)

(:requirements :strips :typing :conditional-effects :negative-preconditions :disjunctive-preconditions :universal-preconditions)

(:types
    reagent coordinate percentage - object
    xcoord ycoord - coordinate
    x1 x2 x3 x4 - xcoord
    y1 y2 y3 y4 - ycoord
    hcl kcl bovine gelatin - reagent
    p0 p5 p10 p15 p20 p25 p30 p35 p40 p45 p50 p55 p60 p65 p70 p75 p80 p85 p90 p95 p100 - percentage
)

(:predicates
    (reagent-type ?r - reagent ?x - xcoord ?y - ycoord)
    (occupied ?x - xcoord ?y - ycoord)
    (VICINITY ?xo - xcoord ?yo - ycoord ?xt - xcoord ?yt - ycoord)
    (NEIGHBOUR ?xo - xcoord ?yo - ycoord ?xt - xcoord ?yt - ycoord)
    (blocked ?x - xcoord ?y - ycoord)
    (MIX ?r1 ?r2 ?rt - reagent)
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
    (moved-four-times ?x - xcoord ?y - ycoord)
    (moved-five-times ?x - xcoord ?y - ycoord)
    (ISEAST ?x1 ?x2 - xcoord)
    (ISWEST ?x1 ?x2 - xcoord)
    (ISNORTH ?y1 ?y2 - ycoord)
    (ISSOUTH ?y1 ?y2 - ycoord)
)

(:action spawn_HCL
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
        (reagent-type hcl x1 y2)
        (occupied x1 y2)
        (small x1 y2)
    )
)

(:action spawn_KCL
    :parameters ()
    :precondition (and
        (not (occupied x1 y3))
        (not (occupied x2 y4))
        (not (occupied x1 y3))
        (not (occupied x2 y4))
    )
    :effect (and
        (reagent-type kcl x1 y4)
        (occupied x1 y4)
        (small x1 y4)
    )
)

(:action spawn_Bovine
    :parameters ()
    :precondition (and
        (not (occupied x2 y3))
        (not (occupied x3 y3))
        (not (occupied x4 y3))
        (not (occupied x2 y4))
        (not (occupied x3 y4))
        (not (occupied x4 y4))
    )
    :effect (and
        (reagent-type bovine x3 y4)
        (occupied x3 y4)
        (small x3 y4)
    )
)

(:action spawn_Gelatin
    :parameters ()
    :precondition (and
        (not (occupied x3 y2))
        (not (occupied x3 y3))
        (not (occupied x3 y4))
        (not (occupied x4 y2))
        (not (occupied x4 y3))
        (not (occupied x4 y4))
    )
    :effect (and
        (reagent-type gelatin x4 y3)
        (occupied x4 y3)
        (small x4 y3)
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
    )
)

(:action move_north
    :parameters (?r - reagent ?xo - xcoord ?yo ?yt - ycoord ?p1 - percentage)
    :precondition (and
        (reagent-type ?r ?xo ?yo)
        (ISNORTH ?yt ?yo)
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
        (not (reagent-type ?r ?xo ?yo))
        (reagent-type ?r ?xo ?yt)
        (not (occupied ?xo ?yo))
        (occupied ?xo ?yt)
        (when (small ?xo ?yo) (and
            (small ?xo ?yt)
            (not (small ?xo ?yo))
            )
        )
        (forall (?p2 - percentage) (and
            (when (and 
                (moved-north ?xo ?yo)
                (moved-four-times ?x ?y)
                (mix-percentage ?p1 ?xo ?yo)
                (NEXTPERCENTAGE ?p1 ?p2)
            ) (and
                (not (moved-four-times ?xo ?yo))
                (not (mix-percentage ?p1 ?xo ?yo))
                (moved-five-times ?xo ?yt)
                (mix-percentage ?p2 ?xo ?yt)
            )
            )
            (when (and
                (moved-north ?xo ?yo)
                (moved-three-times ?xo ?yo)
                (mix-percentage ?p1 ?xo ?yo)
                (NEXTPERCENTAGE ?p1 ?p2)
            ) (and
                (not (moved-three-times ?xo ?yo))
                (not (mix-percentage ?p1 ?xo ?yo))
                (moved-four-times ?xo ?yt)
                (mix-percentage ?p2 ?xo ?yt)
            )
            )
            (when (and 
                (moved-north ?xo ?yo)
                (moved-twice ?xo ?yo)
                (mix-percentage ?p1 ?xo ?yo)
                (NEXTPERCENTAGE ?p1 ?p2)
            ) (and
                (not (moved-twice ?xo ?yo))
                (not (mix-percentage ?p1 ?xo ?yo))
                (moved-three-times ?xo ?yt)
                (mix-percentage ?p2 ?xo ?yt)
            )
            )
        ))
        (when (and 
            (moved-north ?xo ?yo)
            (moved-once ?xo ?yo)
        ) (and
            (not (moved-once ?xo ?yo))
            (moved-twice ?xo ?yt)
        )
        )
        (when (and
            (not (moved-north ?xo ?yo))
        ) (and
            (not (moved-east ?xo ?yt))
            (not (moved-west ?xo ?yt))
            (not (moved-south ?xo ?yt))
            (not (moved-twice ?xo ?yt))
            (not (moved-three-times ?xo ?yt))
            (not (moved-four-times ?xo ?yt))
            (not (moved-five-times ?xo ?yt))
            (moved-north ?xo ?yt)
            (moved-once ?xo ?yo)
        )
        )
    )
)

(:action move_south
    :parameters (?r - reagent ?xo - xcoord ?yo ?yt - ycoord ?p1 - percentage)
    :precondition (and
        (reagent-type ?r ?xo ?yo)
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
        (not (reagent-type ?r ?xo ?yo))
        (reagent-type ?r ?xo ?yt)
        (not (occupied ?xo ?yo))
        (occupied ?xo ?yt)
        (when (small ?xo ?yo) (and
            (small ?xo ?yt)
            (not (small ?xo ?yo))
            )
        )
        (forall (?p1 - percentage) (and
            (when (and
                (moved-south ?xo ?yo)
                (moved-four-times ?xo ?yo)
                (mix-percentage ?p1 ?xo ?yo)
                (NEXTPERCENTAGE ?p1 ?p2)
            ) (and
                (not (moved-four-times ?xo ?yo))
                (not (mix-percentage ?p1 ?xo ?yo))
                (moved-five-times ?xo ?yt)
                (mix-percentage ?p2 ?xo ?yt)
            )
            )
            (when (and
                (moved-south ?xo ?yo)
                (moved-three-times ?xo ?yo)
                (mix-percentage ?p1 ?xo ?yo)
                (NEXTPERCENTAGE ?p1 ?p2)
            ) (and
                (not (moved-three-times ?xo ?yo))
                (not (mix-percentage ?p1 ?xo ?yo))
                (moved-four-times ?xo ?yt)
                (mix-percentage ?p2 ?xo ?yt)
            )
            )
            (when (and
                (moved-south ?xo ?yo)
                (moved-twice ?xo ?yo)
                (mix-percentage ?p1 ?xo ?yo)
                (NEXTPERCENTAGE ?p1 ?p2)
            ) (and
                (not (moved-twice ?xo ?yo))
                (not (mix-percentage ?p1 ?xo ?yo))
                (moved-three-times ?xo ?yt)
                (mix-percentage ?p2 ?xo ?yt)
            )
            )
        ))
        (when (and 
            (moved-south ?xo ?yo)
            (moved-once ?xo ?yo)
        ) (and
            (not (moved-once ?xo ?yo))
            (moved-twice ?xo ?yt)
        )
        )
        (when (and
            (not (moved-south ?xo ?yo))
        ) (and
            (not (moved-east ?xo ?yt))
            (not (moved-west ?xo ?yt))
            (not (moved-north ?xo ?yt))
            (not (moved-twice ?xo ?yt))
            (not (moved-three-times ?xo ?yt))
            (not (moved-four-times ?xo ?yt))
            (not (moved-five-times ?xo ?yt))
            (moved-south ?xo ?yt)
            (moved-once ?xo ?yo)
        )
        )
    )
)

(:action move_west
    :parameters (?r - reagent ?xo ?xt - xcoord ?yo - ycoord ?p1 - percentage)
    :precondition (and
        (reagent-type ?r ?xo ?yo)
        (ISWEST ?xt ?xo)
        (not (blocked ?xt ?yo))
        (forall (?x - xcoord)
          (forall (?y - ycoord)
            (imply (and
                (not (and (= ?x ?xo) (= ?y ?yo)))
                (VICINITY ?x ?y ?xt ?yo)
            )
                (not (occupied ?x ?y))
            )
          )
        )
    )
    :effect (and
        (not (reagent-type ?r ?xo ?yo))
        (reagent-type ?r ?xt ?yo)
        (not (occupied ?xo ?yo))
        (occupied ?xt ?yo)
        (when (small ?xo ?yo) (and
            (small ?xt ?yo)
            (not (small ?xo ?yo))
            )
        )
        (forall (?p2 - percentage) (and
            (when (and
                (moved-west ?xo ?yo)
                (moved-four-times ?xo ?yo)
                (mix-percentage ?p1 ?xo ?yo)
                (NEXTPERCENTAGE ?p1 ?p2)
            ) (and
                (not (moved-four-times ?xo ?yo))
                (not (mix-percentage ?p1 ?xo ?yo))
                (moved-five-times ?xt ?yo)
                (mix-percentage ?p2 ?xt ?yo)
            )
            )
            (when (and
                (moved-west ?xo ?yo)
                (moved-three-times ?xo ?yo)
                (mix-percentage ?p1 ?xo ?yo)
                (NEXTPERCENTAGE ?p1 ?p2)
            ) (and
                (not (moved-three-times ?xo ?yo))
                (not (mix-percentage ?p1 ?xo ?yo))
                (moved-four-times ?xt ?yo)
                (mix-percentage ?p2 ?xt ?yo)
            )
            )
            (when (and
                (moved-west ?xo ?yo) 
                (moved-twice ?xo ?yo)
                (mix-percentage ?p1 ?xo ?yo)
                (NEXTPERCENTAGE ?p1 ?p2)
            ) (and
                (not (moved-twice ?xo ?yo))
                (not (mix-percentage ?p1 ?xo ?yo))
                (moved-three-times ?xt ?yo)
                (mix-percentage ?p2 ?xt ?yo)
            )
            )
        ))
        (when (and
            (moved-west ?xo ?yo)
            (moved-once ?xo ?yo)
        ) (and
            (not (moved-once ?xo ?yo))
            (moved-twice ?xt ?yo)
        )
        )
        (when (and
            (not (moved-west ?xo ?yo))
        ) (and
            (not (moved-east ?xt ?yo))
            (not (moved-north ?xt ?yo))
            (not (moved-south ?xt ?yo))
            (not (moved-twice ?xt ?yo))
            (not (moved-three-times ?xt ?yo))
            (not (moved-four-times ?xt ?yo))
            (not (moved-five-times ?xt ?yo))
            (moved-west ?xt ?yo)
            (moved-once ?xo ?yo)
        )
        )
    )
)

(:action move_east
    :parameters (?r - reagent ?xo ?xt - xcoord ?yo - ycoord ?p1 - percentage)
    :precondition (and
        (reagent-type ?r ?xo ?yo)
        (ISEAST ?xt ?xo)
        (not (blocked ?xt ?yo))
        (forall (?x - xcoord)
          (forall (?y - ycoord)
            (imply (and
                (not (and (= ?x ?xo) (= ?y ?yo)))
                (VICINITY ?x ?y ?xt ?yo)
            )
                (not (occupied ?x ?y))
            )
          )
        )
    )
    :effect (and
        (not (reagent-type ?r ?xo ?yo))
        (reagent-type ?r ?xt ?yo)
        (not (occupied ?xo ?yo))
        (occupied ?xt ?yo)
        (when (small ?xo ?yo) (and
            (small ?xt ?yo)
            (not (small ?xo ?yo))
            )
        )
        (forall (?p2 - percentage) (and
            (when (and
                (moved-east ?xo ?yo)
                (moved-four-times ?xo ?yo)
                (mix-percentage ?p1 ?xo ?yo)
                (NEXTPERCENTAGE ?p1 ?p2)
            ) (and
                (not (moved-four-times ?xo ?yo))
                (not (mix-percentage ?p1 ?xo ?yo))
                (moved-five-times ?xt ?yo)
                (mix-percentage ?p2 ?xt ?yo)
            )
            )
            (when (and
                (moved-east ?xo ?yo)
                (moved-three-times ?xo ?yo)
                (mix-percentage ?p1 ?xo ?yo)
                (NEXTPERCENTAGE ?p1 ?p2)
            ) (and
                (not (moved-three-times ?xo ?yo))
                (not (mix-percentage ?p1 ?xo ?yo))
                (moved-four-times ?xt ?yo)
                (mix-percentage ?p2 ?xt ?yo)
            )
            )
            (when (and
                (moved-east ?xo ?yo) 
                (moved-twice ?xo ?yo)
                (mix-percentage ?p1 ?xo ?yo)
                (NEXTPERCENTAGE ?p1 ?p2)
            ) (and
                (not (moved-twice ?xo ?yo))
                (not (mix-percentage ?p1 ?xo ?yo))
                (moved-three-times ?xt ?yo)
                (mix-percentage ?p2 ?xt ?yo)
            )
            )
        ))
        (when (and
            (moved-east ?xo ?yo)
            (moved-once ?xo ?yo)
        ) (and
            (not (moved-once ?xo ?yo))
            (moved-twice ?xt ?yo)
        )
        )
        (when (and
            (not (moved-east ?xo ?yo))
        ) (and
            (not (moved-west ?xt ?yo))
            (not (moved-north ?xt ?yo))
            (not (moved-south ?xt ?yo))
            (not (moved-twice ?xt ?yo))
            (not (moved-three-times ?xt ?yo))
            (not (moved-four-times ?xt ?yo))
            (not (moved-five-times ?xt ?yo))
            (moved-east ?xt ?yo)
            (moved-once ?xo ?yo)
        )
        )
    )
)

(:action merge_x
    :parameters (?r1 ?r2 ?r3 - reagent ?x1 ?x2 ?xt - xcoord ?yt - ycoord)
    :precondition (and
        (reagent-type ?r1 ?x1 ?yt)
        (reagent-type ?r2 ?x2 ?yt)
        (small ?x1 ?yt)
        (small ?x2 ?yt)
        (NEIGHBOUR ?x1 ?yt ?xt ?yt)
        (NEIGHBOUR ?x2 ?yt ?xt ?yt)
        (not (blocked ?xt ?yt))
        (MIX ?r1 ?r2 ?r3)
    )
    :effect (and
        (not (reagent-type ?r1 ?x1 ?yt))
        (not (reagent-type ?r2 ?x2 ?yt))
        (not (small ?xt ?yt))
        (reagent-type ?r3 ?xt ?yt)
        (not (occupied ?x1 ?yt))
        (not (occupied ?x2 ?yt))
        (occupied ?xt ?yt)
        (mix-percentage p0 ?xt ?yt)
    )
)

(:action merge_y
    :parameters (?r1 ?r2 ?r3 - droplet ?xt - xcoord ?y1 ?y2 ?yt - ycoord)
    :precondition (and
        (reagent-type ?r1 ?xt ?y1)
        (reagent-type ?r2 ?xt ?y2)
        (small ?xt ?y1)
        (small ?xt ?y2)
        (NEIGHBOUR ?xt ?y1 ?xt ?yt)
        (NEIGHBOUR ?xt ?y2 ?xt ?yt)
        (not (blocked ?xt ?yt))
        (MIX ?r1 ?r2 ?r3)
    )
    :effect (and
        (not (reagent-type ?r1 ?xt ?y1))
        (not (reagent-type ?r2 ?xt ?y2))
        (not (small ?xt ?yt))
        (reagent-type ?r3 ?xt ?yt)
        (not (occupied ?xt ?y1))
        (not (occupied ?xt ?y2))
        (occupied ?xt ?yt)
        (mix-percentage p0 ?xt ?yt)
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