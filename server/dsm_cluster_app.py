from typing import Optional, List, Any

import sys
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
    labels: List[Any]
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

        self.dsm_result = None
        self.cluster_result = None
        self.dsm_annotated = None

        self.generator = None

app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app_state = GeneratorState()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/new_example")
async def create_example():
    return {}

@app.post("/new_dsm/")
async def new_dsm(dsm_item: DSMItem):
    d_mat = np.array(dsm_item.mat)
    labels = dsm_item.labels
    system_elements = dsm_item.system_elements

    try:
        d = DSMMatrix(d_mat, activity_labels = labels)
        d.clear_elements(system_elements)
        app_state.dsm = d
    except AssertionError as err:
        return {"result": "AssertionError: " + str(err)}
    except:
        return {"result": "Unexpected error: " + str(sys.exc_info()[0])}

    return dsm_item

@app.post("/params/set")
async def set_params(param_item: ParamItem):
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

    return {"result": "success"}

@app.get("/cluster/")
async def do_cluster():
    app_state.generator = ClusterGenerator(dsm_mat = app_state.dsm)
    c_orig = app_state.generator.cluster(app_state.dsm)
    total_coord_cost = app_state.generator.total_coord_cost
    cost_history = app_state.generator.cost_history
    c = ClusterMatrix.reorder(c_orig)

    new_dsm = DSMMatrix.reorder_by_cluster(app_state.dsm, c)

    d_new_g = DSMMatrix.place_diag(new_dsm)
    app_state.cluster_result = c
    app_state.dsm_result = d_new_g
    app_state.dsm_annotated = DSMMatrix.annotate_clusters(d_new_g, c)

    return {
        "dsm": app_state.dsm_result.tojson(),
        "labels": app_state.dsm_result.labels,
        "cluster": app_state.cluster_result.tojson(),
        "dsm_a": app_state.dsm_annotated.tojson(), 
    }

@app.get("/params/get")
async def get_params():
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
    ) if app_state.params else { "result": "error" }

@app.get("/result/cluster")
async def get_result_cluster():
    return {
        "mat": app_state.cluster_result.tojson()
            if app_state.cluster_result else [],
    }

@app.get("/result/dsm")
async def get_result_dsm():
    return {
        "mat": app_state.dsm.tojson(),
        "labels": app_state.dsm.labels,
        "system_elements": [],
    }

@app.get("/orig/cluster")
async def get_orig_cluster():
    return {
        "mat": [],
    }

@app.get("/orig/cluster")
async def get_orig_dsm():
    return {
        "mat": app_state.dsm.tojson(),
        "labels": app_state.dsm.labels,
    }
