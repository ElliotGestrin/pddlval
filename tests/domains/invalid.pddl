(define (domain stringlights)
  (:requirements :strips :negative-preconditions)

  (:predicates
    (on ?l)
    ; Missing predicate definition for 'next'
  )

  (:action turn-on
    :parameters (?l ?l0)
    :precondition (and
      (not (on ?l))
      (on ?l0)
      (next ?l0 ?l) ; The light to turn on must be next in the order
    )
    :effect (on ?l)
  )
)