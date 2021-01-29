import React, { useState, useEffect } from 'react';
// import './App.css';

import TaskList from './components/TaskList.js';
import TaskForm from './components/TaskForm.js';

const App = () => {
  const [taskData, setTaskData] = useState([
    // { id: 1, seq: 1, name: "Task 1", tasks_in: [], tasks_out: ["2", "3"], desc: "Task 1" },
    // { id: 2, seq: 2, name: "Task 2", tasks_in: ["1"], tasks_out: ["3"], desc: "Task 2" },
    // { id: 3, seq: 3, name: "Task 3", tasks_in: ["1", "2"], tasks_out: [], desc: "Task 3" },
  ]);

  let [idCount, setIdCount] = useState(1);
  const [seqCount, setSeqCount] = useState(1);

  const handleAddTask = (task_name, l_tasks_in, l_tasks_out, task_desc) => {
    console.log("Task received: ", task_name, l_tasks_in,
      l_tasks_out, task_desc);
    let entry = {
      id: idCount,
      seq: seqCount,
      name: task_name,
      tasks_in: l_tasks_in,
      tasks_out: l_tasks_out,
      desc: task_desc,
    };
    console.log(entry);
    var exist_tasks = [...taskData];
    // Add all inputs as outputs for the corresponding tasks + vice versa
    for (let i = 0; i < l_tasks_in.length; i++) {
      let entries_ch = exist_tasks.filter(entry => entry.id === l_tasks_in[i]);
      for (let j = 0; j < entries_ch.length; j++) {
        let new_outs = [... entries_ch[j].tasks_out, entry.id];
        entries_ch[j].tasks_out = new_outs;
        let fj = exist_tasks.findIndex(x => x.id === entries_ch[j].id);
        exist_tasks[fj] = entries_ch[j];
      }
    }
    for (let i = 0; i < l_tasks_out.length; i++) {
      let entries_ch = exist_tasks.filter(entry => entry.id === l_tasks_out[i]);
      for (let j = 0; j < entries_ch.length; j++) {
        let new_ins = [... entries_ch[j].tasks_in, entry.id];
        entries_ch[j].tasks_in = new_ins;
        let fj = exist_tasks.findIndex(x => x.id === entries_ch[j].id);
        exist_tasks[fj] = entries_ch[j];
      }
    }
    setTaskData(taskData => [...exist_tasks, entry]);
    setIdCount(idCount + 1);
    setSeqCount(seqCount + 1);
    console.log("(Add) Id: ", idCount, "Seq: ", seqCount);
  }

  const handleDelete = (id) => {
    let entry_to_del = taskData.filter(entry => entry.id === id);
    let del_id = entry_to_del[0].id;
    let seq = entry_to_del[0].seq;
    console.log("Delete seq: ", seq);

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
        console.log("Need to delete: ", del_id, " from ", other_entries[i].id);
        console.log(filtered);
      }
      if(other_entries[i].tasks_out.includes(del_id)) {
        let filtered =
          other_entries[i].tasks_out.filter(entry => entry !== del_id);
        other_entries[i].tasks_out = filtered;
      }
    }
    setTaskData(other_entries);
    setSeqCount(seqCount-1);
    console.log("(Delete) Id: ", idCount, "Seq: ", seqCount);
  }


  return (
    <div className="App">
      <TaskList
        data={taskData}
        handleDelete={handleDelete}
      />
      <TaskForm
        addTask={handleAddTask}
        availableInTasks={taskData.map((task) => task.id)}
        availableOutTasks={taskData.map((task) => task.id)}
      />

    </div>
  );
}

export default App;
