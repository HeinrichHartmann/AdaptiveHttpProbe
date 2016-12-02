# AdaptiveHttpProbe

The aim of this project is to create a Monitoring Check that is able to detect
failure modes of HTTP APIs reliably, taking into account:

* Partial failures (10% of all requests are failing)

* Flapping states (Service changing between Up/Down quickly)

It does so by:

1. Enriched state model that includes partial failure modes.

2. Adaptive change of the measurement frequency.

3. ? for flapping states.


# TODO

- [x] Make simple bayes model
- [x] Add transition probability parameter
- [ ] Gather real-world data
- [ ] Make a simulation of partial failure modes
