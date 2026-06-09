import os

from PyQt5.QtCore import QCoreApplication

# ------------------------------------------------------------------------------


def process_all_gui_events():
    QCoreApplication.processEvents()


# ------------------------------------------------------------------------------

# configuration file

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".linguistica")
CONFIG_LAST_FILE = os.path.join(CONFIG_DIR, "last_file.json")

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
  vector-effect: non-scaling-stroke;
}}

.link {{
  stroke: #999;
  stroke-opacity: .6;
}}

text.label {{
  pointer-events: none;
}}

</style>
<body>
<script src="{}/d3.min.js"></script>
<script>

var width = {}, height = {};

var color = d3.scaleOrdinal(d3.schemeCategory10);

var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);

// transparent backdrop so pan/zoom works over empty space
svg.append("rect")
    .attr("fill-opacity", "0")
    .attr("width", width)
    .attr("height", height);

// everything that pans/zooms lives inside this container
var container = svg.append("g");

// declared up here so the zoom handler can reach them before the graph renders
var link, node, texts, neighbors;

// target on-screen sizes; nodes/labels/links are counter-scaled by 1/k so they
// stay this big no matter how far you zoom in (semantic zoom, not magnification)
var NODE_RADIUS_PX = 3, LABEL_FONT_PX = 8;

var zoom = d3.zoom()
    .scaleExtent([0.1, 1000])
    .on("zoom", function(event) {{
        var k = event.transform.k;
        container.attr("transform", event.transform);
        // counter-scale so visual size stays constant; zooming spreads nodes
        // apart instead of just blowing everything up together
        if (node) node.attr("r", NODE_RADIUS_PX / k);
        if (link) link.style("stroke-width", function(d) {{
            return Math.sqrt(d.value || 1) / k;
        }});
        if (texts) {{
            // labels always visible; just keep their size constant on screen
            texts.style("font-size", (LABEL_FONT_PX / k) + "px");
        }}
    }});

// disable d3's built-in double-click-to-zoom so it doesn't fight node dblclick
svg.call(zoom).on("dblclick.zoom", null);

var simulation = d3.forceSimulation()
    .force("link", d3.forceLink().id(function(d) {{ return d.id; }}).distance(10))
    .force("charge", d3.forceManyBody().strength(-50))
    .force("center", d3.forceCenter(width / 2, height / 2));

// Graph data is embedded inline (not fetched): Chromium blocks fetch()/
// d3.json() on file:// URLs, which is how QWebEngineView loads this page.
var graph = {};

(function() {{

    // adjacency lookup, keyed by node id, for hover highlighting
    neighbors = {{}};
    graph.nodes.forEach(function(n) {{ neighbors[n.id] = new Set([n.id]); }});
    graph.links.forEach(function(l) {{
        neighbors[l.source].add(l.target);
        neighbors[l.target].add(l.source);
    }});

    link = container.append("g").selectAll("line")
        .data(graph.links)
      .enter().append("line")
        .attr("class", "link")
        .style("stroke-width", function(d) {{ return Math.sqrt(d.value || 1); }});

    node = container.append("g").selectAll("circle")
        .data(graph.nodes)
      .enter().append("circle")
        .attr("class", "node")
        .attr("r", 3)
        .style("fill", function(d) {{ return color(d.group); }})
        .on("mouseover", highlight)
        .on("mouseout", unhighlight)
        .on("dblclick", release)
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));

    node.append("title")
        .text(function(d) {{ return d.name; }});

    texts = container.append("g").selectAll("text")
        .data(graph.nodes)
      .enter().append("text")
        .attr("class", "label")
        .attr("fill", "black")
        .style("font-size", LABEL_FONT_PX + "px")
        .text(function(d) {{ return d.id; }});

    simulation.nodes(graph.nodes).on("tick", ticked);
    simulation.force("link").links(graph.links);

    // frame the whole graph once, after the layout first settles
    var fitted = false;
    simulation.on("end", function() {{
        if (fitted) return;
        fitted = true;
        zoomToFit(graph.nodes);
    }});

    function ticked() {{
        link.attr("x1", function(d) {{ return d.source.x; }})
            .attr("y1", function(d) {{ return d.source.y; }})
            .attr("x2", function(d) {{ return d.target.x; }})
            .attr("y2", function(d) {{ return d.target.y; }});

        node.attr("cx", function(d) {{ return d.x; }})
            .attr("cy", function(d) {{ return d.y; }});

        texts.attr("transform", function(d) {{
            return "translate(" + d.x + "," + d.y + ")";
        }});
    }}

    function highlight(event, d) {{
        var near = neighbors[d.id];
        node.style("opacity", function(o) {{ return near.has(o.id) ? 1 : 0.1; }});
        link.style("opacity", function(o) {{
            return (o.source.id === d.id || o.target.id === d.id) ? 1 : 0.05;
        }});
    }}

    function unhighlight() {{
        node.style("opacity", null);
        link.style("opacity", null);
    }}

    function release(event, d) {{
        // un-pin a node that was dragged into place
        d.fx = null;
        d.fy = null;
        simulation.alphaTarget(0.3).restart();
        simulation.alphaTarget(0);
    }}
}})();

function zoomToFit(nodes) {{
    var xs = nodes.map(function(d) {{ return d.x; }});
    var ys = nodes.map(function(d) {{ return d.y; }});
    var x0 = Math.min.apply(null, xs), x1 = Math.max.apply(null, xs);
    var y0 = Math.min.apply(null, ys), y1 = Math.max.apply(null, ys);
    var dx = (x1 - x0) || 1, dy = (y1 - y0) || 1;
    var k = Math.max(0.1, Math.min(10, 0.9 / Math.max(dx / width, dy / height)));
    var tx = width / 2 - k * (x0 + x1) / 2;
    var ty = height / 2 - k * (y0 + y1) / 2;
    svg.transition().duration(500).call(
        zoom.transform,
        d3.zoomIdentity.translate(tx, ty).scale(k));
}}

function dragstarted(event, d) {{
    if (!event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
}}

function dragged(event, d) {{
    d.fx = event.x;
    d.fy = event.y;
}}

function dragended(event, d) {{
    if (!event.active) simulation.alphaTarget(0);
    // node stays pinned at (fx, fy) until double-clicked to release
}}

</script>
"""
