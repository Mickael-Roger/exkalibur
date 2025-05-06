from geographiclib.geodesic import Geodesic
import math

geod = Geodesic.WGS84

def compute_cross_positions(AB, CD, AX, CX, angle_axc_deg, E, F, EX):
    if AB <= AX:
        raise ValueError("AB doit être plus grand que AX")
    if CD < CX:
        raise ValueError("CD doit être au moins égal à CX")

    # 1. Calcul du point X sur EF
    ef_line = geod.Inverse(E[0], E[1], F[0], F[1])
    x = geod.Direct(E[0], E[1], ef_line['azi1'], EX)
    X = (x['lat2'], x['lon2'])

    # 2. Calcul des points C et D sur EF
    c = geod.Direct(E[0], E[1], ef_line['azi1'], EX - CX)
    C = (c['lat2'], c['lon2'])
    
    d = geod.Direct(E[0], E[1], ef_line['azi1'], EX + (CD - CX))
    D = (d['lat2'], d['lon2'])

    # 3. Calcul de l'azimut de EF au point X
    x_to_f = geod.Inverse(X[0], X[1], F[0], F[1])
    ef_azimuth = x_to_f['azi1']

    # 4. Calcul des deux orientations possibles pour AB
    solutions = []
    for angle_offset in [angle_axc_deg, -angle_axc_deg]:
        # Calcul de l'azimut de AB
        ab_azimuth = (ef_azimuth + angle_offset) % 360
        
        # Calcul du point A
        a = geod.Direct(X[0], X[1], (ab_azimuth + 180) % 360, AX)
        A = (a['lat2'], a['lon2'])
        
        # Calcul du point B
        b = geod.Direct(X[0], X[1], ab_azimuth, AB - AX)
        B = (b['lat2'], b['lon2'])

        solutions.append((A, B))

    return {
        'X': X,
        'C': C,
        'D': D,
        'solution1': {'A': solutions[0][0], 'B': solutions[0][1]},
        'solution2': {'A': solutions[1][0], 'B': solutions[1][1]}
    }

# Exemple d'utilisation
if __name__ == "__main__":

    print("Valeurs :\n")

    AB = float(input("Longueur AB en m: "))
    CD = float(input("Longueur CD en m: "))
    AX = float(input("Distance AX en m: "))
    CX = float(input("Distance CX en m: "))
    angle_axc_deg = float(input("Angle AXC en ° : "))
    
    print("\nCoordonnées GPS du point E :")
    e_lat = float(input("Latitude E: "))
    e_lon = float(input("Longitude E: "))
    E = (e_lat, e_lon)
    
    print("\nCoordonnées GPS du point F :")
    f_lat = float(input("Latitude F: "))
    f_lon = float(input("Longitude F: "))
    F = (f_lat, f_lon)
    
    EX = float(input("\nDistance EX en m: "))

    result = compute_cross_positions(
        AB=AB,
        CD=CD,
        AX=AX,
        CX=CX,
        angle_axc_deg=angle_axc_deg,
        E=E,
        F=F,
        EX=EX
    )

    print("Point X:", result['X'])
    print("Point C:", result['C'])
    print("Point D:", result['D'])
    print("\n")
    print("Solution 1 - A:", result['solution1']['A'], "B:", result['solution1']['B'])
    print("--- My MAPS CSV ---")
    print("WKT,name,description")
    print(f'"LINESTRING ({result['solution1']['A'][1]} {result['solution1']['A'][0]}, {result['solution1']['B'][1]} {result['solution1']['B'][0]})",AB move1,')
    print(f'"LINESTRING ({result['C'][1]} {result['C'][0]}, {result['D'][1]} {result['D'][0]})",CD move1,')
    print("--- END ---")
    print("\n")
    print("Solution 2 - A:", result['solution2']['A'], "B:", result['solution2']['B'])
    print("WKT,name,description")
    print(f'"LINESTRING ({result['solution2']['A'][1]} {result['solution2']['A'][0]}, {result['solution2']['B'][1]} {result['solution2']['B'][0]})",AB move2,')
    print(f'"LINESTRING ({result['C'][1]} {result['C'][0]}, {result['D'][1]} {result['D'][0]})",CD move2,')
    print("--- END ---")
