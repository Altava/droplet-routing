; Domain of a 2-D grid representing a microfluidic biochip.
; 
; N marks the neighbours of X
; V marks the vicinity of X
; every neighbour is also in the vicinity of X
; O marks neutral spots
;
; O O O O O
; O V N V O
; O N X N O
; O V N V O
; O O O O O

(define (domain grid)

;remove requirements that are not needed
(:requirements :strips :typing :conditional-effects :negative-preconditions :disjunctive-preconditions :durative-actions)

(:types ;todo: enumerate types and their hierarchy here, e.g. car truck bus - vehicle
    droplet coordinate - object
    xcoord ycoord - coordinate
    x1 x2 x3 x4 - xcoord
    y1 y2 y3 y4 - ycoord
)

; un-comment following line if constants are needed
;(:constants )

(:predicates ;todo: define predicates here
    (droplet-at ?d ?x ?y)
    (occupied ?x ?y)
    (NEIGHBOUR ?x1 ?y1 ?x2 ?y2)
    (VICINITY ?x1 ?y1 ?x2 ?y2)
)


;(:functions ;todo: define numeric functions here
;)

;Rule #1: |Xi(t+1) − Xj(t+1)| ≥ 2 or |Yi(t+1) − Yj(t+1)| ≥ 2, i.e.,
;their new locations are not adjacent to each other.
;Rule #2: |Xi(t+1) − Xj(t)| ≥ 2 or |Yi(t+1) − Yj(t)| ≥ 2, i.e., the
;activated cell for droplet Di cannot be adjacent to Dj.
;Otherwise, there is more than one activated neighboring
;cell for Dj, which may leads to errant fluidic operation.
;Rule #3: |Xi(t) − Xj(t+1)| ≥ 2 or |Yi(t) − Yj(t+1)| ≥ 2.

;define actions here
; (:action move-x
;     :parameters (?droplet ?x-origin ?y-origin ?x-target)
;     :precondition (and
;         (droplet-at ?droplet ?x-origin ?y-origin)               ; droplet must be present in origin position
;         (not (occupied ?x-target ?y-origin))                    ; target must not be occupied
;         (NEIGHBOUR ?x-origin ?y-origin ?x-target ?y-origin)     ; origin and target must be neighbours
;         (forall (?x - xcoord)
;             (forall (?y - ycoord)
;                 (forall (?d - droplet)
;                     (imply (droplet-at ?d ?x ?y) (not (VICINITY ?x-target ?y-origin ?x ?y)))
;                 )
;             )
;         )                                                       ; target position cannot be in vicinity of any other droplet
;     )
;     :effect (and
;         (not (droplet-at ?droplet ?x-origin ?y-origin))
;         (droplet-at ?droplet ?x-target ?y-origin)
;         (not (occupied ?x-origin ?y-origin))
;         (occupied ?x-target ?y-origin)
;     )
; )

; (:action move-y
;     :parameters (?droplet ?x-origin ?y-origin ?y-target)
;     :precondition (and
;         (droplet-at ?droplet ?x-origin ?y-origin)               ; droplet must be present in origin position
;         (not (occupied ?x-origin ?y-target))                    ; target must not be occupied
;         (NEIGHBOUR ?x-origin ?y-origin ?x-origin ?y-target)     ; origin and target must be neighbours
;         (forall (?x - xcoord)
;             (forall (?y - ycoord)
;                 (forall (?d - droplet)
;                     (imply (droplet-at ?d ?x ?y) (not (VICINITY ?x-origin ?y-target ?x ?y)))
;                 )
;             )
;         )                                                        ; target position cannot be in vicinity of any other droplet
;     )
;     :effect (and
;         (not (droplet-at ?droplet ?x-origin ?y-origin))
;         (droplet-at ?droplet ?x-origin ?y-target)
;         (not (occupied ?x-origin ?y-origin))
;         (occupied ?x-origin ?y-target)
;     )
; )

(:durative-action move_22_23
    :parameters (?d - droplet)
    :duration (= ?duration 1)
    :condition (and 
        (at start (droplet-at ?d x2 y2))
        (over all (not (occupied x1 y4)))
        (over all (not (occupied x2 y4)))
        (over all (not (occupied x3 y4)))
    )
    :effect (and 
        (at start (not (droplet-at ?d x2 y2)))
        (at end (droplet-at ?d x2 y3))
        (at end (not (occupied x2 y2)))
        (at start (occupied x2 y3))
    )
)

)