(define (problem prob1) (:domain stringlights)
    (:objects
        l1 l2 l3
    )

    (:init
        (on l1)
        (next l1 l2)
        (next l2 l3)
    )

    (:goal (and
        (on l1)
        (on l2)
        (on l3)
    ))
)