import heapq
import random
import webbrowser
import tkinter as tk
from tkinter import ttk, messagebox

class CityGraph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, u, v, weight):
        if u not in self.graph:
            self.graph[u] = []
        if v not in self.graph:
            self.graph[v] = []
        self.graph[u].append((v, weight))
        self.graph[v].append((u, weight))

    def dijkstra_all_paths(self, start, end):
        """Finds multiple shortest paths using variations of Dijkstra's algorithm"""
        pq = [(0, start, [])]
        all_routes = []
        visited = set()

        while pq:
            current_distance, current_node, path = heapq.heappop(pq)
            path = path + [current_node]

            if current_node == end:
                all_routes.append((path, current_distance))
                continue

            if current_node in visited:
                continue
            visited.add(current_node)

            for neighbor, weight in self.graph[current_node]:
                heapq.heappush(pq, (current_distance + weight, neighbor, path))

        return all_routes if all_routes else None

def get_real_time_conditions():
    """Simulates real-time traffic and weather conditions"""
    traffic_factor = random.uniform(0.8, 1.5)
    weather_factor = random.uniform(0.9, 1.2)
    return round(traffic_factor * weather_factor, 2)

def find_routes():
    start = start_var.get()
    end = end_var.get()
    vehicle = vehicle_var.get()

    if start == end:
        messagebox.showwarning("Invalid Selection", "Start and End points cannot be the same.")
        return
    if not vehicle:
        messagebox.showwarning("Select Vehicle", "Please choose a vehicle type.")
        return

    real_time_factor = get_real_time_conditions()
    routes = city.dijkstra_all_paths(start, end)

    if not routes:
        messagebox.showerror("Error", "No route found between selected locations.")
        return

    speed = {"Car": 60, "Bike": 50, "Bus": 40}[vehicle]  # Avg speeds in km/h
    result_text = "**🚀 Available Routes:**\n"
    best_route = None
    best_time = float("inf")

    for idx, (path, distance) in enumerate(routes):
        adjusted_distance = round(distance * real_time_factor, 2)
        travel_time = round(adjusted_distance / speed, 2)  # Convert to hours
        travel_cost = round(adjusted_distance * 2, 2)

        route_info = f"\n🔹 **Route {idx+1}:** {' → '.join(path)}\n" \
                     f"   📏 Distance: {distance} km\n" \
                     f"   ⏳ Time: {travel_time} hours\n" \
                     f"   💰 Cost: ₹{travel_cost}\n"

        result_text += route_info

        if travel_time < best_time:
            best_time = travel_time
            best_route = (path, travel_time, travel_cost)

    result_label.config(text=result_text)
    save_recent_search(start, end, best_route[1], best_route[2])

def save_recent_search(start, end, time, cost):
    recent_searches.insert(0, f"{start} → {end} | {time} hours | ₹{cost}")
    if len(recent_searches) > 3:
        recent_searches.pop()
    recent_search_label.config(text="\n".join(recent_searches))

def open_in_google_maps():
    start = start_var.get()
    end = end_var.get()
    if start and end:
        url = f"https://www.google.com/maps/dir/{start}/{end}"
        webbrowser.open(url)
    else:
        messagebox.showwarning("Missing Info", "Select both start and destination!")

city = CityGraph()
recent_searches = []

# Adding cities and routes
city.add_edge("Hyderabad", "Warangal", 140)
city.add_edge("Hyderabad", "Nalgonda", 100)
city.add_edge("Warangal", "Karimnagar", 70)
city.add_edge("Warangal", "Khammam", 120)
city.add_edge("Karimnagar", "Nizamabad", 150)
city.add_edge("Khammam", "Vijayawada", 130)
city.add_edge("Vijayawada", "Guntur", 40)
city.add_edge("Vijayawada", "Visakhapatnam", 350)
city.add_edge("Guntur", "Nellore", 250)
city.add_edge("Nellore", "Tirupati", 140)
city.add_edge("Visakhapatnam", "Srikakulam", 100)
city.add_edge("Srikakulam", "Vizianagaram", 50)
city.add_edge("Vizianagaram", "Rajahmundry", 190)
city.add_edge("Rajahmundry", "Kakinada", 65)
city.add_edge("Kakinada", "Amaravati", 200)

# Creating GUI
root = tk.Tk()
root.title("🚆 Smart Transport System - AP & TS")
root.geometry("700x500")

ttk.Style().configure("TButton", font=("Arial", 12), padding=6)
ttk.Style().configure("TLabel", font=("Arial", 12))

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(pady=10)

tk.Label(frame, text="🏙️ Select Start Point:", font=("Arial", 12)).grid(row=0, column=0, pady=5, sticky="w")
start_var = ttk.Combobox(frame, values=list(city.graph.keys()), state="readonly", width=20)
start_var.grid(row=0, column=1, pady=5)

tk.Label(frame, text="📍 Select Destination:", font=("Arial", 12)).grid(row=1, column=0, pady=5, sticky="w")
end_var = ttk.Combobox(frame, values=list(city.graph.keys()), state="readonly", width=20)
end_var.grid(row=1, column=1, pady=5)

tk.Label(frame, text="🚘 Select Vehicle:", font=("Arial", 12)).grid(row=2, column=0, pady=5, sticky="w")
vehicle_var = ttk.Combobox(frame, values=["Car", "Bike", "Bus"], state="readonly", width=20)
vehicle_var.grid(row=2, column=1, pady=5)

find_button = ttk.Button(frame, text="🚀 Find Best Route", command=find_routes)
find_button.grid(row=3, columnspan=2, pady=10)

map_button = ttk.Button(frame, text="🗺️ Open in Google Maps", command=open_in_google_maps)
map_button.grid(row=4, columnspan=2, pady=5)

recent_search_label = tk.Label(root, text="Recent Searches:\n", font=("Arial", 10), fg="darkgreen")
recent_search_label.pack(pady=5)

result_label = tk.Label(root, text="", font=("Arial", 12), fg="blue", justify="left")
result_label.pack(pady=10)

root.mainloop()
