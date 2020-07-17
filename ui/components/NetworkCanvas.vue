<template>
  <div ref="canvas" class="flex-grow-1"></div>
</template>

<script>
import cytoscape from "cytoscape";
import $ from "jquery";
import contextMenus from "cytoscape-context-menus";
import "cytoscape-context-menus/cytoscape-context-menus.css";
cytoscape.use(contextMenus, $);

import coseBilkent from "cytoscape-cose-bilkent";
import fcose from "cytoscape-fcose";

cytoscape.use(fcose);
cytoscape.use(coseBilkent);
export default {
  data() {
    return {};
  },
  mounted() {
    let cy = cytoscape({
      container: this.$refs.canvas,
      elements: [
        // {
        //   data: {
        //     id: "joe-berardo",
        //     text: "Joe Berardo de seu nome",
        //     label: "PER"
        //   }
        // },
        // { data: { id: "edp", text: "EDP", label: "ORG" } },
        // { data: { id: 3, text: "Porto", label: "LOC" } },
        // { data: { id: 4, text: "cheque", label: "MISC" } },
        // { data: { id: "edp-3", source: "edp", target: 3, weight: 1 } },
        // { data: { id: "edp-4", source: "edp", target: 4, weight: 5 } }
      ],
      style: [
        {
          selector: "node",
          style: {
            "text-valign": "center",
            "text-halign": "center",
            "border-width": 1,
            color: "#353535",
            label: "data(text)",
            "text-wrap": "wrap",
            "text-max-width": 100,
            width: "100",
            height: "100",
            shape: "ellipse"
          }
        },
        {
          selector: "node[label='PER']",
          style: {
            "background-color": "#B2DFDB",
            "border-color": "#009688"
          }
        },
        {
          selector: "node[label='ORG']",
          style: {
            "background-color": "#D1C4E9",
            "border-color": "#673AB7"
            // shape: "round-triangle"
          }
        },
        {
          selector: "node[label='LOC']",
          style: {
            "background-color": "#B2EBF2",
            "border-color": "#00B8D4"
            // shape: "round-diamond"
          }
        },
        {
          selector: "node[label='MISC']",
          style: {
            "background-color": "#CFD8DC",
            "border-color": "#263238"
            // shape: "round-rectangle"
          }
        },
        {
          selector: "edge",
          style: {
            width: 1,
            "curve-style": "haystack",
            "line-color": "#FFCCBC",
            "edge-text-rotation": "autorotate",
            "control-point-step-size": 40,
            width: function(edge) {
              return Math.min(Math.max(edge.data().weight / 5, 1), 6);
            }
          }
        },
        {
          selector: "node:selected",
          style: {
            "border-width": 5
          }
        },
        {
          selector: "edge:selected, edge.selectedEdge",
          style: {
            "line-color": "#FB8C00"
          }
        },
        {
          selector: "node[explored]",
          style: {
            color: "#fff",
            "background-color": "#FF8A65",
            "border-color": "#DD2C00"
          }
        },
        {
          selector: "node[highlight=1]",
          style: {
            color: "#000",
            "background-color": "#FFEB3B",
            "border-color": "#000"
          }
        },
        {
          selector: "node.noticeMe",
          style: {
            color: "#fff",
            "background-color": "#00BFA5",
            "border-color": "#1DE9B6",
            "border-width": 5
          }
        }
      ],
      layout: { name: "cose", animate: false, padding: 150 },
      // layout:{name: "cose-bilkent", animate: true, padding: 40},
      // layout: { name: "random" , padding: 150},
      // zoom: 0.5,
      // pan: { x: 100, y: 100 },
      wheelSensitivity: 0.25,
      boxSelectionEnabled: true
      // textureOnViewport: true
      // hideEdgesOnViewport: true
      // selectionType: "additive",
    });
    let context = this.setupContextMenu(cy);
    this.setupDoubleClick(cy);
    this.loadExamples(cy);
    this.$emit("ready", { cy, context });
  },
  methods: {
    loadExamples(cy) {
      const params = new URLSearchParams(window.location.search);
      const example = params.get("example");
      try {
        let json = require(`../assets/ex/${example}.json`);
        cy.json(json);
      } catch (error) {}
    },
    setupContextMenu(cy) {
      return cy.contextMenus({
        menuItems: [
          {
            id: "expand",
            content: this.$t("network_canvas.context_menu.expand"),
            selector: "node[^explored]",
            onClickFunction: e => {
              this.$emit("expandEntity", e.target);
            },
            hasTrailingDivider: true
          },
          {
            id: "revertExpand",
            content: this.$t("network_canvas.context_menu.revertExpand"),
            selector: "node[explored]",
            onClickFunction: e => {
              this.$emit("expandEntity", e.target);
            },
            hasTrailingDivider: true
          },
          {
            id: "highlight",
            content: this.$t("network_canvas.context_menu.highlight"),
            selector: "node[^highlight], node[highlight=0]",
            onClickFunction: e => {
              if (e.target.selected())
                cy.$(
                  "node[^highlight]:selected, node[highlight=0]:selected"
                ).data("highlight", 1);
              else e.target.data("highlight", 1);
            },
            hasTrailingDivider: true
          },
          {
            id: "removeHighlight",
            content: this.$t("network_canvas.context_menu.removeHighlight"),
            selector: "node[highlight=1]",
            onClickFunction: e => {
              if (e.target.selected())
                cy.$("node[highlight=1]:selected").data("highlight", 0);
              else e.target.data("highlight", 0);
            },
            hasTrailingDivider: true
          },
          {
            id: "select",
            content: this.$t("network_canvas.context_menu.select"),
            selector: ":unselected",
            onClickFunction: e => {
              e.target.select();
            },
            hasTrailingDivider: true
          },
          {
            id: "deselect",
            content: this.$t("network_canvas.context_menu.deselect"),
            selector: ":selected",
            onClickFunction: e => {
              e.target.unselect();
            },
            hasTrailingDivider: true
          },
          {
            id: "selectConnections",
            content: this.$t("network_canvas.context_menu.selectConnections"),
            selector: "node",
            onClickFunction: e => {
              // e.cy.$("").unselect();
              e.target.select();
              e.target
                .connectedEdges(":visible")
                .connectedNodes()
                .select();
            },
            hasTrailingDivider: true
          },
          {
            id: "remove",
            content: this.$t("network_canvas.context_menu.remove"),
            selector: "node, edge",
            onClickFunction: e => {
              if (e.target.selected()) cy.$(":selected").remove();
              else e.target.remove();
            }
          }
        ],
        contextMenuClasses: ["contextMenu"],
        menuItemClasses: ["menuItem"]
      });
    },
    setupDoubleClick(cy) {
      let tappedBefore;
      let tappedTimeout;
      cy.on("tap", function(event) {
        let tappedNow = event.target;
        if (tappedTimeout && tappedBefore) {
          clearTimeout(tappedTimeout);
        }
        if (tappedBefore === tappedNow) {
          tappedNow.trigger("doubleClick");
          tappedBefore = null;
        } else {
          tappedTimeout = setTimeout(function() {
            tappedBefore = null;
          }, 300);
          tappedBefore = tappedNow;
        }
      });
    }
  }
};
</script>

<style>
.contextMenu.cy-context-menus-cxt-menu {
  border-radius: 4px;
  margin: 5px;
  min-width: 90px;
  border: 1px solid #e3e3e3;
  box-shadow: 0px 5px 5px -3px rgba(0, 0, 0, 0.2),
    0px 8px 10px 1px rgba(0, 0, 0, 0.14), 0px 3px 14px 2px rgba(0, 0, 0, 0.12);
}
.menuItem.cy-context-menus-cxt-menuitem {
  background-color: #fff;
  font-family: "Roboto", sans-serif;
  padding: 10px;
  padding-left: 42px;
  line-height: 1.5;
  font-size: 16px !important;
  border: 0px;
  min-width: 120px;
}
#expand.menuItem.cy-context-menus-cxt-menuitem::before {
  content: "\F004C";
}
#revertExpand.menuItem.cy-context-menus-cxt-menuitem::before {
  content: "\F0156";
}
#highlight.menuItem.cy-context-menus-cxt-menuitem::before {
  content: "\F0652";
}
#removeHighlight.menuItem.cy-context-menus-cxt-menuitem::before {
  content: "\F0DD9";
}
#select.menuItem.cy-context-menus-cxt-menuitem::before {
  content: "\F0D32";
}
#deselect.menuItem.cy-context-menus-cxt-menuitem::before {
  content: "\F0777";
}
#selectConnections.menuItem.cy-context-menus-cxt-menuitem::before {
  content: "\F0562";
}
#remove.menuItem.cy-context-menus-cxt-menuitem::before {
  content: "\F01B4";
}
.menuItem.cy-context-menus-cxt-menuitem:before {
  font: normal normal normal 22px/1 "Material Design Icons";
  color: #555;
  position: absolute;
  left: 10px;
  top: 11px;
}
.menuItem.cy-context-menus-cxt-menuitem:hover:before {
  color: #fff;
}
.menuItem.cy-context-menus-cxt-menuitem:hover {
  background-color: #009688;
}
.menuItem.cy-context-menus-cxt-menuitem.cy-context-menus-divider {
  border-bottom: 1px solid #e3e3e3;
}
</style>