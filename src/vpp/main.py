from fastapi import FastAPI, HTTPException
from typing import Dict
from .models import Plant, DispatchRequest, DispatchResponse

app = FastAPI(title="Virtual Power Plant API")

plants: Dict[int, Plant] = {}
next_id = 1

@app.post("/plants/", response_model=Plant)
def register_plant(plant: Plant):
    global next_id
    plant.id = next_id
    plants[next_id] = plant
    next_id += 1
    return plant

@app.get("/plants/", response_model=list[Plant])
def list_plants():
    return list(plants.values())

@app.get("/plants/{plant_id}", response_model=Plant)
def get_plant(plant_id: int):
    plant = plants.get(plant_id)
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    return plant

@app.get("/aggregate/")
def aggregate_power():
    total = sum(p.max_capacity for p in plants.values() if p.status != 'down')
    return {"total_available": total}

@app.post("/dispatch/", response_model=DispatchResponse)
def dispatch(request: DispatchRequest):
    available = [(p.id, p.max_capacity) for p in plants.values() if p.status != 'down']
    if not available:
        return DispatchResponse(allocations={}, total_dispatched=0.0, unmet_demand=request.demand)
    available.sort(key=lambda x: x[1], reverse=True)
    demand = request.demand
    allocations = {}
    for pid, cap in available:
        if demand <= 0:
            allocations[pid] = 0.0
        else:
            alloc = min(cap, demand)
            allocations[pid] = alloc
            demand -= alloc
    total_dispatched = request.demand - demand
    return DispatchResponse(allocations=allocations, total_dispatched=total_dispatched, unmet_demand=demand)
