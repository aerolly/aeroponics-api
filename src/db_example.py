import app



print(app.getResultSetFromDB('"Device".view_availablecontrollers',[]))
print(app.modifyDB('"Device"."Insert_DeviceAction"', [1,"1"]))

