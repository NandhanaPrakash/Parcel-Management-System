import calendar
from django.shortcuts import render, redirect,HttpResponse
import json
from datetime import date,datetime
import random
import string
from dateutil.relativedelta import relativedelta
import heapq
import haversine as hs
from geopy.geocoders import Nominatim

idlist=[]
#data = (y,track_id)

import heapq

class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, source, destination, distance):
        # Add an edge between source and destination with the given distance
        self.graph.setdefault(source, []).append((destination, distance))
        self.graph.setdefault(destination, []).append((source, distance))

    def shortest_distance(self, start):
        distances = {node: float('inf') for node in self.graph}
        distances[start] = 0
        priority_queue = [(0, start)]
        previous = {node: None for node in self.graph}

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)

            # Skip if already visited a shorter path to the node
            if current_distance > distances[current_node]:
                continue

            for neighbor, weight in self.graph[current_node]:
                distance = current_distance + weight

                # Update the distance if a shorter path is found
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_node
                    heapq.heappush(priority_queue, (distance, neighbor))

        return distances, previous

    def get_shortest_path(self, distances, previous, end):
        path = []
        current_node = end

        while current_node is not None:
            path.append(current_node)
            current_node = previous[current_node]

        path.reverse()
        return path
    
    def all_routes(self, start, end, visited=None, path=None):
        if visited is None:
            visited = set()
        if path is None:
            path = []

        # Mark the current node as visited and add it to the path
        visited.add(start)
        path.append(start)

        # If the destination node is reached, add the path to the result
        if start == end:
            yield list(path)

        # Explore all neighbors of the current node
        for neighbor, _ in self.graph.get(start, []):
            if neighbor not in visited:
                # Recursively call all_routes with the neighbor as the new start node
                yield from self.all_routes(neighbor, end, visited, path)

        # Remove the current node from the visited set and path to backtrack
        visited.remove(start)
        path.pop()

    
parcel_system = Graph()
parcel_system.add_edge("600046", "600035", 22)
parcel_system.add_edge("600040", "600033", 11)
parcel_system.add_edge("600033", "600028", 7)
parcel_system.add_edge("600040", "600028", 7)
parcel_system.add_edge("600028", "600035", 3)
parcel_system.add_edge("600033", "600035", 4)


def Calc_Dist(add1,add2):
  import haversine as hs
  from geopy.geocoders import Nominatim
  loc = Nominatim(user_agent="GetLoc")
  getLoc = loc.geocode(add1)
  getL=loc.geocode(add2)
  loc1=(getLoc.latitude,getLoc.longitude)
  loc2=(getL.latitude,getL.longitude)
  return(hs.haversine(loc1,loc2))
# printing latitude and longitude
#sample code

l_o_a={600028:"Mylapore 600028 Chennai",600046:"Tambaram 600046 Chennai",600040:"Anna Nagar 600040 Chennai",600033:"West Mambalam 600033 Chennai",600035:"Nandanam 600035 Chennai"}
def closest_dist(add):
  global l_o_a
  l_o_d={}
  
  for i in l_o_a:
    dist=Calc_Dist(l_o_a[i],add)
    l_o_d[i]=dist 
  return l_o_d

class PriorityQueue():
  
  def __init__(self):
    self.lst= []

  def __str__(self):
    return str(self.lst)

	# for checking if the queue is empty
  def isEmpty(self):
    return len(self.lst) == 0

	# for inserting an element in the queue
  def enqueue(self, data):
    self.lst.append(data)

	# for popping an element based on Priority
  def dequeue(self):

    for i in range(len(self.lst)):
      if self.lst[i][-1] == 'y':
        return self.lst.pop(i)
      
    for i in range(len(self.lst)):
      return self.lst.pop(i)
    


def login_or_create_account(request):
    if request.method == 'POST':
        choice = request.POST.get('choice')

        if choice == "1":
            email = request.POST.get('email')
            password = request.POST.get('password')
            # Perform login validation
            if validate_login(email, password):
                print("Login successful!")
                # Redirect to place order page after successful login
                return redirect('customer_dashboard')
            else:
                error_message = "Invalid email or password. Please try again."
                return render(request, 'login.html', {'error_message': error_message})

        elif choice == "2":
            email = request.POST.get('email')
            name = request.POST.get('name')
            phoneno = request.POST.get('phoneno')
            address = request.POST.get('address')
            # Check if the email already exists
            if email in customer_details:
                error_message = "Email already exists. Please try again."
                return render(request, 'account_creation.html', {'error_message': error_message})
            password = request.POST.get('password')
            # Perform account creation
            create_account(email, name, address, phoneno, password)
            print("Account created successfully!")
            # Redirect to place order page after successful account creation
            return redirect('customer_dashboard')

    return render(request, 'login.html')

def validate_login(email, password):
    # Code to validate the login credentials
    # You can implement your own logic here, such as checking against a database or a file
    if email in customer_details and customer_details[email][0] == password:
        return True
    return False

def create_account(email, name, address, phoneno, password):
    # Code to create a new account
    # You can implement your own logic here, such as storing the customer details in a database or a file
    customer_details[email] = [password, name, address, phoneno]  # Assuming password is the only detail for now
    append_dict_to_json(customer_details, customer_detailsfile)

def client_login_or_create_account(request):
    if request.method == 'POST':
        choice = request.POST.get('choice')

        if choice == "1":
            email = request.POST.get('email')
            password = request.POST.get('password')
            # Perform login validation
            if validate_client_login(email, password):
                print("Login successful!")
                # Redirect to place order page after successful login
                return redirect('client')
            else:
                error_message = "Invalid email or password. Please try again."
                return render(request, 'client_login.html', {'error_message': error_message})

        elif choice == "2":
            email = request.POST.get('email')
            name = request.POST.get('name')
            phoneno = request.POST.get('phoneno')
            address = request.POST.get('address')
            # Check if the email already exists
            if email in client_details:
                error_message = "Email already exists. Please try again."
                return render(request, 'client_account_creation.html', {'error_message': error_message})
            password = request.POST.get('password')
            # Perform account creation
            create_client_account(email, name, address, phoneno, password)
            print("Account created successfully!")
            # Redirect to place order page after successful account creation
            return redirect('client')

    return render(request, 'client_login.html')

def validate_client_login(email, password):
    # Code to validate the client login credentials
    # You can implement your own logic here, such as checking against a database or a file
    if email in client_details and client_details[email][0] == password:
        return True
    return False

def create_client_account(email, name, address, phoneno, password):
    # Code to create a new client account
    # You can implement your own logic here, such as storing the client details in a database or a file
    client_details[email] = [password, name, address, phoneno]  # Assuming password is the only detail for now
    append_dict_to_json(client_details, client_detailsfile)

def client_login(request):
    error_message = None

    if request.method == 'POST':
        # Handle login form submission
        email = request.POST.get('email')
        password = request.POST.get('password')

        if validate_client_login(email, password):
            print("Login successful!")
            # Redirect the user to the client_dashboard page
            return redirect('client_dashboard')
        else:
            error_message = "Invalid email or password. Please try again."

    # Render the login page without the error message initially
    return render(request, 'client_login.html', {'error_message': error_message})


def client_create_account(request):
    if request.method == 'POST':
        # Handle create account form submission
        email = request.POST.get('email')
        name = request.POST.get('name')
        phoneno = request.POST.get('phoneno')
        address = request.POST.get('address')

        if email in client_details:
            error_message = "Email already exists. Please try again."
            return render(request, 'client_create_account.html', {'error_message': error_message})

        password = request.POST.get('password')
        create_client_account(email, name, address, phoneno, password)
        print("Account created successfully!")
        # Proceed with the rest of the program
        return redirect('client_dashboard')

    return render(request, 'client_create_account.html')
'''
def get_orders(date):
    with open("order_details.json", "r") as f:
        data = json.load(f)
        orders = []
        for i in data.keys():
            order_date = datetime.strptime(data[i][5], '%Y-%m-%d').date()
            if order_date == date:
                orders.append(data[i])
        return orders

def index(request):
    today = datetime.now().date()
    month_calendar = calendar.monthcalendar(today.year, today.month)
    return render(request, 'index.html', {'month_calendar': month_calendar})

def orders(request):
    date_str = request.POST.get('date')
    date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else datetime.now().date()
    orders = get_orders(date)
    month_calendar = calendar.monthcalendar(date.year, date.month)
    return render(request, 'orders.html', {'date': date_str, 'orders': orders, 'month_calendar': month_calendar})'''


def append_dict_to_json(data, filename):
    with open(filename, 'r') as file:
        existing_data = dict(json.load(file))

    # Assuming the existing data is a list, you can append the new dictionary to it
    existing_data.update(data)

    with open(filename, 'w') as file:
        json.dump(existing_data, file)

def retrieve_json(filename):
    with open(filename, 'r') as file:
        ret_data = dict(json.load(file))
    return ret_data


customer_detailsfile = r"C:\Users\Monis\OneDrive\Desktop\Project\pds\parcel_system\parcel_system\customer_details.json"
client_detailsfile = r"C:\Users\Monis\OneDrive\Desktop\Project\pds\parcel_system\parcel_system\client_details.json"
employee_detailsfile = r"C:\Users\Monis\OneDrive\Desktop\Project\pds\parcel_system\parcel_system\employee_details.json"
order_detailsfile = r"C:\Users\Monis\OneDrive\Desktop\Project\pds\parcel_system\parcel_system\order_details.json"
customer_details = retrieve_json(customer_detailsfile)
client_details = retrieve_json(client_detailsfile)
employee_details = retrieve_json(employee_detailsfile)
order_details = retrieve_json(order_detailsfile)

def homepage(request):
    return render(request, 'homepage.html')

def index(request):
    return render(request, 'index.html')

def customer(request):
    error_message = None

    if request.method == 'POST':
        choice = request.POST.get('choice')

        if choice == '1':
            return redirect('login')

        elif choice == '2':
            return redirect('account_creation')

    return render(request, 'customer.html', {'error_message': error_message})


def login(request):
    if request.method == 'POST':
        # Handle login form submission
        email = request.POST.get('email')
        password = request.POST.get('password')

        if validate_login(email, password):
            print("Login successful!")
            # Proceed with the rest of the program
            return redirect('customer_dashboard')
        else:
            error_message = "Invalid email or password. Please try again."
            return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'login.html')

def account_creation(request):

    if request.method == 'POST':
        # Handle create account form submission
        email = request.POST.get('email')
        name = request.POST.get('name')
        phoneno = request.POST.get('phoneno')
        address = request.POST.get('address')

        if email in customer_details:
            error_message = "Email already exists. Please try again."
            return render(request, 'account_creation.html', {'error_message': error_message})

        password = request.POST.get('password')
        create_account(email, name, address, phoneno, password)
        print("Account created successfully!")
        # Proceed with the rest of the program
        return redirect('customer_dashboard')

    return render(request, 'account_creation.html')


def success(request):
    return render(request, 'success.html')

def client(request):
    error_message = ''

    if request.method == 'POST':
        choice = request.POST.get('choice')

        if choice == '1':
            return redirect('client_login')

        elif choice == '2':
            return redirect('client_create_account')

        else:
            error_message = 'Invalid choice. Please select a valid option.'

    context = {
        'error_message': error_message,
    }

    return render(request, 'client.html', context)

#Employee page
def employee(request):
    if request.method == 'POST':
        choice = request.POST.get('choice')

        if choice == "1":
            return redirect('today_orders')

    return render(request, 'employee.html')

#Function to display the Todays order for employee
def today_orders(request):
    with open(order_detailsfile, "r") as f:
        order_details = json.load(f)

    today = date.today()
    today_date = today.strftime("%B %d, %Y")
    orders = [order for order in order_details.values() if order[5] == str(today_date)]
    context = {
        'orders': orders
    }
    return render(request, 'orders.html', context)

def get_orders(date):
    # Update with the correct file path
    try:
        with open(order_detailsfile, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    orders = []
    for i in data.keys():
        order_date_str = data[i][5]
        order_date = datetime.strptime(order_date_str, '%B %d, %Y').date()
        if order_date == date:
            orders.append(data[i])
    return orders


def date_order(request, year=None, month=None, day=None):
    if year and month and day:
        try:
            year = int(year)
            month = int(month)
            day = int(day)
            target_date = date(year, month, day)
        except ValueError:
            return HttpResponse("Invalid year, month, or day.")
    else:
        target_date = date.today()

    orders = get_orders(target_date)

    # Generate the month_calendar list manually
    month_calendar = []
    cal = calendar.Calendar()
    weeks = cal.monthdatescalendar(target_date.year, target_date.month)
    for week in weeks:
        week_days = []
        for day in week:
            week_days.append((day.day, day))
        month_calendar.append(week_days)

    previous_month = target_date - relativedelta(months=1)

    return render(request, 'date_order.html', {
        'date': target_date,
        'orders': orders,
        'month_calendar': month_calendar,
        'previous_month': previous_month
    })



def client_dashboard(request):
    current_year = datetime.now().year
    current_month = datetime.now().month
    current_day = datetime.now().day

    if request.method == 'POST':
        user_choice = int(request.POST.get('choice'))

        if user_choice == 1:
            # Redirect to customer_history function
            return redirect('customer_history')

        elif user_choice == 2:
            # Redirect to date_order function with the current year, month, and date
            return redirect('date_order', year=current_year, month=current_month, day=current_day)
        
        elif user_choice == 3:
            return redirect('update_status')

    return render(request, 'client_dashboard.html', {'current_year': current_year, 'current_month': current_month, 'current_day': current_day})

def customer_history(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        customer = customer_details.get(email)
        if customer:
            prev_orders = []
            for i in order_details:
                if order_details[i][0] == customer[1]:
                    prev_orders.append(f"{i} - {order_details[i][2]}")

            context = {
                'customer': {
                    'name': customer[1],
                    'address': customer[2],
                    'phone': customer[3]
                },
                'prev_orders': prev_orders
            }
            return render(request, 'customer_history.html', context)
        else:
            error_message = "Customer not found."
            return render(request, 'customer_history.html', {'error_message': error_message})

    return render(request, 'customer_history.html')



def customer_dashboard(request):
    return render(request, 'customer_dashboard.html')



from twilio.rest import Client
import random

# Twilio account credentials
account_sid = 'AC5fa4870300513395dd697e0a0129b8db'
auth_token = 'f6ae000b48147126f3132279e901c30b'
twilio_phone_number = '+14067197426'

# Initialize pending and completed order queues
pending_order = PriorityQueue()

for id in order_details.keys():
    if order_details[id][-1] == "high" and order_details[id][-4] == 'Yet to be Dispatched':
        pending_order.enqueue((id,'y'))
    elif order_details[id][-1] == "low" and order_details[id][-4] == 'Yet to be Dispatched':
        pending_order.enqueue((id,'n'))

# Function to send SMS
def send_sms(phone_number):

    otp = random.randint(999,10000)
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="OTP-{}".format(otp),
        from_=twilio_phone_number,
        to=phone_number
    )
    print(f"Link sent to {phone_number}. Message SID: {message.sid}")
import string
import random
from datetime import date
from django.shortcuts import render


def id_generator(cust, size=5):
    chars = string.ascii_uppercase + string.digits
    num = ''.join(random.choice(chars) for _ in range(size))
    idlist.append(num)
    while True:
        if num not in idlist:
            order_details[num] = cust
            append_dict_to_json(order_details, order_detailsfile)
            break
        else:
            num = ''.join(random.choice(chars) for _ in range(size))
    return num

def details(request):
    rec_add =[]
    name = request.POST.get('name')
    n = int(request.POST.get('num_orders'))
    send_house_no = request.POST.get('send_house_no')
    send_street_name = request.POST.get('send_street_name')
    send_locality = request.POST.get('send_locality')
    send_pincode = request.POST.get('send_pincode')
    send_city = request.POST.get('send_city')
    send_address = {
        'House No.': send_house_no,
        'Street Name': send_street_name,
        'Locality': send_locality,
        'Pincode': send_pincode,
        'City': send_city
    }
    phone_no = '+91' + request.POST.get('phone_no')

    send_add = str(send_locality)+','+str(send_pincode)+','+str(send_city)


    for i in range(n):
        rec_house_no = request.POST.get('rec_house_no_' + str(i))
        rec_street_name = request.POST.get('rec_street_name_' + str(i))
        rec_locality = request.POST.get('rec_locality_' + str(i))
        rec_pincode = request.POST.get('rec_pincode_' + str(i))
        rec_city = request.POST.get('rec_city_' + str(i))
        rec_address = {
            'House No.': rec_house_no,
            'Street Name': rec_street_name,
            'Locality': rec_locality,
            'Pincode': rec_pincode,
            'City': rec_city
        }

        rec_add += [str(rec_locality)+' '+str(rec_pincode)+' '+str(rec_city)]
        send_dist = closest_dist(send_add)
        rec_dist = closest_dist(rec_add[-1])
        send_min_dis = send_dist[600028]
        send_branch = l_o_a[600028]
        rec_min_dis = rec_dist[600028]
        rec_branch = l_o_a[600028]
        try:
            for i in send_dist:
                if send_dist[i]<=send_min_dis:
                    send_min_dis=send_dist[i]
                    send_branch=l_o_a[i]
                    print(send_branch)
                    start_pincode=str(i) 
        except Exception:
            pass
        for i in rec_dist:
            if rec_dist[i]<=rec_min_dis:
                rec_min_dis=rec_dist[i]
                rec_branch=l_o_a[i]
                end_pincode=str(i) 
        try:
            print(send_min_dis,send_branch)
            print(rec_min_dis,rec_branch)

        except Exception:
            pass

        shortest_distances = parcel_system.shortest_distance(start_pincode)[0]
        shortest_distance = shortest_distances[end_pincode]
        previous=parcel_system.shortest_distance(start_pincode)[1]
        print(f"The shortest distance between {start_pincode} and {end_pincode} is: {shortest_distance}")
        shortest_path = parcel_system.get_shortest_path(shortest_distances, previous, end_pincode)
        sp=""
        route = []
        route_status = []

        routes = parcel_system.all_routes(start_pincode,end_pincode)
        print("All possible routes:")
        all_routes=[]
        for r in routes:
            rr=""
            for i in range(len(r)) :
                rr+=l_o_a[int(r[i])]
                if i !=len(r)-1:
                    rr+="-->"
            all_routes.append(rr)
                    
        print(all_routes)


        for i in range(len(shortest_path)):
            sp+=l_o_a[int(shortest_path[i])]
            route.append(l_o_a[int(shortest_path[i])])

            if i !=len(shortest_path)-1:
                sp+="-->"

            else:
                pass

        for i in range(len(route)):
            route_status.append("Not Reached")

        upd_route = dict(zip(route,route_status))
        print(upd_route)
        priority = request.POST.get(f'priority_{i}', '')
        print(priority)
        item = request.POST.get(f'item_{i}', '')
        print(item)
        today = date.today()
        ord_date = today.strftime("%B %d, %Y")
        Status = "Yet to be Dispatched"

        cust = [name,"{},{},{},{},{}".format(send_house_no,send_street_name,send_locality,send_pincode,send_city),"{}".format(item),"{},{},{},{},{}".format(rec_house_no,rec_street_name,rec_locality,rec_pincode,rec_city),phone_no,ord_date,Status,sp,upd_route,"{}".format(priority)]
        order_id = id_generator(cust)
        pending_order.enqueue(order_id)

        # Send SMS to the provided phone number
        send_sms(phone_no)

    return order_id,all_routes,sp,send_add,rec_add

import folium
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

def place_order(request):
    if request.method == 'POST':
        order_id, all_routes, chosen_route, start, end = details(request)
        
        # Initialize geolocator
        geolocator = Nominatim(user_agent="route_plotter")
        
        # Get the coordinates of the start and end locations
        start_location = geolocator.geocode(start)
        end_location = geolocator.geocode(end)
        
        # Extract the latitude and longitude
        start_lat, start_lon = start_location.latitude, start_location.longitude
        end_lat, end_lon = end_location.latitude, end_location.longitude
        
        # Create a folium map centered at the start location
        route_map = folium.Map(location=[start_lat, start_lon], zoom_start=10)
        
        # Add markers for start and end locations
        folium.Marker(location=[start_lat, start_lon], popup="Start Location").add_to(route_map)
        folium.Marker(location=[end_lat, end_lon], popup="End Location").add_to(route_map)
        
        # Add a polyline to represent the route
        route_points = [(start_lat, start_lon), (end_lat, end_lon)]
        folium.PolyLine(locations=route_points, color='blue', weight=2.5, opacity=1).add_to(route_map)
        
        # Perform any additional actions or redirect to a success page
        return render(request, 'success.html', {'order_id': order_id, 'sms_sent': True, 'chosen_route': chosen_route, 'all_routes': all_routes, 'route_map': route_map._repr_html_()})

    return render(request, 'place_order.html')

def track_order(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        if order_id in order_details:
            details = order_details[order_id]
            context = {
                'order_id': order_id,
                'order_details': details
            }
            return render(request, 'track_order.html', context)
        else:
            error_message = "Invalid order ID. Please try again."
            return render(request, 'track_order.html', {'error_message': error_message})
    else:
        return render(request, 'track_order.html')

print(pending_order)


# views.py
from django.shortcuts import render
from django.http import JsonResponse

def update_status(request):
    if request.method == 'POST':
        option = request.POST.get('option')

        if option == '1':
            # Option for dispatching order
            print('hi')
            print("Pending order-->",pending_order)
            dispatched_order_id = pending_order.dequeue()[0]
            if dispatched_order_id in order_details:
                order_details[dispatched_order_id][-4] = "Dispatched"
                message = f"Dispatched Order ID: {dispatched_order_id}"
                append_dict_to_json(order_details, order_detailsfile)
            else:
                message = "No orders available for dispatch"

        elif option == '2':
            order_id = request.POST.get('order_id')
            if order_id in order_details:
                routes = order_details[order_id][-2]
                print(routes)
                route_status = {}
                for branch, status in routes.items():
                    route_status[branch] = status
            else:
                message = "Order not found"
                return render(request, 'update_status.html', {'message': message, 'order_details': order_details})

            # Check if the form is submitted to update route status
            if 'office' in request.POST and 'status' in request.POST:
                office = request.POST.get('office')
                status = request.POST.get('status')
                if office in route_status:
                    route_status[office] = status
                    message = "Route status updated successfully"
                    order_details[order_id][-2] = route_status
                    append_dict_to_json(order_details, order_detailsfile)
                else:
                    message = "Invalid office selection"

            return render(request, 'update_status.html', {'route_status': route_status, 'order_id': order_id, 'order_details': order_details})

        elif option == '3':
            # Option for completing order
            order_id = request.POST.get('order_id_complete')
            if order_id in order_details:
                order_details[order_id][-4] = "Delivered"
                message = f"Order ID {order_id} marked as delivered"
                append_dict_to_json(order_details, order_detailsfile)
            else:
                message = "Invalid Order ID"

        return render(request, 'update_status.html', {'message': message, 'order_details': order_details})

    return render(request, 'update_status.html', {'order_details': order_details})


def get_routes(request):
    order_id = request.GET.get('order_id')
    if order_id in order_details:
        routes = order_details[order_id][-2]
        return JsonResponse({'routes': routes})
    else:
        return JsonResponse({'routes': {}})
