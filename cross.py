import math
import argparse
import ast

EARTH_RADIUS = 6371000  # Rayon moyen en mètres

def cross(a, b):
    return (
        a[1]*b[2] - a[2]*b[1],
        a[2]*b[0] - a[0]*b[2],
        a[0]*b[1] - a[1]*b[0]
    )

def dot(a, b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

def normalize(v):
    norm = math.sqrt(dot(v, v))
    return (v[0]/norm, v[1]/norm, v[2]/norm) if norm != 0 else (0, 0, 0)

def gps_to_vector(lat, lon):
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)
    x = math.cos(lat_rad) * math.cos(lon_rad)
    y = math.cos(lat_rad) * math.sin(lon_rad)
    z = math.sin(lat_rad)
    return (x, y, z)

def vector_to_gps(v):
    x, y, z = v
    lat_rad = math.asin(z)
    lon_rad = math.atan2(y, x)
    return (math.degrees(lat_rad), math.degrees(lon_rad))

def calculate_distance(v1, v2):
    """Calcule la distance entre deux points sur la sphère unitaire"""
    dot_product = dot(v1, v2)
    dot_product = max(min(dot_product, 1.0), -1.0)  # Clamp pour éviter les erreurs numériques
    central_angle = math.acos(dot_product)
    return EARTH_RADIUS * central_angle

def is_on_arc(P, A, B, epsilon=1e-9):
    theta_AP = math.acos(max(min(dot(A, P), 1.0), -1.0))
    theta_PB = math.acos(max(min(dot(P, B), 1.0), -1.0))
    theta_AB = math.acos(max(min(dot(A, B), 1.0), -1.0))
    return abs(theta_AP + theta_PB - theta_AB) < epsilon

def find_intersection_and_angles(line1, line2):
    # Conversion des points GPS en coordonnées sphériques
    A = gps_to_vector(*line1[0])
    B = gps_to_vector(*line1[1])

    C = gps_to_vector(*line2[0])
    D = gps_to_vector(*line2[1])

    # Calcul des longueurs des segments
    len1 = calculate_distance(A, B)
    len2 = calculate_distance(C, D)

    # Calcul des normales des grands cercles
    normal_AB = cross(A, B)
    normal_CD = cross(C, D)

    # Vérification de l'intersection
    direction = cross(normal_AB, normal_CD)
    dir_norm = math.sqrt(dot(direction, direction))
    if dir_norm < 1e-9:
        return (None, None, len1, len2, None, None, None, None)  # Segments parallèles

    direction = normalize(direction)
    candidates = [direction, (-direction[0], -direction[1], -direction[2])]

    # Recherche du point d'intersection valide
    intersection = None
    for P in candidates:
        if is_on_arc(P, A, B) and is_on_arc(P, C, D):
            intersection = P
            break

    if not intersection:
        return (None, None, len1, len2, None, None, None, None)

    # Conversion du point d'intersection en GPS
    intersection_gps = vector_to_gps(intersection)

    # Calcul des longueurs des segments
    X = gps_to_vector(lat=intersection_gps[0], lon=intersection_gps[1])
    seg1 = calculate_distance(A, X)
    seg2 = calculate_distance(B, X)
    seg3 = calculate_distance(C, X)
    seg4 = calculate_distance(D, X)


    # Calcul des angles
    tangent_AB = normalize(cross(normal_AB, intersection))
    tangent_CD = normalize(cross(normal_CD, intersection))
    
    dot_tangent = dot(tangent_AB, tangent_CD)
    dot_tangent = max(min(dot_tangent, 1.0), -1.0)
    angle = math.degrees(math.acos(dot_tangent))
    
    acute = min(angle, 180 - angle)
    obtuse = 180 - acute
    angles = [acute, obtuse, acute, obtuse]

    return (intersection_gps, angles, len1, len2, seg1, seg2, seg3, seg4)


def main():

    parser = argparse.ArgumentParser(description="Prendre quatre arguments de type tuple depuis la ligne de commande pour deux segments GPS.")
    parser.add_argument('segment1_start', type=ast.literal_eval, help="Tuple représentant la position GPS de départ du segment 1 (latitude, longitude)")
    parser.add_argument('segment1_end', type=ast.literal_eval, help="Tuple représentant la position GPS de fin du segment 1 (latitude, longitude)")
    parser.add_argument('segment2_start', type=ast.literal_eval, help="Tuple représentant la position GPS de départ du segment 2 (latitude, longitude)")
    parser.add_argument('segment2_end', type=ast.literal_eval, help="Tuple représentant la position GPS de fin du segment 2 (latitude, longitude)")


    args = parser.parse_args()

    line1 = (args.segment1_start, args.segment1_end)
    line2 = (args.segment2_start, args.segment2_end)

    result = find_intersection_and_angles(line1, line2)
    intersection, angles, len1, len2, seg1, seg2, seg3, seg4 = result
    
    if angles is None:
        angles=[0,0,0,0]
    
    if intersection:
        print(f"Intersection GPS: {intersection}")
        print(f"    Angle AXC: {angles[0]:.2f}°")
        print(f"    Angle AXD: {angles[1]:.2f}°")
        print(f"    Angle BXC: {angles[3]:.2f}°")
        print(f"    Angle BXD: {angles[2]:.2f}°")
    else:
        print("Pas d'intersection")
    
    print(f"Longueur AB: {len1:.2f} m")
    print(f"    Longueur AX: {seg1:.2f} m")
    print(f"    Longueur BX: {seg2:.2f} m")
    
    print(f"Longueur CD: {len2:.2f} m")
    print(f"    Longueur CX: {seg3:.2f} m")
    print(f"    Longueur DX: {seg4:.2f} m")

if __name__ == "__main__":
    main()

