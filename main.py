"""
Seismic safety simulation — modular implementation.

Each major task (validation, degradation, warnings, score, status) lives in
its own function, with full parameter and return descriptions.
Python ≥ 3.8, standard library only.
"""

from typing import List, Tuple


def validate_parameters(
    building_height: float,
    num_floors: int,
    material_strength: float,
    building_age: int,
    seismic_magnitude: float,
    safety_factor: float,
) -> None:
    """
    Validate all simulation inputs.

    Parameters
    ----------
    building_height : float
        Total height of the building in meters; **must be > 0**.
    num_floors : int
        Number of above-ground floors; **must be ≥ 1**.
    material_strength : float
        Nominal material compressive strength (MPa); **must be > 0**.
    building_age : int
        Age of the building in years; **must be ≥ 0**.
    seismic_magnitude : float
        Design‐basis earthquake magnitude; **must be between 0 and 10**.
    safety_factor : float
        Global safety factor applied to the score; **must be > 1**.

    Raises
    ------
    ValueError
        If any parameter falls outside its acceptable range. The error message
        specifies the offending parameter and the valid range.
    """
    if building_height <= 0:
        raise ValueError("building_height must be > 0")
    if num_floors < 1:
        raise ValueError("num_floors must be ≥ 1")
    if material_strength <= 0:
        raise ValueError("material_strength must be > 0")
    if building_age < 0:
        raise ValueError("building_age must be ≥ 0")
    if not (0 <= seismic_magnitude <= 10):
        raise ValueError("seismic_magnitude must be between 0 and 10")
    if safety_factor <= 1:
        raise ValueError("safety_factor must be > 1")


def apply_material_degradation(
    material_strength: float, building_age: int
) -> Tuple[float, List[str]]:
    """
    Apply age-related degradation to `material_strength`.

    Parameters
    ----------
    material_strength : float
        Nominal material strength before degradation (MPa).
    building_age : int
        Age of the structure in years.

    Returns
    -------
    adjusted_strength : float
        Strength after any degradation.
    warnings : list[str]
        Warning list (e.g., ``["material_degradation_applied"]`` if reduction
        occurs).
    """
    warnings: List[str] = []
    adjusted_strength = material_strength

    if building_age > 50:
        adjusted_strength *= 0.85  # 15 % reduction
        warnings.append("material_degradation_applied")

    return adjusted_strength, warnings


def detect_additional_warnings(
    building_height: float,
    num_floors: int,
    building_age: int,
    material_strength: float,
) -> List[str]:
    """
    Generate warnings that do not modify inputs.

    Parameters
    ----------
    building_height : float
        Total building height (m).
    num_floors : int
        Total floors.
    building_age : int
        Age in years.
    material_strength : float
        Current (possibly degraded) material strength (MPa).

    Returns
    -------
    list[str]
        Zero or more warning codes:
        ``"unrealistic_geometry"`` and/or ``"suspicious_material_strength"``.
    """
    warnings: List[str] = []

    if building_height / num_floors > 5:
        warnings.append("unrealistic_geometry")

    if building_age < 5 and material_strength < 200:
        warnings.append("suspicious_material_strength")

    return warnings


def compute_safety_score(
    material_strength: float,
    num_floors: int,
    building_height: float,
    seismic_magnitude: float,
    safety_factor: float,
) -> float:
    """
    Calculate the structural safety score.

    Formula
    -------
    `safety_score = ((material_strength * num_floors) /
                     (building_height * seismic_magnitude)) * safety_factor`

    Parameters
    ----------
    material_strength : float
        Current material strength (MPa).
    num_floors : int
        Number of floors.
    building_height : float
        Total height (m).
    seismic_magnitude : float
        Design-basis magnitude.
    safety_factor : float
        Global safety factor.

    Returns
    -------
    float
        Computed safety score (dimensionless).
    """
    return (
        (material_strength * num_floors)
        / (building_height * seismic_magnitude)
        * safety_factor
    )


def classify_status(safety_score: float) -> str:
    """
    Convert a numeric `safety_score` to a qualitative status.

    Parameters
    ----------
    safety_score : float
        Value returned by `compute_safety_score`.

    Returns
    -------
    str
        ``"SAFE"`` if `safety_score` ≥ 1.75, otherwise ``"UNSAFE"``.
    """
    return "SAFE" if safety_score >= 1.75 else "UNSAFE"


def main() -> None:
    """
    Demonstration run using the sample dataset.
    Prints score, status and warnings in the requested format.
    """
    # Sample configuration
    building_height = 65
    num_floors = 9
    material_strength = 180
    building_age = 3
    seismic_magnitude = 6.8
    safety_factor = 1.6

    warnings: List[str] = []

    try:
        # 1️⃣ Validation
        validate_parameters(
            building_height,
            num_floors,
            material_strength,
            building_age,
            seismic_magnitude,
            safety_factor,
        )

        # 2️⃣ Degradation & age warnings
        adjusted_strength, age_warnings = apply_material_degradation(
            material_strength, building_age
        )
        warnings.extend(age_warnings)

        # 3️⃣ Geometry / material warnings
        warnings.extend(
            detect_additional_warnings(
                building_height,
                num_floors,
                building_age,
                adjusted_strength,
            )
        )

        # 4️⃣ Score & status
        score = compute_safety_score(
            adjusted_strength,
            num_floors,
            building_height,
            seismic_magnitude,
            safety_factor,
        )
        status = classify_status(score)

        # 5️⃣ Output
        print(f"Score: {score:.2f}")
    except ValueError:
        score = None
        status = "INVALID"
        print("Score: N/A")

    print(f"Status: {status}")
    print(f"Warnings: {warnings}")


if __name__ == "__main__":
    main()