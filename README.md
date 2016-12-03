# AdaptiveHttpProbe

The aim of this project is to create a Monitoring Check that is able to detect
failure modes of HTTP APIs reliably, taking into account:

* Partial failures (10% of all requests are failing)

* Flapping states (Service changing between Up/Down quickly)

It does so by:

1. Enriched state model that includes partial failure modes.

2. Adaptive change of the measurement frequency.

3. ? for flapping states.

## The expermintal UI

The experimental UI was written in Tornado and python3. It is recommended to use a virtualenv when running it.

Install the requirements:
```
pip install -r requirements.txt
```
Then run the probe server:
```
python probe.py
```
And the simulation server:
```
python simulation_server.py
```

Currently configurations must be done in the code. WiP


# TODO

- [x] Make simple bayes model
- [x] Add transition probability parameter
- [ ] Gather real-world data
- [x] Make a simulation of partial failure modes
- [ ] Make the parameters configurable in the UI
- [ ] Alert on transition to "bad" state
