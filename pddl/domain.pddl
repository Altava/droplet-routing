;Header and description

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
    (NEIGHBOUR ?x1 ?x2 ?y1 ?y2)
)


;(:functions ;todo: define numeric functions here
;)

;define actions here
(:action move
    :parameters (?droplet ?x-origin ?y-origin ?x-target ?y-target)
    :precondition (and
        (droplet-at ?droplet ?x-origin ?y-origin)
        (not (occupied ?x-target ?y-target))
        (NEIGHBOUR ?x-origin ?y-origin ?x-target ?y-target)
    )
    :effect (and
        (not (droplet-at ?droplet ?x-origin ?y-origin))
        (droplet-at ?droplet ?x-target ?y-target)
        (not (occupied ?x-origin ?y-origin))
        (occupied ?x-target ?y-target)
    )
)


)