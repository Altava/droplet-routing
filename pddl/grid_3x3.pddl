(define (domain grid_3x3)

(:requirements :strips :typing :conditional-effects :negative-preconditions :disjunctive-preconditions :durative-actions)

(:types
    droplet coordinate - object
    xcoord ycoord - coordinate
    x1 x2 x3 - xcoord
    y1 y2 y3 - ycoord
)

(:predicates
    (droplet-at ?d ?x ?y)
    (occupied ?x ?y)
)


(:durative-action move_11_21
    :parameters (?d - droplet)
    :duration (= ?duration 1)
    :condition (and
        (at start (droplet-at ?d x1 y1))
        (over all (not (occupied x3 y1)))
        (over all (not (occupied x3 y2)))
    )
    :effect (and
        (at start (not (droplet-at ?d x1 y1)))
        (at end (droplet-at ?d x2 y1))
        (at end (not (occupied x1 y1)))
        (at start (occupied x2 y1))
    )
)

(:durative-action move_11_12
  :parameters (?d - droplet)
  :duration (= ?duration 1)
  :condition (and
    (at start (droplet-at ?d x1 y1))
    (over all (not (occupied x1 y3)))
    (over all (not (occupied x2 y3)))
    )
    :effect (and
        (at start (not (droplet-at ?d x1 y1)))
        (at end (droplet-at ?d x1 y2))
        (at end (not (occupied x1 y1)))
        (at start (occupied x1 y2))
    )
)

(:durative-action move_12_22
    :parameters (?d - droplet)
    :duration (= ?duration 1)
    :condition (and
        (at start (droplet-at ?d x1 y2))
        (over all (not (occupied x3 y1)))
        (over all (not (occupied x3 y2)))
        (over all (not (occupied x3 y3)))
    )
    :effect (and
        (at start (not (droplet-at ?d x1 y2)))
        (at end (droplet-at ?d x2 y2))
        (at end (not (occupied x1 y2)))
        (at start (occupied x2 y2))
    )
)

(:durative-action move_12_11
  :parameters (?d - droplet)
  :duration (= ?duration 1)
  :condition (and
    (at start (droplet-at ?d x1 y2))
    )
    :effect (and
        (at start (not (droplet-at ?d x1 y2)))
        (at end (droplet-at ?d x1 y1))
        (at end (not (occupied x1 y2)))
        (at start (occupied x1 y1))
    )
)

(:durative-action move_12_13
  :parameters (?d - droplet)
  :duration (= ?duration 1)
  :condition (and
    (at start (droplet-at ?d x1 y2))
    )
    :effect (and
        (at start (not (droplet-at ?d x1 y2)))
        (at end (droplet-at ?d x1 y3))
        (at end (not (occupied x1 y2)))
        (at start (occupied x1 y3))
    )
)

(:durative-action move_13_23
    :parameters (?d - droplet)
    :duration (= ?duration 1)
    :condition (and
        (at start (droplet-at ?d x1 y3))
        (over all (not (occupied x3 y2)))
        (over all (not (occupied x3 y3)))
    )
    :effect (and
        (at start (not (droplet-at ?d x1 y3)))
        (at end (droplet-at ?d x2 y3))
        (at end (not (occupied x1 y3)))
        (at start (occupied x2 y3))
    )
)

(:durative-action move_13_12
  :parameters (?d - droplet)
  :duration (= ?duration 1)
  :condition (and
    (at start (droplet-at ?d x1 y3))
    (over all (not (occupied x1 y1)))
    (over all (not (occupied x2 y1)))
    )
    :effect (and
        (at start (not (droplet-at ?d x1 y3)))
        (at end (droplet-at ?d x1 y2))
        (at end (not (occupied x1 y3)))
        (at start (occupied x1 y2))
    )
)

(:durative-action move_21_31
    :parameters (?d - droplet)
    :duration (= ?duration 1)
    :condition (and
        (at start (droplet-at ?d x2 y1))
    )
    :effect (and
        (at start (not (droplet-at ?d x2 y1)))
        (at end (droplet-at ?d x3 y1))
        (at end (not (occupied x2 y1)))
        (at start (occupied x3 y1))
    )
)

(:durative-action move_21_11
  :parameters (?d - droplet)
  :duration (= ?duration 1)
  :condition (and
    (at start (droplet-at ?d x2 y1))
    )
    :effect (and
        (at start (not (droplet-at ?d x2 y1)))
        (at end (droplet-at ?d x1 y1))
        (at end (not (occupied x2 y1)))
        (at start (occupied x1 y1))
    )
)

(:durative-action move_21_22
  :parameters (?d - droplet)
  :duration (= ?duration 1)
  :condition (and
    (at start (droplet-at ?d x2 y1))
    (over all (not (occupied x1 y3)))
    (over all (not (occupied x2 y3)))
    (over all (not (occupied x3 y3)))
    )
    :effect (and
        (at start (not (droplet-at ?d x2 y1)))
        (at end (droplet-at ?d x2 y2))
        (at end (not (occupied x2 y1)))
        (at start (occupied x2 y2))
    )
)

(:durative-action move_22_32
    :parameters (?d - droplet)
    :duration (= ?duration 1)
    :condition (and
        (at start (droplet-at ?d x2 y2))
    )
    :effect (and
        (at start (not (droplet-at ?d x2 y2)))
        (at end (droplet-at ?d x3 y2))
        (at end (not (occupied x2 y2)))
        (at start (occupied x3 y2))
    )
)

(:durative-action move_22_21
  :parameters (?d - droplet)
  :duration (= ?duration 1)
  :condition (and
    (at start (droplet-at ?d x2 y2))
    )
    :effect (and
        (at start (not (droplet-at ?d x2 y2)))
        (at end (droplet-at ?d x2 y1))
        (at end (not (occupied x2 y2)))
        (at start (occupied x2 y1))
    )
)

(:durative-action move_22_12
  :parameters (?d - droplet)
  :duration (= ?duration 1)
  :condition (and
    (at start (droplet-at ?d x2 y2))
    )
    :effect (and
        (at start (not (droplet-at ?d x2 y2)))
        (at end (droplet-at ?d x1 y2))
        (at end (not (occupied x2 y2)))
        (at start (occupied x1 y2))
    )
)

(:durative-action move_22_23
  :parameters (?d - droplet)
  :duration (= ?duration 1)
  :condition (and
    (at start (droplet-at ?d x2 y2))
    )
    :effect (and
        (at start (not (droplet-at ?d x2 y2)))
        (at end (droplet-at ?d x2 y3))
        (at end (not (occupied x2 y2)))
        (at start (occupied x2 y3))
    )
)

(:durative-action move_23_33
    :parameters (?d - droplet)
    :duration (= ?duration 1)
    :condition (and
        (at start (droplet-at ?d x2 y3))
    )
    :effect (and
        (at start (not (droplet-at ?d x2 y3)))
        (at end (droplet-at ?d x3 y3))
        (at end (not (occupied x2 y3)))
        (at start (occupied x3 y3))
    )
)

(:durative-action move_23_22
  :parameters (?d - droplet)
  :duration (= ?duration 1)
  :condition (and
    (at start (droplet-at ?d x2 y3))
    (over all (not (occupied x1 y1)))
    (over all (not (occupied x2 y1)))
    (over all (not (occupied x3 y1)))
    )
    :effect (and
        (at start (not (droplet-at ?d x2 y3)))
        (at end (droplet-at ?d x2 y2))
        (at end (not (occupied x2 y3)))
        (at start (occupied x2 y2))
    )
)

(:durative-action move_23_13
  :parameters (?d - droplet)
  :duration (= ?duration 1)
  :condition (and
    (at start (droplet-at ?d x2 y3))
    )
    :effect (and
        (at start (not (droplet-at ?d x2 y3)))
        (at end (droplet-at ?d x1 y3))
        (at end (not (occupied x2 y3)))
        (at start (occupied x1 y3))
    )
)

(:durative-action move_31_21
  :parameters (?d - droplet)
  :duration (= ?duration 1)
  :condition (and
    (at start (droplet-at ?d x3 y1))
    (over all (not (occupied x1 y1)))
    (over all (not (occupied x1 y2)))
    )
    :effect (and
        (at start (not (droplet-at ?d x3 y1)))
        (at end (droplet-at ?d x2 y1))
        (at end (not (occupied x3 y1)))
        (at start (occupied x2 y1))
    )
)

(:durative-action move_31_32
  :parameters (?d - droplet)
  :duration (= ?duration 1)
  :condition (and
    (at start (droplet-at ?d x3 y1))
    (over all (not (occupied x2 y3)))
    (over all (not (occupied x3 y3)))
    )
    :effect (and
        (at start (not (droplet-at ?d x3 y1)))
        (at end (droplet-at ?d x3 y2))
        (at end (not (occupied x3 y1)))
        (at start (occupied x3 y2))
    )
)

(:durative-action move_32_31
  :parameters (?d - droplet)
  :duration (= ?duration 1)
  :condition (and
    (at start (droplet-at ?d x3 y2))
    )
    :effect (and
        (at start (not (droplet-at ?d x3 y2)))
        (at end (droplet-at ?d x3 y1))
        (at end (not (occupied x3 y2)))
        (at start (occupied x3 y1))
    )
)

(:durative-action move_32_22
  :parameters (?d - droplet)
  :duration (= ?duration 1)
  :condition (and
    (at start (droplet-at ?d x3 y2))
    (over all (not (occupied x1 y1)))
    (over all (not (occupied x1 y2)))
    (over all (not (occupied x1 y3)))
    )
    :effect (and
        (at start (not (droplet-at ?d x3 y2)))
        (at end (droplet-at ?d x2 y2))
        (at end (not (occupied x3 y2)))
        (at start (occupied x2 y2))
    )
)

(:durative-action move_32_33
  :parameters (?d - droplet)
  :duration (= ?duration 1)
  :condition (and
    (at start (droplet-at ?d x3 y2))
    )
    :effect (and
        (at start (not (droplet-at ?d x3 y2)))
        (at end (droplet-at ?d x3 y3))
        (at end (not (occupied x3 y2)))
        (at start (occupied x3 y3))
    )
)

(:durative-action move_33_32
  :parameters (?d - droplet)
  :duration (= ?duration 1)
  :condition (and
    (at start (droplet-at ?d x3 y3))
    (over all (not (occupied x2 y1)))
    (over all (not (occupied x3 y1)))
    )
    :effect (and
        (at start (not (droplet-at ?d x3 y3)))
        (at end (droplet-at ?d x3 y2))
        (at end (not (occupied x3 y3)))
        (at start (occupied x3 y2))
    )
)

(:durative-action move_33_23
  :parameters (?d - droplet)
  :duration (= ?duration 1)
  :condition (and
    (at start (droplet-at ?d x3 y3))
    (over all (not (occupied x1 y2)))
    (over all (not (occupied x1 y3)))
    )
    :effect (and
        (at start (not (droplet-at ?d x3 y3)))
        (at end (droplet-at ?d x2 y3))
        (at end (not (occupied x3 y3)))
        (at start (occupied x2 y3))
    )
)

)