# -*- encoding: utf8 -*-

import os

from PyQt5.QtCore import QCoreApplication

# ------------------------------------------------------------------------------


def process_all_gui_events():
    QCoreApplication.processEvents()

# ------------------------------------------------------------------------------

# configuration file

CONFIG_DIR = os.path.join(os.path.expanduser('~'), '.linguistica')
CONFIG_LAST_FILE = os.path.join(CONFIG_DIR, 'last_file.json')

# ------------------------------------------------------------------------------

# constants for window sizes etc

TREEWIDGET_WIDTH_MIN = 200
TREEWIDGET_WIDTH_MAX = TREEWIDGET_WIDTH_MIN + 50
TREEWIDGET_HEIGHT_MIN = 600

MAIN_WINDOW_WIDTH = 1024
MAIN_WINDOW_HEIGHT = 768

# ------------------------------------------------------------------------------

# string names of lexicon tree objects
# do NOT change the variable names! (strings themselves can be altered though)

WORDLIST = "Wordlist"

WORD_NGRAMS = "Word ngrams"
BIGRAMS = "Bigrams"
TRIGRAMS = "Trigrams"

SIGNATURES = "Signatures"
SIGS_TO_STEMS = "Signatures to stems"
WORDS_TO_SIGS = "Words to signatures"

TRIES = "Tries"
WORDS_AS_TRIES = "Words as tries"
SUCCESSORS = "Successors"
PREDECESSORS = "Predecessors"

PHONOLOGY = "Phonology"
PHONES = "Phones"
BIPHONES = "Biphones"
TRIPHONES = "Triphones"

MANIFOLDS = "Manifolds"
WORD_NEIGHBORS = "Word neighbors"
VISUALIZED_GRAPH = "Visualized graph"

# ------------------------------------------------------------------------------

SHOW_MANIFOLD_HTML = """
<!DOCTYPE html>
<meta charset="utf-8">
<style>

.node {{
  stroke: #fff;
  stroke-width: 1.5px;
}}

.link {{
  stroke: #999;
  stroke-opacity: .6;
}}

</style>
<body>
<script src="{}/d3.min.js"></script>
<script>

var width = {}, height = {};

var color = d3.scale.category20();

var force = d3.layout.force()
    .charge(-50)
    .linkDistance(10)
    .size([width, height]);

var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height)
    .append("g")
    .call(d3.behavior.zoom().scaleExtent([0.1, 10]).on("zoom", zooming))
    .append("g");

svg.append("rect")
    .attr("fill-opacity", "0")
    .attr("width", width)
    .attr("height", height);


function zooming() {{
  svg.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
}};

d3.json("{}", function(error, graph) {{
  if (error) throw error;

  force
      .nodes(graph.nodes)
      .links(graph.links)
      .start();

  var tickLimit = Math.ceil(graph.nodes.length/200)

  var link = svg.selectAll(".link")
      .data(graph.links)
    .enter().append("line")
      .attr("class", "link")
      .style("stroke-width", function(d) {{ return Math.sqrt(d.value); }});

  var node = svg.selectAll(".node")
      .data(graph.nodes)
    .enter().append("circle")
      .attr("class", "node")
      .attr("r", 3)
      .style("fill", function(d) {{ return color(d.group); }})
      .call(force.drag);

  var texts = svg.selectAll("text.label")
    .data(graph.nodes)
    .enter().append("text")
    .attr("class", "label")
    .attr("fill", "black")
    .attr("font-size", "3pt")
    .text(function(d) {{  return d.id;  }});

  node.append("title")
      .text(function(d) {{ return d.name; }});

  var tick = tickLimit;
  force.on("tick", function() {{
//    if (true) {{
    if (tick == tickLimit) {{
        link.attr("x1", function(d) {{ return d.source.x; }})
            .attr("y1", function(d) {{ return d.source.y; }})
            .attr("x2", function(d) {{ return d.target.x; }})
            .attr("y2", function(d) {{ return d.target.y; }});

        node.attr("cx", function(d) {{ return d.x; }})
            .attr("cy", function(d) {{ return d.y; }});

        texts.attr("transform", function(d) {{
            return "translate(" + d.x + "," + d.y + ")";
        }});
        tick = 1;
    }}
    else
        tick++;
  }});
}});

</script>
"""
