from flask import abort
from rapi.autogen.openapi_server import models


def get_restaurant():
    cs = db.cursor()
    cs.execute("SELECT basin_id,name FROM basin")
    result = [models.BasinShort(id,name) for id,name in cs.fetchall()]
    cs.close()
    return result


def get_restaurant_details(restaurantId):
    cs = db.cursor()
    cs.execute("SELECT basin_id,name,area FROM basin WHERE basin_id=%s",[basinId])
    result = cs.fetchone()
    cs.close()
    if result:
        basin_id,name,area = result
        return models.BasinFull(basin_id,name,area)
    else:
        abort(404)


def get_michelin_restaurant():
    cs = db.cursor()
    cs.execute("SELECT station_id,ename FROM station WHERE basin_id=%s",[basinId])
    result = [models.StationShort(id,name) for id,name in cs.fetchall()]
    cs.close()
    return result


def get_restaurant_wongnai_rating(restaurantId):
    cs = db.cursor()
    cs.execute("SELECT station_id,basin_id,ename,lat,lon FROM station WHERE station_id=%s",[stationId])
    result = cs.fetchone()
    cs.close()
    if result:
        station_id,basin_id,ename,lat,lon = result
        return models.StationFull(station_id,basin_id,ename,lat,lon)
    else:
        abort(404)


def get_restaurant_tripadvisor_rating(restaurantId):
    cs = db.cursor()
    cs.execute("SELECT b.basin_id AS basin_id, r.year AS year, SUM(r.amount) / COUNT(DISTINCT s.station_id) AS rainfall FROM rainfall r INNER JOIN station s ON s.station_id=r.station_id INNER JOIN basin b ON b.basin_id=s.basin_id WHERE b.basin_id=%s and r.year=%s",[basinId,year])
    result = cs.fetchone()
    cs.close()
    if result:
        basin_id,year,rainfall = result
        return {
                    "basin_id": basin_id,
                    "year": year,
                    "rainfall": rainfall
                }
    else:
        abort(404)


def get_district():
    cs = db.cursor()
    cs.execute("SELECT station_id,ename FROM station WHERE basin_id=%s",[basinId])
    result = [models.StationShort(id,name) for id,name in cs.fetchall()]
    cs.close()
    return result


def get_restaurant_by_district(districtId):
    cs = db.cursor()
    cs.execute("SELECT station_id,ename FROM station WHERE basin_id=%s",[basinId])
    result = [models.StationShort(id,name) for id,name in cs.fetchall()]
    cs.close()
    return result


def get_cuisine():
    cs = db.cursor()
    cs.execute("SELECT station_id,ename FROM station WHERE basin_id=%s",[basinId])
    result = [models.StationShort(id,name) for id,name in cs.fetchall()]
    cs.close()
    return result


def get_specified_cuisine(cuisineId):
    cs = db.cursor()
    cs.execute("SELECT station_id,ename FROM station WHERE basin_id=%s",[basinId])
    result = [models.StationShort(id,name) for id,name in cs.fetchall()]
    cs.close()
    return result


def get_specified_cuisine_restaurant(cuisineId):
    cs = db.cursor()
    cs.execute("SELECT station_id,ename FROM station WHERE basin_id=%s",[basinId])
    result = [models.StationShort(id,name) for id,name in cs.fetchall()]
    cs.close()
    return result