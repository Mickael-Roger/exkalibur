# Get GPS information about a cross on a map

## Calcul sur une croix

```
python3 cross.py "(55.1234567, -4.1234567)" "(39.1234567, -0.1234567)" "(43.1234567, 1.1234567)" "(43.1234567,-5.1234567)"
```

Vous donne:

```
Intersection GPS: (43.16089427331025, -0.9217536895473282)
    Angle AXC: 80.53°
    Angle AXD: 99.47°
    Angle BXC: 99.47°
    Angle BXD: 80.53°
Longueur AB: 1803927.01 m
    Longueur AX: 1350041.55 m
    Longueur BX: 453885.46 m
Longueur CD: 506877.27 m
    Longueur CX: 165984.98 m
    Longueur DX: 340892.29 m
```


## Translation

```
python3 move.py
```

              A
              |
              |
              |
              |
     C -------X-----D
              |
              |
              B


Vous saisissez les valeurs demandees (Le segment EF est le segment sur lequel vous voulez deplacer CD)
```
Valeurs :

Longueur AB en m: 12345
Longueur CD en m: 657
Distance AX en m: 400
Distance CX en m: 100
Angle AXC en ° : 89.1

Coordonnées GPS du point E :
Latitude E: 41.8281989
Longitude E: -4.71

Coordonnées GPS du point F :
Latitude F: 4.12222
Longitude F: -0.12365

Distance EX en m: 10
```


Vous retourne a la fois le CSV My Map et les valeurs
```
Point X: (41.82810963462257, -4.70998431090568)
Point C: (41.82900228823774, -4.7101412038104495)
Point D: (41.823137547518364, -4.709110497176658)


Solution 1 - A: (41.82863494041836, -4.705220768482448) B: (41.812331668830396, -4.852199582549996)
--- My MAPS CSV ---
WKT,name,description
"LINESTRING (-4.705220768482448 41.82863494041836, -4.852199582549996 41.812331668830396)",AB move1,
"LINESTRING (-4.7101412038104495 41.82900228823774, -4.709110497176658 41.823137547518364)",CD move1,
--- END ---


Solution 2 - A: (41.827696299999154, -4.714767498279118) B: (41.84036101760925, -4.567118152520781)
WKT,name,description
"LINESTRING (-4.714767498279118 41.827696299999154, -4.567118152520781 41.84036101760925)",AB move2,
"LINESTRING (-4.7101412038104495 41.82900228823774, -4.709110497176658 41.823137547518364)",CD move2,
--- END ---
```
