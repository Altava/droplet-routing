(define (domain p5merge_mixer-domain)

(:requirements :strips :typing :conditional-effects :negative-preconditions :disjunctive-preconditions :universal-preconditions :action-costs)

(:types
    reagent coordinate - object
    xcoord ycoord - coordinate
    x1 x2 x3 x4 x5 x6 x7 x8 - xcoord
    y1 y2 y3 y4 y5 y6 y7 y8 - ycoord
    hcl kcl bovine gelatin - reagent
)

(:predicates
    (reagent-type ?r - reagent ?x - xcoord ?y - ycoord)
    (occupied ?x - xcoord ?y - ycoord)
    (VICINITY ?xo - xcoord ?yo - ycoord ?xt - xcoord ?yt - ycoord)
    (blocked ?x - xcoord ?y - ycoord)
    (MIX ?r1 ?r2 ?rt - reagent)
    (is-mixed ?x - xcoord ?y - ycoord)
    (small ?x - xcoord ?y - ycoord)
    (ISEAST ?x1 ?x2 - xcoord)
    (ISWEST ?x1 ?x2 - xcoord)
    (ISNORTH ?y1 ?y2 - ycoord)
    (ISSOUTH ?y1 ?y2 - ycoord)
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
        (reagent-type hcl x1 y7)
        (occupied x1 y7)
        (small x1 y7)
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
        (reagent-type kcl x2 y8)
        (occupied x2 y8)
        (small x2 y8)
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
        (reagent-type bovine x7 y8)
        (occupied x7 y8)
        (small x7 y8)
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
        (reagent-type gelatin x8 y7)
        (occupied x8 y7)
        (small x8 y7)
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
        (not (is-mixed x8 y4))
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
        (when (is-mixed ?xo ?yo) (and
            (is-mixed ?xo ?yt)
            (not (is-mixed ?xo ?yo))
            )
        )
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
        (when (is-mixed ?xo ?yo) (and
            (is-mixed ?xo ?yt)
            (not (is-mixed ?xo ?yo))
            )
        )
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
        (when (is-mixed ?xo ?yo) (and
            (is-mixed ?xt ?yo)
            (not (is-mixed ?xo ?yo))
            )
        )
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
        (when (is-mixed ?xo ?yo) (and
            (is-mixed ?xt ?yo)
            (not (is-mixed ?xo ?yo))
            )
        )
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
        (is-mixed ?xo ?yo)
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
        (not (is-mixed ?xo ?yo))
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
        (is-mixed ?xo ?yo)
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
        (not (is-mixed ?xo ?yo))
        (small ?xo ?yt)
        (reagent-type ?r ?xo ?yt)
        (occupied ?xo ?yt)
        (small ?xo ?yb)
        (reagent-type ?r ?xo ?yb)
        (occupied ?xo ?yb)
    )
)

(:action mix_top_right
    :parameters (?r - reagent ?x - xcoord ?y - ycoord)
    :precondition (and
        (reagent-type ?r ?x ?y)
        (not (small ?x ?y))
        ; check that the padding cells are free
        (not (occupied x4 y8))
        (not (occupied x4 y7))
        (not (occupied x4 y6))
        (not (occupied x5 y6))
        (not (occupied x6 y6))
        (not (occupied x7 y6))
        (not (occupied x8 y6))
        (or
            ; check that all cells except my own are free
            (and
                (= ?x x5)
                (= ?y y8)
                (not (occupied x5 y7))
                (not (occupied x6 y8))
                (not (occupied x6 y7))
                (not (occupied x7 y8))
                (not (occupied x7 y7))
                (not (occupied x8 y8))
                (not (occupied x8 y7))
            )
            (and
                (= ?x x5)
                (= ?y y7)
                (not (occupied x5 y8))
                (not (occupied x6 y8))
                (not (occupied x6 y7))
                (not (occupied x7 y8))
                (not (occupied x7 y7))
                (not (occupied x8 y8))
                (not (occupied x8 y7))
            )
            (and
                (= ?x x8)
                (= ?y y8)
                (not (occupied x5 y8))
                (not (occupied x5 y7))
                (not (occupied x6 y8))
                (not (occupied x6 y7))
                (not (occupied x7 y8))
                (not (occupied x7 y7))
                (not (occupied x8 y7))
            )
            (and
                (= ?x x8)
                (= ?y y7)
                (not (occupied x5 y8))
                (not (occupied x5 y7))
                (not (occupied x6 y8))
                (not (occupied x6 y7))
                (not (occupied x7 y8))
                (not (occupied x7 y7))
                (not (occupied x8 y8))
            )
        )
    )
    :effect (and
        (is-mixed ?x ?y)
    )
)

(:action mix_bottom_left
    :parameters (?r - reagent ?x - xcoord ?y - ycoord)
    :precondition (and
        (reagent-type ?r ?x ?y)
        (not (small ?x ?y))
        (not (occupied x1 y3))
        (not (occupied x2 y3))
        (not (occupied x3 y3))
        (not (occupied x4 y3))
        (not (occupied x5 y3))
        (not (occupied x5 y2))
        (not (occupied x5 y1))
        (or
            (and
                (= ?x x1)
                (= ?y y1)
                (not (occupied x1 y2))
                (not (occupied x2 y1))
                (not (occupied x2 y2))
                (not (occupied x3 y1))
                (not (occupied x3 y2))
                (not (occupied x4 y1))
                (not (occupied x4 y2))
            )
            (and
                (= ?x x1)
                (= ?y y2)
                (not (occupied x1 y1))
                (not (occupied x2 y1))
                (not (occupied x2 y2))
                (not (occupied x3 y1))
                (not (occupied x3 y2))
                (not (occupied x4 y1))
                (not (occupied x4 y2))
            )
            (and
                (= ?x x4)
                (= ?y y1)
                (not (occupied x1 y1))
                (not (occupied x1 y2))
                (not (occupied x2 y1))
                (not (occupied x2 y2))
                (not (occupied x3 y1))
                (not (occupied x3 y2))
                (not (occupied x4 y2))
            )
            (and
                (= ?x x4)
                (= ?y y2)
                (not (occupied x1 y1))
                (not (occupied x1 y2))
                (not (occupied x2 y1))
                (not (occupied x2 y2))
                (not (occupied x3 y1))
                (not (occupied x3 y2))
                (not (occupied x4 y1))
            )
        )
    )
    :effect (and
        (is-mixed ?x ?y)
    )
)

)