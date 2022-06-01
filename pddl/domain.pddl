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
(:requirements :strips :typing :conditional-effects :negative-preconditions)

;(:types ;todo: enumerate types and their hierarchy here, e.g. car truck bus - vehicle
;    droplet - object
;    xcoord ycoord - object
;)

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
(:action move
    :parameters (?droplet ?x-origin ?y-origin ?x-target ?y-target)
    :precondition (and
        (droplet-at ?droplet ?x-origin ?y-origin)               ; droplet must be present in origin position
        (not (occupied ?x-target ?y-target))                    ; target must not be occupied
        (NEIGHBOUR ?x-origin ?y-origin ?x-target ?y-target)     ; origin and target must be neighbours
        ;(VICINITY .....)                                         target position cannot be in vicinity of any other droplet
    )
    :effect (and
        (not (droplet-at ?droplet ?x-origin ?y-origin))
        (droplet-at ?droplet ?x-target ?y-target)
        (not (occupied ?x-origin ?y-origin))
        (occupied ?x-target ?y-target)
    )
)


)