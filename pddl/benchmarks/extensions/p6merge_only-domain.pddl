(define (domain p6merge_only-domain)

(:requirements :strips :typing :conditional-effects :negative-preconditions :disjunctive-preconditions :universal-preconditions :action-costs)

(:types
    reagent coordinate - object
    xcoord ycoord - coordinate
    x1 x2 x3 x4 x5 x6 x7 x8 - xcoord
    y1 y2 y3 y4 y5 y6 y7 y8 - ycoord
    hcl kcl bovine gelatin primer beosynucleotide amplitag lambdadna - reagent
)

(:predicates
    (reagent-type ?r - reagent ?x - xcoord ?y - ycoord)
    (occupied ?x - xcoord ?y - ycoord)
    (VICINITY ?xo - xcoord ?yo - ycoord ?xt - xcoord ?yt - ycoord)
    (blocked ?x - xcoord ?y - ycoord)
    (MIX ?r1 ?r2 ?rt - reagent)
    (small ?x - xcoord ?y - ycoord)
    (ISEAST ?x1 ?x2 - xcoord)
    (ISWEST ?x1 ?x2 - xcoord)
    (ISNORTH ?y1 ?y2 - ycoord)
    (ISSOUTH ?y1 ?y2 - ycoord)
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
        (reagent-type primer x1 y2)
        (occupied x1 y2)
        (small x1 y2)
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
        (reagent-type beosynucleotide x2 y1)
        (occupied x2 y1)
        (small x2 y1)
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
        (reagent-type amplitag x7 y1)
        (occupied x7 y1)
        (small x7 y1)
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
        (reagent-type lambdadna x8 y2)
        (occupied x8 y2)
        (small x8 y2)
    )
)

(:action dispose
    :parameters (?r - reagent)
    :precondition (and 
        (reagent-type ?r x8 y4)
    )
    :effect (and
        (not (reagent-type ?r x8 y4))
        (not (occupied x8 y4))
        (not (small x8 y4))
    )
)

(:action move_north
    :parameters (?r - reagent ?xo - xcoord ?yo ?yt - ycoord)
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
        (when (small ?xo ?yo) (and
            (small ?xo ?yt)
            (not (small ?xo ?yo))
            )
        )
        (not (reagent-type ?r ?xo ?yo))
        (reagent-type ?r ?xo ?yt)
        (not (occupied ?xo ?yo))
        (occupied ?xo ?yt)
    )
)

(:action move_south
    :parameters (?r - reagent ?xo - xcoord ?yo ?yt - ycoord)
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
        (when (small ?xo ?yo) (and
            (small ?xo ?yt)
            (not (small ?xo ?yo))
            )
        )
        (not (reagent-type ?r ?xo ?yo))
        (reagent-type ?r ?xo ?yt)
        (not (occupied ?xo ?yo))
        (occupied ?xo ?yt)
    )
)

(:action move_west
    :parameters (?r - reagent ?xo ?xt - xcoord ?yo - ycoord)
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
        (when (small ?xo ?yo) (and
            (small ?xt ?yo)
            (not (small ?xo ?yo))
            )
        )
        (not (reagent-type ?r ?xo ?yo))
        (reagent-type ?r ?xt ?yo)
        (not (occupied ?xo ?yo))
        (occupied ?xt ?yo)
    )
)

(:action move_east
    :parameters (?r - reagent ?xo ?xt - xcoord ?yo - ycoord)
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
        (when (small ?xo ?yo) (and
            (small ?xt ?yo)
            (not (small ?xo ?yo))
            )
        )
        (not (reagent-type ?r ?xo ?yo))
        (reagent-type ?r ?xt ?yo)
        (not (occupied ?xo ?yo))
        (occupied ?xt ?yo)
    )
)

(:action merge_x
    :parameters (?r1 ?r2 ?r3 - reagent ?x1 ?x2 ?xt - xcoord ?yt - ycoord)
    :precondition (and
        (reagent-type ?r1 ?x1 ?yt)
        (reagent-type ?r2 ?x2 ?yt)
        (small ?x1 ?yt)
        (small ?x2 ?yt)
        (ISEAST ?x1 ?xt)
        (ISWEST ?x2 ?xt)
        (not (blocked ?xt ?yt))
        (MIX ?r1 ?r2 ?r3)
    )
    :effect (and
        (not (reagent-type ?r1 ?x1 ?yt))
        (not (reagent-type ?r2 ?x2 ?yt))
        (not (small ?xt ?yt))
        (not (small ?x1 ?yt))
        (not (small ?x2 ?yt))
        (not (occupied ?x1 ?yt))
        (not (occupied ?x2 ?yt))
        (reagent-type ?r3 ?xt ?yt)
        (occupied ?xt ?yt)
    )
)

(:action merge_y
    :parameters (?r1 ?r2 ?r3 - droplet ?xt - xcoord ?y1 ?y2 ?yt - ycoord)
    :precondition (and
        (reagent-type ?r1 ?xt ?y1)
        (reagent-type ?r2 ?xt ?y2)
        (small ?xt ?y1)
        (small ?xt ?y2)
        (ISNORTH ?y1 ?yt)
        (ISSOUTH ?y2 ?yt)
        (not (blocked ?xt ?yt))
        (MIX ?r1 ?r2 ?r3)
    )
    :effect (and
        (not (reagent-type ?r1 ?xt ?y1))
        (not (reagent-type ?r2 ?xt ?y2))
        (not (small ?xt ?yt))
        (not (small ?xt ?y1))
        (not (small ?xt ?y2))
        (not (occupied ?xt ?y1))
        (not (occupied ?xt ?y2))
        (reagent-type ?r3 ?xt ?yt)
        (occupied ?xt ?yt)
    )
)

(:action split_x
    :parameters (?r - reagent ?xo ?xl ?xr - xcoord ?yo - ycoord)
    :precondition (and
        (reagent-type ?r ?xo ?yo)
        (ISWEST ?xl ?xo)
        (ISEAST ?xr ?xo)
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
        (ISNORTH ?yt ?yo)
        (ISSOUTH ?yb ?yo)
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