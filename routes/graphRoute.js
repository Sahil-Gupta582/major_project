const express = require('express');
const Router = express.Router();
const {fetchGraphNodesEdges} = require('./../services/fetchGraphNodesEdges');

Router.get('/get-updated-graph', fetchGraphNodesEdges);

module.exports = Router;