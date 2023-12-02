from functions.Promedio import convertDurationToMinutes
from routes.routes import routes

@routes.context_processor
def utility_processor():
    def convertMin(duration):
        return convertDurationToMinutes(duration)
    return dict(convertMin=convertMin)