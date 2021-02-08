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
    <div className="container">
      <h2>Add Task</h2>
      <form>
        <div className="form-group row form_elem_p">
          <label htmlFor="inputTaskName"
            className="col-sm-2 col-form-label">
            Task Name
          </label>
          <div className="col-sm-10">
            <input
              className="form-control"
              id="inputTaskName"
              placeholder="Task Name"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            />
          </div>
        </div>
        <div className="form-group row form_elem_p">
          <label htmlFor="inputTaskDesc"
            className="col-sm-2 col-form-label margin-bottom">
            Description
          </label>
          <div className="col-sm-10">
            <input
              className="form-control"
              id="inputTaskDesc"
              placeholder="Description"
              value={formData.desc}
              onChange={(e) => setFormData({ ...formData, desc: e.target.value })}
            />
          </div>
        </div>

        <div className="form-group row form_elem_p">
          <div className="col-sm-2 col-form-label">
            <label htmlFor="taskInputChoices">Add task input</label>
          </div>
          <div className="col-sm-2">
            <select className="form-control"
              id="taskInputChoices"
              onClick={(e) => setCurrTaskInput(e.target.value)}
              onChange={(e) => setCurrTaskInput(e.target.value)}
            >
              {
                availableInTasks ?
                  availableInTasks.filter(n => !taskInputs.includes(n))
                  .map((t) => (
                  <option key={"input_ops_" + t}>{t}</option>
                )) : <option key={"input_ops_blank"}></option>
              }
            </select>
          </div>
          <div className="col-sm-1">
            <button
              className="btn btn-outline-secondary"
              type="button"
              id="button-addon2"
              onClick={() => handleAddTaskInput(currTaskInput)}
            >
            Add</button>
          </div>
          <div className="col-sm-7">
            { taskInputs ? taskInputs.map((t) =>
              <span key={"in_span_" + t}>
                <span key={"in_badge_" + t} className="badge bg-secondary">
                  In {t} &nbsp;
                  <button key={"in_btn_" + t} type="button" className="btn btn-dark btn-sm"
                    onClick={() => handleDeleteTaskInput(t)}>
                    <span>&times;</span>
                  </button>
                </span>
                <span key={"out_bspace_" + t}>&nbsp;</span>
              </span>
            ) : <span key={"in_span_blank"}>No inputs</span> }
          </div>
        </div>

        <div className="form-group row form_elem_p">
          <div className="col-sm-2 col-form-label">
            <label htmlFor="taskInputChoices">Add task output</label>
          </div>
          <div className="col-sm-2">
            <select className="form-control"
              id="taskInputChoices"
              onClick={(e) => setCurrTaskOutput(e.target.value)}
            >
              {
                availableOutTasks ?
                  availableOutTasks.filter(n => !taskOutputs.includes(n))
                  .map((t) => (
                  <option key={"output_ops_" + t}>{t}</option>
                )) : <option key={"output_ops_blank"}></option>
              }
            </select>
          </div>
          <div className="col-sm-1 input-group-append">
            <button
              className="btn btn-outline-secondary"
              type="button"
              id="button-addon2"
              onClick={() => handleAddTaskOutput(currTaskOutput)}
            >Add</button>
          </div>
          <div className="col-sm-7">
            { taskOutputs ? taskOutputs.map((t) =>
              <span key={"out_span_" + t}>
                <span key={"out_badge_" + t} className="badge bg-secondary">
                  Out {t} &nbsp;
                  <button key={"out_button_" + t} type="button" className="btn btn-dark btn-sm"
                    onClick={() => handleDeleteTaskOutput(t)}>
                    <span>&times;</span>
                  </button>
                </span>
                <span key={"out_bspace_" + t}>&nbsp;</span>
              </span>
            ) : <span key={"out_span_blank"}>No outputs</span> }
          </div>
        </div>
        <div className="row">
          <div className="col-sm-2">
          </div>
          <div className="col-sm-3">
            <button
              type="button"
              className="btn btn-primary"
              onClick={() => handleSubmit()}
            >
              Add Task
            </button>
            <span>&nbsp;</span>
            <button
              type="button"
              className="btn btn-danger"
              onClick={() => clear()}
              >
              Clear
            </button>
          </div>
          <div className="col-sm-1">
          </div>

        </div>
      </form>
  </div>

  );
}

// <h3>Bruh. <span className="badge badge-warning">Output 1</span></h3>
// ^old form style

export default TaskForm;
