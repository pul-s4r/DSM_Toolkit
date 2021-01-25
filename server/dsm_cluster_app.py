from typing import Optional, List

import json
from fastapi import FastAPI
from pydantic import BaseModel

from cluster_parameters import ClusterParameters, set_default_cluster_parameters
from cluster_matrix import ClusterMatrix
from dsm_matrix import DSMMatrix
from clustering_functions import *
from plotting_functions import *

class ParamItem(BaseModel):
    pow_cc: int
    pow_bid: int
    pow_dep: int
    max_cluster_size: int
    rand_accept: int
    rand_bid: int
    times: Optional[int] = 2
    stable_limit: Optional[int] = 2
    max_repeat: Optional[int] = 10

class DSMItem(BaseModel):
    mat: Optional[List[List[int]]] = [
        [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], ]
    labels: List[int]
    system_elements: List[int]

class GeneratorState():
    def __init__(self):
        self.params = ClusterParameters(
            pow_cc = 1,
            pow_bid = 1,
            pow_dep = 4,
            max_cluster_size = 8,
            rand_accept = 16,
            rand_bid = 16,
            times = 2,
            stable_limit = 2,
            max_repeat = 10
        )

        self.dsm = DSMMatrix.from_size(4)

app = FastAPI()

app_state = GeneratorState()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/new_example")
async def create_example():
    return {}

@app.post("/new_dsm/")
async def new_dsm(dsm_item: DSMItem):
    return dsm_item

@app.post("/params/set")
async def set_params(param_item: ParamItem):
    import pdb; pdb.set_trace()
    new_params_set = ClusterParameters(
        pow_cc = int(param_item.pow_cc),
        pow_bid = int(param_item.pow_bid),
        pow_dep = int(param_item.pow_dep),
        max_cluster_size = int(param_item.max_cluster_size),
        rand_accept = int(param_item.rand_accept),
        rand_bid = int(param_item.rand_bid),
        times = int(param_item.times),
        stable_limit = int(param_item.stable_limit),
        max_repeat = int(param_item.max_repeat)
    )

    app_state.params = new_params_set

    # app_state.params.pow_cc = int(param_item.pow_cc)
    # app_state.params.pow_bid = int(param_item.pow_bid)
    # app_state.params.pow_dep = int(param_item.pow_dep)
    # app_state.params.max_cluster_size = int(param_item.max_cluster_size)
    # app_state.params.rand_accept = int(param_item.rand_accept)
    # app_state.params.rand_bid = int(param_item.rand_bid)
    # app_state.params.times = int(param_item.times)
    # app_state.params.stable_limit = int(param_item.stable_limit)
    # app_state.params.max_repeat = int(param_item.max_repeat)

    return {"result": "success"}

@app.get("/params/get")
async def get_params():
    import pdb; pdb.set_trace()
    return ParamItem(
        pow_cc = int(app_state.params.pow_cc),
        pow_bid = int(app_state.params.pow_bid),
        pow_dep = int(app_state.params.pow_dep),
        max_cluster_size = int(app_state.params.max_cluster_size),
        rand_accept = int(app_state.params.rand_accept),
        rand_bid = int(app_state.params.rand_bid),
        times = int(app_state.params.times),
        stable_limit = int(app_state.params.stable_limit),
        max_repeat = int(app_state.params.max_repeat)
    ) if app_state.params else { 'result': 'error' }

@app.get("/result/cluster")
async def get_result_cluster():
    return {}

@app.get("/result/dsm")
async def get_result_dsm():
    return {}

@app.get("/orig/cluster")
async def get_orig_cluster():
    return {}

@app.get("/orig/cluster")
async def get_orig_dsm():
    return {}
