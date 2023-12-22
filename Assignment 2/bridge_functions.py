"""Assignment 2: Bridges"""

import csv
from copy import deepcopy
from math import sin, cos, asin, radians, sqrt, inf
from typing import TextIO

from constants import (
    ID_INDEX, NAME_INDEX, HIGHWAY_INDEX, LAT_INDEX,
    LON_INDEX, YEAR_INDEX, LAST_MAJOR_INDEX,
    LAST_MINOR_INDEX, NUM_SPANS_INDEX,
    SPAN_DETAILS_INDEX, LENGTH_INDEX,
    LAST_INSPECTED_INDEX, BCIS_INDEX, FROM_SEP, TO_SEP,
    HIGH_PRIORITY_BCI, MEDIUM_PRIORITY_BCI,
    LOW_PRIORITY_BCI, HIGH_PRIORITY_RADIUS,
    MEDIUM_PRIORITY_RADIUS, LOW_PRIORITY_RADIUS,
    EARTH_RADIUS)
EPSILON = 0.01


def read_data(csv_file: TextIO) -> list[list[str]]:
    """Read and return the contents of the open CSV file csv_file as a
    list of lists, where each inner list contains the values from one
    line of csv_file.

    Docstring examples not given since the function reads from a file.

    """

    lines = csv.reader(csv_file)
    return list(lines)[2:]


def calculate_distance(lat1: float, lon1: float,
                       lat2: float, lon2: float) -> float:
    """Return the distance in kilometers between the two locations defined by
    (lat1, lon1) and (lat2, lon2), rounded to the nearest meter.

    >>> abs(calculate_distance(43.659777, -79.397383, 43.657129, -79.399439)
    ...     - 0.338) < EPSILON
    True
    >>> abs(calculate_distance(43.42, -79.24, 53.32, -113.30)
    ...     - 2713.226) < EPSILON
    True
    >>> abs(calculate_distance(0, 0, 0, 0) - 0) < EPSILON
    True
    """

    lat1, lon1, lat2, lon2 = (radians(lat1), radians(lon1),
                              radians(lat2), radians(lon2))

    haversine = (sin((lat2 - lat1) / 2) ** 2
                 + cos(lat1) * cos(lat2) * sin((lon2 - lon1) / 2) ** 2)

    return round(2 * EARTH_RADIUS * asin(sqrt(haversine)), 3)


THREE_BRIDGES_UNCLEANED = [
    ['1 -  32/', 'Highway 24 Underpass at Highway 403', '403', '43.167233',
     '-80.275567', '1965', '2014', '2009', '4',
     'Total=64  (1)=12;(2)=19;(3)=21;(4)=12;', '65', '04/13/2012', '72.3', '',
     '72.3', '', '69.5', '', '70', '', '70.3', '', '70.5', '', '70.7', '72.9',
     ''],
    ['1 -  43/', 'WEST STREET UNDERPASS', '403', '43.164531', '-80.251582',
     '1963', '2014', '2007', '4',
     'Total=60.4  (1)=12.2;(2)=18;(3)=18;(4)=12.2;', '61', '04/13/2012',
     '71.5', '', '71.5', '', '68.1', '', '69', '', '69.4', '', '69.4', '',
     '70.3', '73.3', ''],
    ['2 -   4/', 'STOKES RIVER BRIDGE', '6', '45.036739', '-81.33579', '1958',
     '2013', '', '1', 'Total=16  (1)=16;', '18.4', '08/28/2013', '85.1',
     '85.1', '', '67.8', '', '67.4', '', '69.2', '70', '70.5', '', '75.1', '',
     '90.1', '']
]

THREE_BRIDGES = [
    [1, 'Highway 24 Underpass at Highway 403', '403', 43.167233, -80.275567,
     '1965', '2014', '2009', 4, [12.0, 19.0, 21.0, 12.0], 65.0, '04/13/2012',
     [72.3, 69.5, 70.0, 70.3, 70.5, 70.7, 72.9]],
    [2, 'WEST STREET UNDERPASS', '403', 43.164531, -80.251582,
     '1963', '2014', '2007', 4, [12.2, 18.0, 18.0, 12.2], 61.0, '04/13/2012',
     [71.5, 68.1, 69.0, 69.4, 69.4, 70.3, 73.3]],
    [3, 'STOKES RIVER BRIDGE', '6', 45.036739, -81.33579,
     '1958', '2013', '', 1, [16.0], 18.4, '08/28/2013',
     [85.1, 67.8, 67.4, 69.2, 70.0, 70.5, 75.1, 90.1]]
]

# Extra for examples
THREE_BRIDGES_UNCLEANED2 = [
    ['1 -  32/', 'Highway 24 Underpass at Highway 403', '403', '43.167233',
     '-80.275567', '1965', '2014', '2010', '4',
     'Total=64  (1)=12;(2)=19;(3)=21;(4)=12;', '65', '04/13/2012', '72.3', '',
     '72.3', '', '69.5', '', '70', '', '70.3', '', '70.5', '', '70.7', '72.9',
     ''],
    ['1 -  43/', 'WEST STREET UNDERPASS', '403', '43.164531', '-80.251582',
     '1963', '2014', '2007', '4',
     'Total=60.4  (1)=12.2;(2)=18;(3)=18;(4)=12.2;', '61', '04/13/2012',
     '71.5', '', '71.5', '', '68.1', '', '69', '', '69.4', '', '69.4', '',
     '70.3', '73.3', ''],
    ['2 -   4/', 'STOKES RIVER BRIDGE', '6', '45.036739', '-81.33579', '1958',
     '2013', '', '1', 'Total=16  (1)=16;', '18.4', '08/28/2013', '85.1',
     '85.1', '', '67.8', '', '67.4', '', '69.2', '70', '70.5', '', '75.1', '',
     '90.1', '']
]

THREE_BRIDGES2 = [
    [1, 'Highway 24 Underpass at Highway 403', '403', 43.167233, -80.275567,
     '1965', '2014', '2010', 4, [12.0, 19.0, 21.0, 12.0], 65.0, '04/13/2012',
     [72.3, 69.5, 70.0, 70.3, 70.5, 70.7, 72.9]],
    [2, 'WEST STREET UNDERPASS', '403', 43.164531, -80.251582,
     '1963', '2014', '2007', 4, [12.2, 18.0, 18.0, 12.2], 61.0, '04/13/2012',
     [71.5, 68.1, 69.0, 69.4, 69.4, 70.3, 73.3]],
    [3, 'STOKES RIVER BRIDGE', '6', 45.036739, -81.33579,
     '1958', '2013', '', 1, [16.0], 18.4, '08/28/2013',
     [85.1, 67.8, 67.4, 69.2, 70.0, 70.5, 75.1, 90.1]]
]

THREE_BRIDGES_UNCLEANED3 = [
    ['1 -  32/', 'Highway 24 Underpass at Highway 403', '403', '43.167233',
     '-80.275567', '1965', '2014', '2011', '4',
     'Total=64  (1)=12;(2)=19;(3)=21;(4)=12;', '65', '04/13/2012', '72.3', '',
     '72.3', '', '69.5', '', '70', '', '70.3', '', '70.5', '', '70.7', '72.9',
     ''],
    ['1 -  43/', 'WEST STREET UNDERPASS', '403', '43.164531', '-80.251582',
     '1963', '2014', '2007', '4',
     'Total=60.4  (1)=12.2;(2)=18;(3)=18;(4)=12.2;', '61', '04/13/2012',
     '71.5', '', '71.5', '', '68.1', '', '69', '', '69.4', '', '69.4', '',
     '70.3', '73.3', ''],
    ['2 -   4/', 'STOKES RIVER BRIDGE', '6', '45.036739', '-81.33579', '1958',
     '2013', '', '1', 'Total=16  (1)=16;', '18.4', '08/28/2013', '85.1',
     '85.1', '', '67.8', '', '67.4', '', '69.2', '70', '70.5', '', '75.1', '',
     '90.1', '']
]

THREE_BRIDGES3 = [
    [1, 'Highway 24 Underpass at Highway 403', '403', 43.167233, -80.275567,
     '1965', '2014', '2011', 4, [12.0, 19.0, 21.0, 12.0], 65.0, '04/13/2012',
     [72.3, 69.5, 70.0, 70.3, 70.5, 70.7, 72.9]],
    [2, 'WEST STREET UNDERPASS', '403', 43.164531, -80.251582,
     '1963', '2014', '2007', 4, [12.2, 18.0, 18.0, 12.2], 61.0, '04/13/2012',
     [71.5, 68.1, 69.0, 69.4, 69.4, 70.3, 73.3]],
    [3, 'STOKES RIVER BRIDGE', '6', 45.036739, -81.33579,
     '1958', '2013', '', 1, [16.0], 18.4, '08/28/2013',
     [85.1, 67.8, 67.4, 69.2, 70.0, 70.5, 75.1, 90.1]]
]


def get_bridge(bridge_data: list[list], bridge_id: int) -> list:
    """Return the data for the bridge with id bridge_id from bridge data
    bridge_data. If there is no bridge with id bridge_id, return [].

    Precondition: The bridge is in correct format.

    >>> result = get_bridge(THREE_BRIDGES, 1)
    >>> result == [
    ...    1, 'Highway 24 Underpass at Highway 403', '403', 43.167233,
    ...    -80.275567, '1965', '2014', '2009', 4,
    ...    [12.0, 19.0, 21.0, 12.0], 65.0, '04/13/2012',
    ...    [72.3, 69.5, 70.0, 70.3, 70.5, 70.7, 72.9]]
    True
    >>> result2 = get_bridge(THREE_BRIDGES, 2)
    >>> result2 == [
    ...    2, 'WEST STREET UNDERPASS', '403', 43.164531,
    ...    -80.251582, '1963', '2014', '2007', 4,
    ...    [12.2, 18.0, 18.0, 12.2], 61.0, '04/13/2012',
    ...    [71.5, 68.1, 69.0, 69.4, 69.4, 70.3, 73.3]]
    True
    >>> get_bridge(THREE_BRIDGES, 42)
    []

    """

    for bridge in bridge_data:
        if bridge[ID_INDEX] == bridge_id:
            return bridge

    return []


def get_average_bci(bridge_data: list[list], bridge_id: int) -> float:
    """Return the average BCI of the bridge with id bridge_id from bridge data
    bridge_data. If there is no bridge with id bridge_id, return 0.

    Precondition: The bridge is in correct format.

    >>> abs(get_average_bci(THREE_BRIDGES, 1) - 70.8857) < EPSILON
    True
    >>> abs(get_average_bci(THREE_BRIDGES, 2) - 70.1429) < EPSILON
    True
    >>> abs(get_average_bci(THREE_BRIDGES, 4) - 0.0) < EPSILON
    True

    """

    bridge = get_bridge(bridge_data, bridge_id)
    average = 0

    if len(bridge) > 0:
        sum_bci = 0
        for bci in bridge[BCIS_INDEX]:
            sum_bci += bci
            average = sum_bci / len(bridge[BCIS_INDEX])

    return average


def get_total_length_on_hwy(bridge_data: list[list], bridge_hwy: str) -> float:
    """Return the total length of bridges on the highway bridge_hwy from bridge
    data bridge_data. If there are no bridges on bridge_hwy, return 0.

    Precondition: The bridge is in correct format.

    >>> abs(get_total_length_on_hwy(THREE_BRIDGES, '403') - 126.0) < EPSILON
    True
    >>> abs(get_total_length_on_hwy(THREE_BRIDGES, '6') - 18.4) < EPSILON
    True
    >>> abs(get_total_length_on_hwy(THREE_BRIDGES, '300') - 0.0) < EPSILON
    True

    """

    sum_bridge = 0

    for bridge in bridge_data:
        if bridge[HIGHWAY_INDEX] == bridge_hwy:
            sum_bridge += bridge[LENGTH_INDEX]

    return sum_bridge


def get_distance_between(bridge1: list, bridge2: list) -> float:
    """Return the distance in kilometers, rounded to the nearest metre
    (i.e., 3 decimal places) between bridge1 and bridge2.

    Precondition: The bridges exist and are in correct format.

    >>> abs(get_distance_between(THREE_BRIDGES[0], THREE_BRIDGES[1])
    ...     - 1.968) < EPSILON
    True
    >>> abs(get_distance_between(THREE_BRIDGES[1], THREE_BRIDGES[2])
    ...     - 225.459) < EPSILON
    True
    >>> abs(get_distance_between(THREE_BRIDGES[0], THREE_BRIDGES[2])
    ...     - 224.451) < EPSILON
    True

    """

    lat1 = bridge1[LAT_INDEX]
    lon1 = bridge1[LON_INDEX]
    lat2 = bridge2[LAT_INDEX]
    lon2 = bridge2[LON_INDEX]

    return calculate_distance(lat1, lon1, lat2, lon2)


def get_closest_bridge(bridge_data: list[list], bridge_id: int) -> int:
    """Return the id of a bridge that has the shortest distance to the
    bridge with the given id bridge_id from bridge data bridge_data. The
    function should not return the bridge with the given id itself, i.e.,
    we do not consider a bridge to be closest to itself.

    Precondition: The bridges exist and are in correct format and and that
    there are at least two bridge in the bridge data.

    >>> get_closest_bridge(THREE_BRIDGES, 2)
    1
    >>> get_closest_bridge(THREE_BRIDGES, 1)
    2
    >>> get_closest_bridge(THREE_BRIDGES, 3)
    1

    """

    closest_bridge_id = None
    shortest_distance = float('inf')

    bridge1 = None
    for bridge in bridge_data:
        if bridge[ID_INDEX] == bridge_id:
            bridge1 = bridge
            break

    for bridge in bridge_data:
        if bridge[ID_INDEX] != bridge_id and \
           get_distance_between(bridge1, bridge) < shortest_distance:
            shortest_distance = get_distance_between(bridge1, bridge)
            closest_bridge_id = bridge[ID_INDEX]

    return closest_bridge_id


def get_bridges_in_radius(bridge_data: list[list], lat: float, long: float,
                          rad: float) -> list[list]:
    """Return a list of ids of all bridges that are within the given distance,
    or radius, calculated using latitude, lat, and longitude, long, of the given
    location from bridge data bridge_data.

    Precondition: The bridge is in correct format.

    >>> get_bridges_in_radius(THREE_BRIDGES, 43.10, -80.15, 50)
    [1, 2]
    >>> get_bridges_in_radius(THREE_BRIDGES, 43.10, -80.15, 20)
    [1, 2]
    >>> get_bridges_in_radius(THREE_BRIDGES, 32.10, -90.15, 40)
    []

    """

    in_radius = []

    for i in bridge_data:
        if rad >= calculate_distance(lat, long, i[LAT_INDEX], i[LON_INDEX]):
            in_radius.append(i[ID_INDEX])
    return in_radius


def get_bridges_with_bci_below(bridge_data: list[list], bridge_ids: list[int],
                               bci: float) -> list[int]:
    """Return a list of ids of all bridges whose ids, bridge_ids, are in the
    given list of ids and whose BCI is less than or equal to the given BCI from
    bridge data bridge_data.

    Precondition: The bridge is in correct format.

    >>> get_bridges_with_bci_below(THREE_BRIDGES, [1,2], 72)
    [2]
    >>> get_bridges_with_bci_below(THREE_BRIDGES, [1,3], 86)
    [1, 3]
    >>> get_bridges_with_bci_below(THREE_BRIDGES, [1,2, 3], 73)
    [1, 2]

    """

    matching_bridge_ids = []

    for bridge in bridge_data:
        if bridge[ID_INDEX] in bridge_ids:
            if bridge[BCIS_INDEX][0] <= bci:
                matching_bridge_ids.append(bridge[ID_INDEX])

    return matching_bridge_ids


def get_bridges_containing(bridge_data: list[list], search: str) -> list[int]:
    """Return a list of ids of all bridges whose names contain the search
    string, search, from bridge data bridge_data.The search is case-insensitive.

    Precondition: The bridge is in correct format.

    >>> get_bridges_containing(THREE_BRIDGES, 'underpass')
    [1, 2]
    >>> get_bridges_containing(THREE_BRIDGES, 'pass')
    [1, 2]
    >>> get_bridges_containing(THREE_BRIDGES, 'stokes')
    [3]
    >>> get_bridges_containing(THREE_BRIDGES, 'valley')
    []

    """

    word_to_search = search.lower()
    bridges_containing = []

    for bridge in bridge_data:
        if word_to_search in bridge[NAME_INDEX].lower():
            bridges_containing.append(bridge[ID_INDEX])

    return bridges_containing


def inspect_bridges(bridge_data: list[list], bridge_ids: list[int], date: str,
                    bci: float) -> None:
    """Update the bridges in bridge_data with id in bridge_ids with the new
    date and BCI score for a new inspection.

    Precondition: The bridge is in correct format.

    >>> bridges = deepcopy(THREE_BRIDGES)
    >>> inspect_bridges(bridges, [1], '09/15/2018', 71.9)
    >>> bridges == [
    ...   [1, 'Highway 24 Underpass at Highway 403', '403',
    ...    43.167233, -80.275567, '1965', '2014', '2009', 4,
    ...    [12.0, 19.0, 21.0, 12.0], 65, '09/15/2018',
    ...    [71.9, 72.3, 69.5, 70.0, 70.3, 70.5, 70.7, 72.9]],
    ...   [2, 'WEST STREET UNDERPASS', '403', 43.164531, -80.251582,
    ...    '1963', '2014', '2007', 4, [12.2, 18.0, 18.0, 12.2],
    ...    61, '04/13/2012', [71.5, 68.1, 69.0, 69.4, 69.4, 70.3, 73.3]],
    ...   [3, 'STOKES RIVER BRIDGE', '6', 45.036739, -81.33579,
    ...    '1958', '2013', '', 1, [16.0], 18.4, '08/28/2013',
    ...    [85.1, 67.8, 67.4, 69.2, 70.0, 70.5, 75.1, 90.1]]]
    True
    >>> bridges2 = deepcopy(THREE_BRIDGES)
    >>> inspect_bridges(bridges2, [2], '10/14/2019', 80.3)
    >>> bridges2 == [
    ...   [1, 'Highway 24 Underpass at Highway 403', '403',
    ...    43.167233, -80.275567, '1965', '2014', '2009', 4,
    ...    [12.0, 19.0, 21.0, 12.0], 65, '04/13/2012',
    ...    [72.3, 69.5, 70.0, 70.3, 70.5, 70.7, 72.9]],
    ...   [2, 'WEST STREET UNDERPASS', '403', 43.164531, -80.251582,
    ...    '1963', '2014', '2007', 4, [12.2, 18.0, 18.0, 12.2],
    ...    61, '10/14/2019', [80.3, 71.5, 68.1, 69.0, 69.4, 69.4, 70.3, 73.3]],
    ...   [3, 'STOKES RIVER BRIDGE', '6', 45.036739, -81.33579,
    ...    '1958', '2013', '', 1, [16.0], 18.4, '08/28/2013',
    ...    [85.1, 67.8, 67.4, 69.2, 70.0, 70.5, 75.1, 90.1]]]
    True
    >>> bridges3 = deepcopy(THREE_BRIDGES)
    >>> inspect_bridges(bridges3, [3], '01/21/2020', 77.2)
    >>> bridges3 == [
    ...   [1, 'Highway 24 Underpass at Highway 403', '403',
    ...    43.167233, -80.275567, '1965', '2014', '2009', 4,
    ...    [12.0, 19.0, 21.0, 12.0], 65, '04/13/2012',
    ...    [72.3, 69.5, 70.0, 70.3, 70.5, 70.7, 72.9]],
    ...   [2, 'WEST STREET UNDERPASS', '403', 43.164531, -80.251582,
    ...    '1963', '2014', '2007', 4, [12.2, 18.0, 18.0, 12.2],
    ...    61, '04/13/2012', [71.5, 68.1, 69.0, 69.4, 69.4, 70.3, 73.3]],
    ...   [3, 'STOKES RIVER BRIDGE', '6', 45.036739, -81.33579,
    ...    '1958', '2013', '', 1, [16.0], 18.4, '01/21/2020',
    ...    [77.2, 85.1, 67.8, 67.4, 69.2, 70.0, 70.5, 75.1, 90.1]]]
    True

    """

    for bridge in bridge_data:
        if bridge[ID_INDEX] in bridge_ids:
            bridge[LAST_INSPECTED_INDEX] = date
            bridge[BCIS_INDEX].insert(0, bci)


def add_rehab(bridge_data: list[list], bridge_id: int, date: str,
              maj_min: bool) -> None:
    """Update the bridge in bridge_data with the given id, bridge_id with the
    new rehab year record: year of major rehab, if the last argument is True,
    and year of minor rehab if the last argument is False.
    If there is no bridge with the given id in the given bridge data, the
    function has no effect.

    Precondition: The bridge is in correct format.

    >>> bridges = deepcopy(THREE_BRIDGES)
    >>> add_rehab(bridges, 1, '09/15/2023', False)
    >>> bridges == [
    ...   [1, 'Highway 24 Underpass at Highway 403', '403',
    ...    43.167233, -80.275567, '1965', '2014', '2023', 4,
    ...    [12.0, 19.0, 21.0, 12.0], 65, '04/13/2012',
    ...    [72.3, 69.5, 70.0, 70.3, 70.5, 70.7, 72.9]],
    ...   [2, 'WEST STREET UNDERPASS', '403', 43.164531, -80.251582,
    ...    '1963', '2014', '2007', 4, [12.2, 18.0, 18.0, 12.2],
    ...    61, '04/13/2012', [71.5, 68.1, 69.0, 69.4, 69.4, 70.3, 73.3]],
    ...   [3, 'STOKES RIVER BRIDGE', '6', 45.036739, -81.33579,
    ...    '1958', '2013', '', 1, [16.0], 18.4, '08/28/2013',
    ...    [85.1, 67.8, 67.4, 69.2, 70.0, 70.5, 75.1, 90.1]]]
    True
    >>> bridges2 = deepcopy(THREE_BRIDGES)
    >>> add_rehab(bridges2, 2, '08/13/2021', True)
    >>> bridges2 == [
    ...   [1, 'Highway 24 Underpass at Highway 403', '403',
    ...    43.167233, -80.275567, '1965', '2014', '2009', 4,
    ...    [12.0, 19.0, 21.0, 12.0], 65, '04/13/2012',
    ...    [72.3, 69.5, 70.0, 70.3, 70.5, 70.7, 72.9]],
    ...   [2, 'WEST STREET UNDERPASS', '403', 43.164531, -80.251582,
    ...    '1963', '2021', '2007', 4, [12.2, 18.0, 18.0, 12.2],
    ...    61, '04/13/2012', [71.5, 68.1, 69.0, 69.4, 69.4, 70.3, 73.3]],
    ...   [3, 'STOKES RIVER BRIDGE', '6', 45.036739, -81.33579,
    ...    '1958', '2013', '', 1, [16.0], 18.4, '08/28/2013',
    ...    [85.1, 67.8, 67.4, 69.2, 70.0, 70.5, 75.1, 90.1]]]
    True
    >>> bridges3 = deepcopy(THREE_BRIDGES)
    >>> add_rehab(bridges3, 4, '11/23/2020', False)
    >>> bridges3 == [
    ...   [1, 'Highway 24 Underpass at Highway 403', '403',
    ...    43.167233, -80.275567, '1965', '2014', '2009', 4,
    ...    [12.0, 19.0, 21.0, 12.0], 65, '04/13/2012',
    ...    [72.3, 69.5, 70.0, 70.3, 70.5, 70.7, 72.9]],
    ...   [2, 'WEST STREET UNDERPASS', '403', 43.164531, -80.251582,
    ...    '1963', '2014', '2007', 4, [12.2, 18.0, 18.0, 12.2],
    ...    61, '04/13/2012', [71.5, 68.1, 69.0, 69.4, 69.4, 70.3, 73.3]],
    ...   [3, 'STOKES RIVER BRIDGE', '6', 45.036739, -81.33579,
    ...    '1958', '2013', '', 1, [16.0], 18.4, '08/28/2013',
    ...    [85.1, 67.8, 67.4, 69.2, 70.0, 70.5, 75.1, 90.1]]]
    True

    """

    for bridge in bridge_data:
        if bridge[ID_INDEX] == bridge_id:
            if maj_min:
                bridge[LAST_MAJOR_INDEX] = date[6:]
            else:
                bridge[LAST_MINOR_INDEX] = date[6:]


def format_data(data: list[list[str]]) -> None:
    """Modify the uncleaned bridge data data, so that it contains proper
    bridge data, i.e., follows the format outlined in the 'Data
    formatting' section of the assignment handout.

    >>> d = THREE_BRIDGES_UNCLEANED
    >>> format_data(d)
    >>> d == THREE_BRIDGES
    True
    >>> d2 = THREE_BRIDGES_UNCLEANED2
    >>> format_data(d2)
    >>> d2 == THREE_BRIDGES2
    True
    >>> d3 = THREE_BRIDGES_UNCLEANED3
    >>> format_data(d3)
    >>> d3 == THREE_BRIDGES3
    True

    """

    bridge_id = 1
    for bridge in data:
        bridge[ID_INDEX] = bridge_id
        bridge_id += 1
        bridge[NAME_INDEX] = str(bridge[NAME_INDEX])
        bridge[HIGHWAY_INDEX] = str(bridge[HIGHWAY_INDEX])
        bridge[YEAR_INDEX] = str(bridge[YEAR_INDEX])
        bridge[LAST_MAJOR_INDEX] = str(bridge[LAST_MAJOR_INDEX])
        bridge[LAST_MINOR_INDEX] = str(bridge[LAST_MINOR_INDEX])

        format_location(bridge)
        format_spans(bridge)
        format_length(bridge)
        format_bcis(bridge)


def assign_inspectors(bridge_data: list[list], inspectors: list[list[float]],
                      max_bridges: int) -> list[list[int]]:
    """Return a list of bridge IDs from bridge data bridge_data, to be
    assigned to each inspector in inspectors. inspectors is a list
    containing (latitude, longitude) pairs representing each
    inspector's location. At most max_bridges are assigned to each
    inspector, and each bridge is assigned once (to the first
    inspector that can inspect that bridge).

    Precondition: The bridge is in correct format.

    See the "Assigning Inspectors" section of the handout for more details.

    >>> assign_inspectors(THREE_BRIDGES, [[43.10, -80.15], [42.10, -81.15]], 0)
    [[], []]
    >>> assign_inspectors(THREE_BRIDGES, [[43.10, -80.15]], 1)
    [[1]]
    >>> assign_inspectors(THREE_BRIDGES, [[43.10, -80.15]], 2)
    [[1, 2]]
    >>> assign_inspectors(THREE_BRIDGES, [[43.10, -80.15]], 3)
    [[1, 2]]
    >>> assign_inspectors(THREE_BRIDGES, [[43.20, -80.35], [43.10, -80.15]], 1)
    [[1], [2]]
    >>> assign_inspectors(THREE_BRIDGES, [[43.20, -80.35], [43.10, -80.15]], 2)
    [[1, 2], []]
    >>> assign_inspectors(THREE_BRIDGES, [[43.20, -80.35], [45.0368, -81.34]],
    ...                   2)
    [[1, 2], [3]]
    >>> assign_inspectors(THREE_BRIDGES, [[38.691, -80.85], [43.20, -80.35]],
    ...                   2)
    [[], [1, 2]]

    """

    assigned_bridges = []
    check_list = []
    bridges = list(range(1, len(bridge_data) + 1))

    priorities = [HIGH_PRIORITY_BCI, MEDIUM_PRIORITY_BCI, LOW_PRIORITY_BCI]

    for inspector in inspectors:
        lon1 = inspector[1]  # lat1 is inspector[0] in the variable 'pr_rad'
        counter = 0
        inspector_list = []

        for i in priorities:
            pr_rad = get_bridges_in_radius(bridge_data, inspector[0], lon1, i)
            pr_brid = get_bridges_with_bci_below(bridge_data, bridges, i)

            _ = [
                (
                    inspector_list.append(bridge[ID_INDEX]),
                    check_list.extend([bridge[ID_INDEX]]),
                    (counter := counter + 1)
                )
                for bridge in bridge_data
                if (bridge[ID_INDEX] in pr_rad
                    and bridge[ID_INDEX] in pr_brid
                    and bridge[ID_INDEX] not in check_list
                    and counter < max_bridges)
            ]

        assigned_bridges.append(inspector_list)

    return assigned_bridges


def format_location(bridge_record: list) -> None:
    """Format latitude and longitude data in the bridge record bridge_record.

    Precondition: LAT_INDEX and LON_INDEX have digits.

    >>> record = ['1 -  32/', 'Highway 24 Underpass at Highway 403', '403',
    ...           '43.167233', '-80.275567', '1965', '2014', '2009', '4',
    ...           'Total=64  (1)=12;(2)=19;(3)=21;(4)=12;', '65', '04/13/2012',
    ...           '72.3', '', '72.3', '', '69.5', '', '70', '', '70.3', '',
    ...           '70.5', '', '70.7', '72.9', '']
    >>> format_location(record)
    >>> record == ['1 -  32/', 'Highway 24 Underpass at Highway 403', '403',
    ...           43.167233, -80.275567, '1965', '2014', '2009', '4',
    ...           'Total=64  (1)=12;(2)=19;(3)=21;(4)=12;', '65', '04/13/2012',
    ...           '72.3', '', '72.3', '', '69.5', '', '70', '', '70.3', '',
    ...           '70.5', '', '70.7', '72.9', '']
    True
    >>> record2 = ['1 -  32/', 'Highway 24 Underpass at Highway 403', '403',
    ...           '34.522256', '-76.654676', '1965', '2014', '2009', '4',
    ...           'Total=64  (1)=12;(2)=19;(3)=21;(4)=12;', '65', '04/13/2012',
    ...           '72.3', '', '72.3', '', '69.5', '', '70', '', '70.3', '',
    ...           '70.5', '', '70.7', '72.9', '']
    >>> format_location(record2)
    >>> record2 == ['1 -  32/', 'Highway 24 Underpass at Highway 403', '403',
    ...           34.522256, -76.654676, '1965', '2014', '2009', '4',
    ...           'Total=64  (1)=12;(2)=19;(3)=21;(4)=12;', '65', '04/13/2012',
    ...           '72.3', '', '72.3', '', '69.5', '', '70', '', '70.3', '',
    ...           '70.5', '', '70.7', '72.9', '']
    True
    >>> record3 = ['1 -  32/', 'Highway 24 Underpass at Highway 403', '403',
    ...           '43', '-80', '1965', '2014', '2009', '4',
    ...           'Total=64  (1)=12;(2)=19;(3)=21;(4)=12;', '65', '04/13/2012',
    ...           '72.3', '', '72.3', '', '69.5', '', '70', '', '70.3', '',
    ...           '70.5', '', '70.7', '72.9', '']
    >>> format_location(record3)
    >>> record3 == ['1 -  32/', 'Highway 24 Underpass at Highway 403', '403',
    ...           43.0, -80.0, '1965', '2014', '2009', '4',
    ...           'Total=64  (1)=12;(2)=19;(3)=21;(4)=12;', '65', '04/13/2012',
    ...           '72.3', '', '72.3', '', '69.5', '', '70', '', '70.3', '',
    ...           '70.5', '', '70.7', '72.9', '']
    True
    """

    bridge_record[LAT_INDEX] = float(bridge_record[LAT_INDEX])
    bridge_record[LON_INDEX] = float(bridge_record[LON_INDEX])


def format_spans(bridge_record: list) -> None:
    """Format the bridge spans data in the bridge record bridge_record.

    Precondition: SPAN_DETAILS_INDEX separates spans by "=" and ";"

    >>> record = ['1 -  32/', 'Highway 24 Underpass at Highway 403', '403',
    ...           '43.167233', '-80.275567', '1965', '2014', '2009', '4',
    ...           'Total=64  (1)=12;(2)=19;(3)=21;(4)=12;', '65', '04/13/2012',
    ...           '72.3', '', '72.3', '', '69.5', '', '70', '', '70.3', '',
    ...           '70.5', '', '70.7', '72.9', '']
    >>> format_spans(record)
    >>> record == ['1 -  32/', 'Highway 24 Underpass at Highway 403', '403',
    ...           '43.167233', '-80.275567', '1965', '2014', '2009', 4,
    ...           [12.0, 19.0, 21.0, 12.0], '65', '04/13/2012',
    ...           '72.3', '', '72.3', '', '69.5', '', '70', '', '70.3', '',
    ...           '70.5', '', '70.7', '72.9', '']
    True
    >>> record2 = ['1 -  32/', 'Highway 24 Underpass at Highway 403', '403',
    ...           '43.167233', '-80.275567', '1965', '2014', '2009', '4',
    ...           'Total=64  (1)=22;(2)=10;(3)=12;(4)=22;', '65', '04/13/2012',
    ...           '72.3', '', '72.3', '', '69.5', '', '70', '', '70.3', '',
    ...           '70.5', '', '70.7', '72.9', '']
    >>> format_spans(record2)
    >>> record2 == ['1 -  32/', 'Highway 24 Underpass at Highway 403', '403',
    ...           '43.167233', '-80.275567', '1965', '2014', '2009', 4,
    ...           [22.0, 10.0, 12.0, 22.0], '65', '04/13/2012',
    ...           '72.3', '', '72.3', '', '69.5', '', '70', '', '70.3', '',
    ...           '70.5', '', '70.7', '72.9', '']
    True
    >>> record3 = ['1 -  32/', 'Highway 24 Underpass at Highway 403', '403',
    ...           '43.167233', '-80.275567', '1965', '2014', '2009', '4',
    ...           'Total=64  (1)=12;(2)=32;(3)=22;(4)=14;', '65', '04/13/2012',
    ...           '72.3', '', '72.3', '', '69.5', '', '70', '', '70.3', '',
    ...           '70.5', '', '70.7', '72.9', '']
    >>> format_spans(record3)
    >>> record3 == ['1 -  32/', 'Highway 24 Underpass at Highway 403', '403',
    ...           '43.167233', '-80.275567', '1965', '2014', '2009', 4,
    ...           [12.0, 32.0, 22.0, 14.0], '65', '04/13/2012',
    ...           '72.3', '', '72.3', '', '69.5', '', '70', '', '70.3', '',
    ...           '70.5', '', '70.7', '72.9', '']
    True


    """

    span_data = bridge_record[SPAN_DETAILS_INDEX][6:-1].split(TO_SEP)
    span_list = [span.split(FROM_SEP)[1] for span in span_data]
    bridge_record[SPAN_DETAILS_INDEX] = list(map(float, span_list))

    bridge_record[NUM_SPANS_INDEX] = int(bridge_record[NUM_SPANS_INDEX])


def format_length(bridge_record: list) -> None:
    """Format the bridge length data in the bridge record bridge_record.

    Precondition: LENGTH_INDEX is a digit or an empty string

    >>> record = ['1 -  32/', 'Highway 24 Underpass at Highway 403', '403',
    ...           '43.167233', '-80.275567', '1965', '2014', '2009', '4',
    ...           'Total=64  (1)=12;(2)=19;(3)=21;(4)=12;', '65', '04/13/2012',
    ...           '72.3', '', '72.3', '', '69.5', '', '70', '', '70.3', '',
    ...           '70.5', '', '70.7', '72.9', '']
    >>> format_length(record)
    >>> record == ['1 -  32/', 'Highway 24 Underpass at Highway 403', '403',
    ...            '43.167233', '-80.275567', '1965', '2014', '2009', '4',
    ...            'Total=64  (1)=12;(2)=19;(3)=21;(4)=12;', 65, '04/13/2012',
    ...            '72.3', '', '72.3', '', '69.5', '', '70', '', '70.3', '',
    ...            '70.5', '', '70.7', '72.9', '']
    True
    >>> record2 = ['1 -  32/', 'Highway 24 Underpass at Highway 403', '403',
    ...           '43.167233', '-80.275567', '1965', '2014', '2009', '4',
    ...           'Total=64  (1)=12;(2)=19;(3)=21;(4)=12;', '44', '04/13/2012',
    ...           '72.3', '', '72.3', '', '69.5', '', '70', '', '70.3', '',
    ...           '70.5', '', '70.7', '72.9', '']
    >>> format_length(record2)
    >>> record2 == ['1 -  32/', 'Highway 24 Underpass at Highway 403', '403',
    ...            '43.167233', '-80.275567', '1965', '2014', '2009', '4',
    ...            'Total=64  (1)=12;(2)=19;(3)=21;(4)=12;', 44, '04/13/2012',
    ...            '72.3', '', '72.3', '', '69.5', '', '70', '', '70.3', '',
    ...            '70.5', '', '70.7', '72.9', '']
    True
    >>> record3 = ['1 -  32/', 'Highway 24 Underpass at Highway 403', '403',
    ...           '43.167233', '-80.275567', '1965', '2014', '2009', '4',
    ...           'Total=64  (1)=12;(2)=19;(3)=21;(4)=12;', '', '04/13/2012',
    ...           '72.3', '', '72.3', '', '69.5', '', '70', '', '70.3', '',
    ...           '70.5', '', '70.7', '72.9', '']
    >>> format_length(record3)
    >>> record3 == ['1 -  32/', 'Highway 24 Underpass at Highway 403', '403',
    ...            '43.167233', '-80.275567', '1965', '2014', '2009', '4',
    ...            'Total=64  (1)=12;(2)=19;(3)=21;(4)=12;', 0.0, '04/13/2012',
    ...            '72.3', '', '72.3', '', '69.5', '', '70', '', '70.3', '',
    ...            '70.5', '', '70.7', '72.9', '']
    True

    """

    if bridge_record[LENGTH_INDEX] == '':
        bridge_record[LENGTH_INDEX] = 0.0
    else:
        bridge_record[LENGTH_INDEX] = float(bridge_record[LENGTH_INDEX])


def format_bcis(bridge_record: list) -> None:
    """Format the bridge BCI data in the bridge record bridge_record.

    Precondition: [BCIS_INDEX + 1:] are digits

    >>> record = ['1 -  32/', 'Highway 24 Underpass at Highway 403', '403',
    ...           '43.167233', '-80.275567', '1965', '2014', '2009', '4',
    ...           'Total=64  (1)=12;(2)=19;(3)=21;(4)=12;', '65', '04/13/2012',
    ...           '72.3', '', '72.3', '', '69.5', '', '70', '', '70.3', '',
    ...           '70.5', '', '70.7', '72.9', '']
    >>> format_bcis(record)
    >>> record == ['1 -  32/', 'Highway 24 Underpass at Highway 403', '403',
    ...           '43.167233', '-80.275567', '1965', '2014', '2009', '4',
    ...           'Total=64  (1)=12;(2)=19;(3)=21;(4)=12;', '65', '04/13/2012',
    ...           [72.3, 69.5, 70.0, 70.3, 70.5, 70.7, 72.9]]
    True
    >>> record2 = ['1 -  32/', 'Highway 24 Underpass at Highway 403', '403',
    ...           '43.167233', '-80.275567', '1965', '2014', '2009', '4',
    ...           'Total=64  (1)=12;(2)=19;(3)=21;(4)=12;', '65', '04/13/2012',
    ...           '68.2', '', '68.2', '', '69.5', '', '71', '', '72.3', '',
    ...           '74.5', '', '75.1', '72', '']
    >>> format_bcis(record2)
    >>> record2 == ['1 -  32/', 'Highway 24 Underpass at Highway 403', '403',
    ...           '43.167233', '-80.275567', '1965', '2014', '2009', '4',
    ...           'Total=64  (1)=12;(2)=19;(3)=21;(4)=12;', '65', '04/13/2012',
    ...           [68.2, 69.5, 71.0, 72.3, 74.5, 75.1, 72.0]]
    True
    >>> record3 = ['1 -  32/', 'Highway 24 Underpass at Highway 403', '403',
    ...           '43.167233', '-80.275567', '1965', '2014', '2009', '4',
    ...           'Total=64  (1)=12;(2)=19;(3)=21;(4)=12;', '65', '04/13/2012',
    ...           '68.2', '', '72.8', '', '79.5', '', '73.5', '', '75', '',
    ...           '73.5', '', '71', '75.7', '']
    >>> format_bcis(record3)
    >>> record3 == ['1 -  32/', 'Highway 24 Underpass at Highway 403', '403',
    ...           '43.167233', '-80.275567', '1965', '2014', '2009', '4',
    ...           'Total=64  (1)=12;(2)=19;(3)=21;(4)=12;', '65', '04/13/2012',
    ...           [72.8, 79.5, 73.5, 75, 73.5, 71.0, 75.7]]
    True

    """

    bcis = []

    for char in bridge_record[BCIS_INDEX + 1:]:
        if char != '':
            bcis.append(char)

    float_bcis = [float(i) for i in bcis]

    del bridge_record[BCIS_INDEX + 1:]
    bridge_record[BCIS_INDEX] = float_bcis
