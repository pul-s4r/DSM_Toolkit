import React, { useState, useEffect } from "react";

import 'bootstrap/dist/css/bootstrap.css';

const TaskForm = ({
  setCurrentId,
  createTask,
  availableInTasks,
  availableOutTasks,
  addTask,
}) => {
  const [formData, setFormData] = useState({
      name: "",
      desc: ""
    });
  const [taskInputs, updateTaskInputs] = useState([]);
  const [taskOutputs, updateTaskOutputs] = useState([]);
  const [currTaskInput, setCurrTaskInput] = useState(0);
  const [currTaskOutput, setCurrTaskOutput] = useState(0);

  useEffect(() => {

  }, [])

  const handleSubmit = () => {
    console.log("Data: ", formData);
    console.log("Ins: ", taskInputs);
    console.log("Outs: ", taskOutputs);

    // addTask(data);
    addTask(formData.name, taskInputs, taskOutputs, formData.desc);
    clear();
  }

  const handleAddTaskInput = (val) => {
    let val_int = parseInt(val);
    console.log("id to add: ", val);
    if(val && val_int !== NaN && !taskInputs.includes(val_int)) {
      updateTaskInputs(taskInputs => [...taskInputs, val_int]);
      console.log("Added in: ", val);
    }
  }

  const handleDeleteTaskInput = (val) => {
    let val_int = parseInt(val);
    const newInputs = taskInputs.filter((item) => item !== val);
    updateTaskInputs(newInputs);
    console.log("Deleted in: ", val);
  }

  const handleAddTaskOutput = (val) => {
    let val_int = parseInt(val);
    if (val && val_int !== NaN && !taskOutputs.includes(val_int)) {
      updateTaskOutputs(taskOutputs => [...taskOutputs, val_int]);
      console.log("Added out: ", val);
    }
  }

  const handleDeleteTaskOutput = (val) => {
    let val_int = parseInt(val);
    const newOutputs = taskOutputs.filter((item) => item !== val);
    updateTaskOutputs(newOutputs);
    console.log("Deleted out: ", val);
  }

  const clear = () => {
    // setCurrentId(0);
    setFormData({
        name: "",
        desc: "",
      })
    updateTaskInputs([]);
    updateTaskOutputs([]);
    setCurrTaskInput(0);
    setCurrTaskOutput(0);
  }

  return(
    <form>
      <div class="form-group row">
        <label for="inputTaskName"
          class="col-sm-2 col-form-label">
          Task Name
        </label>
        <div class="col-sm-10">
          <input
            class="form-control"
            id="inputTaskName"
            placeholder="Task Name"
            value={formData.name}
            onChange={(e) => setFormData({... formData, name: e.target.value})}/>
        </div>
      </div>
      <div class="form-group row">
        <label for="inputTaskDesc"
          class="col-sm-2 col-form-label">
          Description
        </label>
        <div class="col-sm-10">
          <input
            class="form-control"
            id="inputTaskDesc"
            placeholder="Description"
            value={formData.desc}
            onChange={(e) => setFormData({... formData, desc: e.target.value})}/>
        </div>
      </div>

      <div class="form-group">
        <label for="taskInputChoices">Add task input</label>
        <select class="form-control"
          id="taskInputChoices"
          onClick={(e) => setCurrTaskInput(e.target.value)}
          onChange={(e) => setCurrTaskInput(e.target.value)}
        >
          {
            availableInTasks ?
              availableInTasks.filter(n => !taskInputs.includes(n))
              .map((t) => (
              <option>{t}</option>
            )) : <option></option>
          }
        </select>
        <div class="input-group-append">
          <button
            class="btn btn-outline-secondary"
            type="button"
            id="button-addon2"
            onClick={() => handleAddTaskInput(currTaskInput)}
          >Add</button>
        </div>
        <div>
          { taskInputs ? taskInputs.map((t) =>
            <span className="badge bg-secondary">
              In {t} &nbsp;
              <button type="button" class="btn btn-dark btn-sm"
                onClick={() => handleDeleteTaskInput(t)}>
                <span>&times;</span>
              </button>
            </span>
          ) : <span>No inputs</span> }
        </div>
      </div>

      <div class="form-group">
        <label for="taskInputChoices">Add task output</label>
        <select class="form-control"
          id="taskInputChoices"
          onClick={(e) => setCurrTaskOutput(e.target.value)}
        >
          {
            availableOutTasks ?
              availableOutTasks.filter(n => !taskOutputs.includes(n))
              .map((t) => (
              <option>{t}</option>
            )) : <option></option>
          }
        </select>
        <div class="input-group-append">
          <button
            class="btn btn-outline-secondary"
            type="button"
            id="button-addon2"
            onClick={() => handleAddTaskOutput(currTaskOutput)}
          >Add</button>
        </div>
        <div>
          { taskOutputs ? taskOutputs.map((t) =>
            <span className="badge bg-secondary">
              Out {t} &nbsp;
              <button type="button" class="btn btn-dark btn-sm"
                onClick={() => handleDeleteTaskOutput(t)}>
                <span>&times;</span>
              </button>
            </span>
          ) : <span>No outputs</span> }
        </div>
      </div>
      <button
        type="button"
        class="btn btn-primary"
        onClick={() => handleSubmit()}
      >
        Add Task
      </button>
    </form>
  );
}

// <h3>Bruh. <span className="badge badge-warning">Output 1</span></h3>
// ^old form style

export default TaskForm;
