import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.css';

const TaskList = ({ setCurrentId, setEditMode, data, handleDelete }) => {
  // const [taskData, setTaskData] = useState();

  // const { data } = props.data;

  useEffect(() => {

  }, [])

  return(
    <div class="table-responsive">
        <table class="table table-striped table-sm">
          <thead>
            <tr>
              <th>ID</th>
              <th>Seq</th>
              <th>Name</th>
              <th>Input</th>
              <th>Output</th>
              <th>Description</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
          {
            Array.isArray(data) && data ? data.map((task) => (
              <tr>
                <td>{task.id}</td>
                <td>{task.seq}</td>
                <td>{task.name}</td>
                <td>{task.tasks_in.length ? task.tasks_in.toString() : "-"}</td>
                <td>{task.tasks_out.length ? task.tasks_out.toString() : "-"}</td>
                <td>{task.desc}</td>
                <td>
                  <button
                    className="btn btn-primary btn-sm m-2"
                    onClick={() => {
                      setEditMode(1);
                      setCurrentId(task.id);
                    }}
                  >
                    Edit
                  </button>
                  <button
                    className="btn btn-danger btn-sm m-2"
                    onClick={() => handleDelete(task.id)}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            )) : <tr>
              <td>empty</td>
              <td>empty</td>
              <td>empty</td>
              <td>empty</td>
              <td>empty</td>
              <td>empty</td>
              <td></td>
            </tr>
          }
          </tbody>
        </table>
      </div>
  );
}

export default TaskList;
