import sys, json
from twisted.internet import reactor
from twisted.web import server, resource
from twisted.web.static import File
from twisted.python import log
from datetime import datetime

#we will modify the values below using REST
values = ['1','2','3','4','5']

#main server resource
class Root(resource.Resource):

    def render_GET(self, request):
        '''
        get response method for the root resource
        localhost:8000/
        '''
        return 'Welcome to the REST API'

    def getChild(self, name, request):
        '''
        We overrite the get child function so that we can handle invalid
        requests
        '''
        if name == '':
            return self
        else:
            if name in VIEWS.keys():
                return resource.Resource.getChild(self, name, request)
            else:
                return PageNotFoundError()

class ListValues(resource.Resource):

    def render_GET(self, request):
        '''
        get response method for the ListValues resource
        localhost:8000/ListValues/
        '''
        log.msg('The values are: ' + ','.join(str(val) for val in values))
        return json.dumps(values)

class AddValue(resource.Resource):

    def render_GET(self, request):
        '''
        get response method for the AddValue resource
        localhost:8000/AddValue/
        '''
        try:
            values.append(request.args['name'][0])
            log.msg(
                'Value added: %s' %(request.args['name'][0]))
            log.msg(
                'Current values:%s' %(','.join(str(val) for val in values)))
            return json.dumps(values)
        except:
            log.err()
            return 'Error adding value: %s' %(request.args['name'][0])

        def render_POST(self, request):
            '''to make sure both GET/POST are handled'''
            return self.render_GET(request)

class DeleteValue(resource.Resource):

    def render_GET(self, request):
    '''
    get response method for the DeleteValue resource
    localhost:8000/DeleteValue/
    '''
    try:
        log.msg('Deleting value: %s' %(request.args['name'][0]))
        values.remove(request.args['name'][0])
        log.msg('Current values:%s' %(','.join(str(val) for val in values)))
        return json.dumps(values)
    except:
        log.err()
        return 'Error deleting value: %s' %(request.args['name'][0])

    def render_POST(self, request):
        '''to make sure both GET/POST are handled'''
        return self.render_GET(request)

class ClearValues(resource.Resource):

    def render_GET(self, request):
    '''
    get response method for the ClearValues resource
    localhost:8000/ClearValues/
    '''
        try:
            log.msg('Clearing values')
            values = list()
            return json.dumps(values)
        except:
            log.err()
            return 'Error clearing values'

    def render_POST(self, request):
        '''to make sure both GET/POST are handled'''
        return self.render_GET(request)

class PageNotFoundError(resource.Resource):

    def render_GET(self, request):
        return 'Page Not Found!'

#to make the process of adding new views less static
VIEWS = {
    'ListValues': ListValues(),
    'AddValue': AddValue(),
    'DeleteValue': DeleteValue(),
    'ClearValues': ClearValues()
}

if __name__ == '__main__':
    root = Root()
    for viewName, className in VIEWS.items():
        #add the view to the web service
        root.putChild(viewName, className)
    log.startLogging(sys.stdout)
    log.msg('Starting server: %s' %str(datetime.now()))
    server = server.Site(root)
    reactor.listenTCP(8000, server)
    reactor.run()
