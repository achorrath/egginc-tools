import farm
import pytest


def test_time_to_chickens():
    f = farm.Farm()
    with pytest.raises(ValueError) as excinfo:
        f.time_to_chickens(100)
    assert 'farm population required' in str(excinfo.value)

    f = farm.Farm(farm_population=1)
    with pytest.raises(ValueError) as excinfo:
        f.time_to_chickens(100)
    assert 'int hatchery rate required' in str(excinfo.value)

    # verify that no exceptions happen
    f = farm.Farm(farm_population=1, int_hatchery_rate=1)
    f.time_to_chickens(100)


def test_time_to_eggs():
    f = farm.Farm()
    with pytest.raises(ValueError) as excinfo:
        f.time_to_eggs(100)
    assert 'eggs required' in str(excinfo.value)

    f = farm.Farm(eggs=0)
    with pytest.raises(ValueError) as excinfo:
        f.time_to_eggs(100)
    assert 'farm population required' in str(excinfo.value)

    f = farm.Farm(eggs=0, farm_population=1)
    with pytest.raises(ValueError) as excinfo:
        f.time_to_eggs(100)
    assert 'egg laying rate required' in str(excinfo.value)

    f = farm.Farm(eggs=0, farm_population=1, egg_laying_rate=1)
    with pytest.raises(ValueError) as excinfo:
        f.time_to_eggs(100)
    assert 'int hatchery rate required' in str(excinfo.value)

    # verify that no exceptions happen
    f = farm.Farm(eggs=0, farm_population=1, egg_laying_rate=1,
                  int_hatchery_rate=1)
    f.time_to_eggs(100)


def test_time_to_max_chickens():
    f = farm.Farm()
    with pytest.raises(ValueError) as excinfo:
        f.time_to_max_chickens()
    assert 'max capacity required' in str(excinfo.value)

    # Other possible exceptions are covered by test_time_to_chickens()

    # verify that no exceptions happen
    f = farm.Farm(farm_population=1, int_hatchery_rate=1, max_capacity=250)
    f.time_to_max_chickens()


def test_time_to_value():
    f = farm.Farm()
    with pytest.raises(ValueError) as excinfo:
        f.time_to_max_chickens()
    assert 'max capacity required' in str(excinfo.value)

    f = farm.Farm(max_capacity=250)
    with pytest.raises(ValueError) as excinfo:
        f.time_to_value(100)
    assert 'farm value required' in str(excinfo.value)

    f = farm.Farm(max_capacity=250, farm_value=1)
    with pytest.raises(ValueError) as excinfo:
        f.time_to_value(100)
    assert 'farm population required' in str(excinfo.value)

    f = farm.Farm(max_capacity=250, farm_value=1, farm_population=1)
    with pytest.raises(ValueError) as excinfo:
        f.time_to_value(100)
    assert 'int hatchery rate required' in str(excinfo.value)

    # verify that no exceptions happen
    f = farm.Farm(max_capacity=250, farm_value=1, farm_population=1,
                  int_hatchery_rate=1)
    f.time_to_value(100)

