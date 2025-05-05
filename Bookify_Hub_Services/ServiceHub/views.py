from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from Bookify_Hub_Services.db import dbconn
from bson.objectid import ObjectId
from datetime import datetime,timedelta, time, timezone
import pprint
from json import loads
from Bookify_Hub_Services.aws import get_ecr_client
from django.http import HttpResponse
from botocore.exceptions import ClientError
from django.http import HttpResponse

def my_view(request):
    try:
        ecr = get_ecr_client()
        response = ecr.describe_repositories()
        repository_names = [repo['repositoryName'] for repo in response['repositories']]
        return HttpResponse(f"ECR Repositories: {', '.join(repository_names)}")
    except ClientError as e:
        return HttpResponse(f"Error: {str(e)}")
class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows events to be viewed or edited.
    """
    def __init__(self):
        self.eventOp = EventViewSet.as_view({
            'get': 'fn_load_data',
            'post': 'fn_save_events',
            'delete': 'fn_delete_events'
        })

        self.userDetails = EventViewSet.as_view({
            'get': 'fn_get_user_details'

        })

        self.eventDetails = EventViewSet.as_view({
            'get': 'fn_get_event_details',
            'patch': 'fn_update_event'
        })

    
    def fn_load_data(self, request):
       events = list(dbconn.clnEvents.find())
       users = list(dbconn.clnUser.find())
       events = fn_convert_objects_to_string(events)
       users = fn_convert_objects_to_string(users)
       total_events = len(events)
       total_users = len(users)
       response_data = {'statusCode': 200, 'events': events, 'total_events': total_events, 'users': users, 'total_users': total_users}
       return Response(response_data)

    def fn_save_events(self, request):

        try:
            data= loads(request.body)
            
            if 'title' not in data:
                return Response({'statusCode': 400, 'message': 'bad request - event_name not found'})
            if 'booking_date' not in data:
                return Response({'statusCode': 400, 'message': 'bad request - booking_date not found'})
            if 'start_time' not in data:
                return Response({'statusCode': 400, 'message': 'bad request - start_time not found'})
            if 'end_time' not in data:
                return Response({'statusCode': 400, 'message': 'bad request - end_time not found'})
            if 'email' not in data:
                return Response({'statusCode': 400, 'message': 'bad request - email not found'})
            
            
            data['status'] = 'bookings'
            data['booking_date'] = datetime.strptime(data['booking_date'], '%Y-%m-%d').strftime('%Y-%m-%dT%H:%M:%SZ')
            data['start_time'] = datetime.strptime(data['start_time'], '%H:%M').strftime('%H:%M:%S')
            data['end_time'] = datetime.strptime(data['end_time'], '%H:%M').strftime('%H:%M:%S')

            query_check_availability = {
                 'booking_date': data['booking_date'],
                 'start_time': {'$lte': data['start_time']},
                 'end_time': {'$gt': data['start_time']}
            }
            pipline = [
                    {
                        '$match': query_check_availability
                    }
                ]
            
            document = list(dbconn.clnEvents.aggregate(pipline))
            if document :
                    print("Event already exists")
                    return Response({'statusCode': 400, 'message': 'bad request - event already exists'})
            else:
                query={'email': data['email']}
                user_id =dbconn.clnUser.find_one(query, {'_id': 1})

                if user_id is not None:
                    print("user id found")
                    data['user_id'] = ObjectId(user_id['_id'])
                    dbconn.clnEvents.update_one(query, {'$set': data})
                    return Response({'statusCode': 200 ,'message': 'success'})
                else:
   
                    query = {
                        'email': data['email'],
                        'username': data['username'],
                        'password': 'password123'
                    }  

                    dbconn.clnUser.insert_one(query)
                    user_id =dbconn.clnUser.find_one(query, {'_id': 1})
                    data['user_id'] = ObjectId(user_id['_id'])
                    pprint.pprint(data)
                    dbconn.clnEvents.insert_one(data)
                
            response_data = {'statusCode': 200, 'message': 'success saved'}
            return Response(response_data)   

        except Exception as error:
            return Response({'statusCode': 500, 'message': 'An error occurred', 'error': str(error)})
    

    def fn_delete_events(self, request):
        try:
            data = request.GET
           
            if 'user_id' not in data:
                return Response({'statusCode': 400, 'message': 'bad request - event_id not found'})
            
            query = {
                'user_id': ObjectId(data['user_id']),
                'title': data['title'],
                'booking_date': data['booking_date'],
                'start_time': data['start_time'],
                'end_time': data['end_time'],
            }

            dbconn.clnUser.delete_one({'_id':ObjectId(data['user_id'])})
            dbconn.clnEvents.delete_one(query) 
            response_data = {'statusCode': 200}
            return Response(response_data)
 

        except Exception as error:
            return Response({'statusCode': 500, 'message': 'An error occurred', 'error': str(error)})



    def fn_update_event(self, request):

        try:
            data = request.data
            if '_id' not in data:
                return Response({'statusCode': 400, 'message': 'bad request - event_id not found'})
            
            query = {
                '_id': ObjectId(data['_id']),
            }
           
            dbconn.clnEvents.update_one(query, {'$set': {'status': 'completed'}})
            response_data = {'statusCode': 200}
            return Response(response_data)

        except Exception as error:
            return Response({'statusCode': 500, 'message': 'An error occurred', 'error': str(error)})




    def fn_get_user_details(self, request):
        try:
            data = loads(request.body)
            query = {'username': data['username']}
            data['user_id'] = dbconn.clnUser.find_one(query, {'_id': 1})
            if 'user_id' not in data:
                return Response({'statusCode': 400, 'message': 'bad request - user_id not found'})
            
            query = {'_id': ObjectId(data['user_id'])}
            data = dbconn.clnUser.find_one(query)
            response_data = {'statusCode': 200, 'data': data}
            return Response(response_data)   

        except Exception as error:
            return Response({'statusCode': 500, 'message': 'An error occurred', 'error': str(error)})


    def fn_get_event_details(self, request):
        try:
            data = request.GET

            if 'title' not in data:
                return Response({'statusCode': 400, 'message': 'bad request - title not found'})
            if 'start' not in data:
                return Response({'statusCode': 400, 'message': 'bad request - start not found'})
            if 'end' not in data:
                return Response({'statusCode': 400, 'message': 'bad request - end not found'})
            
            query = {
                'title': data['title'],
                'booking_date': fn_format_date_string(data['start']),
                'end_time': fn_convert_times_to_string(data['end']),
                'start_time': fn_convert_times_to_string(data['start']),
            }
            pipeline = [
                { '$match': query }
            ]

            data = list(dbconn.clnEvents.aggregate(pipeline))
            data = fn_convert_objects_to_string(data)
            response_data = {'statusCode': 200, 'data': data}
            return Response(response_data)   

        except Exception as error:
            return Response({'statusCode': 500, 'message': 'An error occurred', 'error': str(error)})


def fn_convert_times_to_string(date):
    time_part = date.split(' ')[4] 
    return time_part
def fn_format_date_string(input_date_string):
    # Extract relevant information from the string
    date_part = input_date_string.split(' ')[1:4]
    time_part = input_date_string.split(' ')[4]

    # Create a new string in a format that can be parsed
    new_date_string = f"{date_part[2]}-{date_part[0]}-{date_part[1]}T{time_part}Z"

    # Parse the string to a datetime object
    input_datetime = datetime.strptime(new_date_string, "%Y-%b-%dT%H:%M:%SZ")

    # Set the time part to midnight (00:00:00) and use UTC
    formatted_datetime = datetime.combine(input_datetime.date(), time.min, tzinfo=timezone.utc)

    # Extract the time part using strftime
    formatted_string = formatted_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")

    return formatted_string

def fn_convert_objects_to_string(data):

    """ 
    The following function will convert all objectids in passed
    argument to string

    Args:
        data: any
    
    Return:
        data: any
    """

    try:

        if isinstance(data, dict):
            for key in list(data):
                data[key] = fn_convert_objects_to_string(data[key])
        elif isinstance(data, list):
            index = 0
            for value in data:
                data[index] = fn_convert_objects_to_string(value)
                index += 1
        elif isinstance(data, ObjectId):
            data = str(data)
        elif isinstance(data, datetime):
            data = datetime.strftime(data, '%Y-%m-%d %H:%M:%S')
        
        return data
        

    except Exception as error:
        return {'statusCode': 500, 'message': 'An error occurred', 'error': str(error)}