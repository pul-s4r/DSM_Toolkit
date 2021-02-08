import React, { useState, useEffect } from 'react';
// import './App.css';
import { strict as assert } from 'assert';

import usePersistedState from './usePersistedState.js';
import TaskList from './components/TaskList.js';
import TaskForm from './components/TaskForm.js';
import DSMatrix from './components/DSMatrix.js';

// import cdata from './sampletaskdata.js';
const margin = {
  top: 150,
  right: 0,
  bottom: 0,
  left: 150,
}

// const cdata = [13, 5, 6, 6, 9, 11];
const dsm_app_url = "http://127.0.0.1:8000";

const App = () => {
  // const [taskData, setTaskData] = useState([
    // { id: 1, seq: 1, name: "Task 1", tasks_in: [], tasks_out: ["2", "3"], desc: "Task 1" },
    // { id: 2, seq: 2, name: "Task 2", tasks_in: ["1"], tasks_out: ["3"], desc: "Task 2" },
    // { id: 3, seq: 3, name: "Task 3", tasks_in: ["1", "2"], tasks_out: [], desc: "Task 3" },
  // ]);

  const [taskData, setTaskData] = usePersistedState("taskData", [])

  const [idCount, setIdCount] = usePersistedState("idCount", 1);
  const [seqCount, setSeqCount] = usePersistedState("seqCount", 1);
  const [currentId, setCurrentId] = usePersistedState("currentId", 0);
  const [editMode, setEditMode] = usePersistedState("editMode", 0);

  const [matDispData, setMatDispData] = usePersistedState("matData",
    {"nodes": [], "links": []});

  const handleAddOrChangeTask = async (task_name, l_tasks_in, l_tasks_out, task_desc, change_mode, ch_id) => {
    let task_id = change_mode ? currentId : idCount;
    let task_seq = change_mode ? taskData.filter((e) => e.id === currentId)[0].seq
                    : seqCount;
    let entry = {
      id: task_id,
      seq: task_seq,
      name: task_name,
      tasks_in: l_tasks_in,
      tasks_out: l_tasks_out,
      desc: task_desc,
    };

    var exist_tasks = [...taskData];
    // Add all inputs as outputs for the corresponding tasks + vice versa
    for (let i = 0; i < l_tasks_in.length; i++) {
      let entries_ch = exist_tasks.filter(entry => entry.id === l_tasks_in[i]);
      for (let j = 0; j < entries_ch.length; j++) {
        if (entries_ch[j].tasks_out.includes(entry.id)) { continue; }
        let new_outs = [... entries_ch[j].tasks_out, entry.id];
        entries_ch[j].tasks_out = new_outs;
        let fj = exist_tasks.findIndex(x => x.id === entries_ch[j].id);
        exist_tasks[fj] = entries_ch[j];
      }
    }
    // Add all outputs as inputs for the listed tasks
    for (let i = 0; i < l_tasks_out.length; i++) {
      let entries_ch = exist_tasks.filter(entry => entry.id === l_tasks_out[i]);
      for (let j = 0; j < entries_ch.length; j++) {
        if (entries_ch[j].tasks_in.includes(entry.id)) { continue; }
        let new_ins = [... entries_ch[j].tasks_in, entry.id];
        entries_ch[j].tasks_in = new_ins;
        let fj = exist_tasks.findIndex(x => x.id === entries_ch[j].id);
        exist_tasks[fj] = entries_ch[j];
      }
    }
    if (change_mode === 1 && ch_id) {
      let i_change = exist_tasks.findIndex(x => x.id === ch_id);
      exist_tasks[i_change] = entry;
      await setTaskData(taskData => [...exist_tasks]);
    } else {
      await setTaskData(taskData => [...exist_tasks, entry]);
    }
  }

  const handleAddTask = async (task_name, l_tasks_in, l_tasks_out, task_desc) => {
    await handleAddOrChangeTask(task_name, l_tasks_in, l_tasks_out, task_desc, 0, currentId);
    setIdCount(idCount + 1);
    setSeqCount(seqCount + 1);
  }

  const handleChangeTask = async (task_name, l_tasks_in, l_tasks_out, task_desc) => {
    handleAddOrChangeTask(task_name, l_tasks_in, l_tasks_out, task_desc, 1, currentId);
    setEditMode(0);
  }

  const handleDelete = (id) => {
    let entry_to_del = taskData.filter(entry => entry.id === id);
    let del_id = entry_to_del[0].id;
    let seq = entry_to_del[0].seq;

    // Exclude entry to delete and adjust sequence numbers of remaining entries
    let other_entries = taskData.filter(entry => entry.id !== id);
    for (let i = 0; i < other_entries.length; i++ ) {
      if(other_entries[i].seq >= seq) {
        other_entries[i].seq--;
      }
      if(other_entries[i].tasks_in.includes(del_id)) {
        let filtered =
          other_entries[i].tasks_in.filter(entry => entry !== del_id);
        other_entries[i].tasks_in = filtered;
      }
      if(other_entries[i].tasks_out.includes(del_id)) {
        let filtered =
          other_entries[i].tasks_out.filter(entry => entry !== del_id);
        other_entries[i].tasks_out = filtered;
      }
    }
    setTaskData(other_entries);
    setSeqCount(seqCount-1);
  }

  const clear = () => {
    setTaskData([]);
    setIdCount(1);
    setSeqCount(1);
    setCurrentId(0);
    setEditMode(0);
  }

  const toDSM = (taskList) => {
    assert(Array.isArray(taskList));
    var lt = taskList.length;
    var dsm = Array(lt).fill(0).map(() => Array(lt).fill(0));
    var labels = taskList.map(t => t.name ? t.name : t.id);

    for (const id in taskList) {
      let seq = taskList[id].seq-1;
      for (const ti in taskList[id].tasks_in) {
        let inp = taskList[id].tasks_in[ti]-1;
        dsm[seq][inp] = 1;
      }
    }

    return {dsm: dsm, labels: labels};
  }

  const handleSubmit = async () => {
    var { dsm, labels } = toDSM(taskData);

    var query_data = JSON.stringify({
      "mat": dsm,
      "labels": labels,
      "system_elements": []
    });

    var create_response = await fetch(
      dsm_app_url + "/new_dsm/",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json;charset=utf-8"
        },
        body: query_data
      }
    );

    var create_result = await create_response.json();

    var cluster_response = await fetch(
      dsm_app_url + "/cluster/"
    );

    var cluster_result = await cluster_response.json();

    var dsmaNodes = dsmToDisplayNodes(JSON.parse(cluster_result.dsm_a),
      cluster_result.labels);
    setMatDispData(dsmaNodes);
  }

  const dsmToDisplayNodes = (rmat, mlabels) => {
    var data = {
      "nodes": [],
      "links": [],
    };

    mlabels.map((ma, mi) => data.nodes.push(
      {"index" : mi, "name": ma.toString(), "group": ""}
    ));

    rmat.map((tr, ri) => tr.map((tc, ci) => {
      data.links.push({"source": ri, "target": ci, "value": tc >= 0 ? 1 : 0,
        "group": tc > 0 ? tc : 0});
    }));

    return data;
  }


  return (
    <div className="App">
      <TaskList
        setCurrentId={setCurrentId}
        setEditMode={setEditMode}
        data={taskData}
        handleSubmit={handleSubmit}
        handleDelete={handleDelete}
        handleClear={clear}
      />
      <TaskForm
        currentId={currentId}
        setCurrentId={setCurrentId}
        editMode={editMode}
        setEditMode={setEditMode}
        addTask={handleAddTask}
        editTask={handleChangeTask}
        availableInTasks={taskData.map((task) => task.id)}
        availableOutTasks={taskData.map((task) => task.id)}
        data={taskData}
      />
    <DSMatrix data={matDispData} width={700} height={700} margin={margin}/>

    </div>
  );
}

export default App;
