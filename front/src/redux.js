import { SET_FLOW_DATA, SET_PATH } from './actionTypes';
import * as d3 from 'd3';

export function flowReducer(state = null, action) {
    switch (action.type) {
        case SET_FLOW_DATA:
            return action.data;
        default:
            return state;
    }
}

export function pathReducer(state = null, action) {
    switch (action.type) {
        case SET_PATH:
            return action.path;
        case SET_FLOW_DATA:
            // if path foo/bar/baz.js is selected, but errors messages
            // no more include this path, refresh it.
            const oldPath = state;
            if (oldPath === null) return null;

            let node, newPath;
            const root = d3.hierarchy(action.data);

            if (root.data.name === oldPath[0]) {
                node = root;
                newPath = [ oldPath[0] ];
            } else {
                return null;
            }

            for (let i = 1 ; i < oldPath.length ; i++) {
                const name = oldPath[i];
                node = node.children.find(node => node.data.name === name);
                if (node === undefined) {
                    break;
                } else {
                    newPath.push(name);
                }
            }
            return newPath;
        default:
            return state;
    }
}
