

class VehiclePosition:
    longitude = 0.00000
    latitude = 0.00000
    timeStamp = 0

    def __init__(self, driverId, orderId , timeStamp , longitude, latitude, time):
        self.driverId = driverId
        self.orderId = orderId
        VehiclePosition.timeStamp = timeStamp
        VehiclePosition.longitude = longitude
        VehiclePosition.latitude = latitude
        self.time = time
    def toString(self):
        vehiclePositon = "{driverId: %s , orderId: %s , timeStamp: %d  longitude: %.14f , latitude: %.15f , time: %s }" % (self.driverId, self.orderId, VehiclePosition.timeStamp, VehiclePosition.longitude, VehiclePosition.latitude, self.time)
        return vehiclePositon

    def resetLonAndLat(self, longitude, latitude):
        VehiclePosition.longitude = longitude
        VehiclePosition.latitude = latitude
