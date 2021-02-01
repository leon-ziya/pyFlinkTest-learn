


class VehicleOrder:
    id = 0
    startTimeStamp = 0
    endTimeStamp = 0
    getOnLongitude = 0.000
    getOnLatitude = 0.000
    getOffLongitude = 0.000
    getOffLatitude = 0.000
    value = 0
    startTime = 0
    endTime = 0

    def __init__(self, orderId, startTimeStamp, endTimeStamp, getOnLongitude, getOnLatitude, getOffLongitude, getOffLatitude, value, startTime, endTime):
        VehicleOrder.id += 1
        self.orderId = orderId
        VehicleOrder.startTimeStamp = startTimeStamp
        VehicleOrder.endTimeStamp = endTimeStamp
        VehicleOrder.getOnLongitude = getOnLongitude
        VehicleOrder.getOnLatitude = getOnLatitude
        VehicleOrder.getOffLongitude = getOffLongitude
        VehicleOrder.getOffLatitude = getOffLatitude
        VehicleOrder.value = value
        VehicleOrder.startTime = startTime
        VehicleOrder.endTime = endTime

    def toString(self):
        vehicleOrder = "{order: %s, startTimeStamp: %d, endTimeStamp: %d, " \
                       "getOnLongitude: %1.4f, getOnLatitude: %1.5f, " \
                       "getOffLongitude: %1.4f, getOffLatitude: %1.5f, " \
                       "value: %d, startTime: %s, endTime: %s}" % \
                       (self.orderId, VehicleOrder.startTimeStamp,
                        VehicleOrder.endTimeStamp, VehicleOrder.getOnLongitude,
                        VehicleOrder.getOnLatitude, VehicleOrder.getOffLongitude,
                        VehicleOrder.getOffLatitude, VehicleOrder.value, VehicleOrder.startTime,
                        VehicleOrder.endTime)
