import React, { useEffect, useState, useRef } from 'react';
import * as d3 from 'd3';
import 'bootstrap/dist/css/bootstrap.css';

const DSMatrix = ( props ) => {
  var margin = props.margin,
  width = props.width,
  height = props.height;

  margin.top = margin.top ? margin.top : 100;
  margin.right = margin.right ? margin.right : 0;
  margin.bottom = margin.bottom ? margin.bottom : 0;
  margin.left = margin.left ? margin.left : 100;


  const d3cont = useRef(null);
  var data = props.data;

  useEffect(() => {
    if (data && d3cont.current) {
      drawChart(data);
    }
  }, [data, d3cont.current])

  const drawChart = (data) => {
    // const h = props.height;
    // const w = props.width;
    d3.select(d3cont.current).selectAll("*").remove();

    const svg = d3.select(d3cont.current)
      .append("svg")
      .attr("class", "matrix_plot_area")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    // svg.append("rect")
    //   .attr("class", "background")
    //   .attr("width", width - margin.right)
    //   .attr("height", height - margin.top)
    //   .attr("transform", "translate(" + margin.right + "," + margin.top + ")");

    svg.append("rect")
      .attr("class", "background")
      .attr("width", width)
      .attr("height", height);

    drawSquares(data, svg);

    // // Remove old D3 elements
    // svg.exit().remove();
  }

  const drawSquares = (data, svg) => {
    const tooltip = d3.select("body")
                .append("div")
                .attr("class", "tooltip")
                .style("opacity", 0);

    const mouseover = (event, p) => {
      d3.selectAll(".row text").classed("active", (d, i) => {
          return i === p.y;
      });
      d3.selectAll(".column text").classed("active", (d, i) => {
          return i === p.x;
      });
      tooltip.transition().duration(200).style("opacity", .9);
      tooltip.html("Task: " + nodes[p.y].name + "</br>" +
              "Depends on task: " + nodes[p.x].name + "</br>" +
              "Is in group: " + (matrix[p.x][p.y].g > 0
              ? matrix[p.x][p.y].g : "None"))
          .style("left", (event.pageX + 30) + "px")
          .style("top", (event.pageY - 50) + "px");
    }

    const mouseout = () => {
      d3.selectAll("text").classed("active", false);
      tooltip.transition().duration(500).style("opacity", 0);
    }

    var matrix = [];
    var nodes = data.nodes;
    var total_items = nodes.length;

    var matrixScale = d3.scaleBand().range([0, width]).domain(d3.range(total_items));
    var opacityScale = d3.scaleLinear().domain([0, 10]).range([0.3, 1.0]).clamp(true);
    var colorScale = d3.scaleOrdinal(d3.schemeAccent);

    // Create rows for the matrix
    nodes.forEach(function(node) {
      node.count = 0;
      matrix[node.index] =
        d3.range(total_items).map(item_index => {
          return {
            x: item_index,
            y: node.index,
            z: 0,
            g: 0,
          };
      });
    });

    // Fill matrix with data from links and count how many times each item appears
    // Currently underused: number of relations (z)
    data.links.forEach(function(link) {
        matrix[link.source][link.target].z += link.value;
        // matrix[link.target][link.source].z += link.value;
        matrix[link.source][link.target].g = link.group;
        nodes[link.source].count += link.value;
        // nodes[link.target].count += link.value;
    });

    // Insert squares
    var rows = svg.selectAll(".row")
        .data(matrix)
        .enter().append("g")
        .attr("class", "row_custom")
        .attr("transform", (d, i) => {
            return "translate(0," + matrixScale(i) + ")";
        });

    var squares = rows.selectAll(".cell")
        .data(d => d.filter(item => item.z > 0))
        .enter()
        .append("rect")
        .attr("class", "cell")
        .attr("x", d => matrixScale(d.x))
        .attr("width", matrixScale.bandwidth())
        .attr("height", matrixScale.bandwidth())
        .style("fill-opacity", d => opacityScale(d.z)).style("fill", d => {
            return matrix[d.x][d.y].g > 0 ? colorScale(matrix[d.x][d.y].g) : "grey";
        })
        .on("mouseover", mouseover)
        .on("mouseout", mouseout);

    var columns = svg.selectAll(".column")
        .data(matrix)
        .enter().append("g")
        .attr("class", "column")
        .attr("transform", (d, i) => {
            return "translate(" + matrixScale(i) + ")rotate(-90)";
        });

    rows.append("text")
        .attr("class", "label")
        .attr("x", -5)
        .attr("y", matrixScale.bandwidth() / 2)
        .attr("dy", ".32em")
        .attr("text-anchor", "end")
        .text((d, i) => nodes[i].name);

    columns.append("text")
        .attr("class", "label")
        .attr("y", 100)
        .attr("y", matrixScale.bandwidth() / 2)
        .attr("dy", ".32em")
        .attr("text-anchor", "start")
        .text((d, i) => nodes[i].name);

    rows.append("line")
        .attr("x2", width);

    columns.append("line")
        .attr("x1", -width);
  }

  return (
    <div className="container">
      <h1>Matrix area</h1>
      <svg
        className="d3-component"
        width={width + margin.left + margin.right}
        height={height + margin.top + margin.bottom}
        ref={d3cont}
      />
    </div>
  );
}

export default DSMatrix;
