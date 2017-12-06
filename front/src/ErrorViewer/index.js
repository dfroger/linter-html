import React, { Component } from 'react';
import { connect } from 'react-redux';
import * as d3 from 'd3';


function pathToNode(root, path) {
    let node = root;
    path.slice(1).forEach(name => {
        node = node.children.find(node => node.data.name === name);
    });
    return node;
}


function nodeToPath(root, node) {
    return node.path(root).reverse().map(node => node.data.name);
}


class FlowError extends Component {
    render() {
        return this.props.lines.map(line => <p>{line}</p>);
    }
}


class FlowFileErrors extends Component {
    render() {
        return (
            <section>
                <h3>{this.props.filepath}</h3>
                <ul>
                    {this.props.errors.map(e => <li>{e}</li>)}
                </ul>
            </section>
        );
    }
}


class ErrorViewer extends Component {

    render() {
        if (this.props.path === null) return null;
        const root = d3.hierarchy(this.props.flow);
        const node = pathToNode(root, this.props.path);
        return (
            <div>
                { node.leaves().map(node => {
                    const path = nodeToPath(root, node).join('/');
                    return <FlowFileErrors key={path} filepath={path} errors={node.data.errors} />;
                }) }
            </div>
        );
    }
}


export default connect(
    state => ({
        // TODO: selector
        flow: state.flow,
        path: state.path
    }),
    null
)(ErrorViewer);
