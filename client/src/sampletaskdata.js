export default {
  "nodes": [
    {"index": 0, "name": "Task 1", "group": "A"},
    {"index": 1, "name": "Task 2", "group": "B"},
    {"index": 2, "name": "Task 3", "group": "C"},
    {"index": 3, "name": "Task 4", "group": "D"},
  ],
  "links": [
    {"source": 0, "target": 0, "value": 1},
    {"source": 0, "target": 1, "value": 0},
    {"source": 0, "target": 2, "value": 0},
    {"source": 0, "target": 3, "value": 1},
    {"source": 1, "target": 0, "value": 0},
    {"source": 1, "target": 1, "value": 1},
    {"source": 1, "target": 2, "value": 0},
    {"source": 1, "target": 3, "value": 0},
    {"source": 2, "target": 0, "value": 1},
    {"source": 2, "target": 1, "value": 0},
    {"source": 2, "target": 2, "value": 1},
    {"source": 2, "target": 3, "value": 0},
    {"source": 3, "target": 0, "value": 0},
    {"source": 3, "target": 1, "value": 0},
    {"source": 3, "target": 2, "value": 1},
    {"source": 3, "target": 3, "value": 1}, 
  ],
};
