import React, { Component } from 'react';
import { connect } from 'react-redux';
import * as d3 from 'd3';

import { setPath } from '../actions';

const pi = Math.PI;

class Sunburst extends Component {
    update() {
        if (this.props.data === null) return;

        const width = 500;
        const height = 500;
        const radius = Math.min(width, height) / 2;

        this.svg.attr("width", width)
           .attr("height", height)
           .append("g")
           .attr("transform", "translate(" + width/2 + "," + height/2 + ")");

        const root = d3.hierarchy(this.props.data)
            .sum(d => d.errors? d.errors.length : 0);

        const color = d3.scaleOrdinal(d3.schemeCategory20c);

        const partition = d3.partition()
            .size([2*pi, radius]);

        partition(root);

        const arc = d3.arc()
            .startAngle(d => d.x0)
            .endAngle(d => d.x1)
            .innerRadius(d => d.y0)
            .outerRadius(d => d.y1);

        this.svg.select('g').selectAll('path.node')
            .data(root.descendants())
            .enter()
                .append('path')
                .attr('class', 'node')
                .attr('fill', (d, i) => color(i))
            .attr('d', arc);

        this.svg.select('g').selectAll('path.node')
            .on('click', clicked  => {
                const rootPath = clicked.path(root);
                this.props.setPath(rootPath.reverse().map(d => d.data.name));
                this.svg.select('g').selectAll('path.node')
                    .style('opacity', 0.4)
                    .style('stroke', '#fff')
                    .filter(d => rootPath.indexOf(d) >= 0)
                    .style('opacity', 1.)
                    .style('stroke', '#000')
            });
    }

    render() {
        const container = <svg ref={el => { this.svg = d3.select(el) }} />;
        this.update();
        return container;
    };
}

export default connect(
    state => ({
        data: state.flow
    }),
    dispatch => ({
        setPath: path => dispatch(setPath(path))
    })
)(Sunburst);
