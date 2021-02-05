import React, { useState, useEffect } from "react";

import 'bootstrap/dist/css/bootstrap.css';
import './styles.css'

const TaskForm = ({
  currentId,
  setCurrentId,
  editMode,
  setEditMode,
  createTask,
  availableInTasks,
  availableOutTasks,
  addTask,
  editTask,
  data
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
    if(editMode === 1) {
      // console.log("Edit: ", editMode, ", Current ID:", currentId);
      let entry = data.find((n) => n.id === currentId);
      console.log("Finding: ", entry);
      setFormData({name: entry.name, desc: entry.desc});
      updateTaskInputs(entry.tasks_in);
      updateTaskOutputs(entry.tasks_out);
    }
  }, [editMode, currentId, data])

  const handleSubmit = () => {
    console.log("Data: ", formData);
    console.log("Ins: ", taskInputs);
    console.log("Outs: ", taskOutputs);

    // addTask(data);
    if (editMode === 1) {
      editTask(formData.name, taskInputs, taskOutputs, formData.desc);
    } else {
      addTask(formData.name, taskInputs, taskOutputs, formData.desc);
    }
    clear();
  }

  const handleAddTaskInput = (val) => {
    let val_int = parseInt(val);
    console.log("id to add: ", val);
    if(val && !isNaN(val_int) && !taskInputs.includes(val_int)) {
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
    if (val && !isNaN(val_int) && !taskOutputs.includes(val_int)) {
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
    setCurrentId(0);
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
    <div class="container">
      <h2>Add Task</h2>
      <form>
        <div class="form-group row form_elem_p">
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
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            />
          </div>
        </div>
        <div class="form-group row form_elem_p">
          <label for="inputTaskDesc"
            class="col-sm-2 col-form-label margin-bottom">
            Description
          </label>
          <div class="col-sm-10">
            <input
              class="form-control"
              id="inputTaskDesc"
              placeholder="Description"
              value={formData.desc}
              onChange={(e) => setFormData({ ...formData, desc: e.target.value })}
            />
          </div>
        </div>

        <div class="form-group row form_elem_p">
          <div class="col-sm-2 col-form-label">
            <label for="taskInputChoices">Add task input</label>
          </div>
          <div class="col-sm-2">
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
          </div>
          <div class="col-sm-1">
            <button
              class="btn btn-outline-secondary"
              type="button"
              id="button-addon2"
              onClick={() => handleAddTaskInput(currTaskInput)}
            >
            Add</button>
          </div>
          <div class="col-sm-7">
            { taskInputs ? taskInputs.map((t) =>
              <span>
                <span className="badge bg-secondary">
                  In {t} &nbsp;
                  <button type="button" class="btn btn-dark btn-sm"
                    onClick={() => handleDeleteTaskInput(t)}>
                    <span>&times;</span>
                  </button>
                </span>
                <span>&nbsp;</span>
              </span>
            ) : <span>No inputs</span> }
          </div>
        </div>

        <div class="form-group row form_elem_p">
          <div class="col-sm-2 col-form-label">
            <label for="taskInputChoices">Add task output</label>
          </div>
          <div class="col-sm-2">
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
          </div>
          <div class="col-sm-1 input-group-append">
            <button
              class="btn btn-outline-secondary"
              type="button"
              id="button-addon2"
              onClick={() => handleAddTaskOutput(currTaskOutput)}
            >Add</button>
          </div>
          <div class="col-sm-7">
            { taskOutputs ? taskOutputs.map((t) =>
              <span>
                <span className="badge bg-secondary">
                  Out {t} &nbsp;
                  <button type="button" class="btn btn-dark btn-sm"
                    onClick={() => handleDeleteTaskOutput(t)}>
                    <span>&times;</span>
                  </button>
                </span>
                <span>&nbsp;</span>
              </span>
            ) : <span>No outputs</span> }
          </div>
        </div>
        <div class="row">
          <div class="col-sm-2">
          </div>
          <div class="col-sm-3">
            <button
              type="button"
              class="btn btn-primary"
              onClick={() => handleSubmit()}
            >
              Add Task
            </button>
            <span>&nbsp;</span>
            <button
              type="button"
              class="btn btn-danger"
              onClick={() => clear()}
              >
              Clear
            </button>
          </div>
          <div class="col-sm-1">
          </div>

        </div>
      </form>
  </div>

  );
}

// <h3>Bruh. <span className="badge badge-warning">Output 1</span></h3>
// ^old form style

export default TaskForm;
